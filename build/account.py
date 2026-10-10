# -*- coding: utf-8 -*-
"""The signed-in account area: five pages behind one side menu.

Tableau de bord, Mes cours, Mes certificats, Mes commandes, Paramètres. They
share the signed-in header already used by the cart, a sticky side menu that
marks the page you are on, and one page title block, so moving between them
feels like staying in the same room rather than arriving somewhere new.

The state rendered here is the design-phase fiction a signed-in Cherif would
see: the CIB parcours bought in three instalments, one course finished, two
under way. Everything reads from COURSES and PARCOURS, so the pages stay true
to the real catalogue.
"""
import os, sys, html, re
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, FOOTER, MONO, ROOT
from courses import COURSES
from parcours_data import PARCOURS
from cartkit import cart_js
from shop import (AUTH_HEADER, AUTH_MNAV, AUTH_CSS, ACCT_JS, USER, esc, fr, ico,
                  I_ARROW, CHECK)
from svc_icons import TICK_CIRCLE, MEDAL, TEACHER, sized
import modals as MOD

BY = {c['slug']: c for c in COURSES}
P = PARCOURS[0]

# ── what this account owns and how far it has got ────────────────────────
PROGRESS = [
    ('fondamentaux-finance-islamique', 100),
    ('islamic-retail-banking', 42),
    ('comptabilite-audit-islamique', 15),
    ('contrats-islamiques-structuration', 0),
    ('islamic-corporate-banking', 0),
    ('gestion-des-risques-compliance', 0),
    ('islamic-treasury-liquidite', 0),
    ('digital-islamic-banking', 0),
]
# the course the dashboard offers to resume; which lesson that is comes out of
# PROGRESS below rather than being written down twice
RESUME_SLUG = 'islamic-retail-banking'

CERTS = [
    dict(kind='cours', slug='fondamentaux-finance-islamique', state='delivre',
         date='12 mars 2026', ref='AA-FFI-2026-0184'),
]
ORDERS = [
    dict(ref='CMD-2026-0412', date='18 juin 2026', state='en-cours',
         items=[('parcours', P['slug'])], plan=3, per=146667, total=440000, paid=1,
         next_due='18 septembre 2026', method='Wave'),
    dict(ref='CMD-2026-0103', date='14 janvier 2026', state='payee',
         items=[('cours', 'fondamentaux-finance-islamique')], plan=1, per=69000,
         total=69000, paid=1, next_due=None, method='Carte bancaire'),
]


def lessons_of(c):
    """Every lesson of a course, flat. Predika publishes module counts and
    running times but not lesson titles, so a lesson is its number inside its
    module and a share of the module's time — the last one carrying whatever
    the division leaves over."""
    out = []
    for mi, m in enumerate(c['modules']):
        n = m[1]
        h = re.search(r'(\d+)\s*h', m[2])
        mn = re.search(r'(\d+)\s*min', m[2])
        total = (int(h.group(1)) * 60 if h else 0) + (int(mn.group(1)) if mn else 0)
        for li in range(n):
            share = total // n if li < n - 1 else total - (total // n) * (n - 1)
            out.append(dict(mi=mi, li=li, mins=share))
    return out


def current(c):
    """(every lesson, how many are done, which one is next) for one course.
    One computation, so the dashboard, the card and the player all agree."""
    flat = lessons_of(c)
    if not flat:
        return None
    done = int(round(len(flat) * dict(PROGRESS).get(c['slug'], 0) / 100.0))
    return flat, done, min(done, len(flat) - 1)


def minutes(c):
    t = 0
    for m in c['modules']:
        d = m[2]
        h = re.search(r'(\d+)\s*h', d)
        mi = re.search(r'(\d+)\s*min', d)
        t += (int(h.group(1)) * 60 if h else 0) + (int(mi.group(1)) if mi else 0)
    return t


