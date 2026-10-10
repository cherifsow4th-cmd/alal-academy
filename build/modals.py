# -*- coding: utf-8 -*-
"""The two account dialogs — Connexion and Créer un compte — as one kit.

Both are the same sheet: photograph and welcome line on the left, the form on
the right. Signing in and signing up are a moment, not a destination, so they
open over whatever the visitor was reading rather than taking them to a page.
Anything pointing at #login or #signup opens the matching dialog, and the two
swap into each other without closing.

The whole form is set in Poppins (brand guideline §4). The CSS lives in gen's
BASE so every page carries it; MODALS(root) emits the markup and MODAL_JS the
behaviour, both appended next to the cart script.
"""

POPPINS = "'Poppins','General Sans',-apple-system,BlinkMacSystemFont,sans-serif"

MODAL_CSS = """
  /* ── Account dialogs ───────────────────────────────────────────────── */
  /* flex-start + auto margins: the sheet is centred while it fits and
     scrolls from its own top once it is taller than the window, instead of
     being clipped at both ends the way align-items:center leaves it */
  .aa-modal { position:fixed; inset:0; z-index:100; display:none;
    align-items:flex-start; justify-content:center; padding:24px; overflow:auto; }
  .aa-modal.is-open { display:flex; }
  .aa-modal-overlay { position:absolute; inset:0; background:rgba(31,31,31,.58); }
  /* the sticky header's backdrop-filter makes it paint through an overlay
     that is correctly above it, so the filter is dropped while open */
  body.aa-modal-open { overflow:hidden; }
  body.aa-modal-open header { backdrop-filter:none !important; -webkit-backdrop-filter:none !important; }
  .aa-modal-dialog { position:relative; margin:auto; width:min(1040px, 100%); min-width:0; background:#FFFFFF;
    border-radius:18px; overflow:hidden; display:grid; grid-template-columns:1fr 1fr;
    box-shadow:0 40px 90px -30px rgba(31,31,31,.45); }
  .aa-modal-close { position:absolute; top:16px; right:16px; z-index:2; width:38px; height:38px;
    display:flex; align-items:center; justify-content:center; border-radius:10px;
    border:1px solid rgba(31,31,31,.14); background:#FFFFFF; color:#1F1F1F; cursor:pointer;
    font:inherit; transition:background .25s ease, color .25s ease; }
  .aa-modal-close:hover { background:#1F1F1F; color:#FFFFFF; }

  /* the whole form is set in Poppins — headings, labels, fields, buttons, links */
  .aa-modal-dialog, .aa-modal-dialog input, .aa-modal-dialog button,
  .aa-modal-dialog a { font-family:__POPPINS__; }

  .aa-modal-aside { position:relative; isolation:isolate; padding:40px; display:flex;
    flex-direction:column; justify-content:space-between; gap:28px; min-height:560px;
    background:#EAEAEA url('assets/modal/login.jpg') center/cover no-repeat; }
  /* scrim: the photo runs dark at the sky and light across the concrete, so the
     type needs its own ground at both ends rather than a flat tint */
  .aa-modal-aside::before { content:''; position:absolute; inset:0; z-index:-1;
    background:linear-gradient(to bottom, rgba(31,31,31,.72) 0%, rgba(31,31,31,.18) 32%,
                                          rgba(31,31,31,.30) 68%, rgba(31,31,31,.82) 100%); }
  .aa-modal-aside h3 { margin:0; font-size:22px; font-weight:500; letter-spacing:-0.02em; color:#FFFFFF; }
  .aa-modal-aside p { margin:0; font-size:14px; color:rgba(255,255,255,.78); }
  .aa-modal-aside a { color:#FFFFFF; font-weight:500; text-decoration:underline; text-underline-offset:3px; }

  .aa-modal-main { min-width:0; padding:50px; display:flex; flex-direction:column; }
  .aa-modal-main h2 { margin:0; font-size:26px; font-weight:500; letter-spacing:-0.02em; color:#1F1F1F; }
  .aa-modal-lede { margin:12px 0 0; font-size:14.5px; line-height:1.6; color:#7a7a7a; }
  .aa-modal-row { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
  .aa-field { margin-top:26px; }
  .aa-field label { display:block; font-size:11px; font-weight:500;
    letter-spacing:.1em; text-transform:uppercase; color:#7a7a7a; }
  .aa-field input { width:100%; height:48px; border:0; border-bottom:1px solid rgba(31,31,31,.14);
    border-radius:0; background:transparent; font:inherit; font-size:15px; color:#1F1F1F; }
  .aa-field input::placeholder { color:#A7A7A7; }
  .aa-field input:focus { outline:none; border-bottom-color:#1F1F1F; }
  .aa-field .hint { display:block; margin-top:8px; font-size:12.5px; color:#A7A7A7; }
  .aa-modal-keep { display:flex; align-items:flex-start; gap:10px; margin:24px 0 0; font-size:14px;
    line-height:1.5; color:#7a7a7a; }
  .aa-modal-keep input { width:16px; height:16px; flex:none; margin-top:2px; accent-color:#1F1F1F; }
  .aa-modal-keep a { color:#1F1F1F; text-decoration:underline; text-underline-offset:3px; }
  .aa-modal-submit { width:100%; height:62px; margin-top:26px; border:0; border-radius:12px;
    background:#1F1F1F; color:#FFFFFF; font:inherit; font-size:16px; font-weight:500; cursor:pointer; }
  .aa-modal-forgot { margin:14px 0 0; text-align:right; font-size:13.5px; }
  .aa-modal-forgot a { color:#7a7a7a; text-decoration:underline; text-underline-offset:3px; }
  .aa-modal-or { margin:30px 0 14px; font-size:13.5px; color:#7a7a7a; }
  .aa-modal-social { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
  .aa-modal-social a { display:flex; align-items:center; justify-content:center; gap:8px; height:48px;
    border:1px solid rgba(31,31,31,.14); border-radius:10px; font-size:14px; color:#1F1F1F; }
  /* the aside already carries the line across to the other dialog, so the
     one at the foot of the form only appears once the aside is gone */
  .aa-modal-swap { display:none; margin:26px 0 0; padding-top:20px;
    border-top:1px solid rgba(31,31,31,.09); font-size:14px; color:#7a7a7a; }
  .aa-modal-swap a { color:#1F1F1F; font-weight:500; text-decoration:underline; text-underline-offset:3px; }
  @media (max-width:820px) {
    .aa-modal { padding:14px; }
    .aa-modal-dialog { grid-template-columns:1fr; }
    .aa-modal-aside { display:none; }
    .aa-modal-main { padding:44px 26px 34px; }
    .aa-modal-row { grid-template-columns:1fr; gap:0; }
    .aa-modal-social { grid-template-columns:1fr; }
    .aa-modal-swap { display:block; }
  }
""".replace('__POPPINS__', POPPINS)

