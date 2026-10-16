---
title: "OverTheWire: Bandit Walkthrough"
type: lab-writeup
platform: OverTheWire
status: in-progress
current_level: 13
tags:
  - lab
  - wargame
  - linux
  - overthewire
aliases:
  - Over The Wire
  - Bandit
---

# OverTheWire: Bandit Learning Journal

Related notes:
- [[Linux Fundamentals]]
- [[Linux CLI Utilities]]
- [[Lab Tracker]]
- [[Learning Roadmap]]
- [[2026-10-15 - Cybersecurity Learning Session]]
- [[2026-10-16 - Cybersecurity Learning Session]]

> [!note] Password Storage
> Wargame passwords are kept securely out of Git in `.secrets/bandit_passwords.txt`.

---

## Overview
So, OverTheWire has different levels it wants you to complete. I am starting from Level 0.

In Level 0, it showed me that `man <command>` displays the user guide or documentation for a command, where you can type `/` to search for a specific keyword.

But for shell-builtin commands, you need to use `help <command>`.

So, **Level 0** had me SSH into their machine with the command:

```bash
ssh -p 2220 bandit.labs.overthewire.org -l bandit0
```

With the password:
```text
bandit0
```

---

## Level 1
Now I am moving to **Level 1**.

Level 1 has you working with a few commands:

| Command | Description |
|---|---|
| `ls` | To list files in the directory |
| `cd` | To move into a folder or out of one |
| `cat` | To print the content of the file in the terminal |
| `file` | To know the type and format of the file from the content itself |
| `du` | To know the amount of storage used by the file/folder |
| `find` | Find files |

The password for the next level is stored in a file called **`readme`**, located in the home directory. Use this password to log into `bandit1` using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

### Steps I took to clear this level
I just did `ls`, and the file `readme` was just there. The password I got from it using `cat` was saved to `.secrets/bandit_passwords.txt`.

So I am exiting out of `bandit0` and logging into **`bandit1`** using this password.
I am inside `bandit1`.

> [!tip] Quick Solution
> `cat readme`

---

## Level 2
The password for the next level is stored in a file called **`-`**, located in the home directory.

For this, those same commands are given as "commands you may need to solve this level," but it needs us to find a file named `-`. Looking for _dashed filenames_ in Google.

Since CLI programs use the dash (`-`) to specify flags and options, we have two ways to bypass this issue:

- **The path prefix `./`:** Adding a relative path, for example, `./-`.
  ```bash
  bandit1@bandit:~$ cat ./-
  ```
- **The End-Of-Options Delimiter `--`:** Typing double-dash tells the command that all subsequent arguments are strictly filenames. (Google said this works, but it did not work for me.)
- But `cat < -` worked, as it gave me this:
  ```bash
  bandit1@bandit:~$ cat < -
  ```

> [!tip] Quick Solution
> `cat ./-` or `cat < -`

---

## Level 3
The password for the next level is stored in a file called **`--spaces in this filename--`**, located in the home directory.

For this level, however, `cat ./ --spaces in this filename--` does not work, as this command does not like spaces in commands.

I also tried this:
```bash
cat "--spaces in this filename--"
```
And escaping it also works: `cat \-\-spaces\ in\ this\ filename\-\-`.

> [!tip] Quick Solution
> `cat "--spaces in this filename--"`

---

## Level 4
The password for the next level is stored in a hidden file in the `inhere` directory.

Commands:
```bash
cd inhere
ls -la
cat .hidden-file-name
```

> [!tip] Quick Solution
> `ls -la inhere/` to find hidden files, then `cat inhere/.<filename>`

---

## Level 5
The password for the next level is stored in a file somewhere under the `inhere` directory and has all of the following properties: human-readable, 1033 bytes in size, not executable.

```bash
file inhere/*
```
Look for the one that says `ASCII text`.

> [!tip] Quick Solution
> `find inhere/ -size 1033c ! -executable`

---

## Level 6
The password for the next level is stored somewhere on the server and has all of the following properties: owned by user bandit7, owned by group bandit6, 33 bytes in size.

```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
```

> [!tip] Quick Solution
> `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`
> **Takeaway:** `2>/dev/null` hides the sea of permission-denied errors.

---

## Level 7
The password for the next level is stored in the file **data.txt** next to the word **millionth**.

```bash
cat data.txt | grep millionth
```

> [!tip] Quick Solution
> `grep millionth data.txt`

---

## Level 8
The password for the next level is stored in the file **data.txt** next to the word **millionth**.

```text
Commands I may need to use to solve this: 
grep - (Global Regular Expression Print) used to search for specific words, phrases, or patterns inside files or outputs
sort - used to arrange lines of text files or command outputs in a specific order
uniq - used to filter out or report repeated lines from a text file or standard input (only checks the adjacent line)
strings - extracts and prints sequences of printable characters from files
base64 - to encode or decode data into Base64 format  
tr - used to translate delete or squeeze characters from standard input and write result to standard output
tar - bundle multiple files and directories into a single archive file 
gzip -compresses individual files to reduce their size
bzip2 -command line utility to compress and decompress giles
xxd - creates hexadecimal dumps of binary files and vice-versa
```

