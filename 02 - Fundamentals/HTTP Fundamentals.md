---
title: "HTTP Fundamentals"
type: concept
category: web
status: not-started
tags:
  - web
  - http
  - fundamentals
---

# HTTP Fundamentals

> Hypertext Transfer Protocol: request/response cycle, methods, headers, and status codes.

Related notes:
- [[Networking Fundamentals]]
- [[Learning Roadmap]]

---

## 1. Request / Response Anatomy

HTTP operates as a client-server protocol over TCP (port 80 for HTTP, port 443 for HTTPS).

### HTTP Request Format
```http
GET /path/resource HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Authorization: Bearer <token>

[Optional Body Content]
```

### HTTP Response Format
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 1234
Set-Cookie: session_id=xyz; HttpOnly; Secure

<!DOCTYPE html>
<html>...</html>
```

---

## 2. Common HTTP Methods
- `GET` — Retrieve data without side effects.
- `POST` — Submit data to be processed (e.g., login forms, comments).
- `PUT` — Replace an entire resource with new data.
- `PATCH` — Partially modify an existing resource.
- `DELETE` — Remove a specified resource.
- `HEAD` — Retrieve headers only without the body.

---

## 3. Status Code Ranges
- `1xx` Informational (e.g. 101 Switching Protocols)
- `2xx` Success (e.g. 200 OK, 201 Created, 204 No Content)
- `3xx` Redirection (e.g. 301 Moved Permanently, 302 Found)
- `4xx` Client Errors (e.g. 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
- `5xx` Server Errors (e.g. 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable)
