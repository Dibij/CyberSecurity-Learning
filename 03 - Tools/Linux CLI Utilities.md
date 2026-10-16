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
