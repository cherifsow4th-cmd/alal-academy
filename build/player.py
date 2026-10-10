# -*- coding: utf-8 -*-
"""The lesson player: where a course is actually watched.

One page per course under apprendre/. The screen is split the way a lesson is
consumed — the video and what belongs to it on the left, the table of contents
on the right, always visible, so you always know where you are in the course
and what comes next.

Predika does not publish lesson titles (the accordions on the public course
page show counts and running times only), so lessons are numbered inside their
module and carry a share of the module's running time. The titles drop in from
the LMS later without touching the layout.

The video itself is a shell: the course artwork as poster, real controls, and a
clock that runs when you press play. There is no lesson footage to serve yet,
and a <video> pointing at nothing would be worse than an honest placeholder.
"""
import os, sys, html, re, json
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, FOOTER, MONO, ROOT
from courses import COURSES
from cartkit import cart_js
from shop import AUTH_HEADER, AUTH_MNAV, AUTH_CSS, ACCT_JS, esc, ico, I_ARROW, CHECK
from account import PROGRESS, ACC_CSS, minutes, hm, lessons_of, current
from svc_icons import TICK_CIRCLE, sized
import modals as MOD

BY = {c['slug']: c for c in COURSES}
PCT = dict(PROGRESS)

I_PLAY_BIG = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" '
              'aria-hidden="true"><path d="M8 5.5v13l11-6.5L8 5.5Z"/></svg>')
I_PAUSE = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" '
           'aria-hidden="true"><rect x="7" y="5.5" width="3.6" height="13" rx="1"/>'
           '<rect x="13.4" y="5.5" width="3.6" height="13" rx="1"/></svg>')
I_PREV = ico('<path d="m14 6-6 6 6 6"/>', 17)
I_NEXT = ico('<path d="m10 6 6 6-6 6"/>', 17)
I_FULL = ico('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>', 17)
I_DOC = ico('<path d="M6 3.5h7.5L19 9v11.5H6z"/><path d="M13.5 3.5V9H19"/>', 16)
I_BACK = ico('<path d="M19 12H5m0 0 6-6m-6 6 6 6"/>', 16)
I_OK = sized(TICK_CIRCLE, 17)   # the library's tick-circle marks a finished lesson


PLAY_CSS = """
  [hidden]{display:none !important}
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}

  .pl-crumbs{display:flex;align-items:center;gap:10px;padding:26px 0 0;font-size:13.5px;
    color:#7a7a7a}
  .pl-crumbs a{display:inline-flex;align-items:center;gap:8px;color:#7a7a7a}
  .pl-crumbs a:hover{color:#1F1F1F}
  .pl-crumbs b{font-weight:400;color:#1F1F1F}

  /* the lesson on the left, the course on the right — the contents stay in
     view so you always know where you are and what follows */
  .pl-layout{display:grid;grid-template-columns:minmax(0,1fr) 388px;gap:44px;
    padding:22px 0 104px;align-items:start}

  /* ── the screen ───────────────────────────────────────────────────────
     Ink surround, artwork as poster, the controls sitting on a scrim at the
     foot rather than floating over the middle of the picture. */
  .vid{position:relative;border-radius:18px;overflow:hidden;background:#1F1F1F;
    aspect-ratio:16/9}
  .vid img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;
    transition:opacity .5s ease,transform 4s linear}
  .vid.is-playing img{opacity:.55;transform:scale(1.03)}
  .vid-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
    border:0;background:transparent;cursor:pointer;color:#FFFFFF}
  .vid-play span{display:flex;align-items:center;justify-content:center;width:84px;height:84px;
    border-radius:50%;background:rgba(255,255,255,.14);backdrop-filter:blur(6px);
    -webkit-backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.3);padding-left:4px;
    transition:transform .4s cubic-bezier(.22,1,.36,1),background .3s ease}
  .vid-play:hover span{transform:scale(1.07);background:rgba(255,255,255,.24)}
  .vid.is-playing .vid-play span{opacity:0;transform:scale(.8)}

  .vid-bar{position:absolute;left:0;right:0;bottom:0;padding:34px 20px 16px;
    display:flex;align-items:center;gap:16px;color:#FFFFFF;
    background:linear-gradient(to top,rgba(31,31,31,.86),rgba(31,31,31,0))}
  .vid-bar button{display:flex;align-items:center;justify-content:center;border:0;padding:0;
    background:transparent;color:#FFFFFF;cursor:pointer;opacity:.9;transition:opacity .2s ease}
  .vid-bar button:hover{opacity:1}
  .vid-time{font-family:__MONO__;font-size:11.5px;letter-spacing:.06em;white-space:nowrap;
    opacity:.85}
  .vid-track{flex:1;height:4px;border-radius:999px;background:rgba(255,255,255,.26);
    cursor:pointer;position:relative}
  .vid-track i{display:block;height:100%;border-radius:999px;background:#FFFFFF;width:0}
  .vid-rate{font-family:__MONO__;font-size:11px;letter-spacing:.06em;
    border:1px solid rgba(255,255,255,.3) !important;border-radius:999px;height:26px;padding:0 10px}

  /* ── under the screen ─────────────────────────────────────────────────── */
  .pl-mod{margin:26px 0 0;font-family:__MONO__;font-size:10.5px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a}
  .pl-title{margin:14px 0 0;font-size:clamp(27px,3vw,38px);line-height:1.14;
    letter-spacing:-0.034em;font-weight:400}
  .pl-sub{margin:12px 0 0;font-size:15.5px;color:#7a7a7a}
  .pl-acts{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:26px 0 0;
    padding-bottom:30px;border-bottom:1px solid rgba(31,31,31,.12)}
  .pl-done{display:inline-flex;align-items:center;gap:10px;height:50px;padding:0 22px;border:0;
    border-radius:12px;background:#1F1F1F;color:#FFFFFF;font:inherit;font-size:15px;
    font-weight:500;cursor:pointer;transition:background .3s ease,color .3s ease}
  .pl-done.is-done{background:rgba(14,105,92,.1);color:#0E695C}
  .pl-next{display:inline-flex;align-items:center;gap:9px;height:50px;padding:0 20px;
    border:1px solid rgba(31,31,31,.16);border-radius:12px;background:#FFFFFF;color:#1F1F1F;
    font:inherit;font-size:15px;cursor:pointer;
    transition:border-color .25s ease,box-shadow .3s ease}
  .pl-next:hover{border-color:rgba(31,31,31,.34);box-shadow:0 2px 5px rgba(0,0,0,.07)}
  .pl-next:disabled{opacity:.4;cursor:default;box-shadow:none;border-color:rgba(31,31,31,.16)}

  .tabs{display:flex;gap:28px;margin-top:30px;border-bottom:1px solid rgba(31,31,31,.12)}
  .tabs button{position:relative;border:0;background:transparent;padding:0 0 14px;cursor:pointer;
    font:inherit;font-size:15px;color:#7a7a7a;transition:color .2s ease}
  .tabs button:hover{color:#1F1F1F}
  .tabs button.is-on{color:#1F1F1F}
  .tabs button::after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:2.5px;
    background:#1F1F1F;transform:scaleX(0);transform-origin:left;
    transition:transform .35s cubic-bezier(.22,1,.36,1)}
  .tabs button.is-on::after{transform:scaleX(1)}
  .pane{padding-top:28px;max-width:70ch}
  .pane p{margin:0 0 16px;font-size:16px;line-height:1.72;color:#4a4a4a}
  .pane p:last-child{margin-bottom:0}
  .res{list-style:none;margin:0;padding:0}
  .res li{display:flex;align-items:center;gap:14px;padding:16px 0;
    border-bottom:1px solid rgba(31,31,31,.09)}
  .res li svg{color:#7a7a7a;flex:none}
  .res b{display:block;font-size:15.5px;font-weight:500}
  .res i{display:block;font-style:normal;margin-top:3px;font-size:12.5px;color:#A7A7A7}
  .res a{margin-left:auto;font-size:14px;color:#1F1F1F;text-decoration:underline;
    text-underline-offset:4px;white-space:nowrap}
  .note-box{width:100%;min-height:190px;padding:18px 20px;border:1px solid rgba(31,31,31,.14);
    border-radius:14px;font:inherit;font-size:15px;line-height:1.65;color:#1F1F1F;resize:vertical}
  .note-box:focus{outline:none;border-color:#1F1F1F}
  .note-hint{margin:12px 0 0;font-size:13px;color:#A7A7A7}

  /* ── the contents ─────────────────────────────────────────────────────── */
  .toc{position:sticky;top:104px;border:1px solid rgba(31,31,31,.12);border-radius:18px;
    overflow:hidden;background:#FFFFFF}
  .toc-head{padding:22px 24px;border-bottom:1px solid rgba(31,31,31,.1);background:#FCFBF8}
  .toc-head b{display:block;font-size:16px;font-weight:500;letter-spacing:-0.02em;line-height:1.35}
  .toc-head .prog-line{margin-top:14px}
  .toc-scroll{max-height:min(66vh,720px);overflow-y:auto}
  .toc-mod{border-bottom:1px solid rgba(31,31,31,.09)}
  .toc-mod:last-child{border-bottom:0}
  .toc-mod > button{display:flex;align-items:flex-start;gap:12px;width:100%;padding:16px 22px;
    border:0;background:transparent;font:inherit;text-align:left;cursor:pointer;
    transition:background .2s ease}
  .toc-mod > button:hover{background:#FCFBF8}
  .toc-mod .num{font-family:__MONO__;font-size:10.5px;letter-spacing:.08em;color:#A7A7A7;
    padding-top:3px;flex:none}
  .toc-mod .num.is-full{display:flex;align-items:center;justify-content:center;width:18px;
    height:18px;color:#0E695C;padding-top:0;margin-top:1px}
  .toc-mod .t{flex:1;font-size:14.5px;line-height:1.42}
  .toc-mod .c{font-size:12px;color:#A7A7A7;white-space:nowrap;padding-top:2px}
  .toc-list{list-style:none;margin:0;padding:0 0 10px}
  .toc-list a{display:flex;align-items:center;gap:12px;padding:10px 22px 10px 54px;
    font-size:14px;color:#7a7a7a;transition:background .2s ease,color .2s ease}
  .toc-list a:hover{background:#FCFBF8;color:#1F1F1F}
  .toc-list a.is-now{background:#1F1F1F;color:#FFFFFF}
  .toc-list a.is-now .dur{color:rgba(255,255,255,.7)}
  /* the tick-circle draws its own disc, so the hollow ring is only ever
     the empty state */
  .toc-list .tick{display:flex;align-items:center;justify-content:center;width:17px;height:17px;
    flex:none;border:1px solid rgba(31,31,31,.22);border-radius:50%;color:transparent}
  .toc-list .tick svg{display:none}
  .toc-list a.is-done .tick{border:0;color:#0E695C}
  .toc-list a.is-done .tick svg{display:block}
  .toc-list a.is-now .tick{border-color:rgba(255,255,255,.5)}
  .toc-list a.is-now.is-done .tick{color:#FFFFFF}
  .toc-list .dur{margin-left:auto;font-size:12px;color:#A7A7A7}

  @media (max-width:1180px){
    .pl-layout{grid-template-columns:1fr;gap:34px}
    .toc{position:static}
    .toc-scroll{max-height:none}
  }
  @media (max-width:820px){
    .pl-layout{padding-bottom:72px}
    .vid-bar{padding:26px 14px 12px;gap:11px}
    .vid-rate{display:none}
    .vid-play span{width:64px;height:64px}
    .pl-acts{gap:10px}
    .pl-done,.pl-next{height:46px;font-size:14.5px}
  }
""".replace('__MONO__', MONO)


