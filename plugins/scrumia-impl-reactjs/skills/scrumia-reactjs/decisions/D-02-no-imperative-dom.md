# D-02: Refuse imperative DOM

**Status**: Adopted
**Date**: 2026-08-13
**Impacts**: [guides/01-components-and-props.md](../guides/01-components-and-props.md), [guides/03-control-flow.md](../guides/03-control-flow.md)

## Context

React owns the DOM it renders. Reaching past it with `element.style = …`,
`document.querySelector('…').focus()`, or any direct mutation fights React's own
reconciliation and produces races only visible on the next state change. React 19's
own page on the subject states the rule directly:

> "**Avoid changing DOM nodes managed by React.** Modifying, adding children to, or
> removing children from elements that are managed by React can lead to inconsistent
> visual results or crashes …"
> — [Manipulating the DOM with Refs — React](https://react.dev/learn/manipulating-the-dom-with-refs)

The same page scopes refs to non-destructive actions, which is the boundary this rule
preserves:

> "Refs are an escape hatch. You should only use them when you have to 'step outside
> React'. Common examples of this include managing focus, scroll position, or calling
> browser APIs that React does not expose."
> — [Manipulating the DOM with Refs — React](https://react.dev/learn/manipulating-the-dom-with-refs)

React 19 also makes the ref-as-prop change that reduces the legitimate need for the
imperative path: `ref` is now a regular prop on function components, and ref callbacks
may return cleanup functions for the resources they open.

> "New function components will no longer need `forwardRef` …"
> — [React 19 release notes](https://react.dev/blog/2024/12/05/react-19)

> "When the component unmounts, React will call the cleanup function returned from the
> `ref` callback."
> — [React 19 release notes — ref cleanup](https://react.dev/blog/2024/12/05/react-19)

## Arguments For

- **Race against reconciliation.** React's render output replaces whatever the
  imperative code wrote; the imperative write disappears on the next state change.
  *Visible only then.*
- **The ref-as-prop change reduces the legitimate need.** React 19 lets `ref` be a
  regular prop on function components, and ref callbacks return cleanups; both remove
  the usual excuses ("I need forwardRef to focus the input on mount").
- **A ref is still declarative at the call site.** `<input ref={node => node?.focus()} />`
  names what the component wants; `document.querySelector('input').focus()` from inside
  a `useEffect` names what the file happens to be touching.
- **It is a single source of truth.** A `<form action={search}>` that resets itself
  declaratively does not have a counterpart code path where the DOM is reset manually.

## Arguments Against (trade-offs accepted)

- For an integration with a third-party imperative widget that does not expose a
  declarative React API, imperative DOM is the only answer. The project override file
  records the exception without forking the module.
- Focusing a third-party input on mount may still need a ref-based `focus()` — the
  documented ref-as-prop pattern, used once, named in a comment.

## Verdict

Refuse imperative DOM for what React already renders. Reach for refs only when a
declarative primitive does not exist; name the exception in a comment, and prefer the
ref-as-prop pattern with a cleanup callback over an `useEffect` pair.
