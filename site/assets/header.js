/* The nav rail — design/components/site-header/spec.md, "The rail". */
(function () {
  var header = document.querySelector('.top');
  var nav = header && header.querySelector('nav');
  var rail = nav && nav.querySelector('.nav-rail');
  if (!rail) return;
  if (!(window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches)) return;

  var links = [].slice.call(nav.querySelectorAll(':scope > a'));
  var home = nav.querySelector(':scope > a[aria-current="page"]');
  var oriented = false;

  function place(el) {
    if (!el) { rail.style.width = '0'; return; }
    rail.style.width = el.offsetWidth + 'px';
    rail.style.transform = 'translateX(' + el.offsetLeft + 'px)';
    // First-ever position lands without a transition, or it reads as arriving.
    if (!oriented) {
      void rail.offsetWidth;
      rail.classList.add('is-ready');
      oriented = true;
    }
  }

  links.forEach(function (a) {
    a.addEventListener('mouseenter', function () { place(a); });
    a.addEventListener('focus', function () { place(a); });
  });
  // The rail never chases the language pair or the theme toggle.
  [nav.querySelector('.lang'), nav.querySelector('.theme-btn')].forEach(function (el) {
    if (el) el.addEventListener('mouseenter', function () { place(home); });
  });
  nav.addEventListener('mouseleave', function () { place(home); });
  nav.addEventListener('focusout', function (e) {
    if (links.indexOf(e.relatedTarget) === -1) place(home);
  });

  (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
    header.classList.add('nav-rail-on');
    if (home) place(home);
  });
})();
