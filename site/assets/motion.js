/* Reveal-on-arrival. Motion stands for a state change here — a diagram's columns
   arriving in the order the flow runs — so it is worth a few lines of script.

   This file no longer decides whether anything may be hidden: the inline gate in
   <head> owns that, because it is the only code that runs before the first paint.
   Here we only land the elements the gate allowed to be hidden. */
(function () {
  if (!document.documentElement.classList.contains('js')) return;

  document.addEventListener('DOMContentLoaded', function () {
    var targets = [].slice.call(document.querySelectorAll('.summon'));
    if (!targets.length) return;

    function land(el) { el.classList.add('is-in'); }

    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        land(entry.target);
        seen.unobserve(entry.target);  // arriving happens once; it is not a loop
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.15 });

    targets.forEach(function (el) { seen.observe(el); });

    /* Insurance. Content must never stay hidden because an observer never fired
       — a short viewport, a zoomed page, a browser that throttles the callback. */
    window.setTimeout(function () { targets.forEach(land); }, 4000);
  });
})();