def hm(t):
    return '%d h %02d' % (t // 60, t % 60)


# ── icons ─────────────────────────────────────────────────────────────────
I_GRID = ico('<rect x="3.5" y="3.5" width="7" height="7" rx="2"/>'
             '<rect x="13.5" y="3.5" width="7" height="7" rx="2"/>'
             '<rect x="3.5" y="13.5" width="7" height="7" rx="2"/>'
             '<rect x="13.5" y="13.5" width="7" height="7" rx="2"/>', 17)
I_PLAY = ico('<rect x="3" y="4.5" width="18" height="15" rx="3"/><path d="m10 9.5 5 2.5-5 2.5V9.5Z"/>', 17)
I_SEAL = sized(MEDAL, 17)      # the library's medal, as on the home page
I_OK = sized(TICK_CIRCLE, 17)       # the library's tick-circle — our mark for "done"
I_PARC = sized(TEACHER, 18)    # the library's graduation cap — a parcours
I_DOC = ico('<path d="M6 3.5h7.5L19 9v11.5H6z"/><path d="M13.5 3.5V9H19"/>'
            '<path d="M9 13h7M9 16.5h5"/>', 17)
I_GEAR = ico('<circle cx="12" cy="12" r="3.2"/><path d="M19.4 14.5a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1v.3a2 2 0 1 1-4 0v-.2a1.6 1.6 0 0 0-2.8-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0-1.1-2.7h-.3a2 2 0 1 1 0-4h.2a1.6 1.6 0 0 0 1.1-2.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 2.7-1.1V3a2 2 0 1 1 4 0v.2a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7h.3a2 2 0 1 1 0 4h-.2a1.6 1.6 0 0 0-1.4 1Z"/>', 17)
I_DL = ico('<path d="M12 4v11m0 0 4-4m-4 4-4-4"/><path d="M4.5 18.5h15"/>', 16)
I_CLOCK = ico('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 1.8"/>', 16)
I_LOCK = ico('<rect x="4.5" y="10" width="15" height="10.5" rx="2.5"/>'
             '<path d="M8 10V7.5a4 4 0 0 1 8 0V10"/>', 16)

NAV = [
    ('compte', 'Tableau de bord', 'compte.html', I_GRID),
    ('cours', 'Mes cours', 'mes-cours.html', I_PLAY),
    ('certs', 'Mes certificats', 'mes-certificats.html', I_SEAL),
    ('orders', 'Mes commandes', 'mes-commandes.html', I_DOC),
    ('settings', 'Paramètres', 'parametres.html', I_GEAR),
]


ACC_CSS = """
  [hidden]{display:none !important}
  .rule{border:0;border-top:1px solid rgba(31,31,31,.09);margin:0}

  /* ── the account shell ────────────────────────────────────────────────
     One title block, a sticky side menu on the left, the page's own work on
     the right. The menu is the only thing that changes between the five
     pages, so moving between them reads as staying put. */
  .acc-head{padding:46px 0 0}
  .acc-kicker{font-family:__MONO__;font-size:10.5px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a}
  .acc-head h1{margin:14px 0 0;font-size:clamp(36px,4.6vw,60px);line-height:1.06;
    letter-spacing:-0.04em;font-weight:300}
  .acc-head .lede{margin:14px 0 0;max-width:62ch;font-size:16px;line-height:1.65;color:#7a7a7a}

  .acc-layout{display:grid;grid-template-columns:248px minmax(0,1fr);gap:56px;
    padding:44px 0 110px;align-items:start}
  /* grid items default to min-width:auto, which lets one long word in a card
     push the whole column wider than the page on a phone */
  .acc-layout > div{min-width:0}
  .acc-side{position:sticky;top:104px;display:flex;flex-direction:column;gap:2px}
  .acc-side a{display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:12px;
    font-size:15px;color:#7a7a7a;transition:background .2s ease,color .2s ease}
  .acc-side a svg{color:#A7A7A7;flex:none;transition:color .2s ease}
  .acc-side a:hover{background:#FCFBF8;color:#1F1F1F}
  .acc-side a:hover svg{color:#7a7a7a}
  .acc-side a.is-on{background:#1F1F1F;color:#FFFFFF}
  .acc-side a.is-on svg{color:#FFFFFF}
  .acc-side .acc-side-out{margin-top:10px;padding-top:12px;
    border-top:1px solid rgba(31,31,31,.09);border-radius:0}

  .acc-sec{margin:0 0 81px}
  .acc-sec:last-child{margin-bottom:0}
  .acc-sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;
    padding-bottom:16px;border-bottom:1px solid rgba(31,31,31,.12)}
  .acc-sec-head h2{margin:0;font-size:22px;font-weight:500;letter-spacing:-0.024em}
  .acc-sec-head a{font-size:14px;color:#7a7a7a;text-decoration:underline;
    text-underline-offset:3px;white-space:nowrap}
  .acc-sec-head a:hover{color:#1F1F1F}

  /* ── resume card ──────────────────────────────────────────────────────
     The one thing somebody signing in actually came for: the lesson they
     stopped on, one click away. */
  .acc-resume{display:grid;grid-template-columns:320px minmax(0,1fr);gap:34px;
    margin-top:26px;padding:26px;border-radius:20px;background:#EAEAEA;align-items:center}
  .acc-resume img{display:block;width:100%;aspect-ratio:16/9;border-radius:14px;
    object-fit:contain;background:#FFFFFF}
  .acc-resume .mod{display:flex;align-items:center;gap:9px;font-family:__MONO__;
    font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#7a7a7a}
  .acc-resume h3 svg{vertical-align:-3px;margin-right:8px;color:#7a7a7a}
  .tag svg,.ccard .state svg,.sched li svg{flex:none}
  .acc-resume h3{margin:12px 0 0;font-size:27px;font-weight:500;letter-spacing:-0.028em;
    line-height:1.24}
  .acc-resume p{margin:10px 0 0;font-size:15px;color:#7a7a7a}
  .acc-resume .btn-row{margin-top:24px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}

  .btn-dark2{display:inline-flex;align-items:center;gap:10px;height:54px;padding:0 26px;
    border:0;border-radius:12px;background:#1F1F1F;color:#FFFFFF;font:inherit;font-size:15.5px;
    font-weight:500;cursor:pointer;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .btn-dark2:hover{box-shadow:0 2px 6px rgba(0,0,0,.3),0 7px 16px rgba(0,0,0,.26),
    0 17px 33px rgba(0,0,0,.22)}
  .btn-white{display:inline-flex;align-items:center;gap:9px;height:46px;padding:0 20px;
    border:1px solid rgba(31,31,31,.16);border-radius:11px;background:#FFFFFF;color:#1F1F1F;
    font:inherit;font-size:14.5px;cursor:pointer;
    transition:border-color .25s ease,box-shadow .3s ease}
  .btn-white:hover{border-color:rgba(31,31,31,.34);box-shadow:0 2px 5px rgba(0,0,0,.07)}

  /* ── progress ─────────────────────────────────────────────────────────
     One bar, one grammar: a hairline track with an ink fill, and the figure
     spelled out beside it rather than inside it. */
  .bar{height:4px;border-radius:999px;background:rgba(31,31,31,.12);overflow:hidden}
  .bar i{display:block;height:100%;border-radius:999px;background:#1F1F1F}
  .bar.is-done i{background:#0E695C}
  .prog-line{display:flex;align-items:center;gap:14px;margin-top:14px}
  .prog-line .bar{flex:1}
  .prog-line b{font-size:13px;font-weight:500;color:#7a7a7a;white-space:nowrap}

  /* ── figures table ────────────────────────────────────────────────────
     A closed table rather than the home page's open stat row: four cells
     inside one ruled box, so the account's numbers read as a record of a
     state rather than as a marketing band. */
  .figs{display:grid;grid-template-columns:repeat(4,1fr);margin-top:26px;
    border:1px solid rgba(31,31,31,.14);border-radius:16px;overflow:hidden}
  .figs > div{padding:24px 26px 26px}
  .figs > div + div{border-left:1px solid rgba(31,31,31,.12)}
  .figs b{display:block;font-size:40px;font-weight:300;letter-spacing:-0.04em;line-height:1}
  .figs span{display:block;margin-top:10px;font-size:13.5px;color:#7a7a7a}

  /* ── course cards ─────────────────────────────────────────────────────── */
  .ccards{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,340px));gap:28px;
    margin-top:26px;justify-content:start}
  .ccard{display:flex;min-width:0;flex-direction:column;border:1px solid rgba(31,31,31,.1);
    border-radius:18px;overflow:hidden;background:#FFFFFF;
    transition:border-color .25s ease,box-shadow .35s ease}
  .ccard:hover{border-color:rgba(31,31,31,.22);box-shadow:0 3px 8px rgba(0,0,0,.05),
    0 16px 34px rgba(0,0,0,.08)}
  .ccard-img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:#EAEAEA}
  .ccard-body{padding:20px 22px 24px;display:flex;flex-direction:column;flex:1}
  .ccard .cat{font-family:__MONO__;font-size:9.5px;letter-spacing:.12em;
    text-transform:uppercase;color:#7a7a7a}
  .ccard h3{margin:10px 0 0;font-size:18px;font-weight:500;letter-spacing:-0.02em;line-height:1.34}
  .ccard .meta{margin:8px 0 0;font-size:13px;color:#A7A7A7}
  /* the state line and the link each take their own row, whichever of the
     three states the card is in */
  .ccard .foot{margin-top:auto;padding-top:20px;display:flex;flex-direction:column;
    align-items:flex-start;gap:14px}
  .ccard .foot > *{margin-top:0}
  .ccard .foot .prog-line{align-self:stretch;margin-top:0}
  .ccard .state{display:inline-flex;align-items:center;gap:7px;font-size:13px;color:#0E695C}
  .ccard a.go{display:inline-flex;align-items:center;gap:8px;font-size:14.5px;
    color:#1F1F1F;text-decoration:underline;text-underline-offset:4px}

  /* the filter strip keeps to one line and scrolls sideways on a phone,
     the same behaviour as the catalogue's */
  .fstrip{display:flex;gap:10px;margin-top:26px;overflow-x:auto;padding-bottom:4px;
    scrollbar-width:none}
  .fstrip::-webkit-scrollbar{display:none}
  .fstrip button{flex:none;height:40px;padding:0 18px;border-radius:999px;cursor:pointer;
    border:1px solid rgba(31,31,31,.14);background:#FFFFFF;color:#7a7a7a;font:inherit;
    font-size:14px;white-space:nowrap;transition:background .2s ease,color .2s ease,
    border-color .2s ease}
  .fstrip button:hover{border-color:rgba(31,31,31,.3);color:#1F1F1F}
  .fstrip button.is-on{background:#1F1F1F;border-color:#1F1F1F;color:#FFFFFF}
  .acc-empty{margin:30px 0 0;padding:34px;border:1px dashed rgba(31,31,31,.18);
    border-radius:16px;font-size:15px;color:#7a7a7a}

  /* ── certificates ─────────────────────────────────────────────────────── */
  .cert{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:30px;align-items:center;
    padding:28px 0;border-bottom:1px solid rgba(31,31,31,.12)}
  .cert:first-of-type{border-top:1px solid rgba(31,31,31,.12)}
  .cert h3{margin:10px 0 0;font-size:21px;font-weight:500;letter-spacing:-0.022em}
  .cert .ref{margin:10px 0 0;font-family:__MONO__;font-size:11.5px;letter-spacing:.06em;
    color:#7a7a7a}
  .cert .pend{margin:10px 0 0;font-size:14.5px;color:#7a7a7a}
  .cert-acts{display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:flex-end}
  .tag{display:inline-flex;align-items:center;gap:7px;height:26px;padding:0 11px;
    border-radius:999px;font-family:__MONO__;font-size:9.5px;letter-spacing:.1em;
    text-transform:uppercase}
  .tag-on{background:rgba(14,105,92,.1);color:#0E695C}
  .tag-off{background:rgba(31,31,31,.07);color:#7a7a7a}

  /* ── orders ───────────────────────────────────────────────────────────── */
  .order{margin-top:26px;border:1px solid rgba(31,31,31,.12);border-radius:18px;overflow:hidden}
  .order-top{display:flex;align-items:center;justify-content:space-between;gap:24px;
    flex-wrap:wrap;padding:20px 26px;background:#FCFBF8;
    border-bottom:1px solid rgba(31,31,31,.1)}
  .order-top .ref{font-family:__MONO__;font-size:11.5px;letter-spacing:.08em;color:#7a7a7a}
  .order-top .ref b{color:#1F1F1F;font-weight:500}
  .order-line{display:grid;grid-template-columns:132px minmax(0,1fr) auto;gap:22px;
    align-items:center;padding:22px 26px}
  .order-line + .order-line{border-top:1px solid rgba(31,31,31,.09)}
  .order-line img{display:block;width:132px;aspect-ratio:16/9;border-radius:10px;
    object-fit:contain;background:#EAEAEA}
  .order-line img.is-photo{object-fit:cover}
  .order-line h3{margin:0;font-size:17.5px;font-weight:500;letter-spacing:-0.02em}
  .order-line p{margin:7px 0 0;font-size:13.5px;color:#7a7a7a}
  .order-line .amt{font-size:17px;font-weight:500;white-space:nowrap}
  .order-foot{padding:20px 26px;border-top:1px solid rgba(31,31,31,.09);
    display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
  .sched{list-style:none;margin:0;padding:0;font-size:14px}
  .sched li{display:flex;align-items:center;gap:10px;padding:5px 0;color:#7a7a7a}
  .sched li b{font-weight:500;color:#1F1F1F}
  .sched li.is-paid{color:#0E695C}

  /* ── settings ─────────────────────────────────────────────────────────
     The forms are Poppins throughout, like the account dialogs, so every
     field on the site belongs to the same family. */
  .set{max-width:720px}
  .set-card{margin-top:26px;padding:30px 32px 34px;border:1px solid rgba(31,31,31,.12);
    border-radius:18px;font-family:__POPPINS__}
  .set-card h2{margin:0;font-family:__POPPINS__;font-size:19px;font-weight:500;
    letter-spacing:-0.02em}
  .set-card .note{margin:9px 0 0;font-size:13.5px;line-height:1.6;color:#7a7a7a}
  .set-row{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  .fld{margin-top:22px}
  .fld label{display:block;font-size:11px;font-weight:500;letter-spacing:.1em;
    text-transform:uppercase;color:#7a7a7a}
  .fld input,.fld select{width:100%;height:46px;border:0;
    border-bottom:1px solid rgba(31,31,31,.14);border-radius:0;background:transparent;
    font-family:__POPPINS__;font-size:15px;color:#1F1F1F}
  .fld select{appearance:none;cursor:pointer}
  .fld input:focus,.fld select:focus{outline:none;border-bottom-color:#1F1F1F}
  .set-save{margin-top:26px;height:50px;padding:0 24px;border:0;border-radius:11px;
    background:#1F1F1F;color:#FFFFFF;font-family:__POPPINS__;font-size:15px;font-weight:500;
    cursor:pointer}
  .opt{display:flex;align-items:flex-start;gap:12px;padding:16px 0;
    border-bottom:1px solid rgba(31,31,31,.09)}
  .opt:last-child{border-bottom:0;padding-bottom:0}
  .opt input{width:17px;height:17px;flex:none;margin-top:3px;accent-color:#1F1F1F}
  .opt b{display:block;font-size:15px;font-weight:500}
  .opt i{display:block;font-style:normal;margin-top:4px;font-size:13.5px;line-height:1.55;
    color:#7a7a7a}
  .danger{border-color:rgba(176,52,42,.3)}
  .danger h2{color:#B0342A}
  .set-del{margin-top:24px;height:46px;padding:0 20px;border:1px solid rgba(176,52,42,.4);
    border-radius:11px;background:#FFFFFF;color:#B0342A;font-family:__POPPINS__;font-size:14.5px;
    cursor:pointer;transition:background .2s ease,color .2s ease}
  .set-del:hover{background:#B0342A;color:#FFFFFF}

  @media (max-width:1100px){
    .acc-layout{grid-template-columns:1fr;gap:34px}
    /* the side menu lies down and scrolls sideways once there is no column
       to keep it in */
    .acc-side{position:static;flex-direction:row;gap:8px;overflow-x:auto;min-width:0;
      max-width:100%;padding-bottom:4px;scrollbar-width:none}
    .acc-side::-webkit-scrollbar{display:none}
    .acc-side a{flex:none;white-space:nowrap}
    .acc-side .acc-side-out{margin-top:0;padding-top:11px;border-top:0}
    .figs{grid-template-columns:repeat(2,1fr)}
    .figs > div:nth-child(3),.figs > div:nth-child(4){
      border-top:1px solid rgba(31,31,31,.12)}
    .figs > div:nth-child(odd){border-left:0}
  }
  @media (max-width:820px){
    .acc-resume{grid-template-columns:1fr;gap:22px;padding:20px}
    .cert{grid-template-columns:1fr;gap:18px}
    .cert-acts{justify-content:flex-start}
    .order-line{grid-template-columns:96px minmax(0,1fr);row-gap:14px}
    .order-line img{width:96px}
    .order-line .amt{grid-column:2}
    .set-row{grid-template-columns:1fr;gap:0}
  }
  @media (max-width:560px){
    .ccards{grid-template-columns:1fr}
    .figs{grid-template-columns:1fr}
    .figs > div + div{border-left:0;border-top:1px solid rgba(31,31,31,.12)}
    .acc-layout{padding-bottom:72px}
  }
""".replace('__MONO__', MONO).replace('__POPPINS__', MOD.POPPINS)


def side(active):
    rows = []
    for key, label, href, icon in NAV:
        rows.append('      <a href="%s"%s>%s%s</a>'
                    % (href, ' class="is-on"' if key == active else '', icon, esc(label)))
    rows.append('      <a href="index.html" class="acc-side-out">Déconnexion</a>')
    return '    <nav class="acc-side" aria-label="Mon espace">\n' + "\n".join(rows) + '\n    </nav>'


def page(title, desc, kicker, h1, lede, active, main, css=''):
    head = """  <div class="acc-head">
    <span class="acc-kicker">%s</span>
    <h1>%s</h1>
%s  </div>""" % (esc(kicker), esc(h1),
                 '    <p class="lede">%s</p>\n' % esc(lede) if lede else '')
    body = ('<div class="wrap">\n' + head + '\n  <div class="acc-layout">\n'
            + side(active) + '\n    <div>\n' + main + '\n    </div>\n  </div>\n'
            '  <hr class="rule">\n</div>')
    return __import__('loader').inject("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap" rel="stylesheet">
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
""" % (html.escape(title), html.escape(desc), BASE, AUTH_CSS, ACC_CSS, css,
       AUTH_HEADER + AUTH_MNAV, cart_js(''), body,
       FOOTER.replace('{ROOT}', '') + ACCT_JS + MOD.modals('') + MOD.MODAL_JS))


def watch(slug):
    """Where a course is watched. Contrats Islamiques has no published
    programme, so it has no player yet and keeps pointing at its own page."""
    return ('apprendre/%s.html' % slug) if BY[slug]['modules'] else ('cours/%s.html' % slug)


def programme(slug):
    """The course page in its enrolled state, where there is one."""
    return ('cours/%s-inscrit.html' % slug) if BY[slug]['modules'] else ('cours/%s.html' % slug)


def bar(pct, extra=''):
    return ('<div class="bar%s"><i style="width:%d%%"></i></div>'
            % (' is-done' if pct == 100 else '', pct) + extra)


def course_card(slug, pct):
    c = BY[slug]
    if pct == 100:
        state = '<span class="state">%s Terminé</span>' % I_OK
        go = 'Revoir le cours'
    elif pct:
        state = ('<div class="prog-line"><div class="bar"><i style="width:%d%%"></i></div>'
                 '<b>%d %%</b></div>' % (pct, pct))
        go = 'Reprendre'
    else:
        state = '<span class="meta" style="color:#A7A7A7">Pas encore commencé</span>'
        go = 'Commencer'
    # Contrats Islamiques has no published programme yet, so it carries neither
    # a lesson count nor a running time — the line then says so instead
    meta = ('%d leçons &middot; %s' % (c['lessons'], hm(minutes(c))) if c['lessons']
            else 'Programme à venir')
    return """      <article class="ccard">
        <img class="ccard-img" src="%(img)s" alt="" loading="lazy" width="340" height="191">
        <div class="ccard-body">
          <span class="cat">%(cat)s</span>
          <h3>%(title)s</h3>
          <p class="meta">%(meta)s</p>
          <div class="foot">%(state)s
            <a class="go" href="%(href)s">%(go)s %(arrow)s</a>
          </div>
        </div>
      </article>""" % dict(img=c['image'], cat=esc(c['level']), title=esc(c['title']),
                           meta=meta, state=state, href=watch(slug),
                           slug=slug, go=go, arrow=I_ARROW)


# ─────────────────────────── 1. tableau de bord ───────────────────────────
def build_dash():
    done = sum(1 for _, p in PROGRESS if p == 100)
    mins = sum(minutes(BY[s]) * p / 100.0 for s, p in PROGRESS)
    total = sum(minutes(BY[s]) for s, _ in PROGRESS)
    overall = int(round(sum(minutes(BY[s]) * p for s, p in PROGRESS) / float(total)))
    r = BY[RESUME_SLUG]
    rflat, rdone, rcur = current(r)
    rl = rflat[rcur]

    figs = [(str(done) + ' / ' + str(len(PROGRESS)), 'Cours terminés'),
            (hm(int(mins)), 'Temps de visionnage'),
            (str(overall) + ' %', 'Avancement du parcours'),
            (str(len(CERTS)), 'Certificat obtenu')]

    cards = "\n".join(course_card(s, p) for s, p in PROGRESS if 0 < p < 100)

    main = """      <section class="acc-sec">
        <div class="acc-sec-head"><h2>Reprendre où vous en étiez</h2>
          <a href="mes-cours.html">Tous mes cours</a></div>
        <div class="acc-resume">
          <img src="%(img)s" alt="" width="320" height="180">
          <div>
            <span class="mod">Module %(mod)d &middot; Leçon %(les)d</span>
            <h3>%(mtitle)s</h3>
            <p>%(ctitle)s</p>
            <div class="prog-line"><div class="bar"><i style="width:%(pct)d%%"></i></div>
              <b>%(pct)d %% du cours</b></div>
            <div class="btn-row">
              <a class="btn-dark2" href="%(watch)s">Reprendre la leçon %(arrow)s</a>
              <a class="btn-white" href="%(prog)s">Voir le programme</a>
            </div>
          </div>
        </div>
      </section>

      <section class="acc-sec">
        <div class="acc-sec-head"><h2>Votre parcours en chiffres</h2></div>
        <div class="figs">
%(figs)s
        </div>
      </section>

      <section class="acc-sec">
        <div class="acc-sec-head"><h2>%(ptitle)s</h2>
          <a href="parcours/%(pslug)s.html">Voir le parcours</a></div>
        <div class="acc-resume">
          <img src="%(pimg)s" alt="" width="320" height="180" style="object-fit:cover">
          <div>
            <span class="mod">%(cap)s Parcours certifiant &middot; %(pn)d cours</span>
            <h3>%(done)d cours terminé%(s)s sur %(pn)d</h3>
            <p>Le certificat se débloque une fois les huit cours validés.</p>
            <div class="prog-line"><div class="bar"><i style="width:%(overall)d%%"></i></div>
              <b>%(overall)d %%</b></div>
          </div>
        </div>
      </section>

      <section class="acc-sec">
        <div class="acc-sec-head"><h2>En cours</h2>
          <a href="mes-cours.html">Tous mes cours</a></div>
        <div class="ccards">
%(cards)s
        </div>
      </section>""" % dict(
        img=r['image'], mod=rl['mi'] + 1, les=rl['li'] + 1,
        mtitle=esc(r['modules'][rl['mi']][0]), ctitle=esc(r['title']), slug=RESUME_SLUG,
        pct=dict(PROGRESS)[RESUME_SLUG], arrow=I_ARROW, watch=watch(RESUME_SLUG), prog=programme(RESUME_SLUG),
        figs="\n".join('          <div><b>%s</b><span>%s</span></div>' % (esc(n), esc(l))
                       for n, l in figs),
        ptitle=esc(P['title']), pslug=P['slug'], pimg=P['image'], pn=len(PROGRESS),
        cap=I_PARC,
        done=done, s='s' if done > 1 else '', overall=overall, cards=cards)

    open(os.path.join(ROOT, 'compte.html'), 'w', encoding='utf-8').write(
        page('Tableau de bord — Alal Academy',
             "Votre espace Alal Academy : vos cours en cours, votre avancement et vos certificats.",
             'Mon espace', 'Bonjour %s.' % USER['first'],
             "Vous avez %d cours en cours et %d %% du parcours Certified Islamic Banker derrière vous."
             % (sum(1 for _, p in PROGRESS if 0 < p < 100), overall),
             'compte', main))
    print('compte.html')


# ─────────────────────────────── 2. mes cours ─────────────────────────────
FILTERS = [('tous', 'Tous'), ('encours', 'En cours'), ('fini', 'Terminés'),
           ('neuf', 'Pas commencés')]


def state_key(pct):
    return 'fini' if pct == 100 else ('encours' if pct else 'neuf')


def build_courses():
    cards = []
    for s, p in PROGRESS:
        cards.append(course_card(s, p).replace('<article class="ccard">',
                                               '<article class="ccard" data-state="%s">' % state_key(p)))
    strip = "\n".join('        <button type="button" data-f="%s"%s>%s</button>'
                      % (k, ' class="is-on"' if k == 'tous' else '', esc(l))
                      for k, l in FILTERS)
    main = """      <div class="fstrip" id="accFilter">
%(strip)s
      </div>
      <div class="ccards" id="accCards">
%(cards)s
      </div>
      <p class="acc-empty" id="accNone" hidden>Aucun cours dans cet état pour le moment.</p>

<script>
/* The filter hides cards rather than rebuilding the grid, so the images keep
   their place in the cache and nothing flashes on the way through. */
(function () {
  var strip = document.getElementById('accFilter');
  var cards = [].slice.call(document.querySelectorAll('#accCards .ccard'));
  var none = document.getElementById('accNone');
  strip.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-f]'); if (!b) return;
    [].forEach.call(strip.children, function (x) { x.classList.toggle('is-on', x === b); });
    var f = b.getAttribute('data-f'), shown = 0;
    cards.forEach(function (c) {
      var on = f === 'tous' || c.getAttribute('data-state') === f;
      c.hidden = !on; if (on) shown++;
    });
    none.hidden = shown > 0;
  });
})();
</script>""" % dict(strip=strip, cards="\n".join(cards))

    open(os.path.join(ROOT, 'mes-cours.html'), 'w', encoding='utf-8').write(
        page('Mes cours — Alal Academy',
             "Les cours de votre compte Alal Academy, avec votre avancement sur chacun.",
             'Mon espace', 'Mes cours',
             "Les huit cours du parcours Certified Islamic Banker, et où vous en êtes sur chacun.",
             'cours', main))
    print('mes-cours.html')


# ──────────────────────────── 3. mes certificats ──────────────────────────
def build_certs():
    rows = []
    for c in CERTS:
        s = BY[c['slug']]
        rows.append("""      <div class="cert">
        <div>
          <span class="tag tag-on">%(ok)s Délivré</span>
          <h3>%(title)s</h3>
          <p class="ref">%(ref)s &middot; délivré le %(date)s</p>
        </div>
        <div class="cert-acts">
          <button type="button" class="btn-white">%(dl)s Télécharger le PDF</button>
          <button type="button" class="btn-white">Partager</button>
        </div>
      </div>""" % dict(ok=I_OK, title=esc(s['title']), ref=esc(c['ref']),
                       date=esc(c['date']), dl=I_DL))

    done = sum(1 for _, p in PROGRESS if p == 100)
    rows.append("""      <div class="cert">
        <div>
          <span class="tag tag-off">%(lock)s À venir</span>
          <h3>%(cap)s %(title)s</h3>
          <p class="pend">%(done)d cours validé%(s)s sur %(n)d — le certificat du parcours est
            délivré dès le huitième terminé.</p>
          <div class="prog-line" style="max-width:420px"><div class="bar">
            <i style="width:%(pct)d%%"></i></div><b>%(done)d / %(n)d</b></div>
        </div>
        <div class="cert-acts">
          <a class="btn-white" href="mes-cours.html">Continuer le parcours</a>
        </div>
      </div>""" % dict(lock=I_LOCK, cap=I_PARC, title=esc(P['title']), done=done, n=len(PROGRESS),
                       s='s' if done > 1 else '',
                       pct=int(round(done * 100.0 / len(PROGRESS)))))

    main = """      <section class="acc-sec">
