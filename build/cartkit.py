# -*- coding: utf-8 -*-
"""The shared cart: a catalogue the pages can add from, and the script that
keeps it.

The cart lives in localStorage under one key, so it survives navigation and
reloads without a back end. Every page that includes CART_JS gets three things:
the live count on the header's cart icon, any [data-add] control wired to add
its item, and a toast confirming the add with a link to the cart. panier.html
reads the same store and renders its lines from it.

CATALOG is emitted into the page so a line can be rebuilt from its id alone —
title, price, image and link — without a second request.
"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from courses import COURSES
from parcours_data import PARCOURS

P = PARCOURS[0]


def _price(v):
    return int(str(v).replace(' ', '').replace(' ', ''))


def catalog(root=''):
    """root is the prefix a page needs to reach the site root ('' or '../')."""
    cat = {}
    for c in COURSES:
        cat['cours:' + c['slug']] = dict(
            kind='cours', title=c['title'], price=_price(c['price']),
            cur=c['currency'], img=root + c['image'], url=root + 'cours/%s.html' % c['slug'],
            meta=('%d leçons · ' % c['lessons'] if c['lessons'] else '') + c['level'],
            cat=c['category'])
    cat['parcours:' + P['slug']] = dict(
        kind='parcours', title=P['title'], price=P['price'], cur=P['currency'],
        img=root + P['image'], url=root + 'parcours/%s.html' % P['slug'],
        meta='%s · accès à vie · certificat inclus' % P['level'],
        cat='%d cours' % len(P['courses']), retail=P['retail'],
        plans=[dict(n=pl['n'], per=pl['per'], total=pl['total']) for pl in P['plans']],
        reco=P['recommended'])
    return cat


def cart_js(root=''):
    return """
<script>
/* ── Alal Academy cart ─────────────────────────────────────────────────────
   One localStorage key holds the lines: [{id, plan}]. Any control with
   data-add="<id>" (optionally data-plan="<n>") adds its item; the header
   badge and the toast come free on every page that loads this. panier.html
   renders from the same store. */
window.AA_CATALOG = %(cat)s;
window.AA_ROOT = %(root)s;
window.AA_CART = (function () {
  var KEY = 'aa.cart.v1';
  var listeners = [];

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw === null) return null;            /* never used the cart yet */
      var v = JSON.parse(raw);
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }                  /* private mode, blocked storage */
  }
  function write(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
    listeners.forEach(function (f) { f(items); });
    badge(items);
  }
  function items() { return read() || []; }

  function add(id, plan) {
    if (!window.AA_CATALOG[id]) return false;
    var list = items();
    var found = null;
    list.forEach(function (l) { if (l.id === id) found = l; });
    if (found) {                                /* already there — only the plan can change */
      if (plan) found.plan = plan;
      write(list);
      return 'again';
    }
    list.push(plan ? { id: id, plan: plan } : { id: id });
    write(list);
    return 'added';
  }
  function remove(id) {
    write(items().filter(function (l) { return l.id !== id; }));
  }
  function setPlan(id, plan) {
    var list = items();
    list.forEach(function (l) { if (l.id === id) l.plan = plan; });
    write(list);
  }
  function badge(list) {
    list = list || items();
    var el = document.getElementById('aaCartCount');
    if (!el) return;
    el.textContent = list.length;
    el.classList.toggle('is-zero', list.length === 0);
  }
  function onChange(f) { listeners.push(f); }

  document.addEventListener('DOMContentLoaded', function () {
    badge();

    /* any add-to-cart control on the page */
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-add]');
      if (!btn) return;
      e.preventDefault();
      var res = add(btn.getAttribute('data-add'), +btn.getAttribute('data-plan') || 0);
      if (!res) return;
      var item = window.AA_CATALOG[btn.getAttribute('data-add')];
      toast(res === 'again' ? 'Déjà dans votre panier — ' + item.title
                            : item.title + ' ajouté au panier');
    });
  });

  /* the confirmation, built once and reused */
  var box = null, timer = null;
  function toast(msg) {
    if (!box) {
      box = document.createElement('div');
      box.className = 'aa-toast';
      box.innerHTML = '<span></span><a href="' + window.AA_ROOT + 'panier.html">Voir le panier</a>';
      document.body.appendChild(box);
    }
    box.firstChild.textContent = msg;
    requestAnimationFrame(function () { box.classList.add('is-on'); });
    clearTimeout(timer);
    timer = setTimeout(function () { box.classList.remove('is-on'); }, 4200);
  }

  return { items: items, add: add, remove: remove, setPlan: setPlan,
           write: write, read: read, onChange: onChange, badge: badge, toast: toast };
})();
</script>
""" % dict(cat=json.dumps(catalog(root), ensure_ascii=False), root=json.dumps(root))


CART_CSS_SHARED = """
  /* the add-to-cart confirmation, on every page that can add */
  .aa-toast{position:fixed;left:50%;bottom:28px;transform:translate(-50%,16px);z-index:140;
    display:flex;align-items:center;gap:18px;background:#1F1F1F;color:#FFFFFF;border-radius:14px;
    padding:14px 18px;font-size:14px;box-shadow:0 18px 44px rgba(0,0,0,.28);
    opacity:0;pointer-events:none;transition:opacity .3s ease,transform .35s cubic-bezier(.2,.8,.2,1)}
  .aa-toast.is-on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
  .aa-toast a{color:#FFFFFF;font-weight:500;text-decoration:underline;text-underline-offset:3px}
  @media (max-width:743px){
    .aa-toast{left:16px;right:16px;bottom:16px;transform:translateY(16px);
      justify-content:space-between}
    .aa-toast.is-on{transform:translateY(0)}
  }
  /* the header cart, with its count */
  .cart-btn{position:relative}
  .cart-count{position:absolute;top:-6px;right:-6px;min-width:19px;height:19px;padding:0 5px;
    border-radius:999px;background:#0E695C;color:#FFFFFF;font-size:11px;font-weight:500;
    display:flex;align-items:center;justify-content:center;border:2px solid #FFFFFF}
  .cart-count.is-zero{display:none}
"""
