---
title: "Network Path"
type: concept
category: networking
status: in-progress
tags:
  - networking
  - fundamentals
---

# Network Path

> The journey of a packet or DNS request from user application to target destination.

Related notes:
- [[DNS]]
- [[Networking Fundamentals]]

---

## 1. The DNS Resolution Path

When an application (like your browser) requests a web resource (e.g. `https://example.com`), the name resolution follows this hierarchical path:

```
[Browser Cache]
      │
      ▼ (cache miss)
[Operating System Cache / hosts file]
      │
      ▼ (cache miss)
[Local Router / Gateway DNS Cache]
      │
      ▼ (cache miss)
[ISP / Recursive Resolver] (e.g. 1.1.1.1, 8.8.8.8)
      │
      ├─► [Root Nameserver] (.)
      │
      ├─► [TLD Nameserver] (.com)
      │
      └─► [Authoritative Nameserver] (ns1.example.com) ──► Returns IP
```

---

## 2. Where Caching Happens

To minimize latency and prevent overwhelming DNS servers, responses are cached at multiple layers based on their **TTL** (Time To Live):
1. **Application Layer:** Browser memory cache.
2. **OS Layer:** Local DNS resolver service (e.g. `systemd-resolved` on Linux).
3. **Local Area Network:** Home/office router cache.
4. **Upstream Resolver:** Recursive DNS resolver cache.
