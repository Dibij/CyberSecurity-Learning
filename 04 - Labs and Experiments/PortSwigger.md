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
### **Lab 3: DOM XSS in `document.write` sink using source `location.search`**

>This lab contains a DOM-based cross-site scripting vulnerability in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL.
>
To solve this lab, perform a cross-site scripting attack that calls the `alert` function.

I honestly dont understand what this wants me to do. so i added this part 
`search.location?q=<alert(document.domain)>` after the site url for the lab. But it just lead me to wahtever, and shows just *"Not Found"*. Do i inspect source? and write code in the terminal given by the broswer? or what ? ? 

Then i tried this
```
https://0a89000403a435f0835a3c0d005b00a2.web-security-academy.net/search.location?q=%3Calert(document.write())%3E
```
This didnot work and neither did  this
```
https://0a89000403a435f0835a3c0d005b00a2.web-security-academy.net/document.write(alert)
```
Apparently the goal is not to invent new url paths, but to modify existing paths.
And the vulnerabiltiy this site has is that its location.search allows untested string to be passed directly to the server. I still dont know enough to epxlain properly but just the search bar on this lab lets me access things i should not be able to.
Ok i solved the lab. I got help from claude, but what happened was, apparently i needed to close the image tag then add my script like this
```html
"><script>alert(1)</script>
```
And that solved the issue.
I need to be able to findout about these vulnerabalities and actually work on my own, instead of takign help from ai

> [!tip] Quick Solution & Technical Breakdown
> **Why `"><script>alert(1)</script>` works:**
> If you inspect the page source, you'll find this tracking script:
> ```javascript
> function trackSearch(query) {
>     document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">');
> }
> var query = (new URLSearchParams(window.location.search)).get('search');
> if(query) {
>     trackSearch(query);
> }
> ```
> 1. The input `query` is placed directly inside the `src="..."` attribute of an `<img>` tag written by `document.write()`.
> 2. The leading `"` breaks out of the `src="..."` attribute string.
> 3. The `>` closes the `<img>` tag early: `<img src="/resources/images/tracker.gif?searchTerms=">`.
> 4. The following `<script>alert(1)</script>` is written to the DOM as its own independent HTML element and executes.

---
### **Lab 4: DOM XSS in `innerHTML` sink using source `location.search`**
 
> This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an `innerHTML` assignment, which changes the HTML contents of a `div` element, using data from `location.search`.
>
> To solve this lab, perform a cross-site scripting attack that calls the `alert` function.

i dont understand what it means by innerHTML assignment? i cant find it in the 'Inspect' tab.
Though i did find one in https://0a5f00fb03e855a280d33a3e00970053.web-security-academy.net/resources/labheader/js/labHeader.js at line 25
```js
newWebSocket.onmessage = function (evt) {
                const labSolved = document.getElementById('notification-labsolved');
                const keepAliveMsg = evt.data === 'PONG';
                if (labSolved || keepAliveMsg) {
                    return;
                }
                document.getElementById("academyLabHeader").innerHTML = evt.data;
                animateLabHeader();

                for (const listener of completedListeners) {
                    listener();
                }
            };
```
So we have to modify this ? but i dont know js
Ok i solved the lab and i "searched" this in the search box
` <img src=x onerror="alert(1)"> `.
Main problems are i dont understand what the labs want from me, and second i dunno know how to view for thevulnerabilities

> [!tip] Quick Solution & Technical Breakdown
> **Why `<script>` fails but `<img ... onerror=...>` works:**
> If you inspect the page's search script (in the main HTML source, not labHeader.js):
> ```javascript
> function doSearchQuery(query) {
>     document.getElementById('searchMessage').innerHTML = query;
> }
> var query = (new URLSearchParams(window.location.search)).get('search');
> if(query) {
>     doSearchQuery(query);
> }
> ```
> 1. **The HTML5 spec restriction:** Modern browsers deliberately do not execute `<script>` elements that are added via `element.innerHTML`.
> 2. **The event-handler bypass:** However, when an `<img>` tag with an invalid `src` is placed into `innerHTML`, the browser parses the element into the DOM, attempts to fetch image `x`, fails, and immediately triggers the `onerror` JavaScript handler:
>    ```html
>    <img src=x onerror="alert(1)">
>    ```

---
### **Lab 5: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source**
 
> This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. It uses the jQuery library's `$` selector function to find an anchor element, and changes its `href` attribute using data from `location.search`.
>
> To solve this lab, make the "back" link alert `document.cookie`.

So based on the description, i need to go to submist feedback page first.

So as far as i have done, i have only like searched the search bozes. So how do i change the 'back' link to alert something ?? 
First i also need to look into what document.cookie is.
So document.cookie seems to be a source. 
So in 'Page inspect ' ill search for document.cookie.

but it shows nothing for `document.cookie` ? 

But i was able to find `'back'` link. and it seems to be just `href="/"`
So how do i edit it ?? i doubt i jsut edit the code but this href doesnot take anything so ?? 
ooh wait
```js
   $(function() {
                                $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
                            });
```
i was able to find this. lets explore it.
so i dont understand js, but it seems like backlink is tied to `window.location.search` i hope that means the search button, but ther's no search page in the lab. so what does this mean ? lemme google it i dont understand this code 
So apparently this means that 
**This script allows a webpage to have a dynamic "Back" button or link.**
means, if i put up a script or a url, in the url box, and click on the 'back' button in this page. It will try to get me to that link, or i could use it to alert for document.cookie. 
well this 
```
https://0a1e00ce0388e48280920dab002800cd.web-security-academy.net/feedback?returnPath=<script>alert(document.cookie)</script>
```
did not work. 
so ?  neither did this work? 
```
https://0a1e00ce0388e48280920dab002800cd.web-security-academy.net/%22%3E%3Cscript%3Ealert(document.cookie)%3C/script%3E
```

Now it makes sense. 
href wants javascript code, and not url based html code
so this should work:
```
https://0a1e00ce0388e48280920dab002800cd.web-security-academy.net/feedback?returnPath=javascript:alert(document.cookie)
```
it worked.

> [!tip] Quick Solution & Technical Breakdown
> **Why `returnPath=javascript:alert(document.cookie)` works:**
> 1. The jQuery script extracts `returnPath` from `window.location.search` and sets it directly as the anchor's `href` attribute without protocol validation:
>    ```javascript
>    $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
>    ```
> 2. When an `<a>` tag has `href="javascript:..."`, the browser interprets it using the **`javascript:` pseudo-protocol**.
> 3. Instead of navigating to a URL or submitting HTML, clicking the "Back" link immediately executes the JavaScript payload inside the page origin context, alerting `document.cookie`.

---

## Current Status
- **Completed Labs:**
  - Lab 1: Reflected XSS into HTML context with nothing encoded ✅
  - Lab 3: DOM XSS in `document.write` sink using source `location.search` ✅
  - Lab 4: DOM XSS in `innerHTML` sink using source `location.search` ✅
  - Lab 5: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source ✅
- **Pending / Next:**
  - Lab 2: Stored XSS into HTML context with nothing encoded 🔄
- **Related Sessions:**
  - [[2026-10-20 - PortSwigger DOM XSS Session]] — Session 008 (DOM sinks: document.write, innerHTML, jQuery href)
  - [[2026-10-19 - PortSwigger XSS Session]] — Session 007 (Reflected XSS kickoff)