Before even looking up all these commands i just ran this:
```bash
cat data.txt | grep millionth
```
and it gave this output:
```text
millionth	<see .secrets/bandit_passwords.txt>
```
I hope this works. And it did work.

I am stopping for today here. Use this command to get inside the terminal again:
```bash
ssh -p 2220 bandit.labs.overthewire.org -l bandit8
```
the password is the most recent one in the password file.

---

## Level 9
The password for the next level is stored in the file **data.txt** and is the only line of text that occurs only once.

Level 9 suggests i learn Piping and redirection from: https://ryanstutorials.net/linuxtutorial/piping.php

The ` > ` operator tells the command line to pass the program output to be saved in a file for eg.
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls > tmp
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls
tmp <----------- Here it is
dibij@Dibij:~/projects/CyberSecurity-Learning$ cat tmp
```
You can use the double ` >> ` operator to append to an existing file.

We can also send the data the other way using the ` < ` symbol. For example:
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ wc -l  tmp 
9 tmp
dibij@Dibij:~/projects/CyberSecurity-Learning$ wc -l < tmp 
9
```
You can also combine both like this:
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ wc -l < tmp1 > tmp
```

Now we need to Redirect STDERR - Error into a file.
To do this, we can stream STDERR into a file through an identifier which in this case would be ` 2 `.
For example:
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls -l blah.foo tmp 2> errors.txt
dibij@Dibij:~/projects/CyberSecurity-Learning$ cat errors.txt 
ls: cannot access 'blah.foo': No such file or directory
```
But, we can only pass errors through this command, so to pass both the normal standard output and error message we could:
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls -l blah.foo tmp > errors.txt 2>&1
```

> [!thought]- What the actual problem was & my thinking
> *The password for the next level is stored in the file **data.txt** and is the only line of text that occurs only once*
> So my thinking goes something like this:
> we need to find a unique line of text.
> - first, check / get texts from the file
> - second, use the uniq command to get the unique line
> so i know about linking, i will first write a command like ` strings data.txt | uniq`. Let me try this first.
> so i ran that command, and it gave me tons of of text strings, so unique just gave me all original text strings, i need to find one that shows the only one that occurs once, so i will investigate using ` man uniq `.
> Apparently it has an `-u --unique tag`, i hope it works.
> Again the same problem it just lists all unique values, how do we go about only finding the only string that does not get repeated twice? 
> I could use ` -c --count` maybe ? 
> `uniq ` just gives the unique ones, let me check `strings` command using `man strings`.
> I cant find anything on `man stings` i might need to go on google.
> 
> Well google says to look into the `sort` command. So here it is: I cant find a reliable way to look for the line of text that occurs only once. i might need to go deeper. 
> So i had to google it T.T but it worked, it needed me to combine 3 commands:
> `strings data.txt | sort | uniq -c`
> i was too dumb `strings data.txt` converts the file into each line of string, `sort` actually sorted them and `uniq -c` gave how many times those strings of line were repeated. but why did `strings data.txt | uniq -c` not work ? 
> I forgot what i wrote in this part in the command explanation part, uniq only looks at the line sequentially to it. Thats why we need to sort it.
> Well i have put up the password in `.secrets/bandit_passwords.txt`.

> [!tip] Quick Solution & Lesson
> `strings data.txt | sort | uniq -c` (or `sort data.txt | uniq -u`)
> **Takeaway:** `uniq` only checks adjacent lines! You MUST `sort` first.

---

## Level 10
The password for the next level is stored in the file **data.txt** in one of the few human-readable strings, preceded by several ‘=’ characters.

So, we need to find human readable strings, which would be done by strings? 
We also need to most likely use grep to find strings starting with several '='. i hope this is as easy as it sounds.
Well just `strings data.txt` got me the password, but i doubt this was intended
so ill send this new to grep to only get the ones where it starts with several '=' and then work through it .
Well i was able to get the password, i haven't tried loggin in with it yet but is this it ? 
This is most definitely not it. Let me look at the suggested commands and try again.
But i can't see anything that could help me here.
I am done with this level for now, maybe i will be back.

```text
bandit9@bandit:~$ strings data.txt | grep =
\========== the
q:=V
K	*=
=zZw
w=-1
vc.=
========== password
<u*========== is
=9$s
{=S[
;a =
lp>IoY-b==ld
========== < pwd here >
ec=}
	=ulD
```

> [!tip] Quick Solution
> `strings data.txt | grep "==="`

---

## Level 11
The password for the next level is stored in the file **data.txt**, which contains base64 encoded data.

Since it says *data.txt* contains base64 encoded data, we need to decode it using the `base64` command.
Before jumping in, i think this is the correct way to approach it:
```bash
bandit10@bandit:~$ base64 data.txt
```
but it just gives 2 line string, i think i need to lookup `man base64` to actually decode it.
Well apparently `-d` is the correct flag for it. Kinda dumb of me lol but i got the password.

> [!tip] Quick Solution
> `base64 -d data.txt`

---

## Level 12
The password for the next level is stored in the file **data.txt**, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

So:
`A` becomes `N`
`a` becomes `n`

So i ran this command:
```bash
bandit11@bandit:~$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
The password is <pwd>
```

> [!tip] Quick Solution
> `cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'` (ROT13)

---

## Level 13
The password for the next level is stored in the file **data.txt**, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work. Use mkdir with a hard to guess directory name. Or better, use the command “mktemp -d”. Then copy the datafile using cp, and rename it using mv (read the manpages!)

Ok so i am on an temporary folder:
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ dir
data.txt
```

### Step 1: Reverse the hexdump
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ xxd -r data.txt > binary
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file binary
binary: gzip compressed data, was "data2.bin", last modified: Sat Sep 26 21:54:21 2026, max compression, from Unix, original size modulo 2^32 584
```
The output tells us that `binary` is a GZIP-compressed file.

### Step 2: Decompress using GZIP
Use `gunzip` to decompress the file. The `-c` option writes the decompressed contents to standard output, allowing us to redirect them into a new file.
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ gunzip -c binary > decompressed
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file decompressed
decompressed: bzip2 compressed data, block size = 900k
```
The resulting file is compressed using BZIP2.

### Step 3: Decompress using BZIP2
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ bunzip2 -d decompressed
bunzip2: Can't guess original name for decompressed -- using decompressed.out
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file decompressed.out
decompressed.out: gzip compressed data, was "data4.bin", last modified: Sat Sep 26 21:54:21 2026, max compression, from Unix, original size modulo 2^32 20480
```
BZIP2 decompression produces `decompressed.out`, which is another GZIP-compressed file.
The warning is harmless: BZIP2 could not determine the original filename, so it chose `decompressed.out`.

### Step 4: Decompress using GZIP again
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ gunzip -c decompressed.out > binary2
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file binary2
binary2: POSIX tar archive (GNU)
```
The resulting file is a TAR archive. Unlike GZIP and BZIP2, TAR is an archive format that groups files together. We need to **extract** its contents rather than decompress it.

### Step 5: Extract the first TAR archive
Use `tar` with `--extract` (or `-x`) and `-f` to specify the archive filename.
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ tar --extract -f binary2
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file data5.bin
data5.bin: POSIX tar archive (GNU)
```
The archive contains `data5.bin`, which is another TAR archive.
**Note:** Do not redirect the command to a file using `> tardecompressed`. TAR extracts files into the current directory; it does not print the extracted files' contents to standard output.

### Step 6: Extract the second TAR archive
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ tar --extract -f data5.bin
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file data6.bin
data6.bin: POSIX tar archive (GNU)
```
The extracted `data6.bin` is also a TAR archive.

### Step 7: Extract the third TAR archive
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ tar --extract -f data6.bin
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Sat Sep 26 21:54:21 2026, max compression, from Unix, original size modulo 2^32 49
```
The resulting `data8.bin` is GZIP-compressed. Although its embedded original filename is `data9.bin`, the file currently present in the directory is named `data8.bin`.

### Step 8: Decompress the final GZIP file
Use `gunzip -c` to print the decompressed contents directly to the terminal.
```bash
bandit12@bandit:/tmp/tmp.fCFgrNXhdN$ gunzip -c data8.bin
The password is [password displayed by the command]
```
**The password printed by this command is the password needed to log in as `bandit13`.**

> [!tip] Summary of the process
> | Step | Input file | Operation | Result |
> | --- | --- | --- | --- |
> | 1 | `data.txt` | Reverse hexdump with `xxd -r` | `binary` |
> | 2 | `binary` | GZIP decompression | `decompressed` |
> | 3 | `decompressed` | BZIP2 decompression | `decompressed.out` |
> | 4 | `decompressed.out` | GZIP decompression | `binary2` |
> | 5 | `binary2` | TAR extraction | `data5.bin` |
> | 6 | `data5.bin` | TAR extraction | `data6.bin` |
> | 7 | `data6.bin` | TAR extraction | `data8.bin` |
> | 8 | `data8.bin` | GZIP decompression | Password printed to terminal |
>
> **Key lesson:** Use `file` to identify each file's format before choosing the next operation. The filename extension does not necessarily tell you what format the file contains.

---

## Current Position

**Last completed:** Bandit Level 13 objective.

**Next:** Log in as `bandit13` with the private SSH key and start Bandit Level 14.

**Learning approach:** Attempt each challenge independently before consulting walkthroughs.

**Related session:** [[2026-10-16 - Cybersecurity Learning Session]]
