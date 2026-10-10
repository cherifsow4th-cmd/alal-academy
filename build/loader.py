# -*- coding: utf-8 -*-
"""The page loader: the mark filling up while the page arrives.

A white panel over the whole viewport with the Alal mark at its centre, drawn
twice: once in light grey, and once in Ink clipped to a line that rises from
the foot of the mark as the page loads. The fill tracks real progress — the
document's own milestones plus the images and stylesheets as they land — so
the line stops where loading has actually got to rather than animating on a
timer. When everything is in, the line reaches the top, holds for a beat, and
the whole panel fades away to reveal the page.

The mark is used as a mask rather than an image, so a single PNG gives both
the grey silhouette and the Ink fill, and both stay sharp at any size.
"""

# Two tints of the same silhouette. A CSS mask would have done this from one
# file, but a masked image is fetched under rules that block it on a file://
# page, and the design has to be reviewable by opening the HTML directly.
MARK_LINE = "assets/icons/alal-academy-mark-line.png"   # #CFCFCF
MARK_INK = "assets/icons/alal-academy-mark-ink.png"     # #1F1F1F

LOADER_CSS = """
  /* ── Page loader ──────────────────────────────────────────────────────
     The mark in Line-soft grey, filling bottom to top in Ink as the page
     loads, then the whole panel fades out. The PNG is a mask, so one file
     paints both greys. */
  html.pl-on{overflow:hidden}
  #aaLoad{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;
    justify-content:center;background:#FFFFFF;
    transition:opacity .72s cubic-bezier(.22,1,.36,1)}
  #aaLoad.is-out{opacity:0;pointer-events:none}
  #aaLoad[hidden]{display:none}
  .pl-mark{display:block;position:relative;width:112px}
  .pl-mark img{display:block;width:100%;height:auto}
  .pl-mark .pl-ink{position:absolute;inset:0;height:100%;
    /* clipped from the top down, so what shows grows up from the foot */
    clip-path:inset(100% 0 0 0);
    transition:clip-path .55s cubic-bezier(.22,1,.36,1)}
  .pl-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;
    clip:rect(0,0,0,0);white-space:nowrap;border:0}
  @media (max-width:640px){ .pl-mark{width:88px} }
  @media (prefers-reduced-motion:reduce){
    #aaLoad{transition:opacity .2s linear}
    .pl-mark .pl-ink{transition:none}
  }
"""

MARKUP = """<div id="aaLoad" role="status" aria-live="polite">
  <span class="pl-mark" aria-hidden="true">
    <img class="pl-grey" src="__LINE__" alt="" width="550" height="535">
    <img class="pl-ink" id="aaLoadFill" src="__INK__" alt="" width="550" height="535">
  </span>
  <span class="pl-sr">Chargement…</span>
</div>
<script>
/* The fill follows what has actually loaded: the document's own milestones,
   then every image and stylesheet as it lands. A slow creep keeps the line
   moving between events so a slow asset never looks like a stall, and a
   six-second failsafe guarantees the panel always lifts. */
(function () {
  var el = document.getElementById('aaLoad'); if (!el) return;
  var fill = document.getElementById('aaLoadFill');
  var doc = document.documentElement;
  doc.classList.add('pl-on');

  var shown = 0, target = 8, done = false, creep;

  function paint() {
    shown = Math.max(shown, Math.min(target, shown + (target - shown) * 0.5));
    fill.style.clipPath = 'inset(' + (100 - shown) + '% 0 0 0)';
  }
  function to(v) { target = Math.max(target, Math.min(100, v)); paint(); }

  function assets() {
    var list = [].slice.call(document.images)
      .concat([].slice.call(document.querySelectorAll('link[rel=stylesheet]')));
    var total = list.length, got = 0;
    if (!total) { to(90); return; }
    list.forEach(function (n) {
      /* a cross-origin stylesheet (the font CDN) throws on .cssRules, which
         only tells us it has already arrived */
      var ok = false;
      try { ok = n.complete || !!n.sheet; } catch (e) { ok = true; }
      function tick() { got++; to(45 + got / total * 45); }
      if (ok) { tick(); return; }
      n.addEventListener('load', tick, { once: true });
      n.addEventListener('error', tick, { once: true });
    });
  }

  function finish() {
    if (done) return; done = true;
    clearInterval(creep);
    to(100);
    setTimeout(function () {
      el.classList.add('is-out');
      doc.classList.remove('pl-on');
      window.__aaLoaded = true;
      document.dispatchEvent(new Event('aa-loaded'));
      setTimeout(function () { el.hidden = true; }, 820);
    }, 240);
  }

  /* between milestones the line keeps inching forward, but never past 92 */
  creep = setInterval(function () { if (!done) to(Math.min(92, target + 1.4)); }, 220);

  if (document.readyState === 'loading') {
    document.addEventListener('readystatechange', function () {
      if (document.readyState === 'interactive') to(30);
    });
    document.addEventListener('DOMContentLoaded', function () { to(45); assets(); });
  } else {
    to(45); assets();
  }
  if (document.readyState === 'complete') { to(96); finish(); }
  else window.addEventListener('load', function () { to(96); finish(); });

  setTimeout(finish, 6000);
  paint();
})();
</script>
"""


MARKUP = MARKUP.replace('__LINE__', MARK_LINE).replace('__INK__', MARK_INK)


def inject(out):
    """Put the panel first in the body, so it paints before anything else."""
    i = out.index('<body>') + len('<body>')
    return out[:i] + '\n' + MARKUP + out[i:]
