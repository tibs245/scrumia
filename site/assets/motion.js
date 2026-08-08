/* Reveal-on-arrival. Motion stands for a state change here — a diagram's columns
   arriving in the order the flow runs — so it is worth a few lines of script.

   The opt-in is deliberate: the stylesheet only hides anything once this file has
   set data-motion, so a page without JavaScript, or without IntersectionObserver,
   renders complete instead of blank. prefers-reduced-motion is honoured in CSS,
   not here: the class still lands, the animation just does not travel. */
(function () {
  if (!('IntersectionObserver' in window)) return;
  document.documentElement.setAttribute('data-motion', 'on');

  document.addEventListener('DOMContentLoaded', function () {
    var targets = document.querySelectorAll('.summon');
    if (!targets.length) return;

    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        seen.unobserve(entry.target);  // arriving happens once; it is not a loop
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.15 });

    targets.forEach(function (el) { seen.observe(el); });
  });
})();
