---
title: "Linux Fundamentals"
type: concept
category: linux
status: in-progress
tags:
  - linux
  - cli
  - fundamentals
aliases:
  - Linux
  - Linux Basics
---

# Linux Fundamentals

> Practical notes on the Linux CLI, standard streams, I/O redirection, piping, and common operations.

Related notes:
- [[OverTheWire Bandit]]
- [[Linux CLI Utilities]]
- [[Cyber-Security Home]]

---

## 1. Standard Streams & File Descriptors

Every process started in Linux opens three default data streams (represented by file descriptor numbers):

| FD | Name | Default Device | Description |
|---|---|---|---|
| `0` | `stdin` | Keyboard / terminal input | Standard input stream |
| `1` | `stdout` | Terminal screen | Standard output stream |
| `2` | `stderr` | Terminal screen | Standard error stream |

---

## 2. I/O Redirection

Redirection alters where a command reads its input from or where it sends its output.

### Standard Output Redirection (`>` and `>>`)
- `>` writes output to a file, **overwriting** any existing content:
  ```bash
  ls > directory_list.txt
  ```
- `>>` **appends** output to the end of a file:
  ```bash
  echo "New log line" >> activity.log
  ```

### Standard Input Redirection (`<`)
- `<` feeds a file's contents into a command as standard input:
  ```bash
  wc -l < tmp.txt
  ```

### Redirecting Errors (`2>`)
- `2>` redirects only error messages (`stderr`):
  ```bash
  find / -name "flag.txt" 2> errors.txt
  ```
- To suppress and discard error messages completely, redirect to `/dev/null`:
  ```bash
  find / -user bandit7 2>/dev/null
  ```

### Combining Output and Errors (`2>&1`)
- Redirect standard output to a file and merge standard error into the same stream:
  ```bash
  command > output.txt 2>&1
  ```
- Modern Bash shorthand:
  ```bash
  command &> output.txt
  ```

---

## 3. Piping (`|`)

Piping sends the standard output (`stdout`) of one command directly into the standard input (`stdin`) of another command without needing intermediate temporary files.

### Basic Examples
```bash
# View only the first 3 lines
ls | head -3

# View only the last 3 lines
ls | tail -3

# Extract line 3 specifically (first 3, then the last of those 3)
ls | head -3 | tail -1
```

### Chaining Multiple Commands
Commands can be chained across multiple stages:
```bash
# Save the extracted line into a file
ls | tail -3 | head -1 > tmp
```

### Advanced Pipeline Pattern
Analyzing user file ownership counts in a directory:
```bash
ls -l | tail -n +2 | sed 's/\s\s*/ /g' | cut -d ' ' -f 3 | sort | uniq -c
```
- `ls -l` — Detailed directory listing
- `tail -n +2` — Skip the first header line (`total ...`)
- `sed 's/\s\s*/ /g'` — Normalize multiple spaces to single spaces
- `cut -d ' ' -f 3` — Extract the 3rd field (owner column)
- `sort` — Sort names alphabetically (required before `uniq`)
- `uniq -c` — Count occurrences of each unique owner

---

## 4. Special Characters and Filename Handling

1. **Filenames starting with dashes (`-`):**
   - The shell treats `-` as a flag indicator.
   - Use `./-filename` or `--` (end-of-options delimiter):
     ```bash
     cat ./-
     cat -- -filename
     ```
2. **Filenames with spaces:**
   - Always quote arguments or escape spaces:
     ```bash
     cat "my secret notes.txt"
     cat my\ secret\ notes.txt
     ```
3. **Hidden files:**
   - Any file beginning with `.` is hidden from normal `ls`.
   - Use `ls -a` or `ls -la` to view them.