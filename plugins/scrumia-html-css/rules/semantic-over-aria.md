# Semantic element over ARIA role

When an interactive component expresses the same intent as a native HTML element, the native element wins. A `<div role="button">` carries keyboard activation (`Enter`, `Space`), focus management, and assistive-technology announcement by hand; a `<button>` carries them for free. The role attribute is the override layer the HTML specification reaches for when no element exists, not the route around one.

**Source:** MDN — Learn web development / HTML Accessibility (`https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML`). Licence: MDN content is CC BY-SA 4.0.

**Refusal:** an interactive component implemented as `<div role="...">`, `<span role="...">`, or any non-semantic element with a role attribute that names a behaviour a native HTML element already implements. The component must use the native element (`<button>`, `<a>`, `<input>`, `<select>`, `<textarea>`, `<label>`); ARIA applies only when no element exists.
