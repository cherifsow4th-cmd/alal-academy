# -*- coding: utf-8 -*-
"""Builds parcours.html (the list) and one page per parcours.

The detail page follows pmi.org/certifications/certified-associate-capm section
for section where a bundle of courses has an equivalent — hero with its "no
experience required" line, head figures, who should apply, the content outline
with its weighting, eligibility, a five-step application, what comes next, the
people, and an FAQ — and drops what we have nothing to source (PMI's salary and
ranking statistics, its testimonials carousel).

Its chrome is the homepage's: a sticky section bar under the header whose
buttons light up with the section you are in, carrying the Alal Finance
indicator, and full-bleed bands alternating white and #EAEAEA. There is no side
rail: the price, what the inscription includes, the payment plans and the
figures are sections of the page like the rest.

Every number (lesson counts, running times, the à-la-carte total, the saving,
each instalment) is computed from courses.py at build time; only editorial copy
comes from parcours_data.py.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, HEADER, FOOTER, FONT, MONO, ROOT, nav_active, MNAV
from courses import COURSES, mins
from tutors import TUTORS
from parcours_data import PARCOURS
from cartkit import cart_js
from svc_icons import AUDIENCE_ICONS

BY_SLUG = {c['slug']: c for c in COURSES}
GREY = '#EAEAEA'


def esc(t):
    return html.escape(t, quote=False)


def fr(n):
    s = '%d' % n
    out = ''
    while len(s) > 3:
        out = ' ' + s[-3:] + out
        s = s[:-3]
    return s + out


def hm(total):
    return '%d h %02d' % (total // 60, total % 60)


def avatar(photo):
    head, tail = photo.rsplit('/', 1)
    return head + '/avatars/' + tail


CHECK = ('<svg width="15" height="15" viewBox="5267.0 2012.42 10.0 7.16" fill="none" aria-hidden="true">'
         '<path d="M5267.75 2016L5270.58 2018.83L5276.25 2013.17" stroke="currentColor" '
         'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def ico(d, w=15):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" aria-hidden="true" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (w, w, d))


I_BOOK  = ico('<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5zM20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5z"/>')
I_PLAY  = ico('<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m10 9.5 4.5 2.5L10 14.5z"/>')
I_CLOCK = ico('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/>')
I_SEAL  = ico('<circle cx="12" cy="9" r="5.5"/><path d="m8.5 13.5-1 7 4.5-2.4 4.5 2.4-1-7"/>')
I_CARD  = ico('<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>', 14)
I_CHEV  = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="m9 6 6 6-6 6" stroke="currentColor" stroke-width="1.6" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')
I_ARROW = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="M7 17 17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.6" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')

CSS = """
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}
  .crumbs{display:flex;align-items:center;gap:9px;padding:26px 0 0;font-size:13px;color:#7a7a7a}
  .crumbs a:hover{color:#1F1F1F}
  .crumbs svg{opacity:.5}

  /* ── hero ─────────────────────────────────────────────────────────────
     Full-bleed band, outside .wrap so it reaches both screen edges without a
     100vw trick that would collide with the scrollbar. Two halves: the title
     left, the offer right — overview, rule, price, add to cart. */
  .hero{position:relative;background:#1F1F1F;color:#FFFFFF;overflow:hidden;margin-top:26px;
    min-height:504px;display:flex;align-items:center}
  .hero>.hero-in{flex:1}
  .hero-img{position:absolute;inset:0;background-size:cover;background-position:center 30%%}
  .hero-scrim{position:absolute;inset:0;
    background:linear-gradient(90deg,rgba(31,31,31,.95) 0%%,rgba(31,31,31,.86) 42%%,rgba(31,31,31,.72) 100%%)}
  .hero-in{position:relative;max-width:1920px;margin:0 auto;padding:60px 52px 64px;
    display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:center}
  .hero h1{margin:0;font-size:clamp(34px,4.4vw,64px);line-height:1.02;letter-spacing:-0.04em;
    font-weight:500;max-width:14ch}
  .hero-offer{min-width:0}
  .hero-offer p{margin:0;font-size:17.5px;line-height:1.62;color:rgba(255,255,255,.8);max-width:52ch}
  .hero-offer hr{border:0;border-top:1px solid rgba(255,255,255,.22);margin:30px 0}
  .hero-buy{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
  .hero-price{font-size:42px;font-weight:500;letter-spacing:-0.035em;line-height:1}
  .hero-price i{font-style:normal;font-size:15px;color:rgba(255,255,255,.6);letter-spacing:0;
    margin-left:9px}
  .hero-cart{display:inline-flex;align-items:center;gap:10px;padding:16px 26px;border-radius:12px;
    background:#FFFFFF;color:#1F1F1F;font-size:15px;font-weight:500;
    transition:box-shadow .45s cubic-bezier(.2,.8,.2,1),transform .45s cubic-bezier(.2,.8,.2,1)}
  .hero-cart:hover{transform:translateY(-2px);
    box-shadow:0 2px 6px rgba(0,0,0,.3),0 8px 20px rgba(0,0,0,.26),0 20px 40px rgba(0,0,0,.2)}

  /* hero: the left half carries the flag, the level and the title; the right
     half the promise, the badge row, then the price and the cart button */
  .hero-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:18px}
  .hero .kicker{color:rgba(255,255,255,.6)}
  .pill{font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
    color:#FFFFFF;background:#0E695C;border-radius:6px;padding:5px 10px}
  .badges{display:flex;flex-wrap:wrap;gap:9px;margin-top:22px}
  .badge{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:#FFFFFF;
    background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:999px;
    padding:7px 13px}
  .badge svg{color:#FFFFFF;opacity:.85;flex:none}

  /* ── sticky section bar ───────────────────────────────────────────────
     Sits directly under the site header (77px tall at desktop, 71 at tablet)
     and carries the homepage menu's indicator, thinner and square: a 2.5px bar
     flush with the strip's bottom edge, scaleY(0) at rest, scaleY(1) on hover
     and on the section you are in, 0.6s on Alal Finance's own --ease-btn. */
  .secnav{position:sticky;top:77px;z-index:40;background:rgba(255,255,255,.92);
    backdrop-filter:blur(14px);border-bottom:1px solid rgba(31,31,31,.09)}
  .secnav-in{max-width:1920px;margin:0 auto;padding:0 52px;display:flex;align-items:stretch;
    gap:30px;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;-ms-overflow-style:none}
  .secnav-in::-webkit-scrollbar{display:none}
  .secnav a{position:relative;display:flex;align-items:center;flex:0 0 auto;white-space:nowrap;
    padding:19px 0;font-size:14.5px;color:#7a7a7a;
    transition:color .35s cubic-bezier(.22,1,.36,1)}
  .secnav a:hover,.secnav a.is-active{color:#1F1F1F}
  .secnav a:before{content:'';position:absolute;left:0;right:0;bottom:0;height:2.5px;
    background:#1F1F1F;transform:scaleY(0);transform-origin:50%% 100%%;
    transition:transform .6s cubic-bezier(.22,1,.36,1)}
  .secnav a:hover:before,.secnav a.is-active:before{transform:scaleY(1)}

  /* ── bands ────────────────────────────────────────────────────────────
     Full-bleed sections alternating white and #EAEAEA, as on the homepage.
     scroll-margin-top clears the header plus the sticky bar when a section
     bar button jumps to one. */
  .band{scroll-margin-top:136px}
  .band-grey{background:%(grey)s}
  .band-in{max-width:1920px;margin:0 auto;padding:96px 52px}
  .band-head{display:flex;align-items:baseline;justify-content:space-between;gap:24px}
  .band h2{margin:24px 0 0;font-size:clamp(28px,3.4vw,46px);line-height:1.08;
    letter-spacing:-0.035em;font-weight:300}
  .band h2 b{font-weight:500;color:#1F1F1F}
  .band .intro{margin:20px 0 0;font-size:17px;line-height:1.62;color:#7a7a7a;max-width:60ch}
  .band .body{margin-top:44px}

  /* the three head figures (PMI's statistics strip, with our own facts) */
  .figs{display:grid;grid-template-columns:repeat(3,1fr);gap:0;
    border-top:1px solid rgba(31,31,31,.12);border-bottom:1px solid rgba(31,31,31,.12)}
  .figs div{padding:30px 34px;border-left:1px solid rgba(31,31,31,.12)}
  .figs div:first-child{border-left:0;padding-left:0}
  .figs b{display:block;font-size:46px;line-height:1;letter-spacing:-0.04em;font-weight:400}
  .figs b i{font-style:normal;font-size:20px;color:#7a7a7a;letter-spacing:0;margin-left:5px}
  /* no measure cap: each description runs the full width of its column */
  .figs span{display:block;margin-top:12px;font-size:14.5px;line-height:1.45;color:#7a7a7a}

  .outcomes{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);
    gap:16px 30px}
  .outcomes li{display:flex;gap:12px;font-size:16px;line-height:1.5}
  .outcomes svg{flex:none;color:#0E695C;margin-top:4px}

  /* who it is for */
  .who{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  /* six benefits over a four-column grid left two orphans hanging on the left
     of the second row; flex-wrap lets that short row centre itself */
  #avantages .who{display:flex;flex-wrap:wrap;justify-content:center}
  #avantages .who>div{flex:0 1 calc(25%% - 12px);min-width:0}
  .who div{background:#FFFFFF;border:1px solid rgba(31,31,31,.09);border-radius:20px;
    padding:32px;transition:border-color .4s ease,box-shadow .5s cubic-bezier(.2,.8,.2,1)}
  .who div:hover{border-color:rgba(31,31,31,.2);box-shadow:0 2px 5px rgba(0,0,0,.05),0 10px 24px rgba(0,0,0,.05)}
  /* .p-svc-icon on the Finance site: a bare 32px glyph in ink, no tile behind
     it, 20px of air before the title */
  .who-icon{display:block;width:32px;height:32px;color:#1F1F1F;margin-bottom:20px}
  .who-icon svg{width:100%%;height:100%%;display:block}
  .who h3{margin:0;font-size:20px;font-weight:700;line-height:1.3;color:#1F1F1F}
  .who p{margin:10px 0 0;font-size:17px;font-weight:400;line-height:1.65;color:#7a7a7a}

  /* the five courses and each one's share of the parcours */
  .crs{list-style:none;margin:0;padding:0;border:1px solid rgba(31,31,31,.1);
    border-radius:18px;overflow:hidden;background:#FFFFFF}
  .crs li{border-top:1px solid rgba(31,31,31,.1)}
  .crs li:first-child{border-top:0}
  .crs a{display:flex;align-items:center;gap:26px;padding:26px 30px;transition:background .3s ease}
  .crs a:hover{background:#FCFBF8}
  .crs .n{font-family:%(mono)s;font-size:13px;color:#A7A7A7;flex:none;width:24px}
  /* twice the size they were, and a true 16:9 box with contain so the artwork
     — which carries its own lettering — is never cropped */
  .crs img{width:192px;height:108px;flex:none;border-radius:12px;object-fit:contain;
    background:#EAEAEA}
  .crs .t{flex:1;min-width:0}
  .crs .t b{display:block;font-size:21px;font-weight:500;line-height:1.3;letter-spacing:-0.018em}
  .crs .t small{display:block;margin-top:8px;font-size:15.5px;line-height:1.5;color:#7a7a7a}
  .crs .w{flex:none;width:150px}
  .crs .w em{display:block;font-style:normal;font-size:12.5px;color:#7a7a7a;margin-bottom:6px}
  .crs .bar{display:block;height:4px;border-radius:999px;background:rgba(31,31,31,.1);overflow:hidden}
  .crs .bar i{display:block;height:100%%;border-radius:999px;background:#0E695C}
  .crs .go{flex:none;color:#7a7a7a}
  .crs a:hover .go{color:#1F1F1F}

  /* Alal_Stats_UnderlineRow — stln001 in the brand guideline app. Flat row, no
     cards or borders; the number keeps the component's light 300 weight and the
     rule under it is a 1px --line-soft track with an ink fill that scales from
     the left. Four columns in the component, three here for six competences. */
  .statsline{display:grid;grid-template-columns:repeat(3,1fr);gap:48px 40px}
  .statsline-bar{display:block;width:100%%;height:1px;background:#CFCFCF;margin-bottom:20px;
    overflow:hidden}
  .statsline-fill{display:block;width:100%%;height:100%%;background:#1F1F1F;transform:scaleX(0);
    transform-origin:left;transition:transform .9s cubic-bezier(.65,0,.35,1)}
  .statsline.in-view .statsline-fill{transform:scaleX(1)}
  .statsline-item h4{margin:0 0 8px;font-size:16px;font-weight:600;letter-spacing:-0.01em}
  .statsline-desc{margin:0;font-size:13.5px;font-weight:400;line-height:1.55;color:#7a7a7a}
  @media (prefers-reduced-motion:reduce){
    .statsline-fill{transition:none;transform:scaleX(1)}
  }

  .sub-h{margin:46px 0 20px;font-size:19px;font-weight:500;letter-spacing:-0.02em}
  .prose{display:grid;grid-template-columns:1fr 1fr;gap:0 64px;align-items:start}
  .prose p{margin:0 0 18px;font-size:16.5px;line-height:1.72;color:#7a7a7a}
  .prose div>p:last-child{margin-bottom:0}

  /* the course rows carry their own price and lead tutor, as the bundle
     section on predika.pro does */
  .crs .t small.by{color:#A7A7A7;font-size:14px;margin-top:8px}
  .crs .w{width:196px;text-align:right}
  .crs .w em{font-style:normal;display:block;font-size:19px;font-weight:500;color:#1F1F1F;
    letter-spacing:-0.02em}
  .crs .w small{display:block;margin-top:7px;font-size:14.5px;color:#7a7a7a}
  /* one card, not two: the à-la-carte value struck on the left, the bundle
     price and the saving on the right, with a hairline between them */
  .crs-sum{display:flex;align-items:center;justify-content:space-between;gap:40px;flex-wrap:wrap;
    margin-top:18px;background:#1F1F1F;border-radius:22px;padding:32px 36px;color:#FFFFFF}
  .crs-sum span{display:block;font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:10px;letter-spacing:.12em;
    text-transform:uppercase;color:rgba(255,255,255,.6)}
  .crs-sum-was{flex:0 1 auto;padding-right:40px;border-right:1px solid rgba(255,255,255,.18)}
  .crs-sum-was b{display:block;margin-top:12px;font-size:28px;font-weight:400;
    letter-spacing:-0.03em;color:rgba(255,255,255,.5);text-decoration:line-through}
  .crs-sum-now{flex:0 1 auto;text-align:right;margin-left:auto}
  .crs-sum-now b{display:block;margin-top:12px;font-size:40px;font-weight:500;
    letter-spacing:-0.04em;line-height:1}
  .crs-sum-now b i{font-style:normal;font-size:16px;color:rgba(255,255,255,.6);
    letter-spacing:0;margin-left:8px}
  .crs-sum-now em{display:block;margin-top:10px;font-style:normal;font-size:13.5px;color:#8FD3C6}

  /* closing band */
  .band-final{background:#1F1F1F;color:#FFFFFF}
  .band-final h2{margin:0;font-size:clamp(28px,3.4vw,46px);line-height:1.08;
    letter-spacing:-0.035em;font-weight:300;color:#FFFFFF;max-width:20ch}
  .band-final .intro{color:rgba(255,255,255,.7);margin-top:20px}
  .band-final .pay-note{color:rgba(255,255,255,.55);margin-top:22px}
  .band-final .pay-note b{color:#FFFFFF}
  .final-buy{display:flex;align-items:center;justify-content:space-between;gap:34px;
    flex-wrap:wrap;margin-top:40px;padding-top:34px;border-top:1px solid rgba(255,255,255,.18)}
  .final-was{display:block;font-size:14px;color:rgba(255,255,255,.5);text-decoration:line-through}
  .final-now{display:block;margin-top:10px;font-size:46px;font-weight:500;letter-spacing:-0.04em;
    line-height:1}
  .final-now i{font-style:normal;font-size:16px;color:rgba(255,255,255,.6);letter-spacing:0;
    margin-left:9px}
  .final-save{display:block;margin-top:12px;font-size:14px;color:#8FD3C6}
  .final-cta{display:inline-flex;align-items:center;gap:10px;flex:none;padding:16px 26px;
    border-radius:12px;background:#FFFFFF;color:#1F1F1F;font-size:15px;font-weight:500;
    transition:box-shadow .45s cubic-bezier(.2,.8,.2,1),transform .45s cubic-bezier(.2,.8,.2,1)}
  .final-cta:hover{transform:translateY(-2px);
    box-shadow:0 2px 6px rgba(0,0,0,.3),0 10px 24px rgba(0,0,0,.26)}

  /* ── price, what is included, payment plans ───────────────────────────
     The price and the inclusions sit on the band itself — no card — so the
     payment plans below are the only cards in this section. */
  .buy-line{margin:0;font-size:18px;line-height:1.6;color:#7a7a7a;max-width:62ch}
  .buy-line b{font-weight:500;color:#1F1F1F}
  .buy-line s{color:#A7A7A7}
  .buy-line em{font-style:normal;font-weight:500;color:#0E695C}
  .gtee{list-style:none;margin:26px 0 0;padding:0;display:grid;
    grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 40px}
  .gtee li{display:flex;gap:11px;font-size:15px;line-height:1.45;color:#7a7a7a}
  .gtee svg{flex:none;color:#0E695C;margin-top:3px}

  /* Payment plans, built like the AAOIFI certification cards on the homepage —
     same 28px radius, 30px padding, green mark square, code, chip, 38px price,
     hairlines and check list — minus their top artwork. The recommended plan
     is the black one. */
  /* Poppins Medium, the brand typeface (guideline §2.2 / §4) — the same face
     and weight the homepage loads for the AAOIFI flip-card headings. */
  .plans-h{margin:54px 0 14px;font-family:'Poppins','General Sans',-apple-system,
    BlinkMacSystemFont,sans-serif;font-size:21px;font-weight:500;letter-spacing:-0.02em;
    text-transform:none;color:#1F1F1F}
  /* no measure cap: the sentence runs the full width of the section */
  .plans-lede{margin:0;font-size:15.5px;line-height:1.6;color:#7a7a7a}
  /* auto-fit rather than a fixed count: the row centres itself on the band
     whatever the number of plans, instead of leaving an empty fourth column */
  .plans{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,340px));gap:18px;
    align-items:stretch;justify-content:center;margin-top:68px}
  .pay-card{position:relative;background:#FFFFFF;border:1px solid rgba(31,31,31,.08);
    border-radius:28px;padding:30px;display:flex;flex-direction:column;gap:20px;
    transition:transform .5s cubic-bezier(.2,.8,.2,1),box-shadow .5s cubic-bezier(.2,.8,.2,1)}
  .pay-card:hover{transform:translateY(-6px);
    box-shadow:0 4px 10px rgba(0,0,0,.05),0 18px 40px rgba(0,0,0,.08)}
  .pay-code{font-size:24px;font-weight:500;letter-spacing:-0.03em;line-height:1.2}
  /* the homepage's "Le plus demandé" flag, straddling the card's top edge */
  .pay-flag{position:absolute;top:-11px;left:30px;font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:9.5px;
    letter-spacing:.12em;text-transform:uppercase;background:#0E695C;color:#FFFFFF;
    padding:5px 10px;border-radius:6px}
  .pay-price{font-size:38px;font-weight:500;letter-spacing:-0.04em;line-height:1}
  .pay-price span{font-size:17px;color:#7a7a7a;letter-spacing:0;margin-left:6px}
  .pay-sub{font-size:13.5px;color:#7a7a7a;margin-top:-10px}
  .pay-sep{display:block;height:1px;background:rgba(31,31,31,.09)}
  .pay-card p{margin:0;font-size:15.5px;line-height:1.45;color:#7a7a7a}
  .pay-list{display:flex;flex-direction:column;gap:11px;min-height:92px}
  .pay-list span{display:flex;gap:11px;font-size:14px;line-height:1.5;color:#7a7a7a}
  .pay-list span>i{color:#0E695C;display:flex;align-items:center;height:21px;flex:none}
  .pay-cta{display:flex;align-items:center;justify-content:center;gap:10px;margin-top:auto;
    padding:14px 20px;border-radius:12px;background:#0E695C;color:#FFFFFF;font-size:14.5px;
    font-weight:500;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .pay-cta:hover{box-shadow:0 2px 6px rgba(14,105,92,.4),0 10px 24px rgba(14,105,92,.3)}
  /* the recommended plan, inverted */
  .pay-card.is-reco{background:#1F1F1F;border-color:#1F1F1F;color:#FFFFFF}
  .is-reco .pay-price span,.is-reco .pay-sub,.is-reco p,.is-reco .pay-list span{color:rgba(255,255,255,.66)}
  .is-reco .pay-sep{background:rgba(255,255,255,.16)}
  .is-reco .pay-list span>i{color:#FFFFFF}
  .is-reco .pay-cta{background:#FFFFFF;color:#1F1F1F}
  .is-reco .pay-cta:hover{box-shadow:0 2px 6px rgba(0,0,0,.34),0 10px 24px rgba(0,0,0,.28)}

  /* How people actually pay, as on predika.pro: the methods as pills under the
     plans, then the one-line reassurance. */
  .pay-ways{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:9px;
    margin-top:30px}
  .pay-ways>span:first-child{font-size:13px;color:#A7A7A7;margin-right:4px}
  .pay-way{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:500;
    color:#1F1F1F;background:#FFFFFF;border:1px solid rgba(31,31,31,.12);border-radius:999px;
    padding:8px 14px}
  .pay-way svg{color:#0E695C;flex:none}
  .pay-note{margin:16px 0 0;text-align:center;font-size:13.5px;color:#7a7a7a}
  .pay-note b{font-weight:500;color:#1F1F1F}

  .facts-box{background:#FFFFFF;border:1px solid rgba(31,31,31,.1);border-radius:24px;
    padding:28px 30px}
  .facts-box h3{margin:0 0 16px;font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:10px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a;font-weight:400}
  .facts{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
  .facts li{display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:14.5px}
  .facts li span{color:#7a7a7a}

  /* eligibility */
  .req{list-style:none;margin:0;padding:0;border-top:1px solid rgba(31,31,31,.12);
    columns:2;column-gap:52px}
  .req li{display:flex;align-items:baseline;gap:20px;padding:16px 0;
    border-bottom:1px solid rgba(31,31,31,.12);font-size:16px;break-inside:avoid}
  .req li b{flex:none;width:148px;font-weight:400;color:#7a7a7a}

  /* the five steps */
  .steps{list-style:none;margin:0;padding:0;counter-reset:s;
    display:grid;grid-template-columns:repeat(5,1fr);gap:0}
  .steps li{counter-increment:s;padding:0 26px;border-left:1px solid rgba(31,31,31,.12)}
  .steps li:first-child{border-left:0;padding-left:0}
  .steps li:before{content:counter(s);display:flex;width:38px;height:38px;border-radius:50%%;
    background:#1F1F1F;color:#FFFFFF;font-size:14.5px;align-items:center;justify-content:center;
    margin-bottom:18px}
  .steps h3{margin:0;font-size:16.5px;font-weight:500;letter-spacing:-0.018em;line-height:1.3}
  .steps p{margin:10px 0 0;font-size:14.5px;line-height:1.6;color:#7a7a7a}

  /* what comes next */
  .next{margin-top:52px;border-radius:24px;background:#1F1F1F;color:#FFFFFF;padding:40px 42px;
    display:flex;align-items:center;justify-content:space-between;gap:34px;flex-wrap:wrap}
  .next h3{margin:0;font-size:25px;font-weight:500;letter-spacing:-0.03em}
  .next p{margin:14px 0 0;font-size:16px;line-height:1.6;color:rgba(255,255,255,.72);max-width:62ch}
  .next a{display:inline-flex;align-items:center;gap:9px;flex:none;padding:14px 22px;
    border-radius:12px;background:#FFFFFF;color:#1F1F1F;font-size:14.5px;font-weight:500;
    transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .next a:hover{box-shadow:0 2px 6px rgba(0,0,0,.3),0 10px 24px rgba(0,0,0,.24)}

  /* tutors */
  .tuts{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
  .tut{display:flex;gap:22px;background:#FFFFFF;border:1px solid rgba(31,31,31,.09);
    border-radius:22px;padding:26px 28px}
  .tut-photo{width:104px;height:104px;flex:none;border-radius:16px;object-fit:cover;
    object-position:center top;background:#EAEAEA}
  .tut h3{margin:0;font-size:19px;font-weight:500;letter-spacing:-0.02em}
  .tut .cred{margin:7px 0 0;font-family:%(mono)s;font-size:10.5px;letter-spacing:.07em;
    text-transform:uppercase;line-height:1.6;color:#7a7a7a}
  .tut p.bio{margin:12px 0 0;font-size:14.5px;line-height:1.6;color:#7a7a7a}
  .tut .li{display:inline-flex;align-items:center;gap:7px;margin-top:13px;font-size:13px;
    font-weight:500}
  .tut .li:hover{color:#0E695C}

  /* FAQ */
  /* two columns: the questions split in half rather than running down the
     left with the right side empty */
  .faq{display:grid;grid-template-columns:1fr 1fr;gap:0 64px;align-items:start}
  .faq-col{border-top:1px solid rgba(31,31,31,.12)}
  .faq details{border-bottom:1px solid rgba(31,31,31,.12)}
  .faq summary{list-style:none;cursor:pointer;display:flex;align-items:center;
    justify-content:space-between;gap:20px;padding:22px 0;font-size:17.5px;font-weight:500;
    letter-spacing:-0.015em}
  .faq summary::-webkit-details-marker{display:none}
  .faq summary span{flex:none;width:26px;height:26px;border-radius:50%%;
    border:1px solid rgba(31,31,31,.18);display:flex;align-items:center;justify-content:center;
    transition:transform .4s cubic-bezier(.2,.8,.2,1),background .3s ease,color .3s ease}
  .faq details[open] summary span{transform:rotate(45deg);background:#1F1F1F;color:#FFFFFF;
    border-color:#1F1F1F}
  .faq p{margin:0;padding:0 46px 24px 0;font-size:15.5px;line-height:1.65;color:#7a7a7a}

  /* ── list page ───────────────────────────────────────────────────────── */
  .plist-head{padding:120px 0 0}
  .plist-title{margin:0;font-size:clamp(46px,7vw,98px);line-height:1.04;letter-spacing:-0.04em;
    font-weight:300;max-width:14ch}
  .plist-lede{margin:30px 0 0;font-size:18px;line-height:1.6;color:#7a7a7a;max-width:60ch}
  /* With one parcours in the catalogue, a grid of cards would be a card and a
     hole. The parcours is shown as a split feature block instead — image left,
     the whole offer right — and the ones in preparation as a strip beneath. */
  .feat{display:grid;grid-template-columns:1fr 1fr;gap:54px;align-items:center;padding:64px 0 0}
  .feat-img{position:relative;display:block;aspect-ratio:4/3;border-radius:22px;overflow:hidden;
    background:#EAEAEA;background-size:cover;background-position:center 32%%}
  .feat-img b{position:absolute;top:16px;left:16px;font-family:%(mono)s;font-size:10px;
    letter-spacing:.1em;text-transform:uppercase;color:#1F1F1F;background:rgba(252,251,248,.92);
    padding:6px 11px;border-radius:999px;font-weight:400}
  .feat-body{min-width:0}
  .feat-body h2{margin:14px 0 0;font-size:clamp(30px,3.3vw,46px);line-height:1.06;
    letter-spacing:-0.04em;font-weight:500}
  .feat-body p{margin:18px 0 0;font-size:16.5px;line-height:1.6;color:#7a7a7a;max-width:46ch}
  .feat-meta{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0 0;font-size:14px;color:#7a7a7a}
  .feat-meta span{display:inline-flex;align-items:center;gap:8px}
  /* a hairline under the description and another under the course list */
  .feat-rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:26px 0 0}
  .feat-courses{list-style:none;margin:22px 0 0;padding:0;display:flex;flex-direction:column;gap:9px}
  .feat-courses li{display:flex;gap:11px;font-size:14.5px;line-height:1.45;color:#1F1F1F}
  .feat-courses svg{flex:none;color:#0E695C;margin-top:3px}
  .feat-foot{display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin:26px 0 0}
  .feat-cta{display:inline-flex;align-items:center;gap:10px;padding:15px 24px;border-radius:12px;
    background:#1F1F1F;color:#FFFFFF;font-size:15px;font-weight:500;
    transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .feat-cta:hover{box-shadow:0 2px 6px rgba(0,0,0,.32),0 7px 16px rgba(0,0,0,.28),
    0 17px 33px rgba(0,0,0,.24)}
  .plist-why{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:92px 0 0;
    border-top:1px solid rgba(31,31,31,.09)}
  .plist-why div{padding:30px 34px;border-left:1px solid rgba(31,31,31,.09)}
  .plist-why div:first-child{border-left:0;padding-left:0}
  .plist-why h3{margin:0;font-size:17px;font-weight:500;letter-spacing:-0.02em}
  .plist-why p{margin:10px 0 0;font-size:14.5px;line-height:1.6;color:#7a7a7a}
  .plist-tail{padding:0 0 96px}


  /* ── tablet ──────────────────────────────────────────────────────────── */
  @media (min-width:744px) and (max-width:1240px){
    .hero{min-height:432px}
    .hero-in{padding:48px 28px 52px;gap:34px}
    .hero h1{font-size:clamp(28px,3.8vw,40px)}
    .hero-offer p{font-size:15px}
    .hero-offer hr{margin:22px 0}
    .hero-price{font-size:31px}
    .hero-cart{padding:13px 20px;font-size:14px}
    .secnav{top:71px}
    .secnav-in{padding:0 28px;gap:18px}
    .secnav a{font-size:13px;padding:15px 0}
    .band{scroll-margin-top:124px}
    .band-in{padding:64px 28px}
    .band h2{font-size:30px;margin-top:18px}
    .band .intro{font-size:15px;margin-top:16px}
    .band .body{margin-top:32px}
    .badge{font-size:12px;padding:6px 11px}
    .sub-h{font-size:17px;margin-top:34px}
    .prose{gap:0 34px}
    .prose p{font-size:15px;margin-bottom:15px}
    .crs .w{width:150px}
    .crs .w em{font-size:16px}
    .crs .w small{font-size:13px}
    .crs-sum{padding:24px 26px;gap:26px;border-radius:18px}
    .crs-sum-was{padding-right:26px}
    .crs-sum-was b{font-size:22px}
    .crs-sum-now b{font-size:30px}
    .final-now{font-size:33px}
    .figs div{padding:22px 20px}
    .figs b{font-size:33px}
    .figs span{font-size:13px;margin-top:9px}
    .outcomes{grid-template-columns:repeat(2,1fr);gap:13px 24px}
    .statsline{gap:36px 28px}
    .statsline-bar{margin-bottom:15px}
    .statsline-item h4{font-size:15px}
    .statsline-desc{font-size:13px}
    .outcomes li,.req li{font-size:14px}
    .who{grid-template-columns:repeat(2,1fr);gap:13px}
    #avantages .who{gap:13px}
    #avantages .who>div{flex:0 1 calc(50%% - 7px)}
    .who div{padding:24px}
    .who-icon{width:28px;height:28px;margin-bottom:16px}
    .who h3{font-size:17px}
    .who p{font-size:15px}
    .steps p,.tut p.bio{font-size:13.5px}
    .crs a{padding:18px 18px;gap:18px}
    .crs img{width:144px;height:81px}
    .crs .t b{font-size:17px}
    .crs .t small{font-size:13.5px}
    .crs .w{width:104px}
    .buy-line{font-size:15.5px}
    .gtee{gap:10px 26px}
    .gtee li{font-size:13.5px}
    /* three across still fits a tablet column and avoids an orphan on row 2 */
    .plans{grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;justify-content:stretch;
      margin-top:52px}
    .pay-card{padding:20px;border-radius:22px;gap:16px}
    .pay-flag{left:20px}
    .pay-code{font-size:17px}
    .pay-price{font-size:28px}
    .pay-price span{font-size:14px}
    .pay-card p{font-size:14px}
    .pay-list span{font-size:13px}
    .pay-list{min-height:80px}
    .pay-cta{padding:12px 14px;font-size:13.5px}
    .plans-h{margin-top:38px}
    .facts li{font-size:13px}
    .req{column-gap:34px}
    .req li b{width:112px}
    /* five steps across a tablet column would be 130px wide — two rows instead */
    .steps{grid-template-columns:repeat(3,1fr);gap:26px 0}
    .steps li{padding:0 18px}
    .steps li:nth-child(3n+1){border-left:0;padding-left:0}
    .steps h3{font-size:15px}
    .next{padding:26px 28px;margin-top:38px}
    .next h3{font-size:21px}
    .next p{font-size:14.5px}
    .tuts{grid-template-columns:1fr;gap:12px}
    .tut{padding:20px 22px;gap:18px}
    .faq{gap:0 34px}
    .faq summary{font-size:15.5px}
    .faq p{font-size:14px}
    .plist-title{font-size:clamp(34px,5.4vw,56px)}
    .plist-lede{font-size:15.5px;margin-top:22px}
    .feat{gap:30px;padding-top:44px}
    .feat-body h2{font-size:28px}
    .feat-body p{font-size:14.5px;margin-top:14px}
    .feat-meta,.feat-courses li{font-size:13px}
    .feat-rule{margin-top:20px}
    .feat-courses{margin-top:18px}
    .plist-why div{padding:22px 20px}
  }

  /* ── phone ───────────────────────────────────────────────────────────── */
  @media (max-width:743px){
    .hero{margin-top:18px;min-height:540px}
    .hero-in{grid-template-columns:1fr;gap:26px;padding:44px 24px 48px}
    .hero h1{font-size:34px;max-width:none}
    .hero-offer p{font-size:15.5px}
    .hero-offer hr{margin:22px 0}
    .hero-price{font-size:32px}
    .hero-buy{gap:16px}
    .hero-cart{flex:1 1 100%%;justify-content:center}
    /* the bar keeps one line and is swiped, bleeding into the gutters so a
       cut-off button reads as scrollable */
    .secnav{top:77px}
    .secnav-in{padding:0 24px;gap:20px}
    .secnav a{font-size:14px;padding:14px 0}
    .band{scroll-margin-top:126px}
    .band-in{padding:52px 24px}
    .band h2{font-size:28px;margin-top:16px}
    .band .intro{font-size:15.5px;margin-top:16px}
    .band .body{margin-top:28px}
    .hero-top{margin-bottom:14px}
    .badges{gap:8px;margin-top:18px}
    .badge{font-size:12.5px;padding:6px 11px}
    .sub-h{font-size:17px;margin-top:32px}
    /* one column at phone width; the two halves run on as one text */
    .prose{grid-template-columns:1fr}
    .prose div:first-child>p:last-child{margin-bottom:18px}
    .prose p{font-size:15.5px}
    /* the price and lesson count drop under the title, as the share bar did */
    .crs .w{flex:1 0 100%%;width:auto;margin-top:12px;text-align:left}
    .crs .w em{font-size:17px}
    /* stacked, the rule moves from the side to between the two halves */
    .crs-sum{flex-direction:column;align-items:flex-start;gap:20px;padding:24px;border-radius:18px}
    .crs-sum-was{padding:0 0 20px;border-right:0;border-bottom:1px solid rgba(255,255,255,.18);
      width:100%%}
    .crs-sum-was b{font-size:24px}
    .crs-sum-now{text-align:left;margin-left:0}
    .crs-sum-now b{font-size:32px}
    .final-buy{gap:22px;margin-top:30px;padding-top:26px}
    .final-now{font-size:34px}
    .final-cta{flex:1 1 100%%;justify-content:center}
    .figs{grid-template-columns:1fr}
    .figs div{padding:20px 0;border-left:0;border-top:1px solid rgba(31,31,31,.12)}
    .figs div:first-child{border-top:0}
    .figs b{font-size:36px}
    .outcomes,.who,.tuts{grid-template-columns:1fr}
    #avantages .who>div{flex:1 1 100%%}
    /* the component drops to two columns under 1100px; one is right at 390 */
    .statsline{grid-template-columns:1fr;gap:28px}
    .who div{padding:26px 24px}
    .who h3{font-size:19px}
    .who p{font-size:16px}
    /* a course row cannot carry thumbnail, title and weighting on a 390px line:
       the share bar drops to its own full-width line under the title */
    .crs li{position:relative}
    .crs a{flex-wrap:wrap;gap:0 16px;padding:20px}
    .crs .n{padding-top:2px}
    .crs img{width:124px;height:70px}
    .crs .t{flex:1 1 0;min-width:0}
    .crs .t b{font-size:17px}
    .crs .w{flex:1 0 100%%;width:auto;margin-top:12px}
    .crs .go{position:absolute;right:16px;top:20px}
    .buy-line{font-size:16px}
    .gtee{grid-template-columns:1fr;gap:11px}
    .plans{grid-template-columns:minmax(0,1fr);gap:20px;margin-top:44px}
    .pay-ways{justify-content:flex-start;gap:8px;margin-top:24px}
    .pay-way{font-size:12.5px;padding:7px 12px}
    .pay-note{text-align:left;font-size:13px}
    .pay-card{padding:24px;border-radius:24px}
    .pay-flag{left:24px}
    .pay-list{min-height:0}
    .plans-h{margin-top:40px}
    .req{columns:1}
    .req li{flex-direction:column;gap:5px}
    .req li b{width:auto}
    .steps{grid-template-columns:1fr;gap:0}
    .steps li{padding:22px 0 0;border-left:0}
    .steps li:before{margin-bottom:14px}
    .next{flex-direction:column;align-items:flex-start;padding:26px 24px;border-radius:20px;margin-top:34px}
    .tut{flex-direction:column;gap:16px;padding:22px}
    .tut-photo{width:84px;height:84px}
    /* one column on a phone; the second half simply follows the first */
    .faq{grid-template-columns:1fr}
    .faq-col+.faq-col{border-top:0}
    .faq summary{font-size:16px;gap:14px}
    .faq p{padding-right:0}
    .plist-head{padding-top:64px}
    .plist-lede{font-size:16px}
    .feat{grid-template-columns:1fr;gap:26px;padding-top:38px}
    .feat-img{aspect-ratio:16/10}
    .feat-body h2{font-size:30px}
    .feat-body p{font-size:15.5px}
    .feat-foot{gap:16px}
    .plist-why{grid-template-columns:1fr;margin-top:56px}
    .plist-why div{padding:22px 0;border-left:0;border-top:1px solid rgba(31,31,31,.09)}
    .plist-why div:first-child{border-top:0}
    .plist-tail{padding-bottom:64px}
  }
""" % dict(mono=MONO, grey=GREY) + """

/* ── Formateurs carousel ──────────────────────────────────
   The homepage's own component (#instructors / .aa-form-*), ported as it is:
   a horizontal scroller of 420px portrait cards whose panel opens its bio and
   LinkedIn button on hover (tap on touch), plus the scroll-progress bar.
   It sits outside the %-formatted block above, so its percentages need no
   escaping. */
  .aa-form-wrap { margin-top:44px; overflow-x:auto; scroll-behavior:smooth; -ms-overflow-style:none; scrollbar-width:none; }
  .aa-form-wrap::-webkit-scrollbar { display:none; }
  .aa-form-track { display:flex; gap:22px; }
  .aa-form-card { position:relative; flex:0 0 420px; width:420px; aspect-ratio:300/460; border-radius:22px; overflow:hidden; background:#1F1F1F; cursor:pointer; }
  .aa-form-photo { position:absolute; inset:0; background-size:cover; background-position:center top; background-repeat:no-repeat;
    transition:transform .6s cubic-bezier(.2,.8,.2,1); }
  .aa-form-card:hover .aa-form-photo { transform:scale(1.04); }
  .aa-form-panel { position:absolute; left:0; right:0; bottom:0; padding:22px 24px; color:#FFFFFF;
    background-color:rgba(31,31,31,0.94); }
  .aa-form-panel h4 { margin:0 0 3px; font-size:21px; font-weight:500; line-height:1.3; letter-spacing:-0.02em; }
  .aa-form-panel p  { margin:0; font-size:12px; color:rgba(255,255,255,0.62); }
  .aa-form-more { display:grid; grid-template-rows:0fr; transition:grid-template-rows .45s cubic-bezier(.65,0,.35,1); }
  .aa-form-more-inner { overflow:hidden; min-height:0; }
  .aa-form-bio { margin:16px 0 0; font-size:14px; line-height:1.55; color:rgba(255,255,255,0.8); opacity:0; transition:opacity .3s ease; }
  /* LinkedIn button — Alal Finance .btn.invert.sm, as on the homepage */
  .aa-form-li { position:relative; overflow:hidden; display:inline-flex; align-items:center; gap:6px;
    margin-top:14px; padding:8px 14px; border-radius:4.5px; border:0.4px solid #FFFFFF;
    background:#FFFFFF; color:#1F1F1F; font-size:12.5px; font-weight:400;
    opacity:0; transform:translateY(6px); transition:opacity .3s ease, transform .3s ease; }
  .aa-form-li .btn-fill { position:absolute; inset:-1%; width:102%; height:102%; background:#3f3f3d;
    transform:translateY(104%); transition:transform .5s cubic-bezier(.22,1,.36,1); pointer-events:none; }
  .aa-form-li:hover .btn-fill { transform:translateY(0); }
  .aa-form-li .btn-text-wrap { position:relative; display:inline-block; overflow:hidden; transition:color .4s ease; }
  .aa-form-li .btn-text, .aa-form-li .btn-text-hover { display:block; transition:opacity .5s cubic-bezier(.22,1,.36,1), transform .5s cubic-bezier(.22,1,.36,1); }
  .aa-form-li .btn-text-hover { position:absolute; top:0; left:0; opacity:0; transform:scale(.9) translateY(100%); }
  .aa-form-li:hover .btn-text { opacity:0; transform:scale(.9) translateY(-100%); }
  .aa-form-li:hover .btn-text-hover { opacity:1; transform:scale(1) translateY(0); }
  .aa-form-li .icon-arrow { width:13px; height:13px; flex:none; position:relative; z-index:1; display:inline-flex; color:currentColor; }
  .aa-form-li .icon-arrow svg { width:100%; height:100%; display:block; }
  .aa-form-li:hover .btn-text-wrap, .aa-form-li:hover .icon-arrow { color:#FFFFFF; }
  @media (hover:hover) {
    .aa-form-card:hover .aa-form-more { grid-template-rows:1fr; }
    .aa-form-card:hover .aa-form-bio { opacity:1; transition-delay:.15s; }
    .aa-form-card:hover .aa-form-li  { opacity:1; transform:translateY(0); transition-delay:.2s; }
  }
  .aa-form-card:focus-within .aa-form-more, .aa-form-card.is-open .aa-form-more { grid-template-rows:1fr; }
  .aa-form-card:focus-within .aa-form-bio, .aa-form-card.is-open .aa-form-bio { opacity:1; transition-delay:.15s; }
  .aa-form-card:focus-within .aa-form-li,  .aa-form-card.is-open .aa-form-li  { opacity:1; transform:translateY(0); transition-delay:.2s; }
  .aa-form-progress { margin:32px auto 0; max-width:280px; height:2px; border-radius:2px; background:rgba(31,31,31,0.12); overflow:hidden; position:relative; }
  .aa-form-progress-fill { position:absolute; left:0; top:0; height:100%; background:#1F1F1F; border-radius:2px; transition:transform .25s ease, width .25s ease; }
  @media (min-width:744px) and (max-width:1240px){ .aa-form-card { flex:0 0 360px; width:360px; } }
  @media (max-width:743px){ .aa-form-card { flex:0 0 336px; width:336px; } }
"""


# ───────────────────────────── derived figures ─────────────────────────────
def facts(P):
    """Course-level figures, computed from courses.py.

    The money is NOT computed: the price, the à-la-carte total and the discount
    are printed as predika.pro prints them (see parcours_data.py for the two
    places where its own figures disagree).
    """
    rows = []
    for slug in P['courses']:
        c = BY_SLUG[slug]
        d = sum(mins(m[2]) for m in c['modules']) if c['modules'] else 0
        rows.append((c, d))
    tutors = []
    for c, _ in rows:
        for t in c['tutors']:
            if t not in tutors:
                tutors.append(t)
    return dict(rows=rows, n=len(rows),
                total_min=sum(d for _, d in rows),
                lessons=sum(c['lessons'] or 0 for c, _ in rows),
                retail=P['retail'], price=P['price'],
                save=P['retail'] - P['price'], pct=P['discount'], tutors=tutors)


# the one-line role under each name, as the homepage's formateurs cards print it
ROLES = {
    'Abdoulaye WANE': 'Auditeur Charia — Banque Islamique du Sénégal',
    'Moustapha ABAKAR MOUSSA': 'Reporting, audit & normes comptables',
    'Mohamed Saïd DAOUDA': 'Chargé de conformité islamique — CBI Bénin',
    'Yaya SOW': 'Fiqh al-Muamalat & gouvernance Charia',
    'Modou SALL': 'Islamic Banking & Capital Markets',
    'Bashir Diaby': 'Co-fondateur & CEO, Groupe ALAL',
}

# the sticky bar's buttons, in page order
SECTIONS = [
    ('apercu',       'Aperçu'),
    ('presentation', 'Présentation'),
    ('public',       'Pour qui'),
    ('programme',    'Programme'),
    ('tarif',        'Tarif'),
    ('avantages',    'Avantages'),
    ('conditions',   'Conditions'),
    ('formateurs',   'Formateurs'),
    ('faq',          'FAQ'),
]


def band(sid, kicker, num, title, intro, inner, grey=False, extra=''):
    return """  <section class="band%(g)s" id="%(id)s">
    <div class="band-in">
      <div class="band-head">
        <span class="kicker">%(k)s</span>
        <span class="kicker">(%(n)02d)</span>
      </div>
      <h2>%(t)s</h2>
%(intro)s
      <div class="body">
%(inner)s
      </div>%(extra)s
    </div>
  </section>""" % dict(g=' band-grey' if grey else '', id=sid, k=kicker, n=num, t=title,
                       intro=('      <p class="intro">%s</p>' % intro) if intro else '',
                       inner=inner, extra=extra)


# ───────────────────────────── detail page ─────────────────────────────────
def build_one(P):
    F = facts(P)
    tutors = [dict(TUTORS[n], name=n) for n in F['tutors']]
    cur = P['currency']

    secnav = "\n".join('      <a href="#%s">%s</a>' % (sid, esc(lab)) for sid, lab in SECTIONS)

    badges = "\n".join('          <span class="badge">%s%s</span>' % (CHECK, esc(b))
                       for b in P['badges'])

    figs = """        <div class="figs">
          <div><b>%d<i>cours</i></b><span>Les %d cours du métier, achetés ensemble plutôt qu'un par un.</span></div>
          <div><b>%d<i>heures</i></b><span>%d leçons enregistrées, accessibles à vie.</span></div>
          <div><b>&minus;%d<i>%%</i></b><span>Soit %s %s de moins que les %d cours achetés séparément.</span></div>
        </div>""" % (F['n'], F['n'], F['total_min'] // 60, F['lessons'], F['pct'],
                     fr(F['save']), cur, F['n'])

    # Alal_Stats_UnderlineRow (stln001) from the brand guideline app: a flat row,
    # no cards and no borders — a large light-weight number, a thin rule that
    # draws itself left to right, a bold title and a muted description. Four
    # columns there, three here because the parcours has six competences.
    outcomes = ('        <h3 class="sub-h">Compétences acquises à la fin du parcours</h3>\n'
                '        <div class="statsline" id="pStatsline">\n%s\n        </div>'
                % "\n".join(
                    '          <div class="statsline-item">\n'
                    '            <span class="statsline-bar"><i class="statsline-fill"></i></span>\n'
                    '            <h4>%s</h4>\n'
                    '            <p class="statsline-desc">%s</p>\n'
                    '          </div>' % (esc(t), esc(d))
                    for t, d in P['outcomes']))

    # The presentation runs in two columns rather than one long measure down the
    # left: the first paragraphs on the left, the last two on the right, which
    # is the half that was sitting empty.
    _pp = ['          <p>%s</p>' % esc(p) for p in P['presentation']]
    presentation = ('        <div class="prose">\n'
                    '          <div>\n%s\n          </div>\n'
                    '          <div>\n%s\n          </div>\n'
                    '        </div>' % ("\n".join(_pp[:-2]), "\n".join(_pp[-2:])))

    crs = []
    for c, d in F['rows']:
        lead = c['tutors'][0] if c['tutors'] else ''
        crs.append(
            '          <li><a href="cours/%s.html">\n'
            '            <span class="n">%02d</span>\n'
            '            <img src="%s" alt="" width="192" height="108">\n'
            '            <span class="t"><b>%s</b><small>%s</small>'
            '<small class="by">%s</small></span>\n'
            '            <span class="w"><em>%s %s</em><small>%s</small></span>\n'
            '            <span class="go">%s</span>\n'
            '          </a></li>'
            % (c['slug'], len(crs) + 1, c['image'], esc(c['title']), esc(c['subtitle']),
               esc(lead), fr(int(str(c['price']).replace(' ', '').replace('\u202f', ''))),
               cur,
               ('%d leçons &middot; %s' % (c['lessons'], hm(d))) if c['lessons']
               else 'Programme à paraître',
               I_ARROW))
    # the two summary cards are one: the à-la-carte value and the bundle price
    # read as a single before/after rather than two boxes to compare
    crs = ('        <ol class="crs">\n%s\n        </ol>\n'
           '        <div class="crs-sum">\n'
           '          <div class="crs-sum-was">\n'
           '            <span>Valeur totale si achetés à la carte</span>\n'
           '            <b>%s %s</b>\n'
           '          </div>\n'
           '          <div class="crs-sum-now">\n'
           '            <span>Prix bundle &middot; tout inclus</span>\n'
           '            <b>%s<i>%s</i></b>\n'
           '            <em>%s %s économisés — %d %% de réduction</em>\n'
           '          </div>\n'
           '        </div>' % ("\n".join(crs), fr(F['retail']), cur, fr(F['price']), cur,
                              fr(F['save']), cur, F['pct']))

    plans = []
    for pl in P['plans']:
        reco = pl['n'] == P['recommended']
        plans.append(
            '          <div class="pay-card%(reco)s">\n'
            '%(flag)s'
            '            <span class="pay-code">%(title)s</span>\n'
            '            <div class="pay-price">%(per)s<span>%(cur)s%(each)s</span></div>\n'
            '            <span class="pay-sub">%(sub)s</span>\n'
            '            <span class="pay-sep"></span>\n'
            '            <p>%(line)s</p>\n'
            '            <span class="pay-sep"></span>\n'
            '            <div class="pay-list">%(items)s</div>\n'
            '            <span class="pay-sep"></span>\n'
            '            <a href="panier.html" class="pay-cta" data-add="parcours:%(slug)s" '
            'data-plan="%(n)d">%(cta)s %(arrow)s</a>\n'
            '          </div>'
            % dict(reco=' is-reco' if reco else '',
                   flag=('            <span class="pay-flag">Recommandé</span>\n'
                         if reco else ''),
                   title=esc(pl['title']), per=fr(pl['per']), cur=cur,
                   each='' if pl['n'] == 1 else ' &times; %d' % pl['n'],
                   sub=('Total %s %s' % (fr(pl['total']), cur)) if pl['n'] == 1 else
                       ('Total : %s %s' % (fr(pl['total']), cur)),
                   line=esc(pl['line']),
                   items="".join('<span><i>%s</i>%s</span>' % (CHECK, esc(it))
                                 for it in pl['items']),
                   cta=esc(pl['cta']), arrow=I_ARROW, slug=P['slug'], n=pl['n']))

    buy = """        <p class="buy-line">Le bundle est à <b>%(price)s %(cur)s</b>, contre
          <s>%(retail)s %(cur)s</s> si les %(n)d cours sont achetés séparément —
          <em>%(save)s %(cur)s d'économie, %(pct)d %% de réduction</em>.</p>
        <h3 class="plans-h">Choisissez comment vous payez</h3>
        <p class="plans-lede">%(lede)s</p>
        <div class="plans">
%(plans)s
        </div>
        <div class="pay-ways">
          <span>Paiement via</span>
%(ways)s
        </div>
        <p class="pay-note">%(note)s</p>""" % dict(
        price=fr(F['price']), cur=cur, retail=fr(F['retail']), n=F['n'],
        save=fr(F['save']), pct=F['pct'], lede=esc(P['plans_lede']),
        plans="\n".join(plans), note=P['pay_note'],
        ways="\n".join('          <span class="pay-way">%s%s</span>' % (I_CARD, w)
                        for w in P['pay_ways']))

    benefits = '        <div class="who">\n%s\n        </div>' % "\n".join(
        '          <div><h3>%s</h3><p>%s</p></div>' % (esc(h), esc(b)) for h, b in P['benefits'])

    # the audience cards follow .p-svc-card on the Alal Finance site's
    # "Fenêtre & Banque Islamique" page: a 32px ink glyph above the title,
    # a 20px/700 title and a 17px/1.65 description
    who = '        <div class="who">\n%s\n        </div>' % "\n".join(
        '          <div><span class="who-icon">%s</span><h3>%s</h3><p>%s</p></div>'
        % (AUDIENCE_ICONS[i % len(AUDIENCE_ICONS)], esc(h), esc(b))
        for i, (h, b) in enumerate(P['audience']))

    req = '        <ul class="req">\n%s\n        </ul>' % "\n".join(
        '          <li><b>%s</b><span>%s</span></li>' % (esc(k), esc(v)) for k, v in P['prereqs'])

    # half the questions on each side, so the right half of the band is used
    _plus = ('<svg width="11" height="11" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
             '<path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round"/></svg>')
    _q = ['          <details><summary>%s<span>%s</span></summary><p>%s</p></details>'
          % (esc(q), _plus, esc(a)) for q, a in P['faq']]
    _half = (len(_q) + 1) // 2
    faq = ('        <div class="faq">\n'
           '          <div class="faq-col">\n%s\n          </div>\n'
           '          <div class="faq-col">\n%s\n          </div>\n'
           '        </div>' % ("\n".join(_q[:_half]), "\n".join(_q[_half:])))

    # the homepage's formateurs carousel, same markup and classes
    LI_ARROW = ('<span class="icon-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none">'
                '<path d="M7 17L17 7M17 7H9M17 7V15" stroke="currentColor" stroke-width="1.5" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')
    _cards = "\n".join(
        '            <div class="aa-form-card">\n'
        '              <div class="aa-form-photo" role="img" aria-label="Portrait — %(n)s" '
        'style="background-image:url(\'%(photo)s\');"></div>\n'
        '              <div class="aa-form-panel"><h4>%(n)s</h4><p>%(role)s</p>'
        '<div class="aa-form-more"><div class="aa-form-more-inner">'
        '<p class="aa-form-bio">%(bio)s</p>'
        '<a class="aa-form-li" href="%(li)s" target="_blank" rel="noopener" aria-label="LinkedIn">'
        '<span class="btn-fill" aria-hidden="true"></span>'
        '<span class="btn-text-wrap"><span class="btn-text">LinkedIn</span>'
        '<span class="btn-text-hover" aria-hidden="true">LinkedIn</span></span>%(arrow)s</a>'
        '</div></div></div>\n'
        '            </div>'
        % dict(n=esc(t['name']), photo=t['photo'], li=t['linkedin'], arrow=LI_ARROW,
               role=esc(ROLES.get(t['name'], t['credentials'].split(',')[0])),
               bio=esc(t['bio']))
        for t in tutors)

    tuts = ('        <div class="aa-form-wrap" id="aaFormWrap">\n'
            '          <div class="aa-form-track">\n' + _cards + '\n          </div>\n'
            '        </div>\n'
            '        <div class="aa-form-progress">'
            '<span class="aa-form-progress-fill" id="aaFormFill"></span></div>')

    bands = "\n\n".join([
        band('apercu', 'Ce que vous maîtriserez', 1,
             'Un métier entier, <b>pas juste un cours</b>', P['outcomes_lede'],
             figs + '\n' + outcomes),
        band('presentation', 'Présentation', 2,
             'Pourquoi <b>ce parcours</b>', None, presentation, grey=True),
        band('public', "À qui il s'adresse", 3,
             'Pour <b>qui</b>', None, who),
        band('programme', 'Contenu du bundle', 4,
             '%d cours complets, <b>un seul accès</b>' % F['n'],
             'Achetés à la carte, ces %d cours vous coûteraient %s %s. En bundle, vous '
             'accédez à tout pour %s %s — soit %s %s d\'économie.'
             % (F['n'], fr(F['retail']), cur, fr(F['price']), cur, fr(F['save']), cur),
             crs, grey=True),
        band('tarif', 'Flexible & sans frais caché', 5,
             'Le prix, <b>et comment le régler</b>', None, buy),
        band('avantages', 'Sans compromis', 6,
             'Tout ce que vous obtenez <b>avec ce bundle</b>', None, benefits, grey=True),
        band('conditions', 'Prérequis et conditions', 7,
             'Ce qu\'il faut <b>pour commencer</b>', None, req),
        band('formateurs', 'Vos experts', 8,
             'Vos <b>formateurs</b>', P['tutors_lede'], tuts, grey=True),
        band('faq', 'Questions fréquentes', 9,
             'Vos <b>questions</b>', None, faq),
    ])

    final = """  <section class="band band-final">
    <div class="band-in">
      <h2>%(title)s</h2>
      <p class="intro">%(text)s</p>
      <div class="final-buy">
        <div>
          <span class="final-was">%(retail)s %(cur)s à la carte</span>
          <span class="final-now">%(price)s<i>%(cur)s</i></span>
          <span class="final-save">Économie de %(save)s %(cur)s (%(pct)d %%%%)</span>
        </div>
        <a href="panier.html" class="final-cta" data-add="parcours:%(slug)s"
          data-plan="%(reco)d">%(button)s %(arrow)s</a>
      </div>
      <p class="pay-note" style="text-align:left">%(note)s</p>
    </div>
  </section>""" % dict(title=esc(P['cta']['title']), text=esc(P['cta']['text']),
                       slug=P['slug'], reco=P['recommended'],
                       retail=fr(F['retail']), cur=cur, price=fr(F['price']),
                       save=fr(F['save']), pct=F['pct'], button=esc(P['cta']['button']),
                       note=P['cta']['note'], arrow=I_ARROW)

    body = """<div class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane">
    <a href="index.html">Accueil</a> %(chev)s <a href="parcours.html">Parcours</a> %(chev)s <span>%(title)s</span>
  </nav>
</div>

<section class="hero">
  <div class="hero-img" style="background-image:url('%(img)s')"></div>
  <div class="hero-scrim"></div>
  <div class="hero-in">
    <div>
      <div class="hero-top">
        <span class="pill">%(tagline)s</span>
        <span class="kicker">%(level)s &middot; %(cat)s</span>
      </div>
      <h1>%(title)s</h1>
    </div>
    <div class="hero-offer">
      <p>%(sub)s</p>
      <div class="badges">
%(badges)s
      </div>
      <hr>
      <div class="hero-buy">
        <span class="hero-price">%(price)s<i>%(cur)s</i></span>
        <a href="panier.html" class="hero-cart" data-add="parcours:%(slug)s"
          data-plan="%(reco)d">Ajouter au panier %(arrow)s</a>
      </div>
    </div>
  </div>
</section>

<nav class="secnav" id="pSecnav" aria-label="Sections de la page">
  <div class="secnav-in">
%(secnav)s
  </div>
</nav>

%(bands)s

%(final)s

<script>
  /* progress bar tracks how far the formateurs track is scrolled — the
     homepage's own handler */
  (function () {
    var wrap = document.getElementById('aaFormWrap');
    var fill = document.getElementById('aaFormFill');
    if (!wrap || !fill) return;
    function update() {
      var max = wrap.scrollWidth - wrap.clientWidth;
      var ratio = max > 0 ? wrap.clientWidth / wrap.scrollWidth : 1;
      fill.style.width = (ratio * 100) + '%%';
      var travel = max > 0 ? wrap.scrollLeft / max : 0;
      fill.style.transform = 'translateX(' + (travel * (100 / ratio - 100)) + '%%)';
    }
    wrap.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  })();

  /* touch: tap a formateur card to open its bio, tap again to close */
  document.querySelectorAll('.aa-form-card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      card.classList.toggle('is-open');
    });
  });

  /* Alal_Stats_UnderlineRow's own interaction (initStatsLineReveal): each rule
     draws left to right once the row scrolls into view, one shot, and the rules
     are staggered rather than starting together — a 160ms transition-delay per
     item before the shared .in-view class flips the scaleX. */
  (function () {
    var row = document.getElementById('pStatsline');
    if (!row) return;
    var fills = Array.prototype.slice.call(row.querySelectorAll('.statsline-fill'));
    if (!fills.length) return;
    fills.forEach(function (fill, i) { fill.style.transitionDelay = (i * 160) + 'ms'; });
    if (!('IntersectionObserver' in window)) { row.classList.add('in-view'); return; }
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { row.classList.add('in-view'); obs.disconnect(); }
      });
    }, { threshold: 0.3 });
    obs.observe(row);
  })();

  /* Scroll spy, same as the homepage menu: the button whose section the probe
     line is inside gets .is-active, which both colours it and grows its
     indicator. The probe sits just under the header and the sticky bar. */
  (function () {
    var nav = document.getElementById('pSecnav');
    if (!nav) return;
    var links = {}, ids = [];
    Array.prototype.forEach.call(nav.querySelectorAll('a[href^="#"]'), function (a) {
      var id = a.getAttribute('href').slice(1);
      if (document.getElementById(id)) { links[id] = a; ids.push(id); }
    });
    if (!ids.length) return;
    var header = document.querySelector('header');
    var current = null, ticking = false;

    function spy() {
      ticking = false;
      var probe = window.scrollY + (header ? header.offsetHeight : 0) + nav.offsetHeight + 40;
      var found = null;
      for (var i = 0; i < ids.length; i++) {
        var el = document.getElementById(ids[i]);
        if (el.offsetTop <= probe) found = ids[i];
      }
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) {
        found = ids[ids.length - 1];
      }
      if (found === current) return;
      if (current && links[current]) links[current].classList.remove('is-active');
      current = found;
      if (current && links[current]) links[current].classList.add('is-active');
      if (current && links[current] && nav.firstElementChild.scrollWidth > nav.clientWidth) {
        var a = links[current], box = nav.firstElementChild;
        box.scrollTo({ left: a.offsetLeft - box.clientWidth / 2 + a.offsetWidth / 2,
                       behavior: 'smooth' });
      }
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(spy); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    spy();
  })();
</script>
""" % dict(chev=I_CHEV, title=esc(P['title']), img=P['image'], sub=esc(P['subtitle']),
           slug=P['slug'], reco=P['recommended'],
           tagline=esc(P['tagline']), level=esc(P['level']), cat=esc(P['category']),
           badges=badges, price=fr(F['price']), cur=cur, arrow=I_ARROW,
           secnav=secnav, bands=bands, final=final)

    out = __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap" rel="stylesheet">
<title>%s — Parcours — Alal Academy</title>
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
""" % (html.escape(P['title']), html.escape(P['subtitle'][:180]), BASE, CSS,
       nav_active(HEADER, 'parcours') + MNAV, body, FOOTER.replace('{ROOT}', '../'),
       cart_js('../') + __import__('modals').modals('../') + __import__('modals').MODAL_JS))

    # the shared header/footer and every asset live one level up from parcours/
    out = out.replace('href="index.html', 'href="../index.html')
    out = out.replace('href="blog.html"', 'href="../blog.html"')
    out = out.replace('href="parcours.html"', 'href="../parcours.html"')
    out = out.replace('href="panier.html"', 'href="../panier.html"')
    out = out.replace('href="webinaires.html"', 'href="../webinaires.html"')
    out = out.replace('href="cours/', 'href="../cours/')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace("url('assets/", "url('../assets/")
    out = out.replace('href="../../index.html', 'href="../index.html')
    out = out.replace('src="../../assets/', 'src="../assets/')

    os.makedirs(os.path.join(ROOT, 'parcours'), exist_ok=True)
    open(os.path.join(ROOT, 'parcours', P['slug'] + '.html'), 'w', encoding='utf-8').write(out)
    print('parcours/%s.html  (%d cours, %d leçons, %s, %s → %s %s, -%d%%, %d plans)'
          % (P['slug'], F['n'], F['lessons'], hm(F['total_min']), fr(F['retail']),
             fr(F['price']), P['currency'], F['pct'], len(P['plans'])))


# ─────────────────────────────── list page ─────────────────────────────────
WHY = [
    ("Un métier, pas un sujet",
     "Un parcours réunit les cours qui font tenir un poste, dans l'ordre où ils "
     "se suivent — pas une sélection au hasard du catalogue."),
    ("Moins cher que la carte",
     "Les cours d'un parcours sont vendus ensemble, sous la somme de leurs prix "
     "à l'unité, avec le paiement en 1×, 2× ou 3×."),
    ("Accès à vie, certificat inclus",
     "Le contenu reste le vôtre sans limite de temps, et le parcours terminé "
     "délivre son certificat officiel."),
]


def build_list():
    blocks = []
    for P in PARCOURS:
        F = facts(P)
        # Contrats Islamiques has no published programme yet, so it carries no
        # lesson count — the line then shows the title alone
        inc = "\n".join(
            '        <li>%s<span>%s%s</span></li>'
            % (CHECK, esc(c['title']),
               (' <b style="font-weight:400;color:#A7A7A7">— %d leçons · %s</b>'
                % (c['lessons'], hm(d))) if c['lessons'] else '')
            for c, d in F['rows'])
        blocks.append(
            """  <div class="feat">
    <a class="feat-img" href="parcours/%(slug)s.html" style="background-image:url('%(img)s')"
       aria-label="%(title)s"><b>%(cat)s</b></a>
    <div class="feat-body">
      <span class="kicker">Parcours certifiant &middot; %(tagline)s</span>
      <h2><a href="parcours/%(slug)s.html">%(title)s</a></h2>
      <p>%(sub)s</p>
      <hr class="feat-rule">
      <div class="feat-meta">
        <span>%(i_book)s %(n)d cours</span>
        <span>%(i_play)s %(lessons)d leçons</span>
        <span>%(i_clock)s %(dur)s</span>
        <span>%(i_seal)s Certificat Alal Academy</span>
      </div>
      <hr class="feat-rule">
      <ul class="feat-courses">
%(inc)s
      </ul>
      <hr class="feat-rule">
      <div class="feat-foot">
        <a class="feat-cta" href="parcours/%(slug)s.html">Voir le parcours %(i_arrow)s</a>
      </div>
    </div>
  </div>""" % dict(slug=P['slug'], img=P['image'], cat=esc(P['category']),
                   title=esc(P['title']), tagline=esc(P['tagline']), sub=esc(P['subtitle']),
                   i_book=I_BOOK, i_play=I_PLAY, i_clock=I_CLOCK, i_seal=I_SEAL,
                   i_arrow=I_ARROW, n=F['n'], lessons=F['lessons'], dur=hm(F['total_min']),
                   inc=inc))

    body = """<div class="wrap">
  <div class="plist-head">
    <h1 class="plist-title">Parcours certifiants</h1>
    <p class="plist-lede">Un parcours regroupe les cours essentiels d'une spécialité — vendus ensemble,
      bien moins cher qu'à la carte, et dans l'ordre où ils se suivent. Paiement en 1×, 2× ou 3×,
      accès immédiat dès le premier versement.</p>
  </div>

%s

  <div class="plist-tail"></div>
  <hr class="rule">
</div>
""" % ("\n\n".join(blocks),)

    out = __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Parcours certifiants — Alal Academy</title>
<meta name="description" content="Les parcours Alal Academy : les cours essentiels d'une spécialité, vendus ensemble et moins cher qu'à la carte.">
<style>%s%s</style>
</head>
<body>
%s
%s
%s
%s
</body>
</html>
""" % (BASE, CSS, nav_active(HEADER, 'parcours') + MNAV, body,
       FOOTER.replace('{ROOT}', ''),
       cart_js('') + __import__('modals').modals('') + __import__('modals').MODAL_JS))

    open(os.path.join(ROOT, 'parcours.html'), 'w', encoding='utf-8').write(out)
    print('parcours.html  (%d parcours)' % len(PARCOURS))


def build():
    build_list()
    for P in PARCOURS:
        build_one(P)


if __name__ == '__main__':
    build()
