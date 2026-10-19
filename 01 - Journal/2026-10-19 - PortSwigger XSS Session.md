---
title: "2026-10-19 — PortSwigger XSS Session"
type: journal
session: "007"
date: 2026-10-19
tags:
  - journal
  - portswigger
  - web-security
  - xss
  - injection
aliases:
  - PortSwigger Session 1
  - Session 007
---

# Session 007 — PortSwigger Web Security Academy (XSS Kickoff)

**Date:** 2026-10-19
**Platform:** [[PortSwigger]] (Web Security Academy)
**Topics:** Cross-Site Scripting (XSS) — Reflected, Stored, DOM-Based
**Labs Completed:** Lab 1 (Reflected XSS into HTML context with nothing encoded)
**Current Objective:** Lab 2 (Stored XSS into HTML context with nothing encoded)

---

## What I Did

Switched gears from Linux CLI wargames (Bandit) to practical Web Application Security, starting PortSwigger's Web Security Academy tracks.

### 1. XSS Core Mechanics & Types
Mapped out the three primary categories of XSS:
- **[[Reflected XSS]]:** Non-persistent. The server immediately reflects unencoded user input from the HTTP request into the response body.
- **[[Stored XSS]]:** Persistent. The payload is stored in the backend database (comments, profile fields) and served automatically to anyone viewing that resource.
- **[[DOM-Based XSS]]:** Client-side. The server sends clean markup, but browser JavaScript reads from an untrusted source (`location.search`) and writes to a dangerous sink (`innerHTML`).

### 2. Dissecting How Attacks Actually Work
Looked into key conceptual questions about real-world exploitation:
- **Delivery:** Attackers don't alter the server directly for reflected XSS; they deliver specially crafted URLs through social engineering / phishing.
- **Server behavior:** The server naively concatenates input parameters into HTML output without entity encoding (`<` to `&lt;`), leading the browser to treat characters as code.
- **Scope & Execution boundaries:** Clarified that XSS executes inside the browser's JavaScript sandbox under the origin domain context — it does not directly run arbitrary native system binaries (like C or Python executables) unless chained with browser escape / local client vulnerabilities.

### 3. Lab 1: Reflected XSS into HTML Context with Nothing Encoded (Solved!)
- Target: Search bar on the blog app.
- Input: `<script>alert('XSS')</script>`
- Encountered a Gateway Timeout (504) while the lab container was waking up, but reloading the request reflected the payload into the page body (`<h1>0 search results for '<script>alert('XSS')</script>'</h1>`), successfully popping the alert dialog and completing the lab.

### 4. Lab 2: Stored XSS into HTML Context with Nothing Encoded (Up Next)
- Target: Blog comment section.
- Strategy: Submit `<script>alert(document.domain)</script>` into the comment body so it saves to the database and triggers whenever the post is viewed.

---

## Key Takeaways

| Concept | Explanation |
|---|---|
| Reflected XSS | Injected payload echoes immediately off the server into the response page. |
| Stored XSS | Injected payload persists in the backend datastore and executes for subsequent visitors. |
| DOM XSS | Vulnerability lives entirely in client-side JavaScript execution (Source $\rightarrow$ Sink). |
| Alert Verification | Using `alert(document.domain)` is standard practice to confirm execution within the target site's origin scope. |

---

## Related Notes
- [[PortSwigger]] — Full lab walkthrough tracker
- [[Reflected XSS]] — Concept note & Q&A
- [[Stored XSS]] — Persistent XSS mechanics
- [[DOM-Based XSS]] — Sources and sinks
- [[Lab Tracker]] — Updated progress across labs
