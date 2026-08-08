/* The theme toggle. Applying the saved choice is not done here — the inline
   script in <head> does it before the first paint, which is the only place it
   can be done without a flash. This file owns the control, and can therefore
   be deferred. */
(function () {
  var root = document.documentElement;

  function current() {
    return root.getAttribute('data-theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }

  /* Run a scheme change with every transition frozen, then thaw.
     Two reasons, and the second is the load-bearing one: a page-wide crossfade
     is motion that stands for nothing, and a transition caught running across a
     light-dark() value never re-resolves it — it keeps the old theme's colour
     for good. Reading a computed style is what forces the recalc to happen
     while things are still frozen. */
  function freeze(change) {
    root.setAttribute('data-theme-switching', '');
    change();
    window.getComputedStyle(root).colorScheme;
    window.setTimeout(function () { root.removeAttribute('data-theme-switching'); }, 0);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme');
    if (!btn) return;

    function press() {
      btn.setAttribute('aria-pressed', current() === 'dark' ? 'true' : 'false');
    }
    press();

    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      freeze(function () { root.setAttribute('data-theme', next); });
      press();
      try { localStorage.setItem('scrumia-theme', next); } catch (e) {}
    });

    /* The system preference can move while the page is open. With no explicit
       choice stored, that repaints the whole page — the same freeze applies, and
       the toggle's own label has to follow what the reader is now looking at. */
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      if (root.hasAttribute('data-theme')) return;  // an explicit choice wins
      freeze(function () {});
      press();
    });
  });
})();
