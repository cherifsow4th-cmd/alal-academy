# -*- coding: utf-8 -*-
"""The course page as an enrolled student sees it.

The public page sells the course: a price, a buy button, and a programme that
lists modules without opening them. Once the course is yours none of that is
the question any more — what you want is how far you are, which lesson is next
and a way into it. This builds that second state as cours/<slug>-inscrit.html,
leaving the sales page untouched so the two can be compared side by side.

It works by rewriting the page course.py already produced rather than forking
its template: the two states then cannot drift apart, and anything added to the
course page shows up here on the next build.
"""
import os, sys, re, html
sys.path.insert(0, os.path.dirname(__file__))
from gen import HEADER, MNAV, MONO, ROOT, nav_active
from courses import COURSES
from shop import AUTH_HEADER, AUTH_MNAV, AUTH_CSS, ACCT_JS, esc, ico, CHECK
from account import PROGRESS, current, ORDERS
from svc_icons import TICK_CIRCLE, sized

PCT = dict(PROGRESS)
I_OK = sized(TICK_CIRCLE, 17)     # the library's tick-circle
I_OK_L = sized(TICK_CIRCLE, 19)
I_ARROW = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="M7 17 17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.6" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def rw(markup):
    """The same path rewrites course.py applies to anything it drops in cours/."""
    out = markup.replace('href="index.html', 'href="../index.html')
    for f in ('blog', 'parcours', 'webinaires', 'panier', 'compte', 'mes-cours',
              'mes-certificats', 'mes-commandes', 'parametres'):
        out = out.replace('href="%s.html"' % f, 'href="../%s.html"' % f)
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace("url('assets/", "url('../assets/")
    out = out.replace('href="../../index.html', 'href="../index.html')
    return out


CSS = """
  /* ── the course, once it is yours ─────────────────────────────────────
     The rail stops selling and starts reporting: where you are, what is
     next, one way in. The programme opens, because its lessons are now
     places you can go rather than a list of what you would get. */
  .own{padding:22px 24px 24px;border:1px solid rgba(31,31,31,.12);border-radius:16px}
  .own-tag{display:inline-flex;align-items:center;gap:7px;height:26px;padding:0 11px;
    border-radius:999px;background:rgba(14,105,92,.1);color:#0E695C;font-family:__MONO__;
    font-size:9.5px;letter-spacing:.1em;text-transform:uppercase}
  .own h4{margin:16px 0 0;font-size:17px;font-weight:500;letter-spacing:-0.02em}
  .own .next{margin:6px 0 0;font-size:13.5px;line-height:1.55;color:#7a7a7a}
  .own .prog-line{margin-top:18px}
  .own-go{display:flex;align-items:center;justify-content:center;gap:10px;height:56px;
    margin-top:20px;border-radius:12px;background:#1F1F1F;color:#FFFFFF;font-size:15.5px;
    font-weight:500;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .own-go:hover{box-shadow:0 2px 6px rgba(0,0,0,.3),0 7px 16px rgba(0,0,0,.26),
    0 17px 33px rgba(0,0,0,.22)}
  .own-note{margin:16px 0 0;padding-top:16px;border-top:1px solid rgba(31,31,31,.09);
    font-size:12.5px;line-height:1.6;color:#A7A7A7}
  .own-note a{color:#7a7a7a;text-decoration:underline;text-underline-offset:3px}

  /* the programme, opened out */
  .mods li{flex-wrap:wrap}
  .mods .pill{display:flex;align-items:center;justify-content:center;width:19px;height:19px;
    flex:none;color:#0E695C;margin-left:1px}
  /* .mods li in the public stylesheet matches descendants too, so the nested
     lessons would inherit the module row's padding, rule and hover */
  .mods .mlist li{display:block;padding:0;border:0;background:none;counter-increment:none}
  .mods .mlist li:hover{background:none}
  .mlist{list-style:none;flex:1 0 100%;margin:12px 0 2px;padding:0 0 0 38px}
  .mlist a{display:flex;align-items:center;gap:12px;padding:8px 12px;margin-left:-12px;
    border-radius:10px;font-size:14.5px;color:#7a7a7a;
    transition:background .2s ease,color .2s ease}
  .mlist a:hover{background:#FFFFFF;color:#1F1F1F}
  .mlist a.is-now{background:#1F1F1F;color:#FFFFFF}
  .mlist a.is-now .dur{color:rgba(255,255,255,.7)}
  .mlist .tick{display:flex;align-items:center;justify-content:center;width:17px;height:17px;
    flex:none;border:1px solid rgba(31,31,31,.22);border-radius:50%;color:transparent}
  .mlist .tick svg{display:none}
  .mlist a.is-done .tick{border:0;color:#0E695C}
  .mlist a.is-done .tick svg{display:block}
  .mlist a.is-now .tick{border-color:rgba(255,255,255,.5)}
  .mlist a.is-now.is-done .tick{color:#FFFFFF}
  .mlist .dur{margin-left:auto;font-size:12.5px;color:#A7A7A7}
  .prog-head .own-prog{margin:8px 0 0;font-size:14px;color:#0E695C}
  .bar{height:4px;border-radius:999px;background:rgba(31,31,31,.12);overflow:hidden}
  .bar i{display:block;height:100%;border-radius:999px;background:#1F1F1F}
  .prog-line{display:flex;align-items:center;gap:14px}
  .prog-line .bar{flex:1}
  .prog-line b{font-size:13px;font-weight:500;color:#7a7a7a;white-space:nowrap}
""".replace('__MONO__', MONO)


