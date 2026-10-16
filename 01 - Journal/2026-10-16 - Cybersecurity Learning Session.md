---
title: "Cybersecurity Learning Session — 2026-10-16"
type: journal
session: 002
status: completed
tags:
  - journal
  - linux
  - overthewire
---

# Cybersecurity Learning Session — 2026-10-16

**Session:** 002  
**Focus:** I/O Redirection, Piping, Text Transformations, and Nested Archive Decompression (Bandit Levels 9–13)  
**Status:** Completed for today  

---

## 1. What I Worked On

### OverTheWire: Bandit (Levels 9 through 13)
Continued the Linux track from Level 8 and completed 5 consecutive challenge levels:

- **Level 9 (Unique text):** Learned standard output/error redirection (`>`, `>>`, `<`, `2>`, `2>&1`) and piping (`|`). Used `strings data.txt | sort | uniq -c` to isolate the only unique string.
- **Level 10 (Printable text):** Used `strings data.txt | grep "==="` to locate passwords hidden among non-printable characters.
- **Level 11 (Base64):** Decoded base64 data directly using `base64 -d data.txt`.
- **Level 12 (ROT13):** Decoded a Caesar rotation cipher using `tr 'A-Za-z' 'N-ZA-Mn-za-m'`.
- **Level 13 (Nested Compression):** Practiced systematic reverse engineering of a multi-compressed file:
  - Reversing hexdump with `xxd -r`
  - Decompressing `gzip` with `gunzip -c`
  - Decompressing `bzip2` with `bunzip2 -d`
  - Extracting `tar` archives with `tar -xf`

See [[OverTheWire Bandit]] for the full step-by-step walkthrough.

---

## 2. Key Learnings & "Aha!" Moments

- **`uniq` requires sorted input:** `uniq` only checks adjacent lines. Running `strings data.txt | uniq` did not work because duplicate entries were scattered; piping through `sort` first was critical.
- **File extensions can lie:** In Level 13, files had generic or misleading names. Using `file <filename>` to inspect actual file headers before deciding which tool to run (`gunzip`, `bunzip2`, or `tar`) made solving the puzzle methodical.
- **Standard error vs standard output:** Redirecting errors using `2>/dev/null` keeps terminal output clean when searching restricted filesystems.
- **`tar` behavior:** `tar -xf` extracts files into the current working directory; unlike `gunzip -c`, it does not write file contents to stdout.

---

## 3. What I Still Need to Understand

- How SSH key-based authentication works (using `ssh -i private_key`) versus password authentication.
- How to submit data to a service listening on a specific localhost port (e.g., using `nc` / netcat).
- Unix permissions in detail (`chmod`, numeric representation like `755`, `600`).

---

## 4. Next Session Plan

1. Log into Bandit as `bandit13`.
2. Inspect the SSH private key stored in the home directory (`sshkey.private`).
3. Use the private key to connect to `bandit14` on `localhost`.
4. Connect to port 30000 on localhost to retrieve the Level 14 password.
5. Record steps in [[OverTheWire Bandit]] and save password in `.secrets/bandit_passwords.txt`.

---

## Related Notes

- [[OverTheWire Bandit]]
- [[Linux Fundamentals]]
- [[Linux CLI Utilities]]
- [[Lab Tracker]]
- [[Cyber-Security Home]]
