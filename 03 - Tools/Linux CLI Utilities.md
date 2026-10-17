---
title: "Linux CLI Utilities Cheat-Sheet"
type: tool
category: cli
tags:
  - tools
  - cli
  - linux
  - cheat-sheet
aliases:
  - CLI Tools
  - Linux Tools
---

# Linux CLI Utilities Cheat-Sheet

> Quick reference for text processing, inspection, decompression, and search utilities.

Related notes:
- [[Linux Fundamentals]]
- [[OverTheWire Bandit]]

---

## 1. Text Searching & Inspection

### `file` — Inspect File Type
Determines file type from magic bytes rather than file extensions.
```bash
file target_file
file inhere/*
```

### `strings` — Extract Printable Text
Extracts printable ASCII / UTF-8 strings from binary files.
```bash
strings data.txt
strings data.txt | grep "==="
```

### `grep` — Pattern Searching
Searches for text or regex patterns.
```bash
grep "keyword" filename
grep -i "case-insensitive" filename
grep -r "recursive_search" ./directory/
grep -v "invert_match (exclude)" filename
```

### `sort` & `uniq` — Sorting and Deduplication
> **Rule:** `uniq` only detects adjacent duplicate lines. **Always sort before using uniq.**

```bash
# Sort lines alphabetically
sort filename

# Count occurrences of each line
sort filename | uniq -c

# Show only lines that occur exactly once
sort filename | uniq -u

# Show only lines that occur more than once (duplicates)
sort filename | uniq -d
```

### `tr` — Character Translation & Deletion
Translates, squeezes, or deletes characters from standard input.
```bash
# ROT13 Caesar cipher decode
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'

# Convert uppercase to lowercase
cat file.txt | tr 'A-Z' 'a-z'

# Delete specific characters (e.g. carriage returns)
cat file.txt | tr -d '\r'
```

### `base64` — Base64 Encode / Decode
```bash
# Encode
echo -n "admin" | base64

# Decode
base64 -d data.txt
echo "YWRtaW4=" | base64 -d
```

---

## 2. Searching Filesystem (`find`)

Searches the directory tree based on criteria.
```bash
# Search by exact name
find /path -name "filename.txt"

# Search by file size (c = bytes, k = KB, M = MB)
find . -size 1033c

# Search by owner and group
find / -user bandit7 -group bandit6 2>/dev/null

# Non-executable files only
find . -type f ! -executable
```

---

## 3. Compression, Archives & Hex Dumps

### `xxd` — Hexadecimal Dumps
```bash
# View hexdump
xxd file.bin

# Reverse hexdump back to binary
xxd -r data.txt > output.bin
```

### `tar` — Tape Archive
Bundles multiple files into a single `.tar` archive (does not compress by itself unless paired with gzip/bzip2).
```bash
# Extract tar archive
tar -xf archive.tar

# List contents without extracting
tar -tf archive.tar

# Create tar archive
tar -cf archive.tar file1 dir1/
```

### `gzip` & `gunzip` — GZIP Compression
```bash
# Decompress and write to stdout (-c preserves original file)
gunzip -c file.gz > decompressed_file

# Decompress in-place (replaces file.gz with file)
gunzip file.gz
```

### `bzip2` & `bunzip2` — BZIP2 Compression
```bash
# Decompress in-place
bunzip2 -d file.bz2

# Decompress and keep original file (-k)
bunzip2 -dk file.bz2
```

---

## 4. Remote Access & File Transfer

### `ssh` — Secure Shell
SSH is a program for logging into a remote machine and for executing commands on a remote machine.

**Common Flags:**
- `-p <port>` — Specify port to connect to (e.g. `-p 2220`)
- `-i <keyfile>` — Identity file (selects a private key for public-key authentication)
- `-l <username>` — Selecting username (alternative to `username@host`)
- `-4` — Forces SSH to use IPv4 only
- `-6` — Forces SSH to use IPv6 only
- `-A` — Enables forwarding of connection from an authentication agent
- `-a` — Disables forwarding such connection

**Example:**
```bash
ssh -i /path/to/key -p 2220 bandit.labs.overthewire.org -l bandit14
```

### `scp` — Secure Copy Protocol
`scp` copies files between hosts on a network using an encrypted SSH connection.

