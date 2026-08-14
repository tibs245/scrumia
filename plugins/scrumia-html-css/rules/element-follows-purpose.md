# Element follows the purpose

The element matches the purpose, not the appearance. A `<div>` or `<span>` styled to look like a button, with `cursor: pointer` and an `onClick` handler, is not a button — it is a non-interactive element that mimics one. The W3C ARIA Authoring Practices Guide states that interactive controls must use the element whose contract matches the action, so that keyboard activation, focus, and assistive-technology behaviour are intrinsic rather than simulated.

**Source:** W3C ARIA Authoring Practices Guide (`https://www.w3.org/WAI/ARIA/apg/patterns/`). Licence: W3C documents ship under the W3C Document Licence.

**Refusal:** an interactive widget presented as a button, link, or other native control but implemented as `<div>` or `<span>` (or any element whose default contract does not match the action), with no `role` attribute and no native semantics. The element must be the one whose contract matches the purpose — `<button>` for an action, `<a href>` for navigation, `<input>` for data entry — not the one styled to look like it.
