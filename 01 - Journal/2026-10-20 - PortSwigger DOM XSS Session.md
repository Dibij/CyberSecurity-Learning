---
title: "2026-10-20 — PortSwigger DOM XSS Session"
type: journal
session: "008"
date: 2026-10-20
tags:
  - journal
  - portswigger
  - web-security
  - xss
  - dom
aliases:
  - PortSwigger Session 2
  - Session 008
---

# Session 008 — PortSwigger DOM XSS Deep Dive (Labs 3–5)

**Date:** 2026-10-20
**Platform:** [[PortSwigger]] (Web Security Academy)
**Topic:** DOM-Based Cross-Site Scripting (DOM XSS)
**Labs Completed This Session:**
- Lab 3: DOM XSS in `document.write` sink using source `location.search` ✅
- Lab 4: DOM XSS in `innerHTML` sink using source `location.search` ✅
- Lab 5: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source ✅
**Status:** 4 PortSwigger labs solved in total (Lab 1, 3, 4, 5).

---

## What I Did & Learned Today

Dove headfirst into DOM-based vulnerabilities. This was much more disorienting than reflected XSS at first because you have to read client-side JavaScript code in the browser and trace where variables travel.

### 1. Lab 3 — `document.write` Attribute Breakout
- **The Confusion:** At first I tried inventing random paths in the URL (`/search.location?q=...` or `/document.write(alert)`), thinking the backend handled it. Realized `location.search` is just whatever query parameters are appended to the URL after `?`.
- **The Trap:** The script took the search query and dropped it inside an existing tag attribute:
  `document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">')`
- **The Fix:** A plain `<script>` gets eaten by the `src=""` attribute string. Had to break out of the quotes and close the tag first:
  `"><script>alert(1)</script>`

### 2. Lab 4 — `innerHTML` Spec Restriction
- **The Confusion:** Looked through the Inspect tab trying to find where `innerHTML` was used, got distracted by `labHeader.js`.
- **The Core Gotcha:** When user input is placed into an element via `innerHTML`, the HTML5 specification stops browsers from executing `<script>` tags for security!
- **The Bypass:** Event handlers still execute. Injected an image with an invalid source to force an error:
  `<img src=x onerror="alert(1)">`

### 3. Lab 5 — jQuery Anchor `href` & `javascript:` Protocol
- **The Discovery:** Found this script in the feedback page:
  `$('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));`
- **The Breakdown:** The parameter `returnPath` from the URL query string was directly assigned to the `href` attribute of the "Back" link.
- **The Breakthrough:** You can't inject `<script>` tags into an `href` URL context. Instead, browsers support the `javascript:` pseudo-protocol. Setting `returnPath=javascript:alert(document.cookie)` makes clicking the "Back" link execute the JavaScript directly!

---

## Key Takeaways

| Sink | Why `<script>` Might Fail | Working Technique |
|---|---|---|
| `document.write` in attributes | Trapped inside attribute quotes (`src="..."`) | Break out first with `">` then inject `<script>` |
| `element.innerHTML` | HTML5 spec blocks `<script>` execution in `innerHTML` | Use event handlers: `<img src=x onerror="alert(1)">` |
| `<a>` element `href` | `href` expects a URI, not raw HTML tags | Use `javascript:<payload>` protocol |

---

## Reflections & Next Steps

Reading someone else's client-side JavaScript without formal JS experience was intimidating today, and I relied on AI assistance for syntax hints. But understanding *why* each payload worked—attribute breakouts, HTML5 `innerHTML` limitations, and `javascript:` URLs—demystified DOM XSS significantly.

The goal now is to inspect the page source first, identify the **source** (`location.search`) and the **sink** (`document.write`, `innerHTML`, `attr('href')`), and determine the injection context before testing payloads.

**Next:** Back to Lab 2 (Stored XSS into HTML context with nothing encoded).

---

## Related Notes
- [[PortSwigger]] — Full lab walkthrough
- [[DOM-Based XSS]] — Concept note & practical rules
- [[Reflected XSS]] — Reflected injection comparison
- [[Lab Tracker]] — Updated progress tracker
