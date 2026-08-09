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
  var resting = home;

  function place(el, instant) {
    if (!el) { rail.style.width = '0'; return; }
    // The first-ever position, and any resize-triggered move, land without a
    // transition — a layout change is not the reader pointing at something.
    var skipTransition = instant || !oriented;
    if (skipTransition) rail.classList.remove('is-ready');
    rail.style.width = el.offsetWidth + 'px';
    rail.style.transform = 'translateX(' + el.offsetLeft + 'px)';
    if (skipTransition) {
      void rail.offsetWidth;
      rail.classList.add('is-ready');
      oriented = true;
    }
  }

  links.forEach(function (a) {
    a.addEventListener('mouseenter', function () { resting = a; place(a); });
    a.addEventListener('focus', function () { resting = a; place(a); });
  });
  // The rail never chases the language pair or the theme toggle.
  [nav.querySelector('.lang'), nav.querySelector('.theme-btn')].forEach(function (el) {
    if (el) el.addEventListener('mouseenter', function () { resting = home; place(home); });
  });
  nav.addEventListener('mouseleave', function () { resting = home; place(home); });
  nav.addEventListener('focusout', function (e) {
    if (links.indexOf(e.relatedTarget) === -1) { resting = home; place(home); }
  });
  // A resize stands for a layout change, not a reader's intent: reposition to
  // wherever the rail was resting, without the transition hover/focus earn.
  window.addEventListener('resize', function () {
    if (oriented) place(resting, true);
  });

  (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
    header.classList.add('nav-rail-on');
    if (home) place(home);
  });
})();