```bash
# Basic format:
scp username@remote_host_ip:/path/to/remote/file /path/to/local/destination

# Specifying a custom port (NOTE: uses capital -P):
scp -P 2220 bandit13@bandit.labs.overthewire.org:/remote/path/my_key /local/destination/
```

---

## 5. File Permissions & Masks

### `chmod` — Change File Mode / Permissions
`chmod` is used for changing access modes/permissions of files and directories.

- `chmod 600 file` — Read & Write for owner only (`-rw-------`). **Required for SSH private keys!**
- `chmod 700 file` — Read, Write, & Execute for owner only.
- `chmod 755 file` — Read & Execute for everyone, Write for owner.

### `umask` — User Mask
`umask` is used to strip away default permissions when new files or directories are created.
- A umask of `077` ensures newly created files are only readable/writable by the owner.

---

## 6. Network Connections & Raw Sockets (Unencrypted)

### `nc` (Netcat) — Arbitrary TCP and UDP Connections
Netcat allows you to manually open up a raw socket pipe to send and receive data across a network connection.

```bash
# Connect to a TCP port:
nc localhost 30000

# Send data and pipe output:
echo "current_password" | nc localhost 30000

# Listen on a port (create a server listener):
nc -lvnp 4444
```

### `ncat` — Modern Netcat (from Nmap project)
An improved implementation of Netcat that includes built-in support for SSL/TLS, access control, and proxies.

```bash
# Connect to a plain TCP port:
ncat localhost 30000

# Connect to an SSL/TLS encrypted port:
ncat --ssl localhost 30001

# Listen with SSL:
ncat -lvnp 4444 --ssl
```

### `telnet` — Basic Interactive TCP Connection
An unencrypted protocol and diagnostic tool often used to test if a TCP port is open and accepting text input.

```bash
# Connect to host on port:
telnet localhost 30000

# To exit telnet: press Ctrl + ] then type 'quit'
```

### `socat` — Multipurpose Bidirectional Relay (Socket Cat)
Establishes two bidirectional byte streams and transfers data between them. Very powerful for port forwarding, raw sockets, and encrypted tunnels.

```bash
# Connect standard I/O to a TCP port (like netcat):
socat - TCP:localhost:30000

# Connect standard I/O to an SSL/TLS encrypted port:
socat - OPENSSL:localhost:30001,verify=0
```

---

## 7. Encrypted Connections (SSL / TLS)

### `openssl s_client` — Generic SSL/TLS Client
Connects to any remote service running over SSL/TLS (like HTTPS, SMTPS, or custom encrypted wargame ports).

```bash
# Connect to an SSL/TLS port (interactive):
openssl s_client -connect localhost:30001

# Connect quietly without printing the full certificate chain:
openssl s_client -quiet -connect localhost:30001

# Send password directly into an SSL port:
echo "current_password" | openssl s_client -quiet -connect localhost:30001
```

---

## 8. Port Scanning & Socket Inspection

### `ss` — Socket Statistics (Modern replacement for `netstat`)
Dumps socket statistics directly from the Linux kernel. Faster and more detailed than `netstat`.

```bash
# Show listening TCP sockets with process names and port numbers:
ss -tlpn

# Show listening TCP and UDP sockets:
ss -tulpn

# Common Flags:
# -t : TCP sockets
# -u : UDP sockets
# -l : Listening sockets only
# -p : Show process using the socket (requires sudo/permissions)
# -n : Numeric output (show 30000 instead of service names)
```

### `netstat` — Network Statistics (Classic utility)
Legacy command for inspecting network connections, routing tables, and interface statistics.

```bash
# Show listening TCP ports with process and numeric addresses:
netstat -tlpn

# Show all active listening and established connections:
netstat -tuna
```

### `nmap` — Network Mapper & Port Scanner
Scans target hosts or localhost to identify open ports, active services, and OS fingerprints.

```bash
# Scan a specific port range on localhost:
nmap -p 31000-32000 localhost

# Scan all 65,535 ports:
nmap -p- localhost

# Service version detection on open ports:
nmap -sV -p 31000-32000 localhost

# Scan open ports quietly with fast timing (-T4):
nmap -T4 -p 31000-32000 localhost
```


