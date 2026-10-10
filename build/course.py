# -*- coding: utf-8 -*-
"""Builds one course page, modelled on magnific.com/academy/course/ai-suite-fundamentals.

Magnific's skeleton, kept section for section: breadcrumb; a sticky left rail
holding the module tree; a rounded hero banner carrying the title, subtitle and
a meta strip over the artwork; then a two-column body — the course overview and
a numbered module list on the left, a sticky purchase / details / tags rail on
the right.

Two departures. Magnific lists every individual episode; Predika does not expose
lesson titles publicly (the accordions need an account), so each module shows
its lesson count and running time instead. And the tutors carry portraits in the
hero, which Magnific has no equivalent for.

All copy comes from predika.pro; nothing here is invented. Palette, type, radii
and the header/footer are the Academy's.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, HEADER, FOOTER, FONT, MONO, ROOT, nav_active, MNAV
from cartkit import cart_js
from courses import COURSES, mins
from tutors import TUTORS

# The reassurance lines under the purchase button. Predika prints the same four
# on every course page, so they live here rather than in each course entry.
GUARANTEES = [
    "Confirmation sous 24h après paiement",
    "Certificat à la fin du cours",
    "Accès illimité au contenu",
    "Paiement sécurisé hors-ligne",
]

CSS = """
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}
  .crumbs{display:flex;align-items:center;gap:9px;padding:26px 0 0;font-size:13px;color:#7a7a7a}
  .crumbs a:hover{color:#1F1F1F}
  .crumbs svg{opacity:.5}
  .course-layout{display:grid;grid-template-columns:minmax(0,1fr) 474px;
    gap:52px;padding:26px 0 110px;align-items:start}

  /* hero banner */
  .hero{grid-column:1 / -1;grid-row:1;position:relative;border-radius:26px;overflow:hidden;
    background:#1F1F1F;min-height:366px;display:flex;flex-direction:column;justify-content:flex-end}
  /* The course artwork carries its own baked-in title, which sat exactly behind
     the h1. Pulling the crop up to 12%% drops that lettering out of frame and
     keeps the portrait and the dome. */
  .hero-img{position:absolute;inset:0;background-size:cover;background-position:center 12%%}
  .hero-scrim{position:absolute;inset:0;
    background:linear-gradient(180deg,rgba(31,31,31,.12) 0%%,rgba(31,31,31,.55) 46%%,rgba(31,31,31,.9) 100%%)}
  .hero-in{position:relative;padding:38px 40px 32px;color:#FFFFFF}
  .hero .kicker{color:rgba(255,255,255,.72)}
  .hero h1{margin:16px 0 0;font-size:clamp(32px,3.6vw,52px);line-height:1.04;
    letter-spacing:-0.04em;font-weight:500;max-width:17ch}
  .hero-sub{margin:14px 0 0;font-size:17px;line-height:1.5;color:rgba(255,255,255,.76);max-width:56ch}
  .hero-foot{display:flex;align-items:flex-end;justify-content:space-between;gap:34px;
    flex-wrap:wrap;margin:30px 0 0;padding-top:22px;border-top:1px solid rgba(255,255,255,.18)}
  .hero-meta{display:flex;align-items:center;gap:22px;flex-wrap:wrap;
    font-size:14px;color:rgba(255,255,255,.82)}
  .hero-meta span{display:inline-flex;align-items:center;gap:8px}
  .hero-meta svg{opacity:.8}

  /* tutor profiles in the header */
  .tutors-mini{display:flex;align-items:center;gap:4px}
  /* Portrait stack. At rest the circles overlap by 12px; hovering the stack
     opens the overlap to a 5px gap so every face clears the one in front of it,
     and the one under the cursor lifts, scales and is pulled above its
     neighbours — later siblings paint on top by default, so without the
     z-index the first portraits could never be seen whole. */
  /* padding-right reserves the 17px the trailing portraits travel on hover,
     so the spread can never run into the names beside the stack. */
  .avatars{display:flex;align-items:center;padding-right:17px}
  /* The transform lives on the IMG, never on the <a>: moving the anchor itself
     made it grow and lift out from under the cursor, firing mouseleave and
     mouseenter several times a second. The hit boxes now stay perfectly still
     and only the pictures move. */
  .avatars a{position:relative;display:block;flex:none;margin-left:-12px;line-height:0}
  .avatars a:first-child{margin-left:0}
  /* The spread is anchored on the hovered portrait: only the ones AFTER it
     slide out of the way, so the circle under the cursor never moves and you
     cannot chase it. Using transform rather than margin keeps the row's width
     fixed, so the names beside it stay put too. */
  .avatars a:hover{z-index:6}
  .avatars a:hover img{transform:translateY(-4px) scale(1.09)}
  .avatars a:hover ~ a img{transform:translateX(17px)}
  .avatars img{display:block;width:42px;height:42px;border-radius:50%%;object-fit:cover;
    object-position:center top;border:2px solid rgba(255,255,255,.9);background:#EAEAEA;
    transition:transform .45s cubic-bezier(.2,.8,.2,1),border-color .45s ease}
  .avatars a:hover img{border-color:#FFFFFF}
  /* Hovering a portrait names that person in the byline on the right, in place
     of the "Yaya SOW, Abdoulaye WANE +2" summary, rather than in a tooltip
     floating over the artwork. */
  /* The byline needs a fixed width. .hero-foot is justify-content:space-between,
     so when the text swapped from the summary to a shorter single name the whole
     block narrowed and slid right — out from under the cursor, which restored the
     summary, which widened it again: the hover oscillated several times a second.
     min-width holds the column at the longest name it will ever show. */
  .tutors-mini .tm-text{min-width:15.5em}
  .tutors-mini b{transition:opacity .2s ease;white-space:nowrap}
  .tutors-mini b.is-swapping{opacity:0}
  .tutors-mini b{display:block;font-size:13.5px;font-weight:500;color:#FFFFFF;line-height:1.3}
  .tutors-mini i{display:block;font-style:normal;font-size:12px;color:rgba(255,255,255,.66);margin-top:2px}

  /* main column */
  .col h2{margin:0 0 18px;font-size:27px;line-height:1.2;letter-spacing:-0.025em;font-weight:500}
  .sec{padding:54px 0 0}
  .lede{margin:0;font-size:17.5px;line-height:1.66;color:#7a7a7a}
  .outcomes{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:15px 26px}
  .outcomes li{display:flex;gap:12px;font-size:15.5px;line-height:1.5;color:#1F1F1F}
  .outcomes svg{flex:none;color:#0E695C;margin-top:4px}
  .prog-head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;flex-wrap:wrap}
  .prog-head p{margin:0;font-size:14px;color:#7a7a7a}
  .mods{list-style:none;margin:20px 0 0;padding:0;counter-reset:n;
    border:1px solid rgba(31,31,31,.08);border-radius:18px;overflow:hidden}
  .mods li{counter-increment:n;display:flex;align-items:center;gap:18px;padding:19px 22px;
    border-top:1px solid rgba(31,31,31,.08);transition:background .3s ease}
  .mods li:first-child{border-top:0}
  .mods li:hover{background:#FCFBF8}
  .mods .n{font-family:%(mono)s;font-size:11.5px;color:#A7A7A7;flex:none;width:20px}
  .mods .t{flex:1;min-width:0;font-size:16px;line-height:1.4}
  .mods .t small{display:block;margin-top:4px;font-size:13px;color:#7a7a7a}
  .mods .d{flex:none;font-size:13.5px;color:#7a7a7a;white-space:nowrap}

  /* tutors */
  .tut{display:flex;gap:22px;padding:26px 0;border-top:1px solid rgba(31,31,31,.08)}
  .tut:first-of-type{border-top:0;padding-top:4px}
  .tut-photo{width:104px;height:104px;flex:none;border-radius:16px;object-fit:cover;
    object-position:center top;background:#EAEAEA}
  .tut h3{margin:0;font-size:19px;font-weight:500;letter-spacing:-0.02em}
  .tut .cred{margin:7px 0 0;font-family:%(mono)s;font-size:10.5px;letter-spacing:.07em;
    text-transform:uppercase;line-height:1.6;color:#7a7a7a}
  .tut p.bio{margin:12px 0 0;font-size:14.5px;line-height:1.6;color:#7a7a7a}
  .tut .li{display:inline-flex;align-items:center;gap:7px;margin-top:13px;font-size:13px;
    font-weight:500;color:#1F1F1F}
  .tut .li:hover{color:#0E695C}

  /* right rail */
  .rail{position:sticky;top:104px;display:flex;flex-direction:column;gap:14px}
  .buy{border:1px solid rgba(31,31,31,.09);border-radius:22px;background:#FFFFFF;overflow:hidden}
  /* height:auto matters. The <img> carries width/height attributes so the
     browser can reserve space before it loads, and that height is a
     presentational hint — with no author height to beat it, it won and
     aspect-ratio was ignored. On desktop the rail happened to be 472px wide,
     where 16/9 gives almost exactly the 267px attribute, so nothing looked
     wrong; at tablet the rail is 284px and the box stayed 267 tall, leaving a
     1.06 ratio that `cover` filled by cropping the sides off the artwork. */
  .buy-thumb{display:block;width:100%%;height:auto;aspect-ratio:16/9;
    object-fit:contain;background:#EAEAEA}
  .buy-body{padding:22px 24px 24px}
  .chip{display:inline-flex;align-items:center;gap:7px;font-family:%(mono)s;font-size:9.5px;
    letter-spacing:.12em;text-transform:uppercase;color:#1F1F1F;border:1px solid #1F1F1F;
    border-radius:5px;padding:4px 7px}
  .buy-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .enrolled{font-size:13px;color:#7a7a7a}
  .enrolled b{color:#1F1F1F;font-weight:500}
  .price{margin:18px 0 0;font-size:34px;font-weight:500;letter-spacing:-0.035em;line-height:1}
  .price span{font-size:15px;color:#7a7a7a;letter-spacing:0;margin-left:7px}
  .buy .btn-buy{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:20px;
    padding:14px 18px;border-radius:12px;background:#1F1F1F;color:#FFFFFF;font-size:14.5px;
    font-weight:500;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .buy .btn-buy:hover{box-shadow:0 2px 6px rgba(0,0,0,.32),0 7px 16px rgba(0,0,0,.28),
    0 17px 33px rgba(0,0,0,.24)}
  .buy .btn-cart{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:9px;
    padding:13px 18px;border-radius:12px;background:#FFFFFF;border:1px solid rgba(31,31,31,.14);
    color:#1F1F1F;font-size:14.5px;font-weight:500;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .buy .btn-cart:hover{box-shadow:0 2px 5px rgba(0,0,0,.10),0 6px 14px rgba(0,0,0,.09)}
  .gtee{list-style:none;margin:20px 0 0;padding:18px 0 0;border-top:1px solid rgba(31,31,31,.09);
    display:flex;flex-direction:column;gap:10px}
  .gtee li{display:flex;gap:10px;font-size:13.5px;line-height:1.45;color:#7a7a7a}
  .gtee svg{flex:none;color:#0E695C;margin-top:3px}
  .box{border:1px solid rgba(31,31,31,.09);border-radius:22px;padding:22px 24px}
  .box h4{margin:0 0 15px;font-family:%(mono)s;font-size:10px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a;font-weight:400}
  .facts{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:11px}
  .facts li{display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:14px}
  .facts li span{color:#7a7a7a}
  .tags{display:flex;flex-wrap:wrap;gap:7px}
  .tags b{font-weight:400;font-size:12.5px;color:#7a7a7a;border:1px solid rgba(31,31,31,.12);
    border-radius:999px;padding:6px 11px}
  .share{display:flex;align-items:center;gap:10px;padding:2px 2px 0;font-size:13px;color:#7a7a7a}
  .share button{font:inherit;color:#7a7a7a;background:none;border:0;cursor:pointer;padding:0;
    display:inline-flex;align-items:center;gap:7px}
  .share button:hover{color:#1F1F1F}

  /* Tablet keeps the two-column page — content plus the sticky rail — and
     shrinks the rail, the hero and the type to fit instead of stacking. */
  @media (min-width:744px) and (max-width:1240px){
    .course-layout{grid-template-columns:minmax(0,1fr) 286px;gap:30px;padding-bottom:72px}
    .hero{min-height:280px}
    .hero-in{padding:26px 26px 22px}
    .hero h1{font-size:clamp(26px,3.4vw,34px)}
    .hero-sub{font-size:14.5px}
    .hero-meta{gap:14px;font-size:12.5px}
    .avatars img{width:34px;height:34px}
    .tutors-mini b{font-size:12px}
    .tutors-mini .tm-text{min-width:12em}
    .col h2{font-size:21px}
    .sec{padding-top:40px}
    .lede{font-size:15.5px}
    .outcomes li{font-size:14px}
    .mods li{padding:15px 16px}
    .mods .t{font-size:14.5px}
    .mods .d{font-size:12.5px}
    .buy{border-radius:18px}
    .buy-body{padding:18px}
    .price{font-size:27px}
    .box{padding:18px;border-radius:18px}
    .facts li,.gtee li{font-size:12.5px}
    .tags b{font-size:11.5px;padding:5px 9px}
  }
  @media (max-width:743px){
    .course-layout{grid-template-columns:1fr;gap:0;padding-bottom:72px}
    .hero,.col,.rail{grid-column:1;grid-row:auto}
    .hero{min-height:300px}
    /* At phone width the hero is nearly square, so `cover` scales the 16:9
       artwork by height and the baked-in lettering comes back into frame.
       Oversizing the width re-establishes a vertical crop. */
    .hero-img{background-size:340%% auto;background-position:40%% 5%%}
    .hero-in{padding:28px 24px 24px}
    .rail{position:static;margin-top:46px}
    .outcomes{grid-template-columns:1fr}
    /* a module title and its running time will not share a 390px line */
    .mods li{flex-wrap:wrap;align-items:flex-start;gap:0 14px;padding:18px}
    .mods .n{padding-top:3px}
    .mods .t{flex:1 1 0;min-width:0}
    .mods .d{flex:1 0 100%%;margin:8px 0 0;padding-left:34px}
    .tut{flex-direction:column;gap:16px}
    .tut-photo{width:84px;height:84px}
  }
""" % dict(mono=MONO)

CHECK = ('<svg width="15" height="15" viewBox="5267.0 2012.42 10.0 7.16" fill="none" aria-hidden="true">'
         '<path d="M5267.75 2016L5270.58 2018.83L5276.25 2013.17" stroke="currentColor" '
         'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def ico(d, w=15):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" aria-hidden="true" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (w, w, d))

I_LEVEL  = ico('<path d="M4 20v-5M10 20V9M16 20V4M22 20v-8"/>')
I_MODULE = ico('<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5zM20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5z"/>')
I_PLAY   = ico('<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m10 9.5 4.5 2.5L10 14.5z"/>')
I_CLOCK  = ico('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/>')
I_CHEV   = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<path d="m9 6 6 6-6 6" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
I_ARROW  = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<path d="M7 17 17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
I_SHARE  = ico('<circle cx="18" cy="5.5" r="2.8"/><circle cx="6" cy="12" r="2.8"/>'
               '<circle cx="18" cy="18.5" r="2.8"/><path d="m8.5 10.7 7-3.4M8.5 13.3l7 3.4"/>', 14)


def esc(t):
    return html.escape(t, quote=False)


def avatar(photo):
    """The round-crop version of a portrait.

    assets/formateurs/NN.jpg is a full 760x1362 plate; dropped into a 42px
    circle with object-fit:cover it shows mostly jacket. avatars/NN.jpg is the
    same frame cropped square on the detected face, so the head is centred and
    still readable at 28px.
    """
    head, tail = photo.rsplit('/', 1)
    return head + '/avatars/' + tail


def build_one(C):
    total = sum(mins(m[2]) for m in C['modules'])
    dur = '%d h %02d min' % (total // 60, total % 60)
    nmod = len(C['modules'])
    tutors = [dict(TUTORS[n], name=n) for n in C['tutors']]
    # the lesson counts in the module list must add up to the figure Predika
    # prints at the top of the page; if they ever drift, stop rather than ship
    if C['modules']:
        assert sum(m[1] for m in C['modules']) == C['lessons'], C['slug']

    avatars = "\n".join(
        '        <a href="%s" target="_blank" rel="noopener" data-name="%s" '
        'aria-label="%s — LinkedIn">'
        '<img src="%s" alt="Portrait — %s" width="42" height="42"></a>'
        % (t['linkedin'], esc(t['name']), esc(t['name']), avatar(t['photo']), esc(t['name']))
        for t in tutors)
    lead_names = ', '.join(t['name'] for t in tutors[:2])
    rest = len(tutors) - 2

    outcomes = "\n".join(
        '        <li>%s<span>%s</span></li>' % (CHECK, esc(o)) for o in C['outcomes'])

    mods = "\n".join(
        '        <li id="m%d"><span class="n">%02d</span><span class="t">%s%s</span>'
        '<span class="d">%d leçon%s &middot; %s</span></li>'
        % (i + 1, i + 1, esc(m[0]),
           ('<small>%s</small>' % esc(m[3])) if m[3] else '',
           m[1], 's' if m[1] > 1 else '', m[2])
        for i, m in enumerate(C['modules']))

    gtee = "\n".join('          <li>%s<span>%s</span></li>' % (CHECK, esc(g))
                     for g in GUARANTEES)
    tags = "\n".join('          <b>%s</b>' % esc(t) for t in C['tags'])

    body = """
<div class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane">
    <a href="index.html">Accueil</a>%(chev)s
    <a href="index.html#catalogue">Cours</a>%(chev)s
    <span style="color:#1F1F1F">%(title)s</span>
  </nav>

  <div class="course-layout">

    <section class="hero">
      <span class="hero-img" style="background-image:url('%(hero_img)s')" role="img"
        aria-label="%(title)s"></span>
      <span class="hero-scrim" aria-hidden="true"></span>
      <div class="hero-in">
        <span class="kicker">Cours &middot; %(cat)s</span>
        <h1>%(title)s</h1>
        <p class="hero-sub">%(sub)s</p>
        <div class="hero-foot">
          <div class="hero-meta">
            <span>%(i_level)s %(level)s</span>
%(meta_prog)s
          </div>
          <div class="tutors-mini">
            <span class="avatars">
%(avatars)s
            </span>
            <span class="tm-text">
              <b id="tutorNames">%(lead)s%(more)s</b>
              <i>Vos formateurs</i>
            </span>
          </div>
        </div>
      </div>
    </section>

    <div class="col">
      <div class="sec" style="padding-top:44px">
        <h2>À propos de ce cours</h2>
        <p class="lede">%(desc)s</p>
      </div>

%(learn)s

%(programme)s
    </div>

    <aside class="rail">
      <div class="buy">
        <img class="buy-thumb" src="%(img)s" alt="%(title)s" width="474" height="267">
        <div class="buy-body">
        <div class="buy-top">
          <span class="chip">%(scarcity)s</span>
          %(enrolled)s
        </div>
        <p class="price">%(price)s<span>%(cur)s</span></p>
        <a class="btn-buy" href="panier.html" data-add="cours:%(slug)s">Acheter maintenant</a>
        <a class="btn-cart" href="panier.html" data-add="cours:%(slug)s">Ajouter au panier</a>
        <ul class="gtee">
%(gtee)s
        </ul>
        </div>
      </div>

      <div class="box">
        <h4>Détails du cours</h4>
        <ul class="facts">
          <li><span>Niveau</span> %(level)s</li>
%(facts_prog)s
          <li><span>Catégorie</span> %(cat)s</li>
        </ul>
      </div>

      <div class="box">
        <h4>Thèmes abordés</h4>
        <div class="tags">
%(tags)s
        </div>
      </div>

      <div class="share">
        <button type="button" id="shareBtn">%(i_share)s Partager ce cours</button>
      </div>
    </aside>

  </div>

  <hr class="rule">
</div>

<script>
  /* Portrait hover names the formateur in the byline beside the stack. */
  (function(){
    var names=document.getElementById('tutorNames');
    if(!names) return;
    var original=names.innerHTML, target=original, timer=null;
    function set(html){
      if(target===html) return;          /* compare the TARGET, not what is
                                            on screen — during the 160ms fade
                                            the old text is still in the DOM */
      target=html;
      clearTimeout(timer);
      names.classList.add('is-swapping');
      timer=setTimeout(function(){
        names.innerHTML=target; names.classList.remove('is-swapping');
      },160);
    }
    /* The name is set per portrait but restored on the STACK leaving, not on
       each portrait: the hover transform makes a circle grow and lift under the
       cursor, which fires mouseleave/mouseenter several times in a row, and
       restoring on each of those left the byline blinking and blank. */
    var stack=document.querySelector('.avatars');
    document.querySelectorAll('.avatars a').forEach(function(a){
      a.addEventListener('mouseenter',function(){ set(a.getAttribute('data-name')); });
      a.addEventListener('focus',function(){ set(a.getAttribute('data-name')); });
      a.addEventListener('blur',function(){ set(original); });
    });
    if(stack) stack.addEventListener('mouseleave',function(){ set(original); });
  })();

  (function(){
    var b=document.getElementById('shareBtn');
    if(!b) return;
    b.addEventListener('click', function(){
      var d={title:document.title, url:location.href};
      if(navigator.share){ navigator.share(d).catch(function(){}); return; }
      if(navigator.clipboard){ navigator.clipboard.writeText(location.href).then(function(){
        var t=b.lastChild; b.title='Lien copié'; }); }
    });
  })();
</script>
""" % dict(chev=I_CHEV, title=esc(C['title']), img=C['image'], slug=C['slug'],
           hero_img=C.get('hero_image') or C['image'],
           cat=esc(C['category']), sub=esc(C['subtitle']), level=esc(C['level']),
           nmod=nmod, lessons=C['lessons'], dur=dur, avatars=avatars,
           lead=esc(lead_names),
           more=('<span style="font-weight:400;opacity:.75"> +%d</span>' % rest) if rest > 0 else '', desc=esc(C['description']),
           learn=('''      <div class="sec">
        <h2>Ce que vous apprendrez</h2>
        <ul class="outcomes">
%s
        </ul>
      </div>''' % outcomes) if C['outcomes'] else '',
           scarcity=esc(C['scarcity']),
           enrolled=('<span class="enrolled"><b>%d</b> apprenant%s</span>'
                     % (C['enrolled'], 's' if C['enrolled'] > 1 else ''))
                    if C['enrolled'] else '<span></span>', price=C['price'],
           cur=C['currency'], gtee=gtee, tags=tags,
           i_level=I_LEVEL, i_share=I_SHARE,
           meta_prog=(
             '            <span>%s %d modules</span>\n'
             '            <span>%s %d leçons</span>\n'
             '            <span>%s %s</span>' % (I_MODULE, nmod, I_PLAY, C['lessons'], I_CLOCK, dur)
             if C['modules'] else
             '            <span>%s Programme à paraître</span>' % I_MODULE),
           programme=(
             '''      <div class="sec">
        <div class="prog-head">
          <h2 style="margin:0">Programme du cours</h2>
          <p>%d modules &middot; %d leçons &middot; %s</p>
        </div>
        <ol class="mods">
%s
        </ol>
      </div>''' % (nmod, C['lessons'], dur, mods)
             if C['modules'] else
             '''      <div class="sec">
        <h2>Programme du cours</h2>
        <p class="lede">Le détail des modules de ce cours n'est pas encore publié.
        Il sera ajouté ici dès sa parution.</p>
      </div>'''),
           facts_prog=(
             '          <li><span>Modules</span> %d</li>\n'
             '          <li><span>Leçons</span> %d</li>\n'
             '          <li><span>Durée</span> %s</li>' % (nmod, C['lessons'], dur)
             if C['modules'] else ''))

    out = __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s — Alal Academy</title>
<meta name="description" content="%s">
<style>%s%s</style>
</head>
<body>
%s
%s
%s
%s
</body>
</html>
""" % (html.escape(C['title']), html.escape(C['description'][:180]),
       BASE, CSS, nav_active(HEADER, 'cours') + MNAV, body,
       FOOTER.replace('{ROOT}', '../'),
       cart_js('../') + __import__('modals').modals('../') + __import__('modals').MODAL_JS))

    # the shared header/footer and every asset live one level up from cours/
    out = out.replace('href="index.html', 'href="../index.html')
    out = out.replace('href="blog.html"', 'href="../blog.html"')
    out = out.replace('href="parcours.html"', 'href="../parcours.html"')
    out = out.replace('href="webinaires.html"', 'href="../webinaires.html"')
    out = out.replace('href="panier.html"', 'href="../panier.html"')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace("url('assets/", "url('../assets/")
    out = out.replace('href="../../index.html', 'href="../index.html')
    out = out.replace('src="../../assets/', 'src="../assets/')

    os.makedirs(os.path.join(ROOT, 'cours'), exist_ok=True)
    path = os.path.join(ROOT, 'cours', C['slug'] + '.html')
    open(path, 'w', encoding='utf-8').write(out)
    print('cours/%s.html  (%s)' % (
        C['slug'],
        '%d modules, %d leçons, %s' % (nmod, C['lessons'], dur) if C['modules']
        else 'programme non publié'))


def build():
    for C in COURSES:
        build_one(C)


if __name__ == '__main__':
    build()
