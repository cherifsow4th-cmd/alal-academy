# -*- coding: utf-8 -*-
"""Builds panier.html (the cart) and 404.html, plus the signed-in header.

The signed-in header is the ordinary site header with its two sign-in buttons
replaced by an account chip — avatar, first name, a menu — and a cart icon that
carries a live count. It is defined here rather than in gen.py so the signed-out
pages keep their own header untouched; AUTH_HEADER / AUTH_MNAV can be imported
by any other page that should render as signed in.

The cart carries real catalogue items: the CIB parcours with its three payment
plans (and their fractionnement fees), and courses at 69 000 FCFA each. Every
figure is computed in the page from those, so removing a line, switching a plan
or applying the demo promo code re-totals everything live.
"""
import os, sys, html, json
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, HEADER, FOOTER, MNAV, MONO, ROOT
from courses import COURSES
from parcours_data import PARCOURS
from cartkit import cart_js, CART_CSS_SHARED

BY_SLUG = {c['slug']: c for c in COURSES}
P = PARCOURS[0]

# ── the person we render as signed in ────────────────────────────────────
USER = dict(first='Cherif', last='Sow', initials='CS', email='cs@saalal.com')


def esc(t):
    return html.escape(t, quote=False)


def fr(n):
    s, out = '%d' % n, ''
    while len(s) > 3:
        out, s = ' ' + s[-3:] + out, s[:-3]
    return s + out


def ico(d, w=18):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" aria-hidden="true" '
            'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (w, w, d))


I_CART = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
          '<path d="M2.75 3.25h1.8a1 1 0 0 1 .98.8l.38 1.95m0 0 1.72 8.6a1.6 1.6 0 0 0 1.57 1.28h7.76'
          'a1.6 1.6 0 0 0 1.57-1.26l1.47-6.62a1.2 1.2 0 0 0-1.17-1.46H5.91Z" stroke="currentColor" '
          'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
          '<path d="M9.6 20.75a1.35 1.35 0 1 0 0-2.7 1.35 1.35 0 0 0 0 2.7ZM17.1 20.75a1.35 1.35 0 1 0 '
          '0-2.7 1.35 1.35 0 0 0 0 2.7Z" stroke="currentColor" stroke-width="1.5" '
          'stroke-linecap="round" stroke-linejoin="round"/></svg>')
I_CHEV = ico('<path d="m6 9 6 6 6-6"/>', 14)
I_TRASH = ico('<path d="M3.5 6h17M9 6V4.5A1.5 1.5 0 0 1 10.5 3h3A1.5 1.5 0 0 1 15 4.5V6m3 0-.7 12.1'
              'a2 2 0 0 1-2 1.9H8.7a2 2 0 0 1-2-1.9L6 6"/>', 16)
I_ARROW = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="M7 17 17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.6" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')
I_LOCK = ico('<rect x="4.5" y="10" width="15" height="10.5" rx="2.5"/>'
             '<path d="M8 10V7.5a4 4 0 0 1 8 0V10"/>', 15)