def when_bought(slug):
    """The order this course came in, so the rail can say since when it is
    yours — the parcours covers all eight, a single purchase covers one."""
    for o in ORDERS:
        for kind, s in o['items']:
            if kind == 'cours' and s == slug:
                return o['date'], 'achat du cours'
    for o in ORDERS:
        if any(k == 'parcours' for k, _ in o['items']):
            return o['date'], 'parcours Certified Islamic Banker'
    return None, None


def build_one(c):
    src = os.path.join(ROOT, 'cours', c['slug'] + '.html')
    if not os.path.exists(src) or not c['modules']:
        return False
    out = open(src, encoding='utf-8').read()
    flat, done_n, cur = current(c)
    pct = PCT.get(c['slug'], 0)
    L = flat[cur]
    player = '../apprendre/%s.html' % c['slug']

    # ── 1. the signed-in header ───────────────────────────────────────────
    old_head = rw(nav_active(HEADER, 'cours'))
    old_mnav = rw(MNAV)
    assert old_head in out and old_mnav in out, c['slug']
    out = out.replace(old_head, rw(AUTH_HEADER), 1).replace(old_mnav, rw(AUTH_MNAV), 1)

    # ── 2. the rail stops selling ─────────────────────────────────────────
    i = out.index('<div class="buy">')
    j = out.index('<div class="box">', i)
    date, via = when_bought(c['slug'])
    buy = """<div class="own">
        <span class="own-tag">%(ok)s Cours acquis</span>
        <h4>Module %(mi)d &middot; Leçon %(li)d</h4>
        <p class="next">%(mtitle)s</p>
        <div class="prog-line"><div class="bar"><i style="width:%(pct)d%%"></i></div>
          <b>%(done)d / %(n)d</b></div>
        <a class="own-go" href="%(player)s">%(verb)s %(arrow)s</a>
        <p class="own-note">%(since)s &middot; accès à vie.
          <a href="../mes-commandes.html">Voir la commande</a></p>
      </div>

      """ % dict(ok=I_OK, mi=L['mi'] + 1, li=L['li'] + 1,
                 mtitle=esc(c['modules'][L['mi']][0]), pct=pct, done=done_n, n=len(flat),
                 player=player, arrow=I_ARROW,
                 verb='Commencer le cours' if done_n == 0 else
                      ('Revoir le cours' if done_n >= len(flat) else 'Reprendre la leçon'),
                 since=('Dans votre compte depuis le %s (%s)' % (esc(date), esc(via)))
                       if date else 'Dans votre compte')
    out = out[:i] + buy + out[j:]

    # ── 3. the programme opens ────────────────────────────────────────────
    i = out.index('<ol class="mods">')
    j = out.index('</ol>', i) + len('</ol>')
    rows, k = [], 0
    for mi, m in enumerate(c['modules']):
        lis = []
        for li in range(m[1]):
            cls = []
            if k < done_n:
                cls.append('is-done')
            if k == cur:
                cls.append('is-now')
            lis.append('            <li><a href="%s#l%d"%s><span class="tick">%s</span>'
                       'Leçon %d<span class="dur">%d min</span></a></li>'
                       % (player, k, ' class="%s"' % " ".join(cls) if cls else '',
                          I_OK, li + 1, flat[k]['mins']))
            k += 1
        full = k <= done_n
        rows.append("""        <li id="m%d">
          <span class="n">%s</span>
          <span class="t">%s%s</span>
          <span class="d">%d leçon%s &middot; %s</span>
          <ul class="mlist">
%s
          </ul>
        </li>""" % (mi + 1,
                    '<span class="pill">%s</span>' % I_OK_L if full else '%02d' % (mi + 1),
                    esc(m[0]), ('<small>%s</small>' % esc(m[3])) if m[3] else '',
                    m[1], 's' if m[1] > 1 else '', m[2], "\n".join(lis)))
    out = out[:i] + '<ol class="mods">\n' + "\n".join(rows) + '\n        </ol>' + out[j:]

    # the programme heading reports progress instead of repeating the totals
    i = out.index('<div class="prog-head">')
    j = out.index('</div>', i) + len('</div>')
    out = out[:i] + ("""<div class="prog-head">
          <h2 style="margin:0">Programme du cours</h2>
          <p>%d modules &middot; %d leçons &middot; %s</p>
          <p class="own-prog">%s</p>
        </div>""" % (len(c['modules']), c['lessons'],
                     c['modules'] and sum_dur(c) or '',
                     '%d leçons terminées sur %d — %d %%' % (done_n, len(flat), pct))) + out[j:]

    # ── 4. styles and the chip menu ───────────────────────────────────────
    out = out.replace('</style>', AUTH_CSS + CSS + '</style>', 1)
    out = out.replace('</body>', rw(ACCT_JS) + '</body>', 1)
    # the page is a second state of the same course, not a second course
    out = out.replace('<title>', '<title>', 1)

    open(os.path.join(ROOT, 'cours', c['slug'] + '-inscrit.html'), 'w',
         encoding='utf-8').write(out)
    print('cours/%s-inscrit.html  (leçon %d/%d, %d %%)'
          % (c['slug'], cur + 1, len(flat), pct))
    return True


def sum_dur(c):
    """The course's running time, exactly as the public page spells it."""
    t = 0
    for m in c['modules']:
        h = re.search(r'(\d+)\s*h', m[2])
        mn = re.search(r'(\d+)\s*min', m[2])
        t += (int(h.group(1)) * 60 if h else 0) + (int(mn.group(1)) if mn else 0)
    return '%d h %02d' % (t // 60, t % 60)


def build():
    n = 0
    for c in COURSES:
        if build_one(c):
            n += 1
    return n


if __name__ == '__main__':
    build()
