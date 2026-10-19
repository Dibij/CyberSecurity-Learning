---
title: "Reflected Cross-Site Scripting (XSS)"
type: concept
category: web-security
tags:
  - web-security
  - xss
  - injection
  - portswigger
aliases:
  - Reflected XSS
---

# Reflected Cross-Site Scripting (XSS)

Related notes:
- [[PortSwigger]] — Hands-on labs
- [[Stored XSS]] — Persistent XSS comparison
- [[DOM-Based XSS]] — Client-side XSS comparison
- [[HTTP Fundamentals]] — Request & response flow

---

## What is reflected cross-site scripting? 
Reflected cross-site scripting arises when an application receives data in an HTTP request that includes that data within the immediate response in an unsafe way.
Suppose a website has a search function which receives the user-supplied search term in a URL parameter:
`https://insecure-website.com/search?term=gift`
The application echoes the supplied search term in the response to this URL:
`<p> You Searched for: gift </p>`

Assuming the application doesn't perform any other processing of the data, an attacker can construct an attack like this:
`https://insecure-website.com/search?term=<script>/*+Bad+stuff+here+*/</script>`
This URL results in the following response:
`<p> You searched for: <script> /* Bad stuff here... */</script></p>`
If another user of the application requests the attacker's URL, then the script supplied by the attacker will execute in the victim user's browser, in the context of their session with the application.

> [!question] Q: How will another user request the attacker's URL? How will the attacker's URL even be served by the site?

Answer: So the process apparently goes like this.
1. The attacker first crafts a malicious payload, and create a link around this site, that will serve that up.
2. The attacker, then through Social Engineering / Phishing delivers that link through phishing emails, direct messages, social media posts, or embedded inside a malicious web page using an HTML anchor `(<a href="...">)` or an image redirect.
3.  When an unsuspecting victim clicks the link, their browser makes an outgoing HTTP GET request directly to the legitimate vulnerable website, passing the attacker's payload inside the URL parameters.

> [!question] Q: How is the attacker's payload even served by the site?

Answer: 
1. The vulnerable web application receives the request and extracts the input from the URL parameter without performing input sanitization, validation, or output encoding.
2. The server then builds the HTML response page and embeds that raw, unencoded input string directly back to the HTML body.
3. When the victim's browser receives the HTTP response, it treats the injected script tags as executable code rather than plain text, running the attacker's JavaScript under the victim's active session and security context on that domain.

> [!question] Q: Can you pass in an executable file? If so which languages? If not what is the process?

Answer: Reflected XSS does not automatically allow an executable to run on the victim's computer.
However, Reflected XSS can do these things: 

| ***Operation***                 | ***What it means***                                                  |
| ------------------------------- | -------------------------------------------------------------------- |
| Injecting Javascript            | Causing the browser to execute attacker-controlled script.           |
| Downloading a file              | Transferring file contents to the browser or another application     |
| Executing a downloaded file     | Running a program through the operating system                       |
| Exploiting the operating system | Abusing a separate vulnerability or permission to gain capabilities. |

Languages help separate the environment where it executes

| Language or technology         | Typical role in this context                                                                                                                                         |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **JavaScript**                 | Executes scripts within the browser; central to XSS                                                                                                                  |
| **HTML**                       | Structures the page and determines how injected markup is interpreted                                                                                                |
| **CSS**                        | Controls presentation; not a general-purpose mechanism for executing arbitrary programs                                                                              |
| **WebAssembly**                | Allows supported compiled code to run within the browser's WebAssembly environment, subject to browser security restrictions                                         |
| **Python, C, C++, Rust, etc.** | Can be used to build server-side applications or native executables, but XSS does not automatically execute these languages as native programs on a victim's machine |