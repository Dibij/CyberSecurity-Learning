---
title: "Stored Cross-Site Scripting (Persistent XSS)"
type: concept
category: web-security
tags:
  - web-security
  - xss
  - injection
  - portswigger
aliases:
  - Stored XSS
  - Persistent XSS
---

# Stored Cross-Site Scripting (Persistent XSS)

Related notes:
- [[PortSwigger]] — Hands-on labs (Lab 2)
- [[Reflected XSS]] — Non-persistent comparison
- [[DOM-Based XSS]] — Client-side comparison
- [[HTTP Fundamentals]] — Request & response flow

---

## What is Stored Cross-Site Scripting?

**Stored XSS** (also known as **Persistent XSS** or **Second-Order XSS**) occurs when a web application receives malicious, attacker-supplied data and stores it permanently in a backend datastore (such as a database, comment feed, filesystem, or notification log). 

Whenever any other user subsequently visits the page displaying that stored content, the malicious script is pulled from the database and included directly in the server's HTML response, executing inside the victim's browser context.

```
Attacker                         Vulnerable Server & DB                      Victims
   │                                       │                                    │
   ├── 1. POST comment with payload ──────►│                                    │
   │      <script>alert(1)</script>        ├── 2. Stores in Database            │
   │                                       │      (without encoding)            │
   │                                       │                                    │
   │                                       │◄── 3. GET /blog/post-123 ──────────┤
   │                                       │                                    │
   │                                       ├── 4. Serves HTML with stored ─────►│
   │                                       │      payload embedded              ├── 5. Executes payload
   │                                       │                                    │      in victim session!
```

---

## Stored vs. Reflected XSS

| Characteristic | Reflected XSS | Stored XSS |
|---|---|---|
| **Persistence** | Ephemeral — lives only in the immediate request/response cycle. | Persistent — saved in the server database or backend storage. |
| **Delivery Vector** | Requires tricking victim into clicking a specially crafted URL / link. | Self-serving — triggers automatically whenever any user views the infected page. |
| **Reach & Impact** | One victim per clicked link. | Potentially thousands of users (including administrators) browsing legitimate pages. |
| **Discovery Ease** | Fast to find via URL parameters & search bars. | Requires testing input forms that write to backend state (comments, profiles, logs). |

---

## Common Injection Targets

1. **Comment Sections & Forum Posts:** Blog comments, product reviews, discussion threads.
2. **User Profiles:** Display names, bios, status updates, avatars.
3. **Internal / Administrative Panels:** Contact forms, support tickets, error log viewers (where attackers exploit admin eyes).
4. **Order & Billing Details:** Shipping address fields, order notes.

---

## Basic Proof-of-Concept (PoC) Payloads

```html
<!-- Standard script tag -->
<script>alert(document.domain)</script>

<!-- Event handler on broken image -->
<img src="x" onerror="alert(document.cookie)">

<!-- Autofocus input tag -->
<input autofocus onfocus="alert(1)">
```

---

## Defensive Countermeasures

1. **Context-Aware Output Encoding:** Always HTML-entity encode untrusted data (`<` $\rightarrow$ `&lt;`, `>` $\rightarrow$ `&gt;`, `"` $\rightarrow$ `&quot;`) before rendering it into the HTML body.
2. **Input Sanitization:** Strip dangerous HTML tags and attributes using well-tested libraries (e.g., DOMPurify) if rich-text formatting is required.
3. **Content Security Policy (CSP):** Restrict inline script execution and enforce trusted script origins via HTTP response headers.
4. **`HttpOnly` Cookie Flags:** Prevent JavaScript from accessing sensitive session tokens even if XSS occurs.
