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

  /* The five slots that take one module. Order is the order of the rows, of the
     install lines and of the composition: block — one sequence, said three times. */
  var SINGLE = ['specs', 'tracker', 'team', 'discovery', 'design'];

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

  function compute() {
    var slots = {};
    SINGLE.forEach(function (s) { slots[s] = picked(s); });

    var stacks = pickedAll('impl');
    var practices = pickedAll('practice').map(function (i) { return PRACTICES[i.value]; });

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
    apps.forEach(function (a) { if (a.impl) modules.push(a.impl); });
    practices.forEach(function (p) { modules.push(p.module); });

    return { slots: slots, apps: apps, practices: practices, stacks: stacks, modules: dedupe(modules) };
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

  function configParts(result) {
    var parts = [{ t: S.config, c: 'c' },
                 '\nproject:\n  name: your-project\n  repo: you/your-repo   ',
                 { t: S.project, c: 'c' }, '\n\ncomposition:\n'];

    SINGLE.forEach(function (slot) {
      var input = result.slots[slot];
      var value = input ? input.value : '';
      parts.push('  ' + slot + ': ');
      if (value && value !== 'other') {
        parts.push({ t: value, c: 'm' });
      } else {
        // A null is a decision, so it carries the reason it was made — the one
        // place the consequence survives being pasted into a repo.
        parts.push('null');
        if (note(input)) parts.push('   ', { t: note(input), c: 'c' });
      }
      parts.push('\n');
    });

    if (result.apps.length) {
      parts.push('\napps:\n');
      result.apps.forEach(function (app, index) {
        if (index) parts.push('\n');
        parts.push('  - name: ' + app.name + '\n    path: ' + app.path +
                   '\n    type: ' + app.type + '\n    implementation: ');
        if (app.impl) parts.push({ t: app.impl, c: 'm' });
        else parts.push('null');
        parts.push('\n    practices: [');
        app.practices.forEach(function (p, i) {
          if (i) parts.push(', ');
          parts.push({ t: p, c: 'm' });
        });
        parts.push(']');
      });
    }
    return parts;
  }

  function renderNotes(result) {
    var lines = [];
    var tracker = result.slots.tracker;
    if (tracker && tracker.value === 'other') lines.push(S.noteOwnTracker);
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
    if (!row) return;
    var shown = [].filter.call(row.querySelectorAll('.slot-fill > span'), function (span) {
      return span.offsetParent !== null;
    }).map(function (span) { return span.textContent; });
    live.textContent = row.querySelector('.slot-name').textContent + ' — ' + shown.join(', ');
  }

  choices.addEventListener('change', function (event) {
    render();
    if (event.target.name) announce(event.target);
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