CLOSE_BTN = """      <button type="button" class="aa-modal-close" data-aa-close aria-label="Fermer">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
      </button>"""

SOCIAL = """      <div class="aa-modal-social">
        <a href="#oauth-google">Google</a>
        <a href="#oauth-linkedin">LinkedIn</a>
        <a href="#oauth-apple">Apple</a>
      </div>"""

LOGIN = """
<!-- CONNEXION -->
<div class="aa-modal" id="aaLogin" role="dialog" aria-modal="true" aria-labelledby="aaLoginTitle" hidden>
  <div class="aa-modal-overlay" data-aa-close></div>
  <div class="aa-modal-dialog">
__CLOSE__

    <aside class="aa-modal-aside">
      <h3>Bienvenue.</h3>
      <p>Pas encore membre ? <a href="#signup">Créer un compte</a></p>
    </aside>

    <div class="aa-modal-main">
      <h2 id="aaLoginTitle">Connexion</h2>
      <p class="aa-modal-lede">Retrouvez vos cours, vos certificats et votre panier.</p>
      <form id="aaLoginForm" novalidate>
        <div class="aa-field">
          <label for="aaLoginEmail">E-mail ou identifiant</label>
          <input id="aaLoginEmail" name="email" type="text" autocomplete="username" placeholder="vous@exemple.com">
        </div>
        <div class="aa-field">
          <label for="aaLoginPass">Mot de passe</label>
          <input id="aaLoginPass" name="password" type="password" autocomplete="current-password" placeholder="••••••••">
        </div>
        <label class="aa-modal-keep"><input type="checkbox" name="keep"> <span>Rester connecté</span></label>
        <button type="submit" class="aa-modal-submit">Se connecter</button>
      </form>
      <p class="aa-modal-forgot"><a href="#reset">Mot de passe oublié ?</a></p>
      <p class="aa-modal-or">Ou continuer avec</p>
__SOCIAL__
      <p class="aa-modal-swap">Pas encore de compte ? <a href="#signup">Créer un compte</a></p>
    </div>
  </div>
</div>
""".replace('__CLOSE__', CLOSE_BTN).replace('__SOCIAL__', SOCIAL)

