---
title: "2026-10-17 — Bandit Session 2 (Levels 15–20)"
type: journal
session: "005"
date: 2026-10-17
tags:
  - journal
  - bandit
  - overthewire
  - ssl
  - networking
  - setuid
aliases:
  - Bandit Session 2
  - Session 005
---

# Session 005 — Bandit Levels 15–20

**Date:** 2026-10-17 (late night, ~10 PM – midnight)
**Duration:** ~2 hours
**Platform:** [[OverTheWire Bandit]]
**Levels completed this session:** 15, 16, 17, 18, 19, 20
**Currently stuck on:** Level 21

---

## What I Did

This was a late-night sprint through 6 levels. Went in planning to do Bandit for 2 hours, ended up staying way longer because momentum.

### Level 15 → 16 (SSL/TLS with openssl)
Sent the password to port 30001 using `openssl s_client`. First time using SSL from the command line — turns out it's not that different from `nc`, you just wrap it in TLS. The `-quiet` flag was the key because without it it hangs waiting.

### Level 16 → 17 (nmap port scan + SSL → SSH key)
Had to find which port in 31000–32000 was actually listening *and* speaking SSL. Used `nmap -sV` which showed 5 ports but only one was `ssl/unknown` (port 31790). Submitting the password there gave me an SSH private key instead of a password — that was unexpected. Had to `scp` the key to my local machine, fix permissions with `chmod 600` (still need `/tmp/` because of the WSL/NTFS symlink issue I figured out last session).

### Level 17 → 18 (diff -y)
`diff -y` — side-by-side comparison. `man diff` led me straight to it. The changed line is marked with `|` so it was super obvious which line changed in passwords.new vs passwords.old. Done in like 2 minutes once I found the right flag.

### Level 18 → 19 (.bashrc bypass via SSH command)
The `.bashrc` logs you out on login (shows "Byebye!"). I had no idea what to do at first — tried to log in normally and it just kicked me. Then I figured out you can pass a command directly after the SSH string and it runs before the interactive shell (and therefore before `.bashrc`):
```bash
ssh -p 2220 bandit.labs.overthewire.org -l bandit18 "cat readme"
```
Got the password printed directly. Clean.

### Level 19 → 20 (setuid binary)
There was a binary called `bandit20-do` with the setuid bit (`-rwsr-x---`). Was confused at first because I tried calling `setuid()` as a function from the terminal (??). Then actually read the file listing and saw `bandit20-do`. It lets you run commands *as bandit20*, so:
```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

### Level 20 → 21 (STUCK — the listener puzzle)
This is where I hit a wall. The binary `suconnect` connects to a port *you specify* and reads the password. The hint says "connect to your own network daemon" — but I thought that meant inspecting my local machine's network daemons (`systemctl status NetworkManager`, `ss -tulnp`). Ran all those on my local machine, not on the bandit server. Then ran `nmap -p-` on bandit localhost to check open ports, tried `./suconnect` on various random ports. Nothing worked.

Figured out the mistake too late: the "network daemon" you create is a **listener you spin up yourself on the bandit server**. Level 21 requires two terminals (or background processes). Leaving it for tomorrow.

---

## Key Takeaways

| Concept | What I Learned |
| :--- | :--- |
| `openssl s_client` | Connects to SSL/TLS services from CLI. `-quiet` suppresses session info. |
| `nmap -sV` | Detects service versions on open ports — crucial for finding the SSL port |
| `diff -y` | Side-by-side file diff; `|` marks changed lines |
| SSH remote command execution | Append command to SSH string to bypass `.bashrc` |
| `setuid` binary | Runs as owner (e.g. bandit20), not the caller — allows privilege escalation within rules |
| `nc -lvnp` | Starts a listening netcat server. `-l` listen, `-v` verbose, `-n` no DNS, `-p` port |

---

## Emotions / Reflection

Honestly pumped. 6 levels in one night is a lot. But the Level 21 mistake was rough — why did I check my own laptop's NetworkManager when the challenge is clearly running on the bandit server?? The brain just jumped to the most familiar thing. 

Still — I went from not knowing what openssl is to understanding TLS handshakes, SSH private keys from SSL connections, setuid binaries, and `.bashrc` hijacking in one session. That's not nothing.

Tomorrow: Level 21. Two terminal approach. Spin up `nc -lvnp <port>` first, then `./suconnect <port>`. Probably going to try TryHackMe after.

---

## Related Notes
- [[OverTheWire Bandit]] — Full walkthrough
- [[Linux CLI Utilities]] — `diff`, `openssl`, `nmap`, `nc`, `ssh` added/updated this session
- [[2026-10-17 - Bandit - Session]] — Session 004 (Level 14, SSH keys, chmod)
- [[2026-10-17 - DNS - Session]] — Session 003 (earlier today)