ABOUT = ("Cette leçon fait partie du module « %s ». Elle reprend les notions du module "
         "précédent et les applique à un cas concret du marché UEMOA, avec les écritures "
         "et les contrôles attendus par un comité charia.")
ABOUT2 = ("Prenez le temps de faire l'exercice avant de passer à la suite : les leçons "
          "suivantes supposent que les mécanismes vus ici sont acquis.")

RES = [
    ('Support de la leçon', 'PDF &middot; 18 pages'),
    ('Modèle de fiche produit', 'XLSX &middot; 2 onglets'),
    ('Références AAOIFI citées', 'PDF &middot; 4 pages'),
]


def mmss(mins):
    return '%02d:%02d' % (mins, 0)


def build_one(c):
    got = current(c)
    if not got:
        return None
    flat, done_n, cur = got
    pct = PCT.get(c['slug'], 0)
    L = flat[cur]
    mod_title = c['modules'][L['mi']][0]

    # ── contents ──────────────────────────────────────────────────────────
    mods, k = [], 0
    for mi, m in enumerate(c['modules']):
        rows = []
        for li in range(m[1]):
            cls = []
            if k < done_n:
                cls.append('is-done')
            if k == cur:
                cls.append('is-now')
            rows.append('            <li><a href="#l%d"%s data-i="%d">'
                        '<span class="tick">%s</span>Leçon %d'
                        '<span class="dur">%d min</span></a></li>'
                        % (k, ' class="%s"' % " ".join(cls) if cls else '', k,
                           I_OK, li + 1, flat[k]['mins']))
            k += 1
        # a module whose lessons are all behind you says so in its number
        full = k <= done_n
        mods.append("""        <div class="toc-mod"%s>
          <button type="button" aria-expanded="%s">
            <span class="num%s">%s</span>
            <span class="t">%s</span>
            <span class="c">%d &middot; %s</span>
          </button>
          <ul class="toc-list"%s>
%s
          </ul>
        </div>""" % (' data-open="1"' if mi == L['mi'] else '',
                     'true' if mi == L['mi'] else 'false',
                     ' is-full' if full else '', I_OK if full else '%02d' % (mi + 1),
                     esc(m[0]), m[1], esc(m[2]),
                     '' if mi == L['mi'] else ' hidden', "\n".join(rows)))

    res = "\n".join('          <li>%s<div><b>%s</b><i>%s</i></div>'
                    '<a href="#telecharger">Télécharger</a></li>' % (I_DOC, esc(t), d)
                    for t, d in RES)

    body = """<div class="wrap">
  <div class="pl-crumbs">
    <a href="../mes-cours.html">%(back)s Mes cours</a> &middot;
    <a href="../cours/%(slug)s-inscrit.html"><b>%(ctitle)s</b></a>
  </div>

  <div class="pl-layout">
    <div>
      <div class="vid" id="plVid">
        <img src="%(img)s" alt="" width="1280" height="720">
        <button type="button" class="vid-play" id="plBig" aria-label="Lire la leçon">
          <span>%(play)s</span>
        </button>
        <div class="vid-bar">
          <button type="button" id="plToggle" aria-label="Lire">%(play)s</button>
          <span class="vid-time"><b id="plNow">00:00</b> / %(len)s</span>
          <div class="vid-track" id="plTrack"><i id="plFill"></i></div>
          <button type="button" class="vid-rate" id="plRate">1×</button>
          <button type="button" aria-label="Plein écran">%(full)s</button>
        </div>
      </div>

      <p class="pl-mod">Module %(mi)d &middot; Leçon %(li)d &middot; %(mins)d min</p>
      <h1 class="pl-title">%(mtitle)s</h1>
      <p class="pl-sub">%(ctitle)s</p>

      <div class="pl-acts">
        <button type="button" class="pl-done" id="plDone">%(check)s Marquer comme terminée</button>
        <button type="button" class="pl-next" id="plPrev">%(prev)s Leçon précédente</button>
        <button type="button" class="pl-next" id="plNext">Leçon suivante %(next)s</button>
      </div>

      <div class="tabs" id="plTabs">
        <button type="button" class="is-on" data-t="about">À propos</button>
        <button type="button" data-t="res">Ressources</button>
        <button type="button" data-t="note">Mes notes</button>
      </div>
      <div class="pane" data-p="about">
        <p>%(about)s</p>
        <p>%(about2)s</p>
      </div>
      <div class="pane" data-p="res" hidden>
        <ul class="res">
%(res)s
        </ul>
      </div>
      <div class="pane" data-p="note" hidden>
        <textarea class="note-box" placeholder="Vos notes sur cette leçon…"></textarea>
        <p class="note-hint">Vos notes restent privées et vous suivent d'un appareil à l'autre.</p>
      </div>
    </div>

    <aside class="toc">
      <div class="toc-head">
        <b>%(ctitle)s</b>
        <div class="prog-line"><div class="bar"><i style="width:%(pct)d%%"></i></div>
          <b>%(done)d / %(n)d</b></div>
      </div>
      <div class="toc-scroll">
%(mods)s
      </div>
    </aside>
  </div>
  <hr class="rule">
</div>
""" % dict(back=I_BACK, ctitle=esc(c['title']), slug=c['slug'],
           img=c['image'], play=I_PLAY_BIG,
           len=mmss(L['mins']), full=I_FULL, mi=L['mi'] + 1, li=L['li'] + 1, mins=L['mins'],
           mtitle=esc(mod_title), check=CHECK, prev=I_PREV, next=I_NEXT,
           about=esc(ABOUT % mod_title), about2=esc(ABOUT2), res=res,
           pct=pct, done=done_n, n=len(flat), mods="\n".join(mods))
    return body, L, len(flat), cur


