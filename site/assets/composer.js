/* Composer: writes the two files the seven slot rows imply.

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
  var own = document.getElementById('c-own');
  var ownField = document.getElementById('c-own-key');

  /* The free entry exists only where this file runs. Its own marker rather than the
     root `.js` class, which head.html also withholds under reduced motion: a reader
     who asked for less movement must not lose a capability with it. */
  choices.classList.add('has-script');

  /* The five slots that take one module. Order is the order of the rows, of the
     install lines and of the modules: mapping — one sequence, said three times. */
  var SINGLE = ['specs', 'tracker', 'team', 'discovery', 'design'];

  /* The source half of every key emitted, per ADR-0021 — the marketplace the
     install block adds. A bare name is not a shorter spelling: nothing resolves it. */
  var SOURCE = 'tibs245/scrumia';

  /* A whole key, ADR-0021's grammar: `local:`, `shared:` or `<owner>/<repo>:`, then
     the module. A name typed with no source is refused rather than assumed published
     — that assumption is what would put a key nothing resolves in a visitor's repo. */
  var KEY = /^(?:local|shared|[^\s:/]+\/[^\s:/]+):[A-Za-z0-9._-]+$/;

  var APPS = {
    rust: { name: 'api', path: 'apps/api', type: 'backend', impl: 'scrumia-impl-rust' },
    solidjs: { name: 'web', path: 'apps/web', type: 'frontend', impl: 'scrumia-impl-solidjs' },
    other: { name: 'app', path: 'apps/app', type: 'backend', impl: null }
  };

  /* A practice attaches to the app types it actually speaks for. Copying every
     checked practice onto every app is how a backend ends up declaring a
     frontend data-fetching practice. */
  var PRACTICES = {
    tdd: { module: 'scrumia-practice-tdd', types: ['backend', 'frontend'] },
    solid: { module: 'scrumia-practice-solid', types: ['backend', 'frontend'] },
    tanstack: { module: 'scrumia-practice-tanstack-query', types: ['frontend'] }
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
    if (!own || !own.checked || !ownField) return '';
    var value = ownField.value.trim();
    var valid = KEY.test(value);
    ownField.setAttribute('aria-invalid', value && !valid ? 'true' : 'false');
    return valid ? value : '';
  }

  function compute() {
    var slots = {};
    SINGLE.forEach(function (s) { slots[s] = picked(s); });

    var stacks = pickedAll('impl');
    var practices = pickedAll('practice').map(function (i) { return PRACTICES[i.value]; });
    // Each option's value is the module's own name, so no table of the additions
    // lives here: build_site.py derives them, and nothing here can fall behind it.
    var additions = pickedAll('add').map(function (i) { return i.value; });

    var apps = stacks.map(function (input) {
      var a = APPS[input.value];
      return {
        name: a.name, path: a.path, type: a.type, impl: a.impl,
        practices: practices.filter(function (p) { return p.types.indexOf(a.type) !== -1; })
                            .map(function (p) { return p.module; })
      };
    });

    var modules = ['scrumia-core'];
    SINGLE.forEach(function (s) {
      var v = slots[s] ? slots[s].value : '';
      // `other` names a tracker the reader will write: a module, but not ours.
      if (v && v !== 'other') modules.push(v);
    });
    additions.forEach(function (m) { modules.push(m); });
    apps.forEach(function (a) { if (a.impl) modules.push(a.impl); });
    practices.forEach(function (p) { modules.push(p.module); });

    // `own` is deliberately absent from `modules`: that list is what the install
    // block prints, and we ship no command for a module we do not ship.
    return { slots: slots, apps: apps, practices: practices, stacks: stacks,
             additions: additions, own: ownKey(), modules: dedupe(modules) };
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
        var own = (app.impl ? [app.impl] : []).concat(app.practices);
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
    if (result.practices.length) {
      lines.push(result.apps.length ? S.notePractices : S.notePracticesNoapp);
    }
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
    render();
    if (event.target.name) announce(event.target);
  });

  // A text field only fires `change` on blur, and the two files must follow the typing.
  choices.addEventListener('input', function (event) {
    if (event.target === ownField) render();
  });

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
