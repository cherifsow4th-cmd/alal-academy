# -*- coding: utf-8 -*-
"""Builds webinaires.html.

Layout after coursera.org/enterprise/resources/webinar — a one-claim hero, a row
of format tabs with filters beside them, a featured item above a card grid, then
pagination. Content from predika.pro/webinaires: no session is booked, and the
four replays are reproduced with their dates, summaries and speakers. The most
recent carries Predika's own YouTube recording, its speaker's bio and its
moderator, exactly as that page does.

Nothing on this page is invented. Predika's cards are inert, so ours carry a
status chip rather than a button that would lead nowhere.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, HEADER, FOOTER, MONO, ROOT, nav_active, MNAV
from webinaires_data import UPCOMING, REPLAYS
from cartkit import cart_js


def esc(t):
    return html.escape(t, quote=False)


def ico(d, w=15):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" aria-hidden="true" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (w, w, d))


I_CAL   = ico('<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10h17"/>')
I_BELL  = ico('<path d="M18 9a6 6 0 1 0-12 0c0 5-2 6.5-2 6.5h16S18 14 18 9"/><path d="M13.7 20a2 2 0 0 1-3.4 0"/>')
I_ARROW = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="M7 17 17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.6" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CHEV = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

CSS = """
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}

  /* ── hero ───────────────────────────────────────────────────────────── */
  .wb-head{padding:116px 0 0}
  .wb-head .pill{display:inline-flex;align-items:center;gap:8px;font-family:%(mono)s;
    font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:#0E695C;
    border:1px solid #0E695C;border-radius:5px;padding:5px 9px}
  .wb-title{margin:24px 0 0;font-size:clamp(42px,6.2vw,86px);line-height:1.04;
    letter-spacing:-0.04em;font-weight:300;max-width:17ch}
  .wb-lede{margin:28px 0 0;font-size:18px;line-height:1.6;color:#7a7a7a;max-width:58ch}

  /* ── format tabs + filters (Coursera's resource bar) ────────────────── */
  .wb-bar{display:flex;align-items:center;justify-content:space-between;gap:28px;
    flex-wrap:wrap;margin-top:62px;padding-bottom:18px;
    border-bottom:1px solid rgba(31,31,31,.09)}
  .wb-tabs{display:flex;gap:8px;flex-wrap:nowrap;overflow-x:auto;overflow-y:hidden;
    scrollbar-width:none;-ms-overflow-style:none;padding:4px 0;margin:-4px 0}
  .wb-tabs::-webkit-scrollbar{display:none}
  .wb-tabs a{flex:0 0 auto;white-space:nowrap;font-size:13.5px;padding:9px 16px;
    border-radius:999px;border:1px solid rgba(31,31,31,.12);color:#7a7a7a;background:#FFFFFF;
    transition:border-color .3s ease,color .3s ease,transform .35s cubic-bezier(.2,.8,.2,1)}
  .wb-tabs a:hover{border-color:rgba(31,31,31,.3);color:#1F1F1F;transform:translateY(-2px)}
  .wb-tabs a.is-on{background:#1F1F1F;border-color:#1F1F1F;color:#FFFFFF;font-weight:500}
  .wb-filters{display:flex;gap:10px;flex-wrap:wrap}
  .sel{position:relative}
  .sel select{appearance:none;font:inherit;font-size:14px;color:#1F1F1F;background:#FFFFFF;
    border:1px solid rgba(31,31,31,.14);border-radius:9px;padding:11px 40px 11px 16px;cursor:pointer}
  .sel select:focus{outline:none;border-color:#1F1F1F}
  .sel svg{position:absolute;right:14px;top:50%%;transform:translateY(-50%%);pointer-events:none;
    color:#A7A7A7}

  /* ── next session ────────────────────────────────────────────────────
     Predika has nothing booked, so this is the empty state of the upcoming
     row rather than a card: the message its page carries, and the one action
     worth offering while the calendar is being set. */
  .wb-next{margin-top:40px;border:1px solid rgba(31,31,31,.09);border-radius:24px;
    padding:36px 40px;display:flex;align-items:center;justify-content:space-between;
    gap:30px;flex-wrap:wrap;background:#FFFFFF}
  .wb-next .ico{display:flex;align-items:center;justify-content:center;width:46px;height:46px;
    flex:none;border-radius:50%%;background:#1F1F1F;color:#FFFFFF;margin-bottom:18px}
  .wb-next h2{margin:0;font-size:21px;font-weight:500;letter-spacing:-0.025em}
  .wb-next p{margin:11px 0 0;font-size:15.5px;line-height:1.6;color:#7a7a7a;max-width:58ch}
  .wb-form{display:flex;gap:10px;flex-wrap:wrap;flex:none}
  .wb-form input{font:inherit;font-size:15px;color:#1F1F1F;background:#FFFFFF;
    border:1px solid rgba(31,31,31,.14);border-radius:12px;padding:14px 18px;min-width:262px}
  .wb-form input::placeholder{color:#A7A7A7}
  .wb-form input:focus{outline:none;border-color:#1F1F1F}
  .wb-form button{font:inherit;font-size:15px;font-weight:500;cursor:pointer;color:#FFFFFF;
    background:#1F1F1F;border:0;border-radius:12px;padding:14px 24px;display:inline-flex;
    align-items:center;gap:9px;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .wb-form button:hover{box-shadow:0 2px 6px rgba(0,0,0,.32),0 7px 16px rgba(0,0,0,.28),
    0 17px 33px rgba(0,0,0,.24)}

  /* ── replays ─────────────────────────────────────────────────────────── */
  .wb-sec{padding:84px 0 0}
  .wb-sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:24px;
    flex-wrap:wrap}
  .wb-sec h2{margin:18px 0 0;font-size:clamp(30px,3.6vw,49px);line-height:1.08;
    letter-spacing:-0.035em;font-weight:300}
  .wb-sec h2 b{font-weight:500;color:#1F1F1F}
  .wb-sec .intro{margin:18px 0 0;font-size:16.5px;line-height:1.6;color:#7a7a7a;max-width:52ch}

  /* featured replay — the recording, then who gave it */
  .wb-feat{display:grid;grid-template-columns:1.25fr 1fr;gap:42px;align-items:start;margin-top:40px}
  /* A YouTube facade: the poster frame and a play button, with the iframe
     written in only on click. The embed is third-party and would otherwise
     load its player, and set its cookies, on every visit to this page. */
  .wb-player{position:relative;border-radius:22px;overflow:hidden;background:#1F1F1F;
    aspect-ratio:16/9;cursor:pointer;border:0;padding:0;display:block;width:100%%}
  .wb-player img{width:100%%;height:100%%;object-fit:cover;display:block;
    transition:transform .6s cubic-bezier(.2,.8,.2,1),opacity .4s ease}
  .wb-player:hover img{transform:scale(1.03);opacity:.86}
  .wb-player i{position:absolute;inset:0;margin:auto;width:76px;height:76px;border-radius:50%%;
    background:rgba(255,255,255,.94);display:flex;align-items:center;justify-content:center;
    transition:transform .45s cubic-bezier(.2,.8,.2,1)}
  .wb-player:hover i{transform:scale(1.07)}
  .wb-player i:after{content:'';width:0;height:0;margin-left:5px;
    border-left:19px solid #1F1F1F;border-top:12px solid transparent;border-bottom:12px solid transparent}
  .wb-player iframe{position:absolute;inset:0;width:100%%;height:100%%;border:0}
  .wb-feat-meta{min-width:0}
  .wb-meta-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13.5px;color:#7a7a7a}
  .chip{display:inline-flex;align-items:center;gap:7px;font-family:%(mono)s;font-size:9.5px;
    letter-spacing:.12em;text-transform:uppercase;color:#0E695C;border:1px solid #0E695C;
    border-radius:5px;padding:4px 8px}
  .wb-feat-meta h3{margin:16px 0 0;font-size:clamp(22px,2.3vw,30px);line-height:1.16;
    letter-spacing:-0.03em;font-weight:500}
  .sp{display:flex;gap:16px;margin-top:26px;padding-top:24px;
    border-top:1px solid rgba(31,31,31,.09)}
  .sp:first-of-type{margin-top:28px}
  .sp{align-items:center}
  .sp img,.sp .mono{width:62px;height:62px;flex:none;border-radius:50%%;object-fit:cover;
    object-position:center;background:#EAEAEA}
  .sp .mono{display:flex;align-items:center;justify-content:center;background:#1F1F1F;
    color:#FFFFFF;font-size:17px;font-weight:500;letter-spacing:.02em}
  .sp .role{font-family:%(mono)s;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
    color:#A7A7A7}
  .sp h4{margin:7px 0 0;font-size:17px;font-weight:500;letter-spacing:-0.02em}

  /* the other replays */
  .wb-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:54px}
  .wb-card{border:1px solid rgba(31,31,31,.09);border-radius:24px;background:#FFFFFF;
    overflow:hidden;
    padding:26px 28px 28px;display:flex;flex-direction:column;
    transition:transform .5s cubic-bezier(.2,.8,.2,1),box-shadow .5s cubic-bezier(.2,.8,.2,1),
      border-color .4s ease}
  .wb-card:hover{transform:translateY(-4px);border-color:rgba(31,31,31,.18);
    box-shadow:0 4px 10px rgba(0,0,0,.04),0 16px 36px rgba(0,0,0,.06)}
  .wb-card .top{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .wb-card .date{font-family:%(mono)s;font-size:10.5px;letter-spacing:.11em;
    text-transform:uppercase;color:#7a7a7a}
  .wb-card .st{font-family:%(mono)s;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
    color:#7a7a7a;border:1px solid rgba(31,31,31,.14);border-radius:999px;padding:5px 10px;
    white-space:nowrap}
  .wb-card h3{margin:20px 0 0;font-size:20px;line-height:1.3;letter-spacing:-0.022em;font-weight:500}
  .wb-card p{margin:13px 0 0;font-size:14.5px;line-height:1.6;color:#7a7a7a}
  .wb-card .who{display:flex;align-items:center;gap:12px;margin-top:auto;padding-top:24px}
  /* the replay's own poster, with the same play badge as the featured
     player so the two read as the same object at two sizes */
  .wb-thumb{position:relative;display:block;margin:-26px -28px 22px;overflow:hidden;
    background:#EAEAEA;aspect-ratio:16/9}
  .wb-thumb img{display:block;width:100%%;height:100%%;object-fit:cover}
  /* ink badge, not white: these stills are very pale, and a white disc on
     them disappears */
  .wb-thumb i{position:absolute;left:50%%;top:50%%;width:54px;height:54px;margin:-27px 0 0 -27px;
    border-radius:50%%;background:rgba(31,31,31,.88);
    box-shadow:0 6px 20px rgba(31,31,31,.3);
    transition:transform .4s cubic-bezier(.22,1,.36,1),background .3s ease}
  .wb-thumb i:after{content:'';position:absolute;left:21px;top:17px;border-style:solid;
    border-width:10px 0 10px 16px;border-color:transparent transparent transparent #FFFFFF}
  .wb-card:hover .wb-thumb i{background:#1F1F1F}
  .wb-card:hover .wb-thumb i{transform:scale(1.08)}
  .wb-card .faces{display:flex;align-items:center}
  .wb-card .faces img{width:34px;height:34px;border-radius:50%%;object-fit:cover;
    object-position:center;border:2px solid #FFFFFF;background:#EAEAEA;margin-left:-10px}
  .wb-card .faces img:first-child{margin-left:0}
  .wb-card .names{font-size:13.5px;color:#7a7a7a;min-width:0}
  .wb-card .fmt{font-size:13px;color:#A7A7A7}
  .wb-empty-filter{display:none;grid-column:1/-1;padding:34px 0 0;font-size:15.5px;color:#7a7a7a}

  /* ── pagination ──────────────────────────────────────────────────────── */
  .wb-pager{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:52px}
  .wb-pager span{display:flex;align-items:center;justify-content:center;min-width:38px;height:38px;
    padding:0 12px;border-radius:10px;font-size:14px;color:#A7A7A7;
    border:1px solid rgba(31,31,31,.1)}
  .wb-pager span.is-on{background:#1F1F1F;border-color:#1F1F1F;color:#FFFFFF}

  /* ── what a session is ───────────────────────────────────────────────── */
  .wb-tail{padding:0 0 96px}

  /* ── tablet ──────────────────────────────────────────────────────────── */
  @media (min-width:744px) and (max-width:1199px){
    .wb-head{padding-top:72px}
    .wb-title{font-size:clamp(34px,5.4vw,56px)}
    .wb-lede{font-size:15.5px;margin-top:22px}
    .wb-bar{margin-top:44px;gap:18px}
    .wb-tabs a{font-size:12.5px;padding:8px 13px}
    .sel select{font-size:13px;padding:9px 34px 9px 13px}
    .wb-next{padding:28px}
    .wb-next h2{font-size:19px}
    .wb-next p{font-size:14px}
    .wb-form input{min-width:200px;font-size:14px;padding:12px 15px}
    .wb-form button{font-size:14px;padding:12px 18px}
    .wb-sec{padding-top:60px}
    .wb-feat{grid-template-columns:1.1fr 1fr;gap:26px;margin-top:30px}
    .wb-feat-meta h3{font-size:21px}
    .sp img,.sp .mono{width:50px;height:50px}
    .wb-grid{gap:18px;margin-top:40px}
    .wb-card{padding:20px 20px 22px}
    .wb-thumb{margin:-20px -20px 18px}
    .wb-thumb i{width:46px;height:46px;margin:-23px 0 0 -23px}
    .wb-thumb i:after{left:18px;top:14px;border-width:9px 0 9px 14px}
    .wb-card h3{font-size:17px;margin-top:16px}
    .wb-card p{font-size:13.5px}
  }

  /* ── phone ───────────────────────────────────────────────────────────── */
  @media (max-width:743px){
    .wb-head{padding-top:60px}
    .wb-lede{font-size:16px;margin-top:22px}
    /* the tab strip keeps one line and is swiped, bleeding into the gutters so
       a cut-off tab reads as scrollable — the same strip as the catalogue */
    .wb-bar{margin-top:38px;gap:16px;align-items:stretch;flex-direction:column;flex-wrap:nowrap}
    .wb-tabs{min-width:0;max-width:100%%;margin-left:-24px;margin-right:-24px;
      padding-left:24px;padding-right:24px;
      -webkit-mask-image:linear-gradient(90deg,#000 calc(100%% - 26px),transparent);
      mask-image:linear-gradient(90deg,#000 calc(100%% - 26px),transparent)}
    /* a <select> is sized by its longest option and will not shrink below it,
       so min-width:0 is what lets the two filters fit a 390px column */
    .wb-filters{gap:8px;width:100%%;min-width:0}
    .sel{flex:1 1 100%%;min-width:0}
    .sel select{width:100%%;min-width:0;text-overflow:ellipsis}
    .wb-next{padding:26px 24px;margin-top:30px}
    .wb-form{width:100%%}
    .wb-form input{min-width:0;flex:1 1 100%%}
    .wb-form button{flex:1 1 100%%;justify-content:center}
    .wb-sec{padding-top:56px}
    .wb-feat{grid-template-columns:1fr;gap:26px;margin-top:28px}
    .wb-grid{grid-template-columns:1fr;gap:16px;margin-top:36px}
    .wb-card{padding:22px 22px 24px}
    .wb-card .top{gap:10px}
    .wb-tail{padding-bottom:64px}
  }
""" % dict(mono=MONO)

TABS = [
    ("Webinaires", None),
    ("Replays", "#replays"),
]



def initials(name):
    parts = [p for p in name.replace('Dr', '').replace('Mufti', '').split() if p]
    return ''.join(p[0] for p in parts[:2]).upper()


def avatar(photo):
    """The square, face-centred crop of a portrait. assets/formateurs holds the
    full-length pictures and assets/formateurs/avatars the heads; the round
    frame needs the second."""
    if not photo:
        return None
    name = os.path.basename(photo)
    square = 'assets/formateurs/avatars/' + name
    return square if os.path.exists(os.path.join(ROOT, square)) else photo


def poster(r):
    """A replay's thumbnail. When the session has a recording, the picture is
    YouTube's own: it lives at a fixed address per video, so the card needs no
    asset and cannot fall out of step with what it points at (maxres is missing
    on some uploads, hence the fall back to hq). Sessions Predika never put on
    YouTube carry a still from the brand library instead, named after the
    session — drop a video id into the data and the real poster takes over."""
    v = r.get('video')
    if v:
        img = ('<img src="https://i.ytimg.com/vi/%s/maxresdefault.jpg" alt="" loading="lazy"\n'
               '            width="1280" height="720"\n'
               '            onerror="this.onerror=null;'
               "this.src='https://i.ytimg.com/vi/%s/hqdefault.jpg'\">" % (v['id'], v['id']))
    elif r.get('thumb'):
        img = ('<img src="%s" alt="" loading="lazy" width="1400" height="788">'
               % r['thumb'])
    else:
        return ''
    return ("""        <span class="wb-thumb">
          %s
          <i aria-hidden="true"></i>
        </span>\n""" % img)


def speaker_block(s):
    """Who spoke, not what they have done: a round portrait, their role and
    their name. The biography belongs on the course pages."""
    face = avatar(s.get('photo'))
    if face:
        pic = '<img src="%s" alt="Portrait — %s" width="62" height="62">' % (face, esc(s['name']))
    else:
        # no portrait for this speaker in our assets — a monogram rather than a
        # hotlink to predika.pro's storage
        pic = '<span class="mono" aria-hidden="true">%s</span>' % initials(s['name'])
    return ('      <div class="sp">%s<div><span class="role">%s</span>'
            '<h4>%s</h4></div></div>' % (pic, esc(s['role']), esc(s['name'])))


def build():
    feat = next((r for r in REPLAYS if r.get('featured')), None)
    rest = [r for r in REPLAYS if not r.get('featured')]

    tabs = "\n".join(
        '      <a href="%s"%s>%s</a>'
        % (href or '#webinaires', '' if href else ' class="is-on" aria-current="page"', esc(label))
        for label, href in TABS)

    themes = ['Tous les thèmes'] + sorted({r['theme'] for r in REPLAYS})
    formats = ['Tous les formats'] + sorted({r['format'] for r in REPLAYS})
    filters = "\n".join(
        '      <span class="sel"><select id="%s" aria-label="%s">%s</select>%s</span>'
        % (fid, name, "".join('<option>%s</option>' % esc(o) for o in opts), CHEV)
        for fid, name, opts in [('wbTheme', 'Thème', themes), ('wbFormat', 'Format', formats)])

    # featured
    v = feat['video']
    player = """      <button type="button" class="wb-player" id="wbPlay"
        data-src="https://www.youtube-nocookie.com/embed/%s?start=%d&autoplay=1"
        aria-label="Lire le replay : %s">
        <img src="https://i.ytimg.com/vi/%s/maxresdefault.jpg" alt="" width="1280" height="720"
          onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/%s/hqdefault.jpg'">
        <i aria-hidden="true"></i>
      </button>""" % (v['id'], v['start'], esc(feat['title']), v['id'], v['id'])

    feat_block = """    <div class="wb-feat">
%s
      <div class="wb-feat-meta">
        <div class="wb-meta-row"><span class="chip">%s</span><span>%s</span><span>&middot;</span><span>%s</span></div>
        <h3>%s</h3>
%s
      </div>
    </div>""" % (player, esc(feat['status']), esc(feat['date']), esc(feat['format']),
                 esc(feat['title']),
                 "\n".join(speaker_block(s) for s in feat['speakers']))

    cards = []
    for r in rest:
        faces = "".join('<img src="%s" alt="Portrait — %s" width="34" height="34">'
                        % (avatar(s['photo']), esc(s['name']))
                        for s in r['speakers'] if s.get('photo'))
        names = ', '.join(s['name'] for s in r['speakers'])
        who = ('        <div class="who"><span class="faces">%s</span>'
               '<span class="names">%s</span></div>' % (faces, esc(names))) if names else \
              ('        <div class="who"><span class="fmt">%s</span></div>' % esc(r['format']))
        cards.append("""      <article class="wb-card" data-theme="%s" data-format="%s">
%s        <div class="top"><span class="date">%s</span><span class="st">%s</span></div>
        <h3>%s</h3>
%s
%s
      </article>""" % (esc(r['theme']), esc(r['format']), poster(r),
                       esc(r['date']), esc(r['status']), esc(r['title']),
                       '        <p>%s</p>' % esc(r['summary']) if r['summary'] else '', who))

    body = """<div class="wrap">

  <div class="wb-head">
    <span class="pill">%(i_bell)s Gratuit sur inscription</span>
    <h1 class="wb-title">En direct avec les praticiens du métier</h1>
    <p class="wb-lede">Des sessions courtes, en français : un sujet, une heure, et vos questions
      en direct. Chaque session rejoint ensuite cette page en replay, avec la présentation de
      l'intervenant.</p>
  </div>

  <div class="wb-bar">
    <nav class="wb-tabs" aria-label="Formats de ressources">
%(tabs)s
    </nav>
    <div class="wb-filters">
%(filters)s
    </div>
  </div>

  <section class="wb-next" aria-label="Prochaine session">
    <div>
      <span class="ico">%(i_cal)s</span>
      <h2>Aucun webinaire planifié pour le moment</h2>
      <p>Retrouvez tous nos replays ci-dessous et revenez bientôt pour le prochain événement.
        Laissez votre adresse et vous recevrez l'annonce de la prochaine session, rien d'autre.</p>
    </div>
    <form class="wb-form" method="post" action="#webinaires" onsubmit="return false"
      aria-label="Être prévenu des prochaines sessions">
      <input type="email" name="email" placeholder="votre@email.com" aria-label="Adresse e-mail" required>
      <button type="submit">Me prévenir %(i_arrow)s</button>
    </form>
  </section>

  <section class="wb-sec" id="replays">
    <div class="wb-sec-head">
      <span class="kicker">À revoir</span>
      <span class="kicker">(%(count)02d)</span>
    </div>
    <h2>Replays &amp; <b>Présentations</b></h2>
    <p class="intro">Revivez tous nos webinaires passés et téléchargez les présentations
      des intervenants.</p>

%(feat)s

    <div class="wb-grid" id="wbGrid">
%(cards)s
      <p class="wb-empty-filter" id="wbNone">Aucun replay ne correspond à ces filtres.</p>
    </div>

    <nav class="wb-pager" aria-label="Pagination">
      <span class="is-on">1</span>
    </nav>
  </section>

  <div class="wb-tail"></div>
  <hr class="rule">
</div>

<script>
  /* The embed is written in on click, not on load: before that the block is a
     poster frame and a play button, so no third-party player — and no cookie
     from it — is pulled in just by opening the page. */
  (function () {
    var b = document.getElementById('wbPlay');
    if (!b) return;
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = b.getAttribute('data-src');
      f.title = b.getAttribute('aria-label');
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      b.innerHTML = '';
      b.appendChild(f);
      b.style.cursor = 'default';
    }, { once: true });
  })();

  /* Thème / Format filter the replay cards in place. */
  (function () {
    var t = document.getElementById('wbTheme'), f = document.getElementById('wbFormat');
    var grid = document.getElementById('wbGrid'), none = document.getElementById('wbNone');
    if (!t || !f || !grid) return;
    function apply() {
      var cards = grid.querySelectorAll('.wb-card'), shown = 0;
      Array.prototype.forEach.call(cards, function (c) {
        var ok = (t.selectedIndex === 0 || c.dataset.theme === t.value) &&
                 (f.selectedIndex === 0 || c.dataset.format === f.value);
        c.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      none.style.display = shown ? 'none' : 'block';
    }
    t.addEventListener('change', apply);
    f.addEventListener('change', apply);
  })();
</script>
""" % dict(tabs=tabs, filters=filters, feat=feat_block, cards="\n".join(cards),
           count=len(REPLAYS), i_bell=I_BELL, i_cal=I_CAL, i_arrow=I_ARROW)

    out = __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Webinaires — Alal Academy</title>
<meta name="description" content="Les webinaires Alal Academy : sessions en direct gratuites sur inscription, et les replays des sessions passées avec les présentations des intervenants.">
<style>%s%s</style>
</head>
<body>
%s
%s
%s
%s
</body>
</html>
""" % (BASE, CSS, nav_active(HEADER, 'webinaires') + MNAV, body,
       FOOTER.replace('{ROOT}', ''),
       cart_js('') + __import__('modals').modals('') + __import__('modals').MODAL_JS))

    open(os.path.join(ROOT, 'webinaires.html'), 'w', encoding='utf-8').write(out)
    print('webinaires.html  (%d replays, %d à venir)' % (len(REPLAYS), len(UPCOMING)))


if __name__ == '__main__':
    build()