PLAY_JS = """
<script>
/* The player, the contents and the tabs. The picture is a placeholder — there
   is no lesson footage to serve yet — so the clock is driven by a timer rather
   than by a media element. Everything else is the real behaviour: the bar
   scrubs, the contents fold, the lesson can be ticked off. */
(function () {
  var vid = document.getElementById('plVid'); if (!vid) return;
  var LEN = __LEN__;                      /* the lesson's length, in seconds */
  var t = 0, timer = null, rate = 1, rates = [1, 1.25, 1.5, 2];
  var fill = document.getElementById('plFill'), now = document.getElementById('plNow');
  var toggle = document.getElementById('plToggle'), big = document.getElementById('plBig');
  var PLAY = __PLAY__, PAUSE = __PAUSE__;

  function clock(s) {
    s = Math.max(0, Math.round(s));
    return ('0' + Math.floor(s / 60)).slice(-2) + ':' + ('0' + (s % 60)).slice(-2);
  }
  function paint() {
    fill.style.width = (t / LEN * 100) + '%';
    now.textContent = clock(t);
  }
  function play(on) {
    vid.classList.toggle('is-playing', on);
    toggle.innerHTML = on ? PAUSE : PLAY;
    toggle.setAttribute('aria-label', on ? 'Pause' : 'Lire');
    clearInterval(timer);
    if (on) timer = setInterval(function () {
      t += 0.25 * rate;
      if (t >= LEN) { t = LEN; play(false); }
      paint();
    }, 250);
  }
  toggle.addEventListener('click', function () { play(!vid.classList.contains('is-playing')); });
  big.addEventListener('click', function () { play(true); });
  document.getElementById('plTrack').addEventListener('click', function (e) {
    var r = this.getBoundingClientRect();
    t = Math.min(LEN, Math.max(0, (e.clientX - r.left) / r.width * LEN));
    paint();
  });
  document.getElementById('plRate').addEventListener('click', function () {
    rate = rates[(rates.indexOf(rate) + 1) % rates.length];
    this.textContent = rate + '×';
  });
  /* space plays and pauses, as it does in every player — unless the person is
     typing in their notes */
  document.addEventListener('keydown', function (e) {
    if (e.code !== 'Space' || /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) return;
    e.preventDefault(); play(!vid.classList.contains('is-playing'));
  });
  paint();

  /* marking the lesson off also ticks it in the contents */
  var done = document.getElementById('plDone');
  var here = document.querySelector('.toc-list a.is-now');
  done.addEventListener('click', function () {
    var on = !done.classList.contains('is-done');
    done.classList.toggle('is-done', on);
    done.lastChild.textContent = on ? ' Leçon terminée' : ' Marquer comme terminée';
    if (here) here.classList.toggle('is-done', on);
  });

  /* previous / next walk the flat list of lessons */
  var links = [].slice.call(document.querySelectorAll('.toc-list a'));
  var i = links.indexOf(here);
  var prev = document.getElementById('plPrev'), next = document.getElementById('plNext');
  prev.disabled = i <= 0; next.disabled = i < 0 || i >= links.length - 1;
  function go(step) {
    var target = links[i + step]; if (!target) return;
    target.click();
  }
  prev.addEventListener('click', function () { go(-1); });
  next.addEventListener('click', function () { go(1); });

  /* the contents fold one module at a time */
  document.querySelectorAll('.toc-mod > button').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      b.setAttribute('aria-expanded', open ? 'false' : 'true');
      b.nextElementSibling.hidden = open;
    });
  });

  /* tabs */
  var tabs = document.getElementById('plTabs');
  tabs.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-t]'); if (!b) return;
    [].forEach.call(tabs.children, function (x) { x.classList.toggle('is-on', x === b); });
    document.querySelectorAll('.pane').forEach(function (p) {
      p.hidden = p.getAttribute('data-p') !== b.getAttribute('data-t');
    });
  });
})();
</script>
"""


