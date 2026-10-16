---
title: "Networking Fundamentals"
type: concept
category: networking
status: in-progress
tags:
  - networking
  - fundamentals
---

# Networking Fundamentals

> Core concepts of computer networking: protocols, addressing, ports, and name resolution.

Related notes:
- [[DNS]]
- [[Network Path]]
- [[Learning Roadmap]]

---

## Key Pillars of Networking

### 1. Addressing & Identification
- **MAC Addresses:** Physical hardware address on local network segment (Layer 2).
- **IP Addresses:** Logical network address used for routing across networks (Layer 3).
  - IPv4: 32-bit (e.g. `192.168.1.1`)
  - IPv6: 128-bit (e.g. `fe80::1`)
  - Private vs. Public ranges (RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).

### 2. Transport & Ports
- **Ports (0–65535):** Logical communication endpoints that direct traffic to specific services running on a host.
  - Well-known ports: `22` (SSH), `53` (DNS), `80` (HTTP), `443` (HTTPS).
- **TCP (Transmission Control Protocol):** Connection-oriented, reliable, 3-way handshake (SYN -> SYN-ACK -> ACK).
- **UDP (User Datagram Protocol):** Connectionless, lightweight, no guarantee of delivery (used by DNS queries, streaming).

### 3. Name Resolution
- [[DNS]] — How human-readable domain names map to IP addresses.
- [[Network Path]] — How packets traverse layers and caching systems.
