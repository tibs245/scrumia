/* Composer: writes the two files the six slot rows imply.

   It does not open a row, record a choice, or decide what a row reports —
   <details>, the native inputs and CSS :has() do all three, so the section
   works with this file absent. What it owns is the install block and the
   config file, which no amount of CSS can assemble.

   Every string it prints comes from the markup (site/i18n/), never from here:
   the fixed ones from #composer-strings, the per-slot ones from data-note on
   the option that causes them. */
(function () {
  var choices = document.getElementById('composer-choices');
  if (!choices) return;

  var S = (document.getElementById('composer-strings') || {}).dataset || {};
  var installPre = document.getElementById('composer-install');
  var configPre = document.getElementById('composer-config');
  var notes = document.getElementById('composer-note');
  var live = document.getElementById('composer-live');
  var ownBox = document.getElementById('add-free');
  var ownField = document.getElementById('add-free-key');
  var ownRefused = document.getElementById('add-free-refused');

  /* The five slots that take one module. Order is the order of the rows, of the
     install lines and of the modules: mapping — one sequence, said three times. */
  var SINGLE = ['specs', 'tracker', 'team', 'discovery', 'design'];

  /* The source half of every key emitted, per ADR-0021 — the marketplace the
     install block adds. A bare name is not a shorter spelling: nothing resolves it. */
  var SOURCE = 'tibs245/scrumia';

  /* A whole key, ADR-0021's grammar: `local:`, `shared:` or `<owner>/<repo>:`, then
     the module. A name typed with no source is refused rather than assumed published
     — that assumption is what would put a key nothing resolves in a visitor's repo.
     Both halves are spelled positively. Spelled as an exclusion, the source would
     admit a quote or a control character and emit a file that does not parse — and
     `\s` is a different set in every engine, so a check written elsewhere would
     disagree with this one about which strings those are. */
  var KEY = /^(?:local|shared|[A-Za-z0-9._-]+\/[A-Za-z0-9._-]+):[A-Za-z0-9._-]+$/;

  var APPS = {
    rust: { name: 'api', path: 'apps/api', type: 'backend', impl: 'scrumia-impl-rust' },
    solidjs: { name: 'web', path: 'apps/web', type: 'frontend', impl: 'scrumia-impl-solidjs' },
    reactjs: { name: 'web', path: 'apps/web', type: 'frontend', impl: 'scrumia-impl-reactjs' },
    kotlin: { name: 'api', path: 'apps/api', type: 'backend', impl: 'scrumia-kotlin' },
    kmm: { name: 'mobile', path: 'apps/mobile', type: 'mobile', impl: 'scrumia-kotlin-multiplatform-mobile' },
    other: { name: 'app', path: 'apps/app', type: 'backend', impl: null }
  };

  var PRESETS = {
    solo: { specs: 'scrumia-specs', tracker: '', team: '', discovery: '', design: '' },
    exploring: { specs: 'scrumia-specs', tracker: '', team: '', discovery: 'scrumia-discovery', design: '' },
    production: { specs: 'scrumia-specs', tracker: 'scrumia-github-project', team: 'scrumia-teams', discovery: 'scrumia-discovery', design: 'scrumia-design' },
    othertracker: { specs: 'scrumia-specs', tracker: 'other', team: 'scrumia-teams', discovery: 'scrumia-discovery', design: '' }
  };

  function picked(name) {
    return choices.querySelector('input[name="c-' + name + '"]:checked');
  }
  function pickedAll(name) {
    return [].slice.call(choices.querySelectorAll('input[name="c-' + name + '"]:checked'));
  }
  function note(input) {
    return input && input.dataset.note ? input.dataset.note : '';
  }

  /* The visitor's own module, as one whole key. Unchecked, blank or malformed emits
     nothing: half a key pasted into a repository is worse than no key at all. */
  function ownKey() {
    if (!ownBox || !ownBox.checked || !ownField) return '';
    var value = ownField.value.trim();
    return KEY.test(value) ? value : '';
  }

  /* A box checked with nothing typed is unanswered, not refused — painting that as
     an error is how a composition becomes a form. */
  function refused() {
    var value = ownField ? ownField.value.trim() : '';
    return !!(ownBox && ownBox.checked && value !== '' && !KEY.test(value));
  }

  /* Marked when the visitor leaves the field and cleared on the next keystroke:
     checking per keystroke calls a correctly-typed key wrong for its first six
     characters. Every caller passes the same predicate — one that only ever cleared
     would leave a re-checked box wearing the wash of a decision that did not land.
     The sentence is the one already in the markup, so it stays in site/i18n/. */
  function markRefusal(isRefused) {
    if (!ownField) return;
    ownField.setAttribute('aria-invalid', isRefused ? 'true' : 'false');
    if (isRefused && live && ownRefused) live.textContent = ownRefused.textContent;
  }

  function compute() {
    var slots = {};
    SINGLE.forEach(function (s) { slots[s] = picked(s); });

    var stacks = pickedAll('impl');
    // Each option's value is the module's own name, so no table of the additions
    // lives here: build_site.py derives them, and nothing here can fall behind it.
    var additions = pickedAll('add').map(function (i) { return i.value; });

    var apps = stacks.map(function (input) {
      var a = APPS[input.value];
      return { name: a.name, path: a.path, type: a.type, impl: a.impl };
    });

    var modules = ['scrumia-core'];
    SINGLE.forEach(function (s) {
      var v = slots[s] ? slots[s].value : '';
      // `other` names a tracker the reader will write: a module, but not ours.
      if (v && v !== 'other') modules.push(v);
    });
    additions.forEach(function (m) { modules.push(m); });
    apps.forEach(function (a) { if (a.impl) modules.push(a.impl); });

    modules = dedupe(modules);
    // A key already standing is not emitted twice: a duplicate mapping key is a
    // silent overwrite in whatever parses the file, not a louder declaration.
    var mine = SOURCE + ':';
    var ownEntry = ownKey();
    if (ownEntry.slice(0, mine.length) === mine
        && modules.indexOf(ownEntry.slice(mine.length)) !== -1) ownEntry = '';

    // Absent from `modules`: that list is what the install block prints.
    return { slots: slots, apps: apps, stacks: stacks,
             additions: additions, own: ownEntry, modules: modules };
  }

  function dedupe(list) {
    return list.filter(function (m, i) { return list.indexOf(m) === i; });
  }

  /* Paints a <pre> from a list of plain strings and {t, c} coloured spans. Built
     as nodes rather than markup so a translated string can never become HTML. */
  function paint(pre, parts) {
    pre.textContent = '';
    parts.forEach(function (part) {
      if (typeof part === 'string') {
        pre.appendChild(document.createTextNode(part));
        return;
      }
      var span = document.createElement('span');
      span.className = part.c;
      // A missing string prints nothing rather than the word "undefined".
      span.textContent = part.t || '';
      pre.appendChild(span);
    });
  }

  function installParts(result) {
    var parts = [{ t: S.marketplace, c: 'c' }, '\n/plugin marketplace add tibs245/scrumia\n\n',
                 { t: S.install, c: 'c' }, '\n'];
    result.modules.forEach(function (m) { parts.push('/plugin install ' + m + '@scrumia\n'); });
    parts.push('\n', { t: S.thenInit, c: 'c' }, '\n/scrumia-core:scrumia-init');
    return parts;
  }

  // Only the module name is coloured: the source repeats on every line, so
  // painting it too spends the emphasis on the half nobody chose.
  function keyed(parts, depth, source, module) {
    var pad = new Array(depth + 1).join(' ');
    parts.push(pad + '"' + source + ':', { t: module, c: 'm' }, '": {}');
  }
  function entry(parts, depth, module) { keyed(parts, depth, SOURCE, module); }

  function configParts(result) {
    var parts = [{ t: S.config, c: 'c' },
                 '\nproject:\n  name: your-project\n  repo: you/your-repo   ',
                 { t: S.project, c: 'c' }, '\n\nmodules:\n'];

    SINGLE.forEach(function (slot) {
      var input = result.slots[slot];
      var value = input ? input.value : '';
      if (value && value !== 'other') {
        entry(parts, 2, value);
      } else if (note(input)) {
        // No key exists for an absence, so the consequence is the only thing
        // left standing where the module would have been.
        parts.push('  ', { t: note(input), c: 'c' });
      } else {
        return;
      }
      parts.push('\n');
    });

    result.additions.forEach(function (module) {
      entry(parts, 2, module);
      parts.push('\n');
    });

    // Keyed like every other entry, and installed by none of the commands above.
    if (result.own) {
      var cut = result.own.lastIndexOf(':');
      keyed(parts, 2, result.own.slice(0, cut), result.own.slice(cut + 1));
      parts.push('\n');
    }

    if (result.apps.length) {
      parts.push('\napps:\n');
      result.apps.forEach(function (app, index) {
        if (index) parts.push('\n');
        parts.push('  - name: ' + app.name + '\n    path: ' + app.path +
                   '\n    type: ' + app.type + '\n    modules:');
        var own = app.impl ? [app.impl] : [];
        // `modules:` alone parses as null — a value, not the absence of one. The
        // comment rides the same line so the cost survives the paste here too.
        if (!own.length) parts.push(' {}   ', { t: S.appEmpty, c: 'c' });
        own.forEach(function (module) {
          parts.push('\n');
          entry(parts, 6, module);
        });
      });
    }
    return parts;
  }

  function renderNotes(result) {
    var lines = [];
    var tracker = result.slots.tracker;
    if (tracker && tracker.value === 'other') lines.push(S.noteOwnTracker);
    // Said, not left to be noticed: the install block's silence about this module is
    // what the other commands' trustworthiness rests on.
    if (result.own) lines.push(S.noteOwnModule);
    if (result.stacks.some(function (i) { return i.value === 'other'; })) lines.push(S.noteOwnImpl);
    notes.textContent = '';
    lines.forEach(function (line) {
      var el = document.createElement('span');
      el.textContent = line;
      notes.appendChild(el);
    });
  }

  function render() {
    var result = compute();
    paint(installPre, installParts(result));
    paint(configPre, configParts(result));
    renderNotes(result);
  }

  /* What changed, for a reader who cannot see the row restate itself. The fills
     are pre-rendered and hidden with display:none, so the visible ones are
     exactly the ones with a layout box. */
  function announce(input) {
    if (!live) return;
    var row = input.closest('.slot');
    if (!row) {
      // An addition has no row restating it, so the option's own name is the fact.
      var opt = input.closest('.opt');
      if (opt && opt.querySelector('b')) live.textContent = opt.querySelector('b').textContent;
      return;
    }
    var shown = [].filter.call(row.querySelectorAll('.slot-fill > span'), function (span) {
      return span.offsetParent !== null;
    }).map(function (span) { return span.textContent; });
    live.textContent = row.querySelector('.slot-name').textContent + ' — ' + shown.join(', ');
  }

  choices.addEventListener('change', function (event) {
    if (event.target === ownBox) markRefusal(refused());
    render();
    if (event.target.name) announce(event.target);
  });

  // A text field only fires `change` on blur, and the two files must follow the typing.
  choices.addEventListener('input', function (event) {
    if (event.target !== ownField) return;
    markRefusal(false);
    render();
  });

  if (ownField) {
    ownField.addEventListener('blur', function () { markRefusal(refused()); });
  }

  choices.addEventListener('click', function (event) {
    var button = event.target.closest('.preset');
    if (!button) return;
    var preset = PRESETS[button.dataset.preset];
    if (!preset) return;
    SINGLE.forEach(function (slot) {
      var input = choices.querySelector('input[name="c-' + slot + '"][value="' + preset[slot] + '"]');
      if (input) input.checked = true;
    });
    render();
    if (live) live.textContent = button.textContent;
  });

  // A copy button with no clipboard to write to is a control that lies.
  [].forEach.call(document.querySelectorAll('.copy-btn[data-copy]'), function (button) {
    if (!navigator.clipboard) { button.hidden = true; return; }
    var idle = button.textContent;
    button.addEventListener('click', function () {
      var source = document.getElementById(button.dataset.copy);
      navigator.clipboard.writeText(source.textContent).then(function () {
        button.textContent = button.dataset.done || idle;
        setTimeout(function () { button.textContent = idle; }, 1600);
      });
    });
  });

  /* The markup already shows the default composition's two files, so this first
     pass changes nothing a reader can see. It runs anyway so that a page whose
     defaults were edited without the blocks being updated at least reads
     correctly once scripting is on; tools/test_composer.py is what actually
     holds the two in step, and it runs in CI. */
  render();
})();