CHECK = ('<svg width="15" height="15" viewBox="5267.0 2012.42 10.0 7.16" fill="none" aria-hidden="true">'
         '<path d="M5267.75 2016L5270.58 2018.83L5276.25 2013.17" stroke="currentColor" '
         'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ── signed-in header ──────────────────────────────────────────────────────
ACCOUNT_LINKS = [
    ('Tableau de bord', 'compte.html'),
    ('Mes cours', 'mes-cours.html'),
    ('Mes certificats', 'mes-certificats.html'),
    ('Mes commandes', 'mes-commandes.html'),
    ('Paramètres', 'parametres.html'),
]

_ACTIONS = """<div class="nav-actions">
      <div class="acct" id="aaAcct">
        <button type="button" class="acct-btn" id="aaAcctBtn" aria-haspopup="menu" aria-expanded="false">
          <span class="acct-av">%(ini)s</span>
          <span class="acct-name">%(first)s</span>
          %(chev)s
        </button>
        <div class="acct-menu" id="aaAcctMenu" role="menu" hidden>
          <div class="acct-head">
            <span class="acct-av acct-av-lg">%(ini)s</span>
            <span><b>%(full)s</b><i>%(mail)s</i></span>
          </div>
%(links)s
          <a href="index.html" class="acct-out" role="menuitem">Déconnexion</a>
        </div>
      </div>
      <span class="nav-sep" aria-hidden="true"></span>
      <a href="panier.html" class="btn-icon cart-btn" aria-label="Panier">
        %(cart)s<span class="cart-count" id="aaCartCount">3</span>
      </a>
    </div>""" % dict(
    ini=USER['initials'], first=USER['first'], chev=I_CHEV, cart=I_CART,
    full=USER['first'] + ' ' + USER['last'], mail=USER['email'],
    links="\n".join('          <a href="%s" role="menuitem">%s</a>' % (h, l)
                    for l, h in ACCOUNT_LINKS))

_i = HEADER.index('<div class="nav-actions">')
_j = HEADER.index('</div>\n  </div>\n</header>')
AUTH_HEADER = HEADER[:_i] + _ACTIONS + HEADER[_j + len('</div>'):]

AUTH_MNAV = MNAV.replace("""<div class="mnav-foot">
      <a href="#signup" class="mnav-cta">Créer un compte <span>&rarr;</span></a>
      <div class="mnav-row">
        <a href="#login" class="mnav-ghost">Connexion</a>
        <a href="index.html#panier" class="mnav-ghost">Panier</a>
      </div>
    </div>""",
"""<div class="mnav-foot">
      <div class="mnav-user"><span class="acct-av">%(ini)s</span>
        <span><b>%(full)s</b><i>%(mail)s</i></span></div>
      <a href="panier.html" class="mnav-cta">Mon panier <span>&rarr;</span></a>
      <div class="mnav-row">
        <a href="compte.html" class="mnav-ghost">Tableau de bord</a>
        <a href="mes-cours.html" class="mnav-ghost">Mes cours</a>
        <a href="index.html" class="mnav-ghost">Déconnexion</a>
      </div>
    </div>""" % dict(ini=USER['initials'], full=USER['first'] + ' ' + USER['last'],
                     mail=USER['email']))

AUTH_CSS = """
  /* ── signed-in header ──────────────────────────────────────────────────
     The two sign-in buttons give way to an account chip and a cart that
     carries its count; everything else in the header is unchanged. */
  .acct{position:relative}
  .acct-btn{display:inline-flex;align-items:center;gap:9px;font:inherit;font-size:14.5px;
    font-weight:500;color:#1F1F1F;cursor:pointer;background:#FFFFFF;
    border:1px solid rgba(31,31,31,.14);border-radius:999px;padding:5px 13px 5px 5px;
    transition:box-shadow .3s ease,border-color .3s ease}
  .acct-btn:hover{border-color:rgba(31,31,31,.3);box-shadow:0 2px 5px rgba(0,0,0,.08)}
  .acct-btn svg{color:#7a7a7a;transition:transform .35s cubic-bezier(.22,1,.36,1)}
  .acct.is-open .acct-btn svg{transform:rotate(180deg)}
  .acct-av{display:flex;align-items:center;justify-content:center;width:30px;height:30px;flex:none;
    border-radius:50%;background:#1F1F1F;color:#FFFFFF;font-size:11.5px;font-weight:500;
    letter-spacing:.02em}
  .acct-av-lg{width:40px;height:40px;font-size:14px}
  .acct-menu{position:absolute;top:calc(100% + 12px);right:0;width:272px;z-index:60;
    background:#FFFFFF;border:1px solid rgba(31,31,31,.1);border-radius:16px;padding:8px;
    box-shadow:0 4px 10px rgba(0,0,0,.05),0 18px 44px rgba(0,0,0,.12);
    opacity:0;transform:translateY(-6px);pointer-events:none;
    transition:opacity .25s ease,transform .3s cubic-bezier(.22,1,.36,1)}
  .acct-menu[hidden]{display:none}
  .acct.is-open .acct-menu{opacity:1;transform:translateY(0);pointer-events:auto}
  .acct-head{display:flex;align-items:center;gap:12px;padding:12px 12px 14px;
    border-bottom:1px solid rgba(31,31,31,.09);margin-bottom:6px}
  .acct-head b{display:block;font-size:14.5px;font-weight:500}
  .acct-head i{display:block;font-style:normal;font-size:12.5px;color:#7a7a7a;margin-top:2px}
  .acct-menu a{display:block;padding:10px 12px;border-radius:10px;font-size:14.5px;color:#1F1F1F;
    transition:background .2s ease}
  .acct-menu a:hover{background:#FCFBF8}
  .acct-out{margin-top:6px;border-top:1px solid rgba(31,31,31,.09);border-radius:0 0 10px 10px;
    color:#7a7a7a !important}
  .cart-btn{position:relative}
  .cart-count{position:absolute;top:-6px;right:-6px;min-width:19px;height:19px;padding:0 5px;
    border-radius:999px;background:#0E695C;color:#FFFFFF;font-size:11px;font-weight:500;
    display:flex;align-items:center;justify-content:center;border:2px solid #FFFFFF}
  .cart-count.is-zero{display:none}
  .mnav-user{display:flex;align-items:center;gap:12px;padding:0 0 18px;margin-bottom:4px;
    border-bottom:1px solid rgba(31,31,31,.09)}
  .mnav-user b{display:block;font-size:15px;font-weight:500}
  .mnav-user i{display:block;font-style:normal;font-size:12.5px;color:#7a7a7a;margin-top:2px}
  @media (min-width:744px) and (max-width:1199px){
    .acct-btn{font-size:13px;padding:4px 11px 4px 4px}
    .acct-av{width:26px;height:26px;font-size:10.5px}
  }
  @media (max-width:560px){ .acct-name{display:none} }
"""


# the chip menu's behaviour, so pages outside this module can reuse it
ACCT_JS = """
<script>
/* the account menu: click to open, click outside or Escape to close */
(function () {
  var box = document.getElementById('aaAcct');
  if (!box) return;
  var btn = document.getElementById('aaAcctBtn');
  var menu = document.getElementById('aaAcctMenu');
  function open(on) {
    box.classList.toggle('is-open', on);
    btn.setAttribute('aria-expanded', on ? 'true' : 'false');
    if (on) { menu.hidden = false; }
    else { setTimeout(function () { if (!box.classList.contains('is-open')) menu.hidden = true; }, 260); }
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); open(!box.classList.contains('is-open')); });
  document.addEventListener('click', function (e) { if (!box.contains(e.target)) open(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') open(false); });
})();
</script>
"""

CART_CSS = """
  /* a class that sets display beats the UA's [hidden] rule, and several of the
     rows this page toggles are flex — so hidden has to win outright */
  [hidden]{display:none !important}
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}
  .crumbs{display:flex;align-items:center;gap:9px;padding:26px 0 0;font-size:13px;color:#7a7a7a}
  .crumbs a:hover{color:#1F1F1F}

  .cart-head{padding:34px 0 0;display:flex;align-items:baseline;justify-content:space-between;
    gap:24px;flex-wrap:wrap}
  .cart-head h1{margin:0;font-size:clamp(38px,5.4vw,72px);line-height:1.04;letter-spacing:-0.04em;
    font-weight:300}
  .cart-head .count{font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:10.5px;
    letter-spacing:.12em;text-transform:uppercase;color:#7a7a7a}
  .cart-layout{display:grid;grid-template-columns:minmax(0,1fr) 420px;gap:52px;
    padding:46px 0 110px;align-items:start}

  /* ── lines ───────────────────────────────────────────────────────────── */
  .lines{list-style:none;margin:0;padding:0;border-top:1px solid rgba(31,31,31,.12)}
  .line{display:grid;grid-template-columns:188px minmax(0,1fr) auto;gap:26px;
    padding:28px 0;border-bottom:1px solid rgba(31,31,31,.12);align-items:start}
  /* removing a line collapses it rather than making the page jump */
  .line{overflow:hidden;transition:opacity .3s ease,transform .35s cubic-bezier(.2,.8,.2,1),
    max-height .45s cubic-bezier(.2,.8,.2,1),padding .45s cubic-bezier(.2,.8,.2,1),
    border-color .3s ease;max-height:460px}
  .line.is-going{opacity:0;transform:translateX(-14px);max-height:0;padding-top:0;padding-bottom:0;
    border-color:transparent}
  /* the course artwork is 16:9 with type baked in, so the box matches it and
     object-fit:contain guarantees nothing is cut, whatever the picture's ratio.
     A parcours carries a plain photograph instead, with nothing to clip, so it
     fills the box rather than sitting letterboxed inside it. */
  .line-img{display:block;width:188px;aspect-ratio:16/9;border-radius:14px;object-fit:contain;
    background:#EAEAEA}
  .line-img.is-photo{object-fit:cover}
  .line-kicker{font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:9.5px;
    letter-spacing:.12em;text-transform:uppercase;color:#7a7a7a}
  .line h3{margin:10px 0 0;font-size:21px;font-weight:500;letter-spacing:-0.022em;line-height:1.3}
  .line h3 a:hover{color:#0E695C}
  .line-meta{margin:9px 0 0;font-size:14px;color:#7a7a7a}
  /* a column so the remove button sits under the price rather than beside it */
  .line-right{display:flex;flex-direction:column;align-items:flex-end;text-align:right;
    white-space:nowrap}
  .line-price{font-size:22px;font-weight:500;letter-spacing:-0.03em}
  .line-price i{font-style:normal;font-size:12.5px;color:#7a7a7a;letter-spacing:0;margin-left:6px}
  .line-was{display:block;margin-top:6px;font-size:12.5px;color:#A7A7A7;text-decoration:line-through}
  .line-rm{align-self:flex-end}
  /* a real button under the price, not a link beside it */
  .line-rm{display:inline-flex;align-items:center;justify-content:center;gap:8px;margin-top:16px;
    font:inherit;font-size:13.5px;color:#1F1F1F;background:#FFFFFF;cursor:pointer;
    border:1px solid rgba(31,31,31,.16);border-radius:10px;padding:9px 15px;
    transition:border-color .25s ease,box-shadow .3s ease}
  .line-rm:hover{border-color:rgba(31,31,31,.34);box-shadow:0 2px 5px rgba(0,0,0,.07)}

  /* the parcours line carries its payment plan inline */
  .plan-pick{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
  .plan-pick label{cursor:pointer}
  .plan-pick input{position:absolute;opacity:0;width:0;height:0}
  .plan-pick span{display:inline-flex;flex-direction:column;gap:2px;padding:9px 15px;
    border:1px solid rgba(31,31,31,.14);border-radius:12px;font-size:13.5px;background:#FFFFFF;
    transition:border-color .25s ease,background .25s ease,color .25s ease}
  .plan-pick span b{font-weight:500}
  .plan-pick span i{font-style:normal;font-size:11.5px;color:#7a7a7a}
  .plan-pick label:hover span{border-color:rgba(31,31,31,.34)}
  .plan-pick input:checked + span{background:#1F1F1F;border-color:#1F1F1F;color:#FFFFFF}
  .plan-pick input:checked + span i{color:rgba(255,255,255,.66)}
  .plan-pick input:focus-visible + span{outline:2px solid #0E695C;outline-offset:2px}

  .cart-foot{display:flex;align-items:center;justify-content:space-between;gap:20px;
    flex-wrap:wrap;margin-top:26px}
  .cart-foot a{display:inline-flex;align-items:center;gap:9px;font-size:14.5px;color:#1F1F1F}
  .cart-foot a:hover{color:#0E695C}

  /* ── empty state ─────────────────────────────────────────────────────── */
  .empty{display:none;border:1px dashed rgba(31,31,31,.2);border-radius:24px;padding:54px 44px;
    background:#FCFBF8;text-align:center}
  .empty.is-on{display:block}
  .empty h2{margin:0;font-size:26px;font-weight:500;letter-spacing:-0.03em}
  .empty p{margin:13px auto 0;font-size:16px;line-height:1.6;color:#7a7a7a;max-width:46ch}
  .empty-cta{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:26px}
  .empty-cta a{display:inline-flex;align-items:center;gap:9px;padding:14px 22px;border-radius:12px;
    font-size:14.5px;font-weight:500}
  .empty-cta a:first-child{background:#1F1F1F;color:#FFFFFF}
  .empty-cta a:last-child{background:#FFFFFF;border:1px solid rgba(31,31,31,.16);color:#1F1F1F}

  /* ── summary ─────────────────────────────────────────────────────────── */
  .sum{position:sticky;top:104px;border:1px solid rgba(31,31,31,.1);border-radius:24px;
    background:#FFFFFF;padding:30px 32px}
  .sum h2{margin:0 0 22px;font-size:19px;font-weight:500;letter-spacing:-0.02em}
  .sum-row{display:flex;align-items:baseline;justify-content:space-between;gap:16px;
    font-size:14.5px;color:#7a7a7a;padding:9px 0}
  .sum-row b{font-weight:400;color:#1F1F1F;white-space:nowrap}
  .sum-row.is-save b{color:#0E695C}
  .sum-row.is-fee b{color:#1F1F1F}
  .sum-sep{display:block;height:1px;background:rgba(31,31,31,.1);margin:14px 0}
  .sum-total{display:flex;align-items:baseline;justify-content:space-between;gap:16px}
  .sum-total span{font-size:15px;color:#7a7a7a}
  .sum-total b{font-size:30px;font-weight:500;letter-spacing:-0.035em}
  .sum-total b i{font-style:normal;font-size:13px;color:#7a7a7a;letter-spacing:0;margin-left:7px}
  /* the plan the total is paid on, read before the figure it applies to */
  .sum-plan{margin:4px 0 0;font-size:13.5px;color:#7a7a7a;text-align:right}
  .sum-cta{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:24px;
    padding:15px 20px;border-radius:12px;background:#1F1F1F;color:#FFFFFF;font-size:15px;
    font-weight:500;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .sum-cta:hover{box-shadow:0 2px 6px rgba(0,0,0,.32),0 7px 16px rgba(0,0,0,.28),
    0 17px 33px rgba(0,0,0,.24)}
  .sum-cta[aria-disabled="true"]{background:#EAEAEA;color:#A7A7A7;pointer-events:none}
  .sum-note{display:flex;align-items:center;justify-content:center;gap:8px;margin:14px 0 0;
    font-size:12.5px;color:#7a7a7a}
  .sum-ways{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;margin-top:20px;
    padding-top:20px;border-top:1px solid rgba(31,31,31,.1)}
  .sum-ways b{font-weight:400;font-size:12px;color:#7a7a7a;border:1px solid rgba(31,31,31,.12);
    border-radius:999px;padding:6px 11px}
  .gtee{list-style:none;margin:20px 0 0;padding:18px 0 0;border-top:1px solid rgba(31,31,31,.1);
    display:flex;flex-direction:column;gap:10px}
  .gtee li{display:flex;gap:10px;font-size:13.5px;line-height:1.45;color:#7a7a7a}
  .gtee svg{flex:none;color:#0E695C;margin-top:3px}

  /* promo code */
  .promo{margin-top:20px;padding-top:18px;border-top:1px solid rgba(31,31,31,.1)}
  .promo-row{display:flex;gap:8px}
  .promo input{flex:1;min-width:0;font:inherit;font-size:14px;padding:12px 14px;border-radius:11px;
    border:1px solid rgba(31,31,31,.14);background:#FFFFFF;color:#1F1F1F}
  .promo input::placeholder{color:#A7A7A7}
  .promo input:focus{outline:none;border-color:#1F1F1F}
  .promo button{font:inherit;font-size:14px;font-weight:500;padding:12px 16px;border-radius:11px;
    border:1px solid rgba(31,31,31,.16);background:#FFFFFF;color:#1F1F1F;cursor:pointer;
    transition:box-shadow .3s ease}
  .promo button:hover{box-shadow:0 2px 5px rgba(0,0,0,.08)}
  .promo-msg{margin:10px 0 0;font-size:12.5px;color:#A7A7A7}
  .promo-msg.is-bad{color:#1F1F1F}
  .promo-tag{display:none;align-items:center;gap:9px;margin-top:12px;font-size:13px;color:#0E695C;
    border:1px solid #0E695C;border-radius:999px;padding:7px 12px;width:fit-content}
  .promo-tag.is-on{display:inline-flex}
  .promo-tag button{font:inherit;font-size:13px;line-height:1;color:#0E695C;background:none;
    border:0;padding:0;cursor:pointer}

  /* undo toast */
  .toast{position:fixed;left:50%;bottom:28px;transform:translate(-50%,16px);z-index:120;
    display:flex;align-items:center;gap:18px;background:#1F1F1F;color:#FFFFFF;border-radius:14px;
    padding:14px 18px;font-size:14px;box-shadow:0 18px 44px rgba(0,0,0,.28);
    opacity:0;pointer-events:none;transition:opacity .3s ease,transform .35s cubic-bezier(.2,.8,.2,1)}
  .toast.is-on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
  .toast button{font:inherit;font-size:14px;font-weight:500;color:#FFFFFF;background:none;border:0;
    padding:0;cursor:pointer;text-decoration:underline;text-underline-offset:3px}

  /* ── 404 ─────────────────────────────────────────────────────────────── */
  .nf{padding:110px 0 0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;
    align-items:center}
  .nf-num{margin:0;font-size:clamp(120px,19vw,300px);line-height:.86;letter-spacing:-0.06em;
    font-weight:200;color:#1F1F1F}
  .nf h1{margin:0;font-size:clamp(30px,3.6vw,46px);line-height:1.08;letter-spacing:-0.035em;
    font-weight:300}
  .nf h1 b{font-weight:500}
  /* scoped to the text column: .nf p would out-specify .nf-num, which is a <p> */
  .nf div p{margin:22px 0 0;font-size:17px;line-height:1.62;color:#7a7a7a;max-width:46ch}
  .nf-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:30px}
  .nf-cta a{display:inline-flex;align-items:center;gap:9px;padding:15px 24px;border-radius:12px;
    font-size:15px;font-weight:500;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .nf-cta a:first-child{background:#1F1F1F;color:#FFFFFF}
  .nf-cta a:first-child:hover{box-shadow:0 2px 6px rgba(0,0,0,.3),0 10px 24px rgba(0,0,0,.24)}
  .nf-cta a:last-child{background:#FFFFFF;border:1px solid rgba(31,31,31,.16);color:#1F1F1F}
  .nf-links{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:92px 0 0;
    border-top:1px solid rgba(31,31,31,.09)}
  .nf-links a{display:block;padding:30px 34px;border-left:1px solid rgba(31,31,31,.09);
    transition:background .3s ease}
  .nf-links a:first-child{border-left:0;padding-left:0}
  .nf-links a:hover{background:#FCFBF8}
  .nf-links b{display:block;font-size:17px;font-weight:500;letter-spacing:-0.02em}
  .nf-links span{display:block;margin-top:9px;font-size:14.5px;line-height:1.55;color:#7a7a7a}
  .nf-tail{padding:0 0 100px}

  /* ── tablet ──────────────────────────────────────────────────────────── */
  @media (min-width:744px) and (max-width:1240px){
    .cart-layout{grid-template-columns:minmax(0,1fr) 300px;gap:28px;padding-bottom:72px}
    .line{grid-template-columns:148px minmax(0,1fr);gap:20px}
    .line-img{width:148px}
    .line-right{grid-column:2;align-items:flex-start;text-align:left;margin-top:8px}
    .line h3{font-size:18px}
    .sum{padding:24px 22px;border-radius:20px}
    .sum-total b{font-size:25px}
    .nf{gap:34px;padding-top:72px}
    .nf h1{font-size:32px}
    .nf p{font-size:15px}
    .nf-links{grid-template-columns:repeat(2,1fr);margin-top:64px}
    .nf-links a{padding:22px 20px}
    .nf-links a:nth-child(odd){border-left:0;padding-left:0}
  }
  /* ── phone ───────────────────────────────────────────────────────────── */
  @media (max-width:743px){
    .cart-head{padding-top:26px}
    .cart-layout{grid-template-columns:1fr;gap:0;padding:30px 0 64px}
    .line{grid-template-columns:112px minmax(0,1fr);gap:16px;padding:22px 0}
    .line-img{width:112px}
    .line-right{grid-column:2;align-items:flex-start;text-align:left;margin-top:8px}
    .line-rm{align-self:flex-start}
    .line h3{font-size:17px;margin-top:8px}
    .plan-pick{gap:6px}
    .plan-pick span{padding:8px 12px;font-size:12.5px}
    .sum{position:static;margin-top:34px;padding:24px;border-radius:20px}
    .empty{padding:38px 24px}
    .toast{left:16px;right:16px;bottom:16px;transform:translateY(16px);justify-content:space-between}
    .toast.is-on{transform:translateY(0)}
    .nf{grid-template-columns:1fr;gap:18px;padding-top:56px}
    .nf-num{font-size:116px}
    .nf-cta a{flex:1 1 100%;justify-content:center}
    .nf-links{grid-template-columns:1fr;margin-top:56px}
    .nf-links a{padding:22px 0;border-left:0}
    .nf-links a+a{border-top:1px solid rgba(31,31,31,.09)}
    .nf-tail{padding-bottom:64px}
  }
"""


# ── what is in the cart when the page opens ───────────────────────────────
CART = [
    dict(kind='parcours', slug=P['slug']),
    dict(kind='cours', slug='fondamentaux-finance-islamique'),
    dict(kind='cours', slug='islamic-treasury-liquidite'),
]
PROMO = dict(code='ALAL10', pct=10)   # demo code, swap for the real one


def page(title, desc, body, css=''):
    # cart_js first: the cart page's own script reads window.AA_CART at parse time
    return __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<style>%s%s%s</style>
</head>
<body>
%s
%s
%s
%s
</body>
</html>
""" % (html.escape(title), html.escape(desc), BASE, AUTH_CSS, CART_CSS + css,
       AUTH_HEADER + AUTH_MNAV, cart_js(''), body,
       FOOTER.replace('{ROOT}', '') + __import__('modals').modals('') + __import__('modals').MODAL_JS))


def build_cart():
    """The lines are rendered in the browser from window.AA_CART, so whatever
    was added anywhere on the site is what shows here. The markup below is the
    shell: the empty state, the summary and the toast."""
    ways = "".join('<b>%s</b>' % w for w in P['pay_ways'])

    body = """<div class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane">
    <a href="index.html">Accueil</a> <span>&rsaquo;</span> <span>Panier</span>
  </nav>

  <div class="cart-head">
    <h1>Mon panier</h1>
    <span class="count" id="cartCount">—</span>
  </div>

  <div class="cart-layout">
    <div>
      <ul class="lines" id="cartLines"></ul>

      <div class="cart-foot" id="cartFoot">
        <a href="index.html#catalogue">&larr; Continuer mes achats</a>
        <span class="line-kicker">Les prix sont en FCFA, toutes taxes comprises</span>
      </div>

      <section class="empty" id="cartEmpty" aria-live="polite">
        <h2>Votre panier est vide</h2>
        <p>Parcourez le catalogue ou reprenez le parcours Certified Islamic Banker —
          les huit cours du métier en une seule inscription.</p>
        <div class="empty-cta">
          <a href="index.html#catalogue">Voir le catalogue %(arrow)s</a>
          <a href="parcours.html">Voir les parcours</a>
        </div>
      </section>
    </div>

    <aside class="sum" aria-label="Récapitulatif">
      <h2>Récapitulatif</h2>
      <div class="sum-row"><span id="sumCountLabel">Sous-total</span><b id="sumSub">—</b></div>
      <div class="sum-row is-save" id="sumSaveRow"><span>Économie bundle</span><b id="sumSave">—</b></div>
      <div class="sum-row is-save" id="sumPromoRow" hidden><span>Code %(promo)s</span><b id="sumPromo">—</b></div>
      <div class="sum-row is-fee" id="sumFeeRow"><span id="sumFeeLabel">Frais de fractionnement</span><b id="sumFee">—</b></div>
      <p class="sum-plan" id="sumPlan">—</p>
      <span class="sum-sep"></span>
      <div class="sum-total"><span>Total</span><b id="sumTotal">—<i>%(cur)s</i></b></div>
      <div class="promo">
        <div class="promo-row">
          <input id="promoInput" type="text" placeholder="Code promo" aria-label="Code promo"
            autocomplete="off">
          <button type="button" id="promoBtn">Appliquer</button>
        </div>
        <p class="promo-msg" id="promoMsg">Un seul code par commande.</p>
        <span class="promo-tag" id="promoTag">%(promo)s appliqué
          <button type="button" id="promoRm" aria-label="Retirer le code">&times;</button></span>
      </div>

      <div class="sum-ways">%(ways)s</div>

      <a href="index.html#paiement" class="sum-cta" id="sumCta">Passer au paiement %(arrow)s</a>
      <p class="sum-note">%(lock)s Paiement sécurisé</p>
    </aside>
  </div>
  <hr class="rule">
</div>

<div class="toast" id="toast" role="status">
  <span id="toastText">Article retiré</span>
  <button type="button" id="toastUndo">Annuler</button>
</div>
""" % dict(arrow=I_ARROW, lock=I_LOCK, cur=P['currency'], promo=PROMO['code'],
           ways=ways)

    body += SCRIPT
    out = page('Mon panier — Alal Academy',
               "Votre panier Alal Academy : parcours et cours, plans de paiement et total.",
               body)
    open(os.path.join(ROOT, 'panier.html'), 'w', encoding='utf-8').write(out)
    print('panier.html  (rendu depuis le panier du visiteur)')



SCRIPT = """
<script>
/* The cart page renders window.AA_CART against the catalogue, then totals it.
   Every mutation — remove, undo, plan switch, promo — writes back to the store
   and re-renders, so the header count and any other open tab agree. */
(function () {
  var CUR = 'FCFA';
  var PROMO_CODE = 'ALAL10', PROMO_PCT = 10;
  var CAT = window.AA_CATALOG, STORE = window.AA_CART;

  var listEl   = document.getElementById('cartLines');
  var emptyEl  = document.getElementById('cartEmpty');
  var footEl   = document.getElementById('cartFoot');
  var countEl  = document.getElementById('cartCount');
  var toast    = document.getElementById('toast');
  var toastTx  = document.getElementById('toastText');
  var promoOn  = false, undoTimer = null, undoItem = null;

  function fr(n) {
    return String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '\\u202f');
  }

  /* first visit seeds a demo cart so the page is never empty on arrival;
     after that the real store wins, empty included */
  if (STORE.read() === null) {
    STORE.write([{ id: 'parcours:' + PARCOURS_SLUG, plan: PARCOURS_RECO },
                 { id: 'cours:fondamentaux-finance-islamique' },
                 { id: 'cours:islamic-treasury-liquidite' }]);
  }

  function planOf(item, entry) {
    if (item.kind !== 'parcours') return null;
    var n = entry.plan || item.reco;
    var found = item.plans[0];
    item.plans.forEach(function (p) { if (p.n === n) found = p; });
    return found;
  }

  function lineHTML(entry) {
    var it = CAT[entry.id];
    if (!it) return '';
    var pl = planOf(it, entry);
    var picks = '';
    if (pl) {
      picks = '<div class="plan-pick" role="radiogroup" aria-label="Plan de paiement">' +
        it.plans.map(function (p) {
          return '<label><input type="radio" name="plan-' + entry.id + '" value="' + p.n + '"' +
            (p.n === pl.n ? ' checked' : '') + '><span><b>' + (p.n === 1 ? '1×' : p.n + '×') +
            '</b><i>' + fr(p.per) + ' ' + CUR + (p.n === 1 ? '' : ' / versement') +
            '</i></span></label>';
        }).join('') + '</div>';
    }
    return '<li class="line" data-id="' + entry.id + '">' +
      '<img class="line-img' + (it.kind === 'parcours' ? ' is-photo' : '') +
        '" src="' + it.img + '" alt="" width="188" height="106">' +
      '<div><span class="line-kicker">' +
        (it.kind === 'parcours' ? 'Parcours' : 'Cours') + ' &middot; ' + it.cat + '</span>' +
      '<h3><a href="' + it.url + '">' + it.title + '</a></h3>' +
      '<p class="line-meta">' + it.meta + '</p>' + picks + '</div>' +
      '<div class="line-right"><span class="line-price">' +
        fr(pl ? pl.per : it.price) + '<i>' + CUR + '</i></span>' +
      (it.retail ? '<span class="line-was">' + fr(it.retail) + ' ' + CUR + ' à la carte</span>' : '') +
      '<button type="button" class="line-rm">' + TRASH + ' Retirer</button></div></li>';
  }

  function render() {
    var list = STORE.items();
    listEl.innerHTML = list.map(lineHTML).join('');

    var sub = 0, fee = 0, save = 0, pl = null;
    list.forEach(function (e) {
      var it = CAT[e.id];
      if (!it) return;
      sub += it.price;
      if (it.kind === 'parcours') {
        save += it.retail - it.price;
        pl = planOf(it, e);
        if (pl) fee += pl.total - it.price;
      }
    });
    var promo = promoOn ? Math.round(sub * PROMO_PCT / 100) : 0;
    var total = sub + fee - promo;
    var n = list.length;

    countEl.textContent = n + (n > 1 ? ' articles' : ' article');
    document.getElementById('sumCountLabel').textContent =
      'Sous-total (' + n + (n > 1 ? ' articles)' : ' article)');
    document.getElementById('sumSub').textContent = fr(sub) + ' ' + CUR;
    document.getElementById('sumSave').textContent = '− ' + fr(save) + ' ' + CUR;
    document.getElementById('sumSaveRow').hidden = save === 0;
    document.getElementById('sumPromo').textContent = '− ' + fr(promo) + ' ' + CUR;
    document.getElementById('sumPromoRow').hidden = !promoOn;
    document.getElementById('sumFee').textContent = fee ? '+ ' + fr(fee) + ' ' + CUR : '—';
    document.getElementById('sumFeeRow').hidden = fee === 0;
    document.getElementById('sumFeeLabel').textContent =
      pl && pl.n > 1 ? 'Frais de fractionnement (' + pl.n + '×)' : 'Frais de fractionnement';
    document.getElementById('sumTotal').innerHTML = fr(total) + '<i>' + CUR + '</i>';
    document.getElementById('sumPlan').textContent =
      !pl || pl.n === 1 ? 'Réglé en une fois'
                        : pl.n + ' versements de ' + fr(total / pl.n) + ' ' + CUR;
    document.getElementById('sumCta').setAttribute('aria-disabled', n === 0 ? 'true' : 'false');
    emptyEl.classList.toggle('is-on', n === 0);
    listEl.hidden = n === 0;
    footEl.hidden = n === 0;
    STORE.badge(list);
  }

  listEl.addEventListener('click', function (e) {
    var btn = e.target.closest('.line-rm');
    if (!btn) return;
    var li = btn.closest('.line'), id = li.dataset.id;
    var entry = null;
    STORE.items().forEach(function (x) { if (x.id === id) entry = x; });
    li.style.maxHeight = li.offsetHeight + 'px';
    requestAnimationFrame(function () { li.classList.add('is-going'); });
    setTimeout(function () { STORE.remove(id); render(); }, 320);
    undoItem = entry;
    toastTx.textContent = 'Article retiré du panier';
    toast.classList.add('is-on');
    clearTimeout(undoTimer);
    undoTimer = setTimeout(function () {
      toast.classList.remove('is-on'); undoItem = null;
    }, 6000);
  });

  document.getElementById('toastUndo').addEventListener('click', function () {
    clearTimeout(undoTimer);
    toast.classList.remove('is-on');
    if (undoItem) {
      var list = STORE.items(); list.push(undoItem); STORE.write(list);
      undoItem = null; render();
    }
  });

  listEl.addEventListener('change', function (e) {
    if (e.target.type !== 'radio') return;
    var li = e.target.closest('.line');
    STORE.setPlan(li.dataset.id, +e.target.value);
    render();
  });

  var input = document.getElementById('promoInput');
  var msg = document.getElementById('promoMsg');
  var tag = document.getElementById('promoTag');
  function applyPromo() {
    var v = input.value.trim().toUpperCase();
    if (!v) return;
    if (promoOn) { msg.textContent = 'Un code est déjà appliqué.'; return; }
    if (v === PROMO_CODE) {
      promoOn = true; input.value = '';
      msg.textContent = '−' + PROMO_PCT + ' % appliqués au sous-total.';
      msg.classList.remove('is-bad');
      tag.classList.add('is-on');
    } else {
      msg.textContent = "Ce code n'est pas reconnu.";
      msg.classList.add('is-bad');
    }
    render();
  }
  document.getElementById('promoBtn').addEventListener('click', applyPromo);
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') applyPromo(); });
  document.getElementById('promoRm').addEventListener('click', function () {
    promoOn = false; tag.classList.remove('is-on');
    msg.textContent = 'Un seul code par commande.';
    msg.classList.remove('is-bad');
    render();
  });

  render();
})();

/* the account menu: click to open, click outside or Escape to close */
(function () {
  var box = document.getElementById('aaAcct');
  if (!box) return;
  var btn = document.getElementById('aaAcctBtn');
  var menu = document.getElementById('aaAcctMenu');
  function open(on) {
    box.classList.toggle('is-open', on);
    btn.setAttribute('aria-expanded', on ? 'true' : 'false');
    if (on) { menu.hidden = false; }
    else { setTimeout(function () { if (!box.classList.contains('is-open')) menu.hidden = true; }, 260); }
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); open(!box.classList.contains('is-open')); });
  document.addEventListener('click', function (e) { if (!box.contains(e.target)) open(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') open(false); });
})();
</script>
""".replace('PARCOURS_SLUG', "'" + P['slug'] + "'") \
   .replace('PARCOURS_RECO', str(P['recommended'])) \
   .replace('TRASH', json.dumps(I_TRASH))



NF_LINKS = [
    ('Cours', 'Les huit cours du catalogue, à l\'unité.', 'index.html#catalogue'),
    ('Parcours', 'Le métier entier, en une seule inscription.', 'parcours.html'),
    ('Qualifications AAOIFI', 'CPSS, CIPA, CSAA et les autres titres.', 'index.html#aaoifi'),
    ('Blog', 'Analyses et notes de marché.', 'blog.html'),
]


def build_404():
    links = "\n".join(
        '    <a href="%s"><b>%s</b><span>%s</span></a>' % (h, esc(t), esc(d))
        for t, d, h in NF_LINKS)
    body = """<div class="wrap">
  <div class="nf">
    <p class="nf-num">404</p>
    <div>
      <h1>Cette page <b>n'existe pas</b></h1>
      <p>Le lien est peut-être ancien, ou l'adresse comporte une faute. Le catalogue, les
        parcours et le blog, eux, sont bien là.</p>
      <div class="nf-cta">
        <a href="index.html">Retour à l'accueil %(arrow)s</a>
        <a href="index.html#catalogue">Voir le catalogue</a>
      </div>
    </div>
  </div>

  <div class="nf-links">
%(links)s
  </div>

  <div class="nf-tail"></div>
  <hr class="rule">
</div>

<script>
/* the account menu, same handler as the cart page */
(function () {
  var box = document.getElementById('aaAcct');
  if (!box) return;
  var btn = document.getElementById('aaAcctBtn');
  var menu = document.getElementById('aaAcctMenu');
  function open(on) {
    box.classList.toggle('is-open', on);
    btn.setAttribute('aria-expanded', on ? 'true' : 'false');
    if (on) { menu.hidden = false; }
    else { setTimeout(function () { if (!box.classList.contains('is-open')) menu.hidden = true; }, 260); }
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); open(!box.classList.contains('is-open')); });
  document.addEventListener('click', function (e) { if (!box.contains(e.target)) open(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') open(false); });
})();
</script>
""" % dict(arrow=I_ARROW, links=links)
    out = page('Page introuvable — Alal Academy',
               "La page demandée n'existe pas. Retrouvez le catalogue, les parcours et le blog.",
               body)
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(out)
    print('404.html')


def build():
    build_cart()
    build_404()


if __name__ == '__main__':
    build()
