/* Theme: apply the saved choice immediately (this file is loaded synchronously
   in <head> to avoid a flash of the wrong theme), bind the toggle on DOM ready. */
(function () {
  var root = document.documentElement, saved = null;
  try { saved = localStorage.getItem('scrumia-theme'); } catch (e) {}
  if (saved) root.setAttribute('data-theme', saved);

  function current() {
    var dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return root.getAttribute('data-theme') || (dark ? 'dark' : 'light');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme');
    if (!btn) return;
    btn.setAttribute('aria-pressed', current() === 'dark' ? 'true' : 'false');
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      btn.setAttribute('aria-pressed', next === 'dark' ? 'true' : 'false');
      try { localStorage.setItem('scrumia-theme', next); } catch (e) {}
    });
  });
})();
