# -*- coding: utf-8 -*-
"""Builds connexion.html and inscription.html.

Both are the log-in modal from the homepage, opened out into a page: the same
split — photograph and welcome line on the left, the form on the right — the
same fields, the same social row. The sign-up page adds the name fields, the
terms checkbox and its own copy, and the two pages link to each other.

Per the brand guideline (§4), the form is set in Poppins throughout: headings,
labels, inputs, buttons and links. Poppins 400 and 500 are pulled in the head.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from gen import BASE, HEADER, FOOTER, MNAV, MONO, ROOT, nav_active
from cartkit import cart_js

POPPINS = "'Poppins','General Sans',-apple-system,BlinkMacSystemFont,sans-serif"

CSS = """
  /* ── Sign-in / sign-up ────────────────────────────────────────────────
     The homepage log-in modal as a page: photograph left, form right. The
     whole form is Poppins — headings, labels, fields, buttons and links —
     rather than the site's General Sans with mono labels. */
  .auth{display:grid;grid-template-columns:1fr 1fr;align-items:stretch;
    max-width:1180px;margin:0 auto;padding:56px 0 110px}
  .auth-card{display:grid;min-width:0;grid-template-columns:1fr 1fr;border-radius:18px;overflow:hidden;
    border:1px solid rgba(31,31,31,.1);box-shadow:0 40px 90px -46px rgba(31,31,31,.4);
    grid-column:1 / -1}

  .auth-aside{position:relative;isolation:isolate;padding:44px;display:flex;
    flex-direction:column;justify-content:space-between;gap:28px;min-height:620px;
    background:#EAEAEA url('assets/modal/login.jpg') center/cover no-repeat}
  /* the photo runs dark at the sky and light across the concrete, so the type
     needs its own ground at both ends rather than a flat tint */
  .auth-aside::before{content:'';position:absolute;inset:0;z-index:-1;
    background:linear-gradient(to bottom,rgba(31,31,31,.72) 0%,rgba(31,31,31,.18) 32%,
                                         rgba(31,31,31,.30) 68%,rgba(31,31,31,.82) 100%)}
  .auth-aside h2{margin:0;font-family:%(poppins)s;font-size:24px;font-weight:500;
    letter-spacing:-0.02em;color:#FFFFFF}
  .auth-aside p{margin:0;font-family:%(poppins)s;font-size:14px;color:rgba(255,255,255,.78)}
  .auth-aside a{color:#FFFFFF;font-weight:500;text-decoration:underline;text-underline-offset:3px}

  .auth-main{min-width:0;padding:52px 54px;display:flex;flex-direction:column;background:#FFFFFF;
    font-family:%(poppins)s}
  .auth-main h1{margin:0;font-family:%(poppins)s;font-size:28px;font-weight:500;
    letter-spacing:-0.025em;color:#1F1F1F}
  .auth-main .lede{margin:12px 0 0;font-size:14.5px;line-height:1.6;color:#7a7a7a}
  .auth-row{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  .field{margin-top:24px}
  .field label{display:block;font-family:%(poppins)s;font-size:11px;font-weight:500;
    letter-spacing:.1em;text-transform:uppercase;color:#7a7a7a}
  .field input{width:100%;height:48px;border:0;border-bottom:1px solid rgba(31,31,31,.14);
    border-radius:0;background:transparent;font-family:%(poppins)s;font-size:15px;color:#1F1F1F}
  .field input::placeholder{color:#A7A7A7}
  .field input:focus{outline:none;border-bottom-color:#1F1F1F}
  .field .hint{display:block;margin-top:8px;font-size:12.5px;color:#A7A7A7}
  .auth-keep{display:flex;align-items:flex-start;gap:10px;margin:24px 0 0;font-size:14px;
    line-height:1.5;color:#7a7a7a}
  .auth-keep input{width:16px;height:16px;flex:none;margin-top:2px;accent-color:#1F1F1F}
  .auth-keep a{color:#1F1F1F;text-decoration:underline;text-underline-offset:3px}
  .auth-submit{width:100%;height:62px;margin-top:26px;border:0;border-radius:12px;
    background:#1F1F1F;color:#FFFFFF;font-family:%(poppins)s;font-size:16px;font-weight:500;
    cursor:pointer;transition:box-shadow .45s cubic-bezier(.2,.8,.2,1)}
  .auth-submit:hover{box-shadow:0 2px 6px rgba(0,0,0,.32),0 7px 16px rgba(0,0,0,.28),
    0 17px 33px rgba(0,0,0,.24)}
  .auth-forgot{margin:14px 0 0;text-align:right;font-size:13.5px}
  .auth-forgot a{color:#7a7a7a;text-decoration:underline;text-underline-offset:3px}
  .auth-or{margin:30px 0 14px;font-size:13.5px;color:#7a7a7a}
  .auth-social{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
  .auth-social a{display:flex;align-items:center;justify-content:center;gap:8px;height:48px;
    border:1px solid rgba(31,31,31,.14);border-radius:10px;font-family:%(poppins)s;font-size:14px;
    color:#1F1F1F;transition:border-color .25s ease,box-shadow .3s ease}
  .auth-social a:hover{border-color:rgba(31,31,31,.32);box-shadow:0 2px 5px rgba(0,0,0,.07)}
  .auth-swap{margin:30px 0 0;padding-top:22px;border-top:1px solid rgba(31,31,31,.09);
    font-size:14px;color:#7a7a7a}
  .auth-swap a{color:#1F1F1F;font-weight:500;text-decoration:underline;text-underline-offset:3px}

  @media (min-width:744px) and (max-width:1199px){
    .auth{padding:36px 0 72px}
    .auth-aside{padding:32px;min-height:0}
    .auth-main{padding:36px 32px}
    .auth-main h1{font-size:24px}
  }
  @media (max-width:860px){
    .auth-card{grid-template-columns:1fr}
    /* the photograph is atmosphere, not information — it goes on a phone */
    .auth-aside{display:none}
    .auth-main{padding:40px 26px 34px}
    .auth-row{grid-template-columns:1fr;gap:0}
    .auth-social{grid-template-columns:1fr}
  }
  @media (max-width:743px){ .auth{padding:26px 0 64px} }
""".replace('%(poppins)s', POPPINS)

SOCIAL = """        <div class="auth-social">
          <a href="#oauth-google">Google</a>
          <a href="#oauth-linkedin">LinkedIn</a>
          <a href="#oauth-apple">Apple</a>
        </div>"""


def page(title, desc, body, active=''):
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap" rel="stylesheet">
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
""" % (html.escape(title), html.escape(desc), BASE, CSS,
       nav_active(HEADER, active) + MNAV, body, FOOTER.replace('{ROOT}', ''), cart_js(''))


def build_signin():
    body = """<div class="wrap">
  <div class="auth">
    <div class="auth-card">
      <aside class="auth-aside">
        <h2>Bienvenue.</h2>
        <p>Pas encore membre ? <a href="inscription.html">Créer un compte</a></p>
      </aside>
      <div class="auth-main">
        <h1>Connexion</h1>
        <p class="lede">Retrouvez vos cours, vos certificats et votre panier.</p>
        <form novalidate>
          <div class="field">
            <label for="email">E-mail ou identifiant</label>
            <input id="email" name="email" type="text" autocomplete="username"
              placeholder="vous@exemple.com">
          </div>
          <div class="field">
            <label for="pass">Mot de passe</label>
            <input id="pass" name="password" type="password" autocomplete="current-password"
              placeholder="••••••••">
          </div>
          <label class="auth-keep"><input type="checkbox" name="keep"> <span>Rester connecté</span></label>
          <button type="submit" class="auth-submit">Se connecter</button>
        </form>
        <p class="auth-forgot"><a href="#reset">Mot de passe oublié ?</a></p>
        <p class="auth-or">Ou continuer avec</p>
%(social)s
        <p class="auth-swap">Pas encore de compte ?
          <a href="inscription.html">Créer un compte</a></p>
      </div>
    </div>
  </div>
  <hr class="rule" style="border:0;border-top:1px solid rgba(31,31,31,.09)">
</div>
""" % dict(social=SOCIAL)
    open(os.path.join(ROOT, 'connexion.html'), 'w', encoding='utf-8').write(
        page('Connexion — Alal Academy',
             "Connectez-vous à votre compte Alal Academy : vos cours, vos certificats, votre panier.",
             body))
    print('connexion.html')


def build_signup():
    body = """<div class="wrap">
  <div class="auth">
    <div class="auth-card">
      <aside class="auth-aside">
        <h2>Commencez aujourd'hui.</h2>
        <p>Déjà membre ? <a href="connexion.html">Se connecter</a></p>
      </aside>
      <div class="auth-main">
        <h1>Créer un compte</h1>
        <p class="lede">Un seul compte pour les cours, les parcours et vos certificats.</p>
        <form novalidate>
          <div class="auth-row">
            <div class="field">
              <label for="first">Prénom</label>
              <input id="first" name="first" type="text" autocomplete="given-name"
                placeholder="Cherif">
            </div>
            <div class="field">
              <label for="last">Nom</label>
              <input id="last" name="last" type="text" autocomplete="family-name"
                placeholder="Sow">
            </div>
          </div>
          <div class="field">
            <label for="email">E-mail</label>
            <input id="email" name="email" type="email" autocomplete="email"
              placeholder="vous@exemple.com">
          </div>
          <div class="field">
            <label for="pass">Mot de passe</label>
            <input id="pass" name="password" type="password" autocomplete="new-password"
              placeholder="••••••••">
            <span class="hint">Au moins 8 caractères.</span>
          </div>
          <label class="auth-keep"><input type="checkbox" name="cgu">
            <span>J'accepte les <a href="#terms">conditions d'utilisation</a> et la
            <a href="#privacy">politique de confidentialité</a>.</span></label>
          <button type="submit" class="auth-submit">Créer mon compte</button>
        </form>
        <p class="auth-or">Ou continuer avec</p>
%(social)s
        <p class="auth-swap">Vous avez déjà un compte ?
          <a href="connexion.html">Se connecter</a></p>
      </div>
    </div>
  </div>
  <hr class="rule" style="border:0;border-top:1px solid rgba(31,31,31,.09)">
</div>
""" % dict(social=SOCIAL)
    open(os.path.join(ROOT, 'inscription.html'), 'w', encoding='utf-8').write(
        page('Créer un compte — Alal Academy',
             "Créez votre compte Alal Academy : un seul compte pour les cours, les parcours "
             "et vos certificats.",
             body))
    print('inscription.html')


def build():
    build_signin()
    build_signup()


if __name__ == '__main__':
    build()