%s
        <p class="acc-empty" style="border-style:solid;border-color:rgba(31,31,31,.1)">
          Chaque certificat porte un identifiant vérifiable. Un employeur peut le contrôler
          sans vous demander le fichier.</p>
      </section>""" % "\n".join(rows)

    open(os.path.join(ROOT, 'mes-certificats.html'), 'w', encoding='utf-8').write(
        page('Mes certificats — Alal Academy',
             "Les certificats délivrés par Alal Academy sur votre compte, et ceux à venir.",
             'Mon espace', 'Mes certificats',
             "Un certificat est délivré à la fin de chaque cours validé, et un autre à la fin du parcours.",
             'certs', main))
    print('mes-certificats.html')


# ──────────────────────────── 4. mes commandes ────────────────────────────
def build_orders():
    blocks = []
    for o in ORDERS:
        lines = []
        for kind, slug in o['items']:
            if kind == 'parcours':
                img, title = P['image'], P['title']
                meta = '%d cours &middot; accès à vie' % len(PROGRESS)
                href, cls = 'parcours/%s.html' % P['slug'], ' class="is-photo"'
            else:
                c = BY[slug]
                img, title = c['image'], c['title']
                meta = '%d leçons &middot; accès à vie' % c['lessons']
                href, cls = 'cours/%s.html' % slug, ''
            lines.append("""        <div class="order-line">
          <img%(cls)s src="%(img)s" alt="" width="132" height="74">
          <div><h3><a href="%(href)s">%(title)s</a></h3><p>%(meta)s</p></div>
          <span class="amt">%(amt)s FCFA</span>
        </div>""" % dict(cls=cls, img=img, href=href, title=esc(title), meta=meta,
                         amt=fr(o['total'])))

        if o['plan'] > 1:
            due = []
            for i in range(o['plan']):
                paid = i < o['paid']
                due.append('            <li class="%s">%s<b>Versement %d / %d</b> — %s FCFA %s</li>'
                           % ('is-paid' if paid else '', I_OK if paid else I_CLOCK,
                              i + 1, o['plan'], fr(o['per']),
                              '· payé' if paid else '· à régler le ' + esc(o['next_due'])
                              if i == o['paid'] else '· à venir'))
            foot = """        <div class="order-foot">
          <ul class="sched">
