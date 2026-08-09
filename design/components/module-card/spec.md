# module-card

One installable module: what it is, which slot it answers, what it costs to add,
and the command that adds it.

## When to use it

In a grid of things a reader can install. The card ends on `.mod-cmd` because the
command is the point — a module the reader cannot install is documentation, and
belongs in a table instead.

Anatomy, in order:

- `.mod-ico` — one emoji, the only decorative element on the card
- `.mod-name` — the plugin's real id, mono, never prettified. Links to the module's
  own page when one is generated for it (`modules/<name>.html`) — underlined by the
  page's default link style, not a second accent colour, so the card still points
  with only the command at the bottom
- `.mod-slot` — the slot it fills, or `kernel` / `no slot`
- `.mod-desc` — one or two sentences, what it does and what it needs
- `.mod-foot` — `.pill`s: availability first, then contents (skills, agents, hooks)
- `.mod-cmd` — the exact install command, copyable by eye

## When not to use it

- **A capability with no module behind it.** That is `slot-index`, empty row.
- **A comparison.** Cards sit side by side but do not align field to field. Use a
  table when the reader's job is to compare rather than to pick.

## What it refuses

- **A call-to-action button.** The command *is* the action. A button next to it
  would offer a second, worse way to do the same thing.
- **A count that hides a list.** `3 skills` is a pill; naming those three skills is
  the reference page's job, not the card's.
- **Marketing tone in `.mod-desc`.** Mechanism over claim: say what it does, say
  what it needs. "Powerful" is not a fact about a module.
