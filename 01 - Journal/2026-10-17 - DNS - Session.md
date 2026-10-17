---
title: "Cybersecurity Learning Session — DNS — 2026-10-17"
type: journal
session: "003"
status: in-progress
tags:
  - journal
  - linux
  - dns
  - networking
---

# Cybersecurity Learning Session — DNS — 2026-10-17

**Session:** 003  
**Focus:** DNS Investigation & Local Resolver Mechanics  
**Status:** In progress / Paused for food & Bandit later today  

---

## 1. What I Worked On

### [[DNS#3. Where Could DNS Translation Fail?]]
I googled and looked into where could DNS fail?
- The answers are in the file, but in short: DNS can fail at almost every layer—cache mismatch at the lowest level, stale IPs at higher levels, DNS servers being down, or a resolver running into an issue it cannot resolve.

### [[DNS#1. What are the real upstream DNS servers for my device?]]
Well, the upstream DNS servers are the WorldLink server, and two servers up ahead. Still left to discover what those two servers actually are.

### [[DNS#2. Can you manually delete a stored DNS resolved cache ? If so how ?]]
Yes, using `sudo resolvectl flush-caches`.

### [[DNS#3. What will the effects of having the mismatch in cache be ?]]
Failure to get the IPs, broken connections, SSL certificate warnings, and potential hijacking.

### [[DNS#Why would a domain need multiple IPs?]]
To make sure the domain is not down if one server is overloaded (Load Balancing), for redundancy purposes, and for facilitating CDNs.

---

## 2. What Needs Deeper Exploring
- Explain those two servers at link1 and link2 (`enp7s0` vs `wlp8s0`).
- What is the process for resolving a mismatched IP?
- Why did query time change, and how does local TTL countdown work? (See [[DNS#Huh? it should have taken shorter so why did it take longer?]]).

---

## 3. Next Session Plan (Today's Agenda)
1. **Bandit continuation (~2 hours):**
   - Log in as `bandit13` using the private SSH key (`sshkey.private`).
   - Connect to port 30000 on localhost to retrieve the Bandit 14 password.
   - Continue pushing through the Bandit levels.
2. **Explore TryHackMe:**
   - Sign up / log into TryHackMe.
   - Start the beginner Linux or Pre-Security path to complement Bandit with structured labs.
3. **Follow-up DNS questions:**
   - See the new questions added to [[DNS#4. Questions to Investigate]].

---

## Related Notes
- [[DNS]]
- [[Network Path]]
- [[OverTheWire Bandit]]
- [[Cyber-Security Home]]