%s
          </ul>
          <button type="button" class="btn-white">%s Télécharger la facture</button>
        </div>""" % ("\n".join(due), I_DL)
        else:
            foot = """        <div class="order-foot">
          <span style="font-size:14px;color:#7a7a7a">Réglé en une fois &middot; %s</span>
          <button type="button" class="btn-white">%s Télécharger la facture</button>
        </div>""" % (esc(o['method']), I_DL)

        tag = ('<span class="tag tag-on">%s Payée</span>' % I_OK if o['state'] == 'payee'
               else '<span class="tag tag-off">%s Versements en cours</span>' % I_CLOCK)
        blocks.append("""      <div class="order">
        <div class="order-top">
          <span class="ref"><b>%(ref)s</b> &middot; %(date)s &middot; %(plan)s</span>
          %(tag)s
        </div>
%(lines)s
%(foot)s
      </div>""" % dict(ref=esc(o['ref']), date=esc(o['date']), tag=tag,
                       plan='paiement unique' if o['plan'] == 1 else '%d versements' % o['plan'],
                       lines="\n".join(lines), foot=foot))

    main = '      <section class="acc-sec">\n' + "\n\n".join(blocks) + '\n      </section>'
    open(os.path.join(ROOT, 'mes-commandes.html'), 'w', encoding='utf-8').write(
        page('Mes commandes — Alal Academy',
             "L'historique de vos achats Alal Academy, vos versements et vos factures.",
             'Mon espace', 'Mes commandes',
             "Vos achats, l'état de vos versements et les factures correspondantes.",
             'orders', main))
    print('mes-commandes.html')


# ───────────────────────────── 5. paramètres ──────────────────────────────
NOTIFS = [
    ('Nouvelles leçons et mises à jour de cours',
     "Quand un cours que vous suivez reçoit une leçon ou une correction.", True),
    ('Webinaires à venir',
     "Une fois par mois, les sessions en direct programmées.", True),
    ('Rappels de versement',
     "Trois jours avant chaque échéance d'un paiement fractionné.", True),
    ('Nouveautés du catalogue',
     "Les nouveaux cours et parcours publiés par l'académie.", False),
]


def build_settings():
    notifs = "\n".join(
        """          <label class="opt"><input type="checkbox"%s>
            <span><b>%s</b><i>%s</i></span></label>"""
        % (' checked' if on else '', esc(t), esc(d)) for t, d, on in NOTIFS)

    main = """      <div class="set">
        <section class="set-card">
          <h2>Profil</h2>
          <p class="note">Le nom qui apparaît sur vos certificats. Vérifiez-le avant de
            valider votre premier cours.</p>
          <form novalidate>
            <div class="set-row">
              <div class="fld"><label for="pFirst">Prénom</label>
                <input id="pFirst" type="text" value="%(first)s" autocomplete="given-name"></div>
              <div class="fld"><label for="pLast">Nom</label>
                <input id="pLast" type="text" value="%(last)s" autocomplete="family-name"></div>
            </div>
            <div class="fld"><label for="pMail">E-mail</label>
              <input id="pMail" type="email" value="%(mail)s" autocomplete="email"></div>
            <div class="fld"><label for="pTel">Téléphone</label>
              <input id="pTel" type="tel" placeholder="+221 ..." autocomplete="tel"></div>
            <div class="set-row">
              <div class="fld"><label for="pPays">Pays</label>
                <select id="pPays">
                  <option selected>Sénégal</option><option>Côte d'Ivoire</option>
                  <option>Mali</option><option>Burkina Faso</option><option>France</option>
                  <option>Autre</option>
                </select></div>
              <div class="fld"><label for="pLang">Langue</label>
                <select id="pLang"><option selected>Français</option><option>English</option>
                </select></div>
            </div>
            <button type="submit" class="set-save">Enregistrer</button>
          </form>
        </section>

        <section class="set-card">
          <h2>Mot de passe</h2>
          <p class="note">Au moins 8 caractères. Vous resterez connecté sur cet appareil.</p>
          <form novalidate>
            <div class="fld"><label for="pOld">Mot de passe actuel</label>
              <input id="pOld" type="password" autocomplete="current-password"
                placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;"></div>
            <div class="fld"><label for="pNew">Nouveau mot de passe</label>
              <input id="pNew" type="password" autocomplete="new-password"
                placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;"></div>
            <button type="submit" class="set-save">Mettre à jour</button>
          </form>
        </section>

        <section class="set-card">
          <h2>Notifications</h2>
          <p class="note">Ce que nous vous envoyons par e-mail. Les messages liés à une
            commande en cours vous parviennent dans tous les cas.</p>
          <div style="margin-top:18px">
%(notifs)s
          </div>
        </section>

        <section class="set-card danger">
          <h2>Supprimer le compte</h2>
          <p class="note">Vos cours, votre avancement et vos certificats sont effacés
            définitivement. Les factures sont conservées le temps imposé par la loi.</p>
          <button type="button" class="set-del">Supprimer mon compte</button>
        </section>
      </div>""" % dict(first=esc(USER['first']), last=esc(USER['last']),
                       mail=esc(USER['email']), notifs=notifs)

    open(os.path.join(ROOT, 'parametres.html'), 'w', encoding='utf-8').write(
        page('Paramètres — Alal Academy',
             "Votre profil, votre mot de passe et vos notifications Alal Academy.",
             'Mon espace', 'Paramètres',
             "Votre profil, votre mot de passe et ce que nous vous envoyons.",
             'settings', main))
    print('parametres.html')


def build():
    build_dash()
    build_courses()
    build_certs()
    build_orders()
    build_settings()


if __name__ == '__main__':
    build()
