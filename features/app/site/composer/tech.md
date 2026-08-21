# Tech — Composer

## Structure

**Choosing needs no JavaScript.** `<details name="composer-slot">` owns what
is open, native radios and checkboxes own what is chosen, and CSS `:has()`
owns which fill the row reports. Script owns exactly one thing: writing the
two takeaway artifacts. With scripting off the index still opens, still
chooses and still reports — and the artifacts are pre-rendered in the
template to match the default composition, so the page never shows a stale
or empty takeaway.

**One thing needs script, and is absent without it.** The free entry where a
visitor names their own module is the exception, and it is gated rather than
degraded: text cannot become YAML through `:has()`, so a field left standing
with no script would be a control that silently does nothing under six rows
that all work. It is hidden until `composer.js` marks `#composer-choices` as
running — its own marker, not the root `.js` class, which `partials/head.html`
also withholds from a reader who asked for reduced motion. A motion preference
must not cost a capability.

**The additions shelf is derived, never listed.** `tools/build_site.py` builds
one option per `site/modules.json` entry that fills no slot, minus the kernel,
and each option's value is the module's own name. `composer.js` therefore holds
no table of them to fall out of step with, and the thirteenth module reaches the
shelf on the build that adds it rather than on the day someone remembers.
