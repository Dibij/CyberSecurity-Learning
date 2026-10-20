---
title: "DOM-Based Cross-Site Scripting (DOM XSS)"
type: concept
category: web-security
tags:
  - web-security
  - xss
  - dom
  - javascript
  - portswigger
aliases:
  - DOM XSS
  - DOM-Based XSS
---

# DOM-Based Cross-Site Scripting (DOM XSS)

Related notes:
- [[PortSwigger]] — Hands-on labs
- [[Reflected XSS]] — Server-reflected comparison
- [[Stored XSS]] — Database-stored comparison
- [[HTTP Fundamentals]] — Request & response flow

---

## What is DOM-Based XSS?

**DOM-based XSS** (Document Object Model XSS) occurs when client-side JavaScript reads data from an untrusted **Source** (such as the URL hash or query string) and passes it to an unsafe **Sink** (such as `innerHTML` or `eval()`) that executes it dynamically in the browser.

Unlike Reflected and Stored XSS, **the server response itself often contains no malicious code whatsoever**. The payload is parsed and executed entirely on the client side by the browser's JavaScript engine manipulating the DOM tree.

---

## The Core Concept: Sources vs. Sinks

A DOM XSS vulnerability requires two components:
1. **Source:** An accessible JavaScript property or API through which user-controlled input enters the page.
2. **Sink:** A dangerous JavaScript function or DOM object that can execute code or render unencoded HTML if given malicious input.

### Common Sources (Where Input Enters)
| Source Property | Description |
|---|---|
| `location.search` | The query parameters in the URL (e.g. `?query=payload`). |
| `location.hash` | The fragment identifier after `#` (often never even sent to the server). |
| `location.href` / `document.URL` | The complete URL of the current page. |
| `document.referrer` | The address of the previous web page from which a link was followed. |
| `window.name` | The name attribute of the current window or iframe. |
| `document.cookie` | Locally stored cookies. |

### Dangerous Sinks (Where Execution Occurs)
| Sink Method / Property | Risk & Behavior |
|---|---|
| `document.write()` / `document.writeln()` | Writes raw HTML markup directly into the document stream. |
| `element.innerHTML` | Sets or gets HTML markup within an element, rendering injected tags. |
| `eval()` | Evaluates a string directly as executable JavaScript. |
| `setTimeout()` / `setInterval()` | If passed a string argument instead of a function, evaluates it as code. |
| `location.href` / `location.replace()` | Setting this to a `javascript:` URI executes arbitrary script. |

---

## Example Scenario

Suppose a web page contains this JavaScript script:

```html
<script>
  // Source: reading query string from the URL
  var searchParam = new URLSearchParams(window.location.search).get('q');

  // Sink: inserting raw string into the DOM
  document.getElementById('results').innerHTML = "Results for: " + searchParam;
</script>
```

If an attacker constructs this URL:
```text
https://example.com/search.html?q=<img src=x onerror=alert(document.domain)>
```

1. The browser requests the page; the server returns static HTML/JS.
2. The client script executes in the browser.
3. `searchParam` receives `<img src=x onerror=alert(document.domain)>`.
4. `innerHTML` parses that string into DOM elements, fails to load image `x`, and immediately fires the `onerror` JavaScript payload.

---

## Practical Sink Gotchas & Exploitation Rules

From hands-on testing across [[PortSwigger]] labs:

| Sink Context | Common Gotcha | Working Bypass Technique |
|---|---|---|
| **`document.write` inside attributes** | Input lands inside an existing tag attribute (e.g. `src="...query..."`). Plain `<script>` gets stuck inside the attribute string. | Break out of the attribute and tag first using `">` before injecting tags: `"><script>alert(1)</script>`. |
| **`innerHTML`** | HTML5 specification explicitly forbids `<script>` tags injected via `innerHTML` from executing. | Use HTML tags with inline event handlers that fire automatically: `<img src=x onerror="alert(1)">` or `<svg onload=alert(1)>`. |
| **Anchor `href` (jQuery / DOM)** | Input sets an `<a>` tag's `href` attribute. HTML markup like `<script>` or `"><script>` breaks the URL or fails to execute. | Use the **`javascript:` pseudo-protocol**: `javascript:alert(document.cookie)`. When clicked, the browser executes the script in the page origin context. |

---

## Defense & Remediation

1. **Use Safe Sinks:**
   - Prefer `element.textContent` instead of `element.innerHTML` when inserting text.
   - Use `element.setAttribute()` safely, avoiding `javascript:` pseudo-protocols.
2. **Sanitize Dynamic HTML:**
   - If rich HTML must be parsed on the client side, sanitize it first using trusted libraries like **DOMPurify**:
     ```javascript
     element.innerHTML = DOMPurify.sanitize(userInput);
     ```
3. **Avoid Code Evaluators:**
   - Never pass strings into `eval()`, `new Function()`, `setTimeout()`, or `setInterval()`.