def page(title, desc, body, secs):
    js = (PLAY_JS.replace('__LEN__', str(secs))
                 .replace('__PLAY__', json.dumps(I_PLAY_BIG))
                 .replace('__PAUSE__', json.dumps(I_PAUSE)))
    out = __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<style>%s%s%s%s</style>
</head>
<body>
%s
%s
%s
%s
</body>
</html>
""" % (html.escape(title), html.escape(desc), BASE, AUTH_CSS, ACC_CSS, PLAY_CSS,
       AUTH_HEADER + AUTH_MNAV, cart_js(''), body,
       FOOTER.replace('{ROOT}', '') + ACCT_JS + MOD.modals('') + MOD.MODAL_JS + js))
    # the page lives one folder down, so every root-relative path gains a step
    out = out.replace('href="index.html', 'href="../index.html')
    for f in ('blog', 'parcours', 'webinaires', 'panier', 'compte', 'mes-cours',
              'mes-certificats', 'mes-commandes', 'parametres'):
        out = out.replace('href="%s.html"' % f, 'href="../%s.html"' % f)
    out = out.replace('href="cours/', 'href="../cours/')
    out = out.replace('href="parcours/', 'href="../parcours/')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace("url('assets/", "url('../assets/")
    out = out.replace('href="../../', 'href="../')
    return out


def build():
    os.makedirs(os.path.join(ROOT, 'apprendre'), exist_ok=True)
    n = 0
    for c in COURSES:
        made = build_one(c)
        if not made:
            print('apprendre/%s.html  (programme non publié — pas de lecteur)' % c['slug'])
            continue
        body, L, total, cur = made
        out = page('%s — Alal Academy' % c['title'],
                   "Leçon %d du module %d de %s." % (L['li'] + 1, L['mi'] + 1, c['title']),
                   body, L['mins'] * 60)
        open(os.path.join(ROOT, 'apprendre', c['slug'] + '.html'), 'w',
             encoding='utf-8').write(out)
        print('apprendre/%s.html  (leçon %d/%d, %d min)' % (c['slug'], cur + 1, total, L['mins']))
        n += 1
    return n


if __name__ == '__main__':
    build()
