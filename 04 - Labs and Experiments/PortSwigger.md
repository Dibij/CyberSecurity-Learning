---
title: "PortSwigger Web Security Academy Walkthrough"
type: lab-writeup
platform: PortSwigger
status: in-progress
current_lab: "Lab 2: Stored XSS into HTML context with nothing encoded"
tags:
  - lab
  - web-security
  - portswigger
  - xss
aliases:
  - PortSwigger Labs
  - Web Security Academy
---

# **PortSwigger Web Security Academy**

Related notes:
- [[Lab Tracker]]
- [[Reflected XSS]]
- [[Stored XSS]]
- [[DOM-Based XSS]]
- [[HTTP Fundamentals]]

> **NOTE:** Passwords/flags are saved locally in `_secrets/`.

---
## **Cross-Site Scripting (XSS)**

### Common Injection Contexts
1. **[[Reflected XSS]]:** An attacker crafts a malicious URL (e.g., through a search query or URL parameter) where the server immediately echoes the parameter back into the response page without sanitization.
2. **[[Stored XSS]]:** An attacker submits the payload into a persistent field (such as a comment box, profile name, or forum post) that gets saved to a database and served to every user who loads the page.
3. **[[DOM-Based XSS]]:** Client-side JavaScript takes data from an insecure source (like `location.search` or `window.location.hash`) and writes it directly to the DOM sink using properties like `innerHTML`.

### Basic XSS Payloads with `alert()`
1. **Standard script tag:**
   ```html
   <script>alert('XSS')</script>
   ```
   *If the application places this directly into the HTML body without encoding, the browser treats it as executable JavaScript.*
2. **Event Handler (Image Error):**
   ```html
   <img src="x" onerror="alert('XSS')">
   ```
   *The browser tries to load an invalid image source (`x`), triggers an `onerror` error event, and executes the `alert()` function.*
3. **Context-Aware Payload (Better Practice):**
   ```html
   <script>alert(document.domain)</script>
   ```
   *Instead of a generic number or string like `alert(1)`, displaying `document.domain` proves that code execution is happening within the context and origin scope of the target website.*

---

### **Lab 1: Reflected XSS into HTML context with nothing encoded**

> This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.
> To solve the lab, perform a cross-site scripting attack that calls the `alert` function.

Since i am jumping straight into this. I dont know how to do perform a cross-site scripting attack.
Let me search things up.

Well, there are apparently several ways to do this. For the purposes of this lab, injecting a standard script tag into the search query is the direct approach.

Since i now know this, letme try the lab.
i ran this: `<script>alert('XSS')</script>` and now got this: https://0afe00770397a739812f4d4e00a10001.web-security-academy.net/?search=%3Cscript%3Ealert%3E%28%27XSS%27%29%3C%2Fscript%3E
> # Server Error: Gateway Timeout (0) connecting to 0afe00770397a739812f4d4e00a10001.web-security-academy.net

What ? i face the error a few times, then i solve it another time ? ![[Pasted image 20261019113341.png]] huh ?? well. next level

> [!note] Gateway Timeout Gotcha
> The lab environment container was likely provisioning or waking up. Once it finished starting, reloading the search request processed the payload and completed the lab.

> [!tip] Quick Solution
> In the search bar on the home page, enter:
> ```html
> <script>alert(1)</script>
> ```
> Press enter. The application reflects the payload unsanitized into the response HTML:
> ```html
> <h1>0 search results for '<script>alert(1)</script>'</h1>
> ```
> The browser executes the `<script>` tag and triggers the popup.

---
### **Lab 2: Stored XSS into HTML context with nothing encoded**

> This lab contains a stored cross-site scripting vulnerability in the comment functionality.
> To solve this lab, submit a comment that calls the `alert` function when the blog post is viewed.

**Approach / Concept:**
Unlike reflected XSS where the payload lives in the URL, stored XSS gets saved permanently in the application's backend database. When anyone visits the blog post, the server fetches the comment from the database and inserts it unencoded into the page.

**Payload to submit in the Comment box:**
```html
<script>alert(document.domain)</script>
```
Fill out the required comment fields (Name, Email, Website), submit, and open the post to trigger.

---

## Current Status
- **Last Completed:** Lab 1: Reflected XSS into HTML context with nothing encoded ✅
- **Next Level / Step:** Lab 2: Stored XSS into HTML context with nothing encoded 🔄
- **Related Sessions:**
  - [[2026-10-19 - PortSwigger XSS Session]] — Session 007
