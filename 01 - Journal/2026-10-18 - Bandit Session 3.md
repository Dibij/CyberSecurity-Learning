---
title: "2026-10-18 — Bandit Session 3 (Levels 21–32 Complete)"
type: journal
session: "006"
date: 2026-10-18
tags:
  - journal
  - bandit
  - overthewire
  - cron
  - git
  - privilege-escalation
  - shell-escape
aliases:
  - Bandit Session 3
  - Session 006
---

# Session 006 — Bandit Levels 21–32 (Complete!)

**Date:** 2026-10-18
**Platform:** [[OverTheWire Bandit]]
**Levels completed this session:** 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
**Status:** 🎉 OverTheWire Bandit is 100% COMPLETE!

---

## What I Did

Finished the rest of Bandit today. Solved 12 levels in one massive push from Level 21 all the way to 32.

### Level 21 → 22 (Self-hosted netcat listener)
Finally tackled the Level 21 puzzle I was stuck on yesterday. Understood that `suconnect` is a client that connects back to a port you specify. Spun up a listener on bandit with `nc -l <port>` and piped the password through, then connected with `suconnect` from another session. Got the password back in the listener.

### Level 22 → 23 (Cron inspection)
Inspected `/etc/cron.d/` and found `cronjob_bandit22.sh`. Read the script and saw it dumps the password to a specific file in `/tmp/`. Directly read that file to get the password.

### Level 23 → 24 (Reverse engineering script logic)
The cronjob script hashed the string `I am user <username>` with `md5sum`. Ran the exact same pipeline using `bandit23` as the username to predict the md5 filename in `/tmp`, and read the password directly.

### Level 24 → 25 (Cron spool exploit script)
Discovered that `/var/spool/bandit24/foo` executes any scripts in it as `bandit24` and then deletes them. Wrote my own shell script `exploit.sh` in `/tmp` that copies `/etc/bandit_pass/bandit24` to a world-writable file, made it executable, copied it to the spool folder, and waited for cron to trigger. Worked like a charm.

### Level 25 → 26 (4-digit PIN brute force)
Needed to provide the bandit24 password plus a 4-digit PIN (0000–9999) to a daemon on port 30002. Generated all 10,000 combinations into a file using a bash `for i in {0000..9999}` loop and piped `cat guesses.txt | nc localhost 30002`. Found the correct PIN and got the bandit25 password.

### Level 26 → 27 (Custom login shell / vi escape)
Bandit26's login shell was `/usr/bin/showtext`, which executes `more ~/text.txt`. Because the file was short, `more` would immediately exit and close the connection. Shrunk the terminal window so `more` was forced to pause, hit `v` to drop into `vi`, and escaped to a real shell using `:set shell=/bin/bash` followed by `:shell`.

### Level 27 → 28 (Post-escape password retrieval)
Used the shell gained from Level 26's escape to read `/etc/bandit_pass/bandit27`.

### Levels 28–31 (Git forensics & tricks)
Cloned repos from the server over SSH port 2220 to local machine:
- **Level 28:** Used `git log` to find the password in a previous commit diff before it was redacted.
- **Level 29:** Found the secret on a different branch using `git branch -a`, `git switch`, and `git log`.
- **Level 30:** Found secrets stashed in git tags using `git tag` and `git show <tag>`.
- **Level 31:** Bypassed `.gitignore` using `git add -f` to push the required file to the remote repository.

### Level 32 → Done (Restricted uppercase shell escape)
Encountered a restricted shell that converted every command to uppercase. Escaped it using `$0` (which refers to the current shell program) to spawn a fresh, unrestricted shell.

---

## Key Takeaways

| Concept | Technique / Command |
| :--- | :--- |
| Network Sockets | `nc -l -p <port>` to create your own receiving daemon |
| Cron Inspection | Check `/etc/cron.d/` for scheduled tasks and inspect automated scripts |
| MD5 / Shell Logic | Predictable hashes in scripts can be replicated locally (`md5sum \| cut -d ' ' -f 1`) |
| Scheduled Execution Exploits | Injecting executable shell scripts into automated spool directories |
| Brute Force Piping | `{0000..9999}` bash ranges piped directly over TCP sockets |
| Pager Breakout | Small terminal window forces `more` to page $\rightarrow$ press `v` $\rightarrow$ `vi` `:set shell=/bin/bash` $\rightarrow$ `:shell` |
| Git Forensics | `git log -p`, `git branch -a`, `git tag`, `git show` |
| Git Force Add | `git add -f <file>` to bypass `.gitignore` rules |
| Restricted Shell Breakout | `$0` expands to shell binary name, bypassing character/case filters |

---

## Reflection

Bandit is officially complete! 33 levels down. Started from basic `ls` and `cd`, worked through streams, text manipulation, compression pipelines, SSH keys, SSL/TLS, port scanning, cron vulnerabilities, custom script exploits, brute-forcing, pager breakouts, git internals, and restricted shell escapes.

Huge confidence boost. Ready to move onto TryHackMe next.

---

## Related Notes
- [[OverTheWire Bandit]] — Full 0–32 Walkthrough
- [[Linux CLI Utilities]] — Cron & CLI tools cheat-sheet
- [[Lab Tracker]] — Updated progress tracker
- [[2026-10-17 - Bandit Session 2]] — Session 005 (Levels 15–20)