SIGNUP = """
<!-- CRÉER UN COMPTE -->
<div class="aa-modal" id="aaSignup" role="dialog" aria-modal="true" aria-labelledby="aaSignupTitle" hidden>
  <div class="aa-modal-overlay" data-aa-close></div>
  <div class="aa-modal-dialog">
__CLOSE__

    <aside class="aa-modal-aside">
      <h3>Commencez aujourd'hui.</h3>
      <p>Déjà membre ? <a href="#login">Se connecter</a></p>
    </aside>

    <div class="aa-modal-main">
      <h2 id="aaSignupTitle">Créer un compte</h2>
      <p class="aa-modal-lede">Un seul compte pour les cours, les parcours et vos certificats.</p>
      <form id="aaSignupForm" novalidate>
        <div class="aa-modal-row">
          <div class="aa-field">
            <label for="aaSuFirst">Prénom</label>
            <input id="aaSuFirst" name="first" type="text" autocomplete="given-name" placeholder="Prénom">
          </div>
          <div class="aa-field">
            <label for="aaSuLast">Nom</label>
            <input id="aaSuLast" name="last" type="text" autocomplete="family-name" placeholder="Nom">
          </div>
        </div>
        <div class="aa-field">
          <label for="aaSuEmail">E-mail</label>
          <input id="aaSuEmail" name="email" type="email" autocomplete="email" placeholder="vous@exemple.com">
        </div>
        <div class="aa-field">
          <label for="aaSuPass">Mot de passe</label>
          <input id="aaSuPass" name="password" type="password" autocomplete="new-password" placeholder="••••••••">
          <span class="hint">Au moins 8 caractères.</span>
        </div>
        <label class="aa-modal-keep"><input type="checkbox" name="cgu">
          <span>J'accepte les <a href="#terms">conditions d'utilisation</a> et la
          <a href="#privacy">politique de confidentialité</a>.</span></label>
        <button type="submit" class="aa-modal-submit">Créer mon compte</button>
      </form>
      <p class="aa-modal-or">Ou continuer avec</p>
__SOCIAL__
      <p class="aa-modal-swap">Vous avez déjà un compte ? <a href="#login">Se connecter</a></p>
    </div>
  </div>
</div>
""".replace('__CLOSE__', CLOSE_BTN).replace('__SOCIAL__', SOCIAL)


def modals(root=''):
    """Both dialogs. root only matters for the aside photograph, which is set
    in BASE, so the markup itself is path-free — the argument is kept so the
    call sites read like the cart's."""
    return LOGIN + SIGNUP


MODAL_JS = """
<script>
/* Account dialogs: anything pointing at #login or #signup opens the matching
   sheet over the page. The X, the overlay and Escape close it; the links
   inside each aside swap straight to the other one. Focus moves in on open
   and returns to whatever opened it. Design phase — the forms post nowhere. */
(function () {
  var sheets = { '#login': document.getElementById('aaLogin'),
                 '#signup': document.getElementById('aaSignup') };
  var opener = null, current = null;
  function close() {
    if (!current) return;
    current.classList.remove('is-open'); current.hidden = true; current = null;
    document.body.classList.remove('aa-modal-open');
    if (opener && opener.focus) opener.focus();
  }
  function open(key, from) {
    var m = sheets[key]; if (!m) return false;
    if (current && current !== m) { current.classList.remove('is-open'); current.hidden = true; }
    else if (!current) { opener = from || null; }
    m.hidden = false; m.classList.add('is-open'); current = m;
    document.body.classList.add('aa-modal-open');
    m.scrollTop = 0;
    var f = m.querySelector('input'); if (f) f.focus({ preventScroll: true });
    return true;
  }
  document.addEventListener('click', function (e) {
    var closer = e.target.closest('[data-aa-close]');
    if (closer && closer.closest('.aa-modal')) { e.preventDefault(); close(); return; }
    var a = e.target.closest('a[href="#login"], a[href="#signup"]');
    if (!a) return;
    if (open(a.getAttribute('href'), a)) e.preventDefault();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });
  Array.prototype.forEach.call(document.querySelectorAll('#aaLoginForm, #aaSignupForm'),
    function (f) { f.addEventListener('submit', function (e) { e.preventDefault(); }); });
})();
</script>
"""
