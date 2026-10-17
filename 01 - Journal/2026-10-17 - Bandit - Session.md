---
title: "Cybersecurity Learning Session — Bandit Level 14 & SSH Keys — 2026-10-17"
type: journal
session: "004"
status: completed
tags:
  - journal
  - linux
  - overthewire
  - ssh
---

# Cybersecurity Learning Session — Bandit Level 14 — 2026-10-17

**Session:** 004 (Supplementary Session)  
**Focus:** SSH Private Keys, Strict File Permissions (`chmod 600`), `scp` Remote Copy, and WSL/NTFS Permission Quirks  
**Status:** Completed  

---

## 1. What I Worked On

### OverTheWire: Bandit (Level 14)
- **Objective:** The password for Level 14 is stored in `/etc/bandit_pass/bandit14`, readable only by user `bandit14`. Instead of a password, Level 13 provided an SSH private key (`sshkey.private`) to log in as `bandit14`.
- **Exploration & Tool Research:**
  - Researched `ssh -i` (identity file flag) and `scp` (secure copy).
  - Attempted to install the key into `/tmp` on the remote server, but inter-level connections from localhost were blocked by the OverTheWire firewall.
  - Used `scp -P 2220` from my local terminal to securely download `my_key` from the Bandit server onto my local Linux environment.
  - Ran into the classic SSH security barrier: `Permissions 0755 for 'my_key' are too open... This private key will be ignored.`
  - Discovered that `chmod 600` fails silently on files stored on Windows NTFS-mounted partitions in WSL.
  - Solved it by moving the key to native Linux storage (`/tmp/random_key_for_bandit`), successfully setting `chmod 600`, and authenticating into `bandit14`.
  - Read `/etc/bandit_pass/bandit14` and saved the password in [[Bandit Passwords]].

See [[OverTheWire Bandit#Level 14]] for the full raw walkthrough and terminal logs.

---

## 2. Key Learnings & "Aha!" Moments

- **SSH demands strict private key permissions:** SSH explicitly refuses to use any private key file that other users could read. It requires permissions set to `600` (read/write for owner only) or `400` (read-only for owner).
- **WSL / Windows NTFS Gotcha:** If your project directory is located on a Windows NTFS mount (or symlinked drive), Linux permission bits (`chmod`) cannot be applied natively. Moving sensitive files (like keys) to a native Linux path like `/tmp/` allows `chmod 600` to work properly.
- **`scp` port flag is capital `-P`:** While `ssh` uses lowercase `-p 2220`, `scp` requires uppercase `-P 2220`.
- **Tools updated:** Documented `ssh`, `scp`, `chmod`, `umask`, and `nc` in [[Linux CLI Utilities]].

---

## 3. Next Session Plan

1. **Bandit Level 15:**
   - Log into Bandit as `bandit14`.
   - Use `nc` (netcat) to submit the current password to port `30000` on `localhost`:
     ```bash
     echo "<bandit14_password>" | nc localhost 30000
     ```
   - Record response, capture Bandit 15 password in [[Bandit Passwords]], and document in [[OverTheWire Bandit]].
2. **Explore TryHackMe:**
   - Begin structured beginner Linux / networking modules on TryHackMe.

---

## Related Notes
- [[OverTheWire Bandit]]
- [[Bandit Passwords]]
- [[Linux CLI Utilities]]
- [[Cyber-Security Home]]
- [[2026-10-17 - DNS - Session]]
