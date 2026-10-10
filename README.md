# Alal Academy

The Alal Academy site — the training arm of Alal Technologies: courses,
certifying tracks, webinars, the cart, and the signed-in account area.

The site is static. Every page is plain HTML with its stylesheet inlined in
the head, so a page can be opened straight from disk with no build step and no
server.

## Layout

| Path | What it holds |
|---|---|
| `index.html` | the home page, hand-written |
| `blog.html`, `blog/` | the blog index and its ten articles |
| `cours/` | one page per course, in two states: the public page and `-inscrit` for someone who owns it |
| `parcours.html`, `parcours/` | the certifying tracks |
| `apprendre/` | the lesson player, one page per course |
| `webinaires.html` | the live sessions and their replays |
| `panier.html`, `404.html` | the cart and the not-found page |
| `compte.html`, `mes-*.html`, `parametres.html` | the signed-in account area |
| `connexion.html`, `inscription.html` | standalone sign-in and sign-up pages, kept but not linked — the site uses the dialogs instead |
| `assets/` | images, the mark, the video loop |
| `build/` | the generators |

## build/

Only `index.html` is written by hand. Everything else is produced by the
Python modules in `build/`, which read one set of data files and emit the
pages, so a change to a price or a course lands everywhere at once.

```
python3 build/gen.py         # blog.html and the ten articles
python3 build/course.py      # cours/
python3 build/parcours.py    # parcours.html and parcours/
python3 build/webinaires.py  # webinaires.html
python3 build/shop.py        # panier.html and 404.html
python3 build/account.py     # the account area
python3 build/player.py      # apprendre/
python3 build/enrolled.py    # cours/*-inscrit.html — rewrites course.py's output
```

Run them in that order after a data change: `enrolled.py` reads the pages
`course.py` writes, and `player.py` and `enrolled.py` both read the progress
defined in `account.py`.

The data lives in `build/courses.py`, `build/parcours_data.py`,
`build/webinaires_data.py`, `build/articles_*.py` and `build/tutors.py`.
Shared pieces — the header, the footer, the base stylesheet, the account
dialogs, the cart, the page loader, the icon set — are in `build/gen.py`,
`build/modals.py`, `build/cartkit.py`, `build/loader.py` and
`build/svc_icons.py`.

## State of play

This is a design. The cart keeps its contents in the browser's local storage
and no order reaches a server; the account area renders one worked example of
a signed-in student rather than real data; the lesson player has its controls
but no lesson footage behind them. Each of those needs a back end before the
site can take a customer.
