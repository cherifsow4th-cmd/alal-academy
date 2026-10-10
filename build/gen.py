# -*- coding: utf-8 -*-
"""Builds blog.html (index) and one page per article.

Index layout modelled on yucca.co.za/blog: oversized page title, a featured
split block (image left, meta + title + arrow right), a hairline, then a
section row carrying a category filter, then a three-column card grid.

Article layout modelled on awwwards.com article pages: small centred meta,
oversized centred headline, byline, full-bleed hero, then a single measured
text column with large sentence-case section headings.

Both rebuilt in Alal's palette, type and radii.
"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from articles_a import A
from articles_b import B

ART = sorted(A + B, key=lambda a: a['iso'], reverse=True)
ROOT = os.path.join(os.path.dirname(__file__), '..')

FONT = "'General Sans','Magnetik',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,monospace"

BASE = """
  *{box-sizing:border-box}
  body{margin:0;background:#FFFFFF;color:#1F1F1F;font-family:%(font)s;
    -webkit-font-smoothing:antialiased}
  a{color:inherit;text-decoration:none}
  img{max-width:100%%;display:block}
  .wrap{max-width:1920px;margin:0 auto;padding:0 52px}
  .kicker{font-family:%(mono)s;font-size:10.5px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a}
  header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.86);
    backdrop-filter:blur(14px);border-bottom:1px solid rgba(31,31,31,.07)}
  .nav{max-width:1920px;margin:0 auto;padding:18px 52px;display:flex;
    align-items:center;justify-content:space-between;gap:32px}
  .nav{align-items:stretch}
  .nav>a:first-child,.nav-actions{align-self:center}
  .nav-links{display:flex;align-items:stretch;gap:30px;font-size:14.5px;color:#7a7a7a}
  /* "Active Indicator Grow", ported from the Alal Finance header
     (alal-finance-site/index.html, .nav-toplevel::before / .nav-link-plain::before):
     a 4.4px bar flush with the header's bottom edge, rounded on its top two
     corners only, edge to edge with the text. Rest scaleY(0) anchored at the
     bottom, hover or current page scaleY(1), 0.6s on the site's own --ease-btn
     cubic-bezier(.22,1,.36,1). Finance sets it on hover and on the open group;
     here the second trigger is the page you are on. */
  .nav-links a{position:relative;display:flex;align-items:center;white-space:nowrap;
    color:#7a7a7a;transition:color .35s cubic-bezier(.22,1,.36,1)}
  .nav-links a:hover,.nav-links a.is-active{color:#1F1F1F}
  /* -19px, not 0: the bar has to clear .nav's 18px bottom padding plus the
     header's 1px rule to sit flush on the header edge, the way Finance's does
     (its nav items are full-height, ours are not). */
  .nav-links a:before{content:'';position:absolute;left:0;right:0;bottom:-19px;height:4.4px;
    background:#1F1F1F;border-radius:4px 4px 0 0;transform:scaleY(0);transform-origin:50%% 100%%;
    transition:transform .6s cubic-bezier(.22,1,.36,1)}
  .nav-links a:hover:before,.nav-links a.is-active:before{transform:scaleY(1)}
  .nav-actions{display:flex;align-items:center;gap:10px;flex:none}
  .btn{display:inline-flex;align-items:center;gap:10px;font-size:14.5px;font-weight:500;
    padding:10px 18px;border-radius:10px;transition:box-shadow .3s ease,transform .45s cubic-bezier(.2,.8,.2,1)}
  .btn-dark{background:#1F1F1F;color:#FFFFFF}
  .btn-dark .btn-short{display:none}
  .btn-dark:hover{box-shadow:0 2px 6px rgba(0,0,0,.32),0 7px 16px rgba(0,0,0,.28),
    0 17px 33px rgba(0,0,0,.24),0 34px 60px rgba(0,0,0,.16)}
  .btn-ink{height:40px;padding:0 16px;border:1px solid rgba(31,31,31,.14);background:#FFFFFF;color:#1F1F1F;border-radius:10px;
    display:inline-flex;align-items:center;gap:8px;font-size:14.5px;font-weight:500}
  .btn-ink:hover{box-shadow:0 2px 5px rgba(0,0,0,.10),0 6px 14px rgba(0,0,0,.09),0 16px 30px rgba(0,0,0,.08)}
  .btn-icon{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;flex:none;
    border:1px solid rgba(31,31,31,.14);border-radius:10px;background:#FFFFFF;color:#1F1F1F}
  .btn-icon:hover{box-shadow:0 2px 5px rgba(0,0,0,.10),0 6px 14px rgba(0,0,0,.09)}
  .nav-sep{width:1px;height:26px;background:rgba(31,31,31,.14);flex:none;margin:0 4px}
  .nav-actions svg{display:block;flex:none}
  footer a:hover{color:#1F1F1F}
  /* The footer's padding and gap are inline, so they survive the page's own
     mobile rules and used to push the document to ~500px wide at 390px. The
     !important overrides are the only way to reach an inline style, and
     min-width:0 stops a long link like "Parcours certifiants" setting the
     column floor. */
  @media (max-width:743px){
    .aa-footer-grid{grid-template-columns:1fr 1fr !important;gap:34px 22px !important}
    .aa-footer-grid>*{min-width:0}
    footer{padding-left:24px !important;padding-right:24px !important}
  }
  /* ── Phone navigation ──────────────────────────────────────────────────
     Below 744px the links and controls move into a slide-in panel behind a
     hamburger — the same pattern as the homepage. */
  .burger{display:none;width:40px;height:40px;flex:none;padding:0;cursor:pointer;
    border:1px solid rgba(31,31,31,.14);border-radius:10px;background:#FFFFFF;
    flex-direction:column;align-items:center;justify-content:center;gap:5px}
  .burger span{display:block;width:17px;height:1.6px;background:#1F1F1F;border-radius:2px}
  .mnav[hidden]{display:none}
  .mnav{position:fixed;inset:0;z-index:120}
  .mnav-scrim{position:absolute;inset:0;background:rgba(31,31,31,.42);opacity:0;
    transition:opacity .32s ease}
  .mnav.is-open .mnav-scrim{opacity:1}
  .mnav-panel{position:absolute;top:0;right:0;height:100%%;width:min(86vw,360px);
    background:#FFFFFF;box-shadow:-24px 0 60px rgba(31,31,31,.18);
    padding:18px 24px 26px;display:flex;flex-direction:column;gap:2px;overflow-y:auto;
    transform:translateX(100%%);transition:transform .36s cubic-bezier(.22,1,.36,1)}
  .mnav.is-open .mnav-panel{transform:translateX(0)}
  .mnav-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px}
  .mnav-head img{height:26px;width:auto;display:block}
  .mnav-close{width:36px;height:36px;flex:none;padding:0;cursor:pointer;color:#1F1F1F;
    border:1px solid rgba(31,31,31,.14);border-radius:10px;background:#FFFFFF;
    display:flex;align-items:center;justify-content:center}
  .mnav-close svg{width:17px;height:17px}
  .mnav-panel>a{display:block;padding:14px 0;font-size:20px;font-weight:500;
    letter-spacing:-.02em;color:#1F1F1F;border-bottom:1px solid rgba(31,31,31,.07)}
  .mnav-foot{margin-top:auto;padding-top:24px;display:flex;flex-direction:column;gap:10px}
  .mnav-cta{display:flex;align-items:center;justify-content:center;gap:9px;padding:15px 20px;
    border-radius:12px;background:#1F1F1F;color:#FFFFFF;font-size:15px;font-weight:500}
  .mnav-cta span{font-size:13px}
  /* the three controls stack, full width, one above the other */
  .mnav-row{display:grid;grid-template-columns:1fr;gap:10px}
  .mnav-ghost{display:flex;align-items:center;justify-content:center;gap:8px;padding:13px 10px;
    border-radius:12px;border:1px solid rgba(31,31,31,.14);background:#FFFFFF;color:#1F1F1F;
    font-size:14px;font-weight:500}
  body.mnav-open{overflow:hidden}
  body.mnav-open header{backdrop-filter:none !important}
  @media (prefers-reduced-motion:reduce){ .mnav-panel,.mnav-scrim{transition:none} }
  @media (max-width:743px){
    .burger{display:flex}
    .nav-actions{display:none !important}
  }
  @media (max-width:743px){
    .wrap,.nav,.foot{padding-left:24px;padding-right:24px}
    .nav-links{display:none}
    .btn-ink{width:40px;padding:0;justify-content:center}
    .btn-ink .nav-label{display:none}
    .nav-sep{margin:0 2px;height:22px}
  }
  /* ── Tablet ───────────────────────────────────────────────────────────
     744-1199px keeps the desktop chrome — full menu, four-column footer — and
     fits it by tightening gutters, type and controls rather than collapsing. */
  @media (min-width:744px) and (max-width:1199px){
    .wrap,.nav,.foot{padding-left:28px;padding-right:28px}
    .nav a img{height:25px}
    .nav-links{gap:17px;font-size:13px}
    .nav-actions{gap:7px}
    .btn,.btn-ink{font-size:13px}
    .btn{padding:8px 13px}
    .btn-ink{height:34px;width:34px;padding:0;justify-content:center}
    .btn-ink .nav-label{display:none}
    .btn-icon{width:34px;height:34px}
    .btn-dark .btn-long{display:none}
    .btn-dark .btn-short{display:inline}
    footer{padding:64px 28px 36px !important}
    .aa-footer-grid{gap:28px !important}
    .aa-footer-grid>*{min-width:0}
  }

  /* Below ~560px the lockup plus three controls no longer fit a 390px row.
     The lockup is flex:none so it can never be squashed out of proportion
     again, so the row is made to fit by shrinking it and compacting the
     sign-up button instead. */
  @media (max-width:560px){
    .nav{gap:10px;padding-left:20px;padding-right:20px}
    .nav a img{height:24px}
    .nav-actions{gap:7px}
    .btn-dark{font-size:13px;padding:9px 13px}
    .btn-dark .btn-arrow,.btn-dark .btn-long{display:none}
    .btn-dark .btn-short{display:inline}
  }
""" % dict(font=FONT, mono=MONO) + __import__('cartkit').CART_CSS_SHARED + __import__('modals').MODAL_CSS + __import__('loader').LOADER_CSS

HEADER = """<header>
  <div class="nav">
    <a href="index.html" aria-label="Alal Academy — accueil" style="flex:none"><img src="assets/logo/alal-academy-lockup.png" alt="Alal Academy" width="162" height="30" style="height:30px;width:auto;max-width:none"></a>
    <nav class="nav-links">
      <a href="index.html#catalogue" data-nav="cours">Cours</a>
      <a href="index.html#aaoifi" data-nav="aaoifi">AAOIFI</a>
      <a href="parcours.html" data-nav="parcours">Parcours</a>
      <a href="blog.html" data-nav="blog">Blog</a>
      <a href="webinaires.html" data-nav="webinaires">Webinaires</a>
    </nav>
    <button type="button" class="burger" id="aaBurger" aria-label="Menu"
      aria-expanded="false" aria-controls="aaMobileNav"><span></span><span></span></button>
    <div class="nav-actions">
      <a href="#login" class="btn-ink">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 11.5a3.75 3.75 0 1 0 0-7.5 3.75 3.75 0 0 0 0 7.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M4.5 20c0-3.45 3.36-6.25 7.5-6.25s7.5 2.8 7.5 6.25" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg><span class="nav-label">Connexion</span></a>
      <a href="#signup" class="btn btn-dark"><span class="btn-long">Créer un compte</span><span class="btn-short">S'inscrire</span> <span class="btn-arrow" style="font-size:13px">&rarr;</span></a>
      <span class="nav-sep" aria-hidden="true"></span>
      <a href="panier.html" class="btn-icon cart-btn" aria-label="Panier">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M2.75 3.25h1.8a1 1 0 0 1 .98.8l.38 1.95m0 0 1.72 8.6a1.6 1.6 0 0 0 1.57 1.28h7.76a1.6 1.6 0 0 0 1.57-1.26l1.47-6.62a1.2 1.2 0 0 0-1.17-1.46H5.91Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M9.6 20.75a1.35 1.35 0 1 0 0-2.7 1.35 1.35 0 0 0 0 2.7ZM17.1 20.75a1.35 1.35 0 1 0 0-2.7 1.35 1.35 0 0 0 0 2.7Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg><span class="cart-count is-zero" id="aaCartCount">0</span>
      </a>
    </div>
  </div>
</header>"""

MNAV = """<div class="mnav" id="aaMobileNav" hidden>
  <div class="mnav-scrim" data-aa-mclose></div>
  <nav class="mnav-panel" aria-label="Menu principal">
    <div class="mnav-head">
      <img src="assets/logo/alal-academy-lockup.png" alt="Alal Academy" width="162" height="30">
      <button type="button" class="mnav-close" data-aa-mclose aria-label="Fermer le menu">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"
          stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
      </button>
    </div>
    <a href="index.html#catalogue">Cours</a>
    <a href="index.html#aaoifi">AAOIFI</a>
    <a href="parcours.html">Parcours</a>
    <a href="blog.html">Blog</a>
    <a href="webinaires.html">Webinaires</a>
    <div class="mnav-foot">
      <a href="#signup" class="mnav-cta">Cr\u00e9er un compte <span>&rarr;</span></a>
      <div class="mnav-row">
        <a href="#login" class="mnav-ghost">Connexion</a>
        <a href="panier.html" class="mnav-ghost">Panier</a>
      </div>
    </div>
  </nav>
</div>

<script>
  (function () {
    var burger = document.getElementById('aaBurger');
    var nav = document.getElementById('aaMobileNav');
    if (!burger || !nav) return;
    var panel = nav.querySelector('.mnav-panel');
    function open() {
      nav.hidden = false;
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ nav.classList.add('is-open'); }); });
      document.body.classList.add('mnav-open');
      burger.setAttribute('aria-expanded','true');
      var f = panel.querySelector('a, button'); if (f) f.focus();
    }
    function close() {
      nav.classList.remove('is-open');
      document.body.classList.remove('mnav-open');
      burger.setAttribute('aria-expanded','false');
      burger.focus();
      setTimeout(function(){ if(!nav.classList.contains('is-open')) nav.hidden = true; }, 380);
    }
    burger.addEventListener('click', open);
    nav.addEventListener('click', function(e){
      if (e.target.closest('[data-aa-mclose]') || e.target.closest('a[href]')) close();
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && nav.classList.contains('is-open')) close();
    });
    panel.addEventListener('keydown', function(e){
      if (e.key !== 'Tab') return;
      var it = panel.querySelectorAll('a[href], button'); if (!it.length) return;
      var first = it[0], last = it[it.length-1];
      if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
    });
    window.matchMedia('(min-width:744px)').addEventListener('change', function(m){
      if (m.matches && nav.classList.contains('is-open')) close();
    });
  })();
</script>"""


FOOTER = open(os.path.join(os.path.dirname(__file__), 'footer.html'), encoding='utf-8').read()


def nav_active(markup, key):
    """Mark one header link as the page you are on."""
    return markup.replace('data-nav="%s"' % key, 'data-nav="%s" class="is-active"' % key)


def page(title, desc, css, body, root='', active='blog'):
    from cartkit import cart_js
    return __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
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
""" % (html.escape(title), html.escape(desc), BASE, css, nav_active(HEADER, active) + MNAV,
       body, FOOTER.replace('{ROOT}', root),
       cart_js(root) + __import__('modals').modals(root) + __import__('modals').MODAL_JS))


# ─────────────────────────────── index ───────────────────────────────
INDEX_CSS = """
  .blog-head{padding:120px 0 0}
  .blog-title{margin:0;font-size:clamp(46px,7vw,98px);line-height:1.04;
    letter-spacing:-0.04em;font-weight:300;max-width:16ch}
  .feat{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding:60px 0 88px}
  .feat>span{display:block}
  .feat-img{display:block;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#EAEAEA}
  .feat-img img{width:100%;height:100%;object-fit:cover}
  .feat-meta{display:flex;align-items:center;gap:11px;font-size:17.5px;color:#7a7a7a}
  .feat-meta b{font-weight:400;color:#7a7a7a}
  .feat-meta b:after{content:'\\2022';margin-left:11px;color:#A7A7A7}
  .feat-meta span{color:#7a7a7a}
  .feat h2{margin:18px 0 0;font-size:clamp(26px,2.9vw,36px);line-height:1.22;
    letter-spacing:-0.02em;font-weight:400;max-width:22ch}
  .feat-go{margin-top:30px;width:46px;height:46px;border-radius:10px;background:#1F1F1F;
    color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:15px}
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}
  .list-head{display:flex;align-items:center;justify-content:space-between;gap:24px;
    flex-wrap:wrap;padding:88px 0 34px}
  .list-head h2{margin:0;font-size:clamp(32px,4.4vw,49px);line-height:1.1;
    letter-spacing:-0.03em;font-weight:300}
  .filter{position:relative}
  .filter select{appearance:none;font:inherit;font-size:14px;color:#1F1F1F;background:#FFFFFF;
    border:1px solid rgba(31,31,31,.14);border-radius:9px;padding:11px 40px 11px 16px;cursor:pointer}
  .filter svg{position:absolute;right:14px;top:50%;transform:translateY(-50%);pointer-events:none}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:88px 27px;padding-bottom:110px}
  .post{display:block}
  .post-img{display:block;aspect-ratio:5/3;border-radius:12px;overflow:hidden;background:#EAEAEA}
  .post-img img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
  .post:hover .post-img img{transform:scale(1.03)}
  .post-meta{display:flex;align-items:center;gap:11px;margin-top:18px;font-size:17.5px;color:#7a7a7a}
  .post-meta b{font-weight:400;color:#7a7a7a}
  .post-meta b:after{content:'\\2022';margin-left:11px;color:#A7A7A7}
  .post-meta span{color:#7a7a7a}
  .post h3{margin:10px 0 0;font-size:22px;line-height:1.4;letter-spacing:-0.01em;font-weight:400}
  .empty{padding:0 0 110px;color:#7a7a7a;font-size:15px}
  /* Tablet keeps the three-column grid and the split feature block, scaled. */
  @media (min-width:744px) and (max-width:1199px){
    .blog-title{font-size:clamp(34px,5.4vw,54px)}
    .feat{gap:34px;padding:40px 0 56px}
    .feat h2{font-size:24px}
    .feat-meta,.post-meta{font-size:14px;gap:8px}
    .feat-meta b:after,.post-meta b:after{margin-left:8px}
    .list-head{padding:56px 0 24px}
    .list-head h2{font-size:30px}
    .grid{gap:54px 18px;padding-bottom:72px}
    .post h3{font-size:17px;line-height:1.35}
  }
  @media (max-width:743px){
    .feat{grid-template-columns:1fr;gap:28px;padding:44px 0 56px}
    .grid{grid-template-columns:1fr;gap:34px}
    .blog-head{padding-top:72px}
    .list-head{padding-top:56px}
  }
"""

def card(a):
    return """        <a class="post" href="blog/%(slug)s.html" data-cat="%(cat)s">
          <span class="post-img"><img src="assets/blog/%(img)s.png" alt="" loading="lazy"></span>
          <span class="post-meta"><b>%(cat)s</b> <span>%(date)s</span></span>
          <h3>%(title)s</h3>
        </a>""" % dict(slug=a['slug'], cat=html.escape(a['cat']), date=a['date'],
                       img=a['img'], title=html.escape(a['title']))


def build_index():
    f = ART[0]
    cats = []
    for a in ART:
        if a['cat'] not in cats: cats.append(a['cat'])
    opts = "\n".join('          <option value="%s">%s</option>' % (html.escape(c), html.escape(c)) for c in cats)
    body = """<main>
  <div class="wrap">
    <section class="blog-head">
      <h1 class="blog-title">Derniers articles</h1>
    </section>

    <a class="feat" href="blog/%(fslug)s.html">
      <span class="feat-img"><img src="assets/blog/%(fimg)s.png" alt=""></span>
      <span>
        <span class="feat-meta"><b>%(fcat)s</b> <span>%(fdate)s</span></span>
        <h2>%(ftitle)s</h2>
        <span class="feat-go">&rarr;</span>
      </span>
    </a>
  </div>

  <hr class="rule">

  <div class="wrap">
    <div class="list-head">
      <h2 id="blogHeading">Tous les articles</h2>
      <span class="filter">
        <label class="kicker" for="blogFilter" style="position:absolute;left:-9999px">Filtrer par catégorie</label>
        <select id="blogFilter">
          <option value="all">Catégorie : toutes</option>
%(opts)s
        </select>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="#1F1F1F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </span>
    </div>
    <div class="grid" id="blogGrid">
%(cards)s
    </div>
    <p class="empty" id="blogEmpty" hidden>Aucun article dans cette catégorie pour le moment.</p>
  </div>

  <hr class="rule">
</main>

<script>
  /* category filter — the cards carry their own data-cat, so no re-render */
  (function(){
    var sel=document.getElementById('blogFilter'),
        grid=document.getElementById('blogGrid'),
        empty=document.getElementById('blogEmpty');
    if(!sel||!grid) return;
    sel.addEventListener('change', function(){
      var v=sel.value, shown=0;
      document.getElementById('blogHeading').textContent =
        (v==='all') ? 'Tous les articles' : v;
      Array.prototype.forEach.call(grid.children, function(c){
        var ok = (v==='all' || c.getAttribute('data-cat')===v);
        c.style.display = ok ? '' : 'none';
        if(ok) shown++;
      });
      empty.hidden = shown>0;
    });
  })();
</script>""" % dict(fslug=f['slug'], fimg=f['img'], fcat=html.escape(f['cat']),
                    fdate=f['date'], ftitle=html.escape(f['title']),
                    opts=opts, cards="\n".join(card(a) for a in ART[1:]))
    open(os.path.join(ROOT, 'blog.html'), 'w', encoding='utf-8').write(
        page("Observatoire de la finance islamique — Alal Academy",
             "Analyses, retours d'expérience et veille réglementaire en finance islamique.",
             INDEX_CSS, body))


# ────────────────────────────── articles ──────────────────────────────
ART_CSS = """
  .wrap{max-width:1340px}
  .a-head{padding:78px 0 0;text-align:center}
  .a-meta{display:flex;align-items:center;justify-content:center;gap:14px;
    font-family:%(mono)s;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#7a7a7a}
  .a-meta span:not(:last-child):after{content:'';display:inline-block;width:3px;height:3px;
    border-radius:50%%;background:#A7A7A7;margin-left:14px;vertical-align:middle}
  .a-title{margin:26px auto 0;font-size:clamp(34px,5.2vw,72px);line-height:1.04;
    letter-spacing:-0.035em;font-weight:300;max-width:18ch}
  .a-by{margin:26px 0 0;font-size:14px;color:#7a7a7a}
  .a-hero{margin:56px 0 0;aspect-ratio:16/9;border-radius:18px;overflow:hidden;background:#EAEAEA}
  .a-hero img{width:100%%;height:100%%;object-fit:cover}
  .a-body{max-width:820px;margin:0 auto;padding:72px 0 0}
  .a-body p{margin:0 0 30px;font-size:20px;line-height:1.66;color:#1F1F1F;font-weight:300}
  /* the standfirst and the section headings share one oversized size — the jump
     from 20px body to 48px heading is what gives the reading layout its rhythm */
  .a-body .lead{font-size:clamp(30px,3.6vw,48px);line-height:1.2;letter-spacing:-0.03em;
    font-weight:400;margin-bottom:46px}
  .a-body h2{margin:76px 0 46px;font-size:clamp(30px,3.6vw,48px);line-height:1.2;
    letter-spacing:-0.03em;font-weight:400}
  .a-body figure{margin:0 0 30px}
  .a-body figure img{width:100%%;border-radius:12px;display:block}
  .a-body figcaption{margin-top:14px;font-size:14px;line-height:1.2;font-weight:300;color:#1F1F1F}
  .a-body ul{margin:0 0 30px;padding:0;list-style:none}
  .a-body li{position:relative;padding-left:26px;margin:0 0 15px;font-size:20px;
    line-height:1.6;font-weight:300}
  .a-body li:before{content:'';position:absolute;left:4px;top:13px;width:6px;height:6px;
    border-radius:50%%;background:#0E695C}
  .a-body b{font-weight:500}
  blockquote{margin:46px 0;padding:0 0 0 28px;border-left:2px solid #0E695C}
  blockquote p{font-size:26px;line-height:1.4;font-weight:300;margin:0 0 14px}
  blockquote cite{font-style:normal;font-family:%(mono)s;font-size:10.5px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a}
  .a-cta{max-width:820px;margin:70px auto 0;padding:38px 40px;border-radius:18px;background:#EAEAEA}
  .a-cta h3{margin:12px 0 0;font-size:26px;line-height:1.2;letter-spacing:-0.02em;font-weight:400}
  .a-cta p{margin:12px 0 24px;font-size:16px;line-height:1.6;color:#7a7a7a}
  .a-more{padding:100px 0 110px}
  .a-more h2{margin:0 0 34px;font-size:clamp(26px,2.6vw,34px);letter-spacing:-0.025em;font-weight:400}
  .a-more-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:36px}
  .a-back{display:inline-flex;align-items:center;gap:9px;margin:64px 0 0;font-size:14.5px;color:#7a7a7a}
  .a-back:hover{color:#1F1F1F}
  @media (max-width:900px){
    .a-head{padding-top:48px}
    .a-hero{margin-top:34px;border-radius:12px}
    .a-body{padding-top:44px}
    .a-body p,.a-body li{font-size:17px}
    .a-cta{padding:30px 24px}
    .a-more-grid{grid-template-columns:1fr}
    .a-more{padding:64px 0 72px}
  }
""" % dict(mono=MONO)


def render_blocks(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'lead':
            out.append('      <p class="lead">%s</p>' % b[1])
        elif k == 'p':
            out.append('      <p>%s</p>' % b[1])
        elif k == 'h2':
            out.append('      <h2>%s</h2>' % b[1])
        elif k == 'ul':
            lis = "\n".join('        <li>%s</li>' % x for x in b[1])
            out.append('      <ul>\n%s\n      </ul>' % lis)
        elif k == 'fig':
            cap = ('\n        <figcaption>%s</figcaption>' % b[2]) if len(b) > 2 and b[2] else ''
            out.append('      <figure><img src="../assets/blog/%s" alt="">%s</figure>' % (b[1], cap))
        elif k == 'quote':
            out.append('      <blockquote><p>« %s »</p><cite>%s</cite></blockquote>' % (b[1], b[2]))
    return "\n".join(out)


def mini(a):
    return """        <a class="post" href="%(slug)s.html">
          <span class="post-img"><img src="../assets/blog/%(img)s.png" alt="" loading="lazy"></span>
          <span class="post-meta"><b>%(cat)s</b> <span>%(date)s</span></span>
          <h3>%(title)s</h3>
        </a>""" % dict(slug=a['slug'], img=a['img'], cat=html.escape(a['cat']),
                       date=a['date'], title=html.escape(a['title']))


MINI_CSS = """
  .post{display:block}
  .post-img{display:block;aspect-ratio:5/3;border-radius:12px;overflow:hidden;background:#EAEAEA}
  .post-img img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
  .post:hover .post-img img{transform:scale(1.03)}
  .post-meta{display:flex;align-items:center;gap:11px;margin-top:18px;font-size:16px;color:#7a7a7a}
  .post-meta b{font-weight:400;color:#7a7a7a}
  .post-meta b:after{content:'\\2022';margin-left:11px;color:#A7A7A7}
  .post-meta span{color:#7a7a7a}
  .post h3{margin:10px 0 0;font-size:20px;line-height:1.38;letter-spacing:-0.01em;font-weight:400}
"""


def build_article(a, others):
    rel = [x for x in others if x['slug'] != a['slug']]
    # prefer same-category neighbours, then fall back to the most recent
    same = [x for x in rel if x['cat'] == a['cat']]
    pick = (same + [x for x in rel if x not in same])[:3]
    body = """<main>
  <div class="wrap">
    <article>
      <div class="a-head">
        <div class="a-meta"><span>%(cat)s</span><span>%(date)s</span><span>%(read)s de lecture</span></div>
        <h1 class="a-title">%(title)s</h1>
        <p class="a-by">Observatoire Alal Academy</p>
      </div>
      <div class="a-hero"><img src="../assets/blog/%(img)s.png" alt=""></div>
      <div class="a-body">
%(blocks)s
      </div>
    </article>

    <aside class="a-cta">
      <span class="kicker">Prêt à approfondir ?</span>
      <h3>Formez-vous sur ce sujet avec Alal Academy</h3>
      <p>Des cours pratiques, des cas réels africains, et une certification reconnue AAOIFI &middot; IFSB.</p>
      <a class="btn btn-dark" href="%(chref)s">%(clabel)s <span style="font-size:13px">&rarr;</span></a>
    </aside>

    <section class="a-more">
      <h2>Lire aussi</h2>
      <div class="a-more-grid">
%(more)s
      </div>
      <a class="a-back" href="../blog.html"><span style="font-size:13px">&larr;</span> Tous les articles</a>
    </section>
  </div>
</main>""" % dict(cat=html.escape(a['cat']), date=a['date'], read=a['read'],
                  title=html.escape(a['title']), img=a['img'],
                  blocks=render_blocks(a['blocks']),
                  # a course page sits in cours/ ; an anchor still belongs to the homepage
                  chref=(('../' + a['course'][0]) if a['course'][0].startswith('cours/')
                         else ('../index.html' + a['course'][0])),
                  clabel=html.escape(a['course'][1]),
                  more="\n".join(mini(x) for x in pick))

    css = (ART_CSS + MINI_CSS).replace('assets/logo/', '../assets/logo/')
    out = page(a['title'] + " — Alal Academy", a['excerpt'], ART_CSS + MINI_CSS, body, root='../')
    # the shared header/footer live one level up from blog/
    out = out.replace('href="index.html', 'href="../index.html')
    out = out.replace('href="blog.html"', 'href="../blog.html"')
    out = out.replace('href="parcours.html"', 'href="../parcours.html"')
    out = out.replace('href="webinaires.html"', 'href="../webinaires.html"')
    out = out.replace('href="panier.html"', 'href="../panier.html"')
    out = out.replace('src="assets/logo/', 'src="../assets/logo/')
    out = out.replace("url('assets/", "url('../assets/")
    out = out.replace('href="../../index.html', 'href="../index.html')
    out = out.replace('src="../../assets/logo/', 'src="../assets/logo/')
    os.makedirs(os.path.join(ROOT, 'blog'), exist_ok=True)
    open(os.path.join(ROOT, 'blog', a['slug'] + '.html'), 'w', encoding='utf-8').write(out)


if __name__ == '__main__':
    build_index()
    for a in ART:
        build_article(a, ART)
    print("blog.html + %d article pages" % len(ART))
