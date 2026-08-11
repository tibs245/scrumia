# Tech — Slot index

## Structure

**No JavaScript opens or closes a row.** `name="slot"` groups the six
`<details>` elements into one native accordion; opening one closes the last,
entirely through the browser's own semantics. The alternative — a script
tracking which row is open — was rejected: `design/components/slot-index/spec.md`
already refuses a scripted open/close at the component level, and this
feature's job is to not reach for one either.
