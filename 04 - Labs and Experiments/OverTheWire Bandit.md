---
title: "OverTheWire: Bandit Walkthrough"
type: lab-writeup
platform: OverTheWire
status: in-progress
current_level: 14
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
> Wargame passwords are kept securely out of Git in [[Bandit Passwords]].

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
I just did `ls`, and the file `readme` was just there. The password I got from it using `cat` was saved to [[Bandit Passwords]].

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
millionth	<see [[Bandit Passwords]]>
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
> Well i have put up the password in [[Bandit Passwords]].

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

## **Level 14**
>The password for the next level is stored in **/etc/bandit_pass/bandit14 and can only be read by user bandit14**. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. Look at the commands that logged you into previous bandit levels, and find out how to use the key for this level.  
If you need help with this level: a hint file can be found in the home directory.  
Make sure to read the error messages as they are informative.

*Thought process* : 
So the command that logged me into previous bandit levels was: 
`ssh -p 2220 bandit.labs.overthewire.org -l bandit13`
So there is a file that can only be read by bandit14, but i am logged in as bandit13. And this level only gives you a private SSH key so first i need to know how to use a ssh key with the ssh command. Also, it asks us to research more about several different new commands. Will Research and add them in [[Linux CLI Utilities]]

I googled a bit, and foundout that you can download files from remote client onto your local client using the `scp` command. 

Well from my research, i might need to use probably all the commands suggested by the problem. So here is my thinking again.
Honestly though this numbering has me confused, i am on level 14, but using bandit13 as username and password.
So i log in into it. see that the file is there 
```shell
bandit13@bandit:~$ ls -la 
total 28
drwxr-xr-x   2 root     root     4096 Sep 26 21:52 .
drwxr-xr-x 150 root     root     4096 Sep 26 21:56 ..
-rw-r--r--   1 root     root      220 Feb 13  2026 .bash_logout
-rw-r--r--   1 root     root     3851 Sep 26 21:38 .bashrc
-rw-r--r--   1 root     root      807 Feb 13  2026 .profile
-rw-r-----   1 bandit14 bandit13  467 Sep 26 21:52 HINT
-rw-r-----   1 bandit14 bandit13 2602 Sep 26 21:52 sshkey.private
```
Letme run `cat` on a those files
```shell
andit13@bandit:~$  cat sshkey.private
<it printed the file content>

```
What if i use piping commands like export the content of this cat onto a new file with umask, then use scp to get it outside, like in my local machine? ok letme try this

well there goes my idea, Permission denied

I am trying to use `chmod` here, but i dont even know what Mode argument to give it. so ill just google it , cause even `man chmod ` or `chmod --help` provided no clue.



FUCK THIS SHIT!!!!!!!!!
It was so easy, well not exactly easy but like i know about the `ssh -i` flag, but i also read this line that i misunderstood the line went something like 
>The current version of OverTheWire prevents logging in from one
   level to another via localhost. Log out, and see 1)

But now google says i can just move the file from home.bandit13 into a tmp using `install` command.
I never even looked at the install command because i thought its just the basic one. But apparently not, it is 
`cp + chmod` in one command. 
So i first move it into or install the sshkey.private file into tmp where i can edit or whatever and use that as the identity flag and login into level 14 
And this runs on the assumption that Gemini gave me here

>You **do not** need to download the file to your local computer. Remember, you are already inside a Linux environment. You can SSH _from_ the Bandit server _to_... well, localhost (bandit14)!

so here goes my command
```bash
bandit13@bandit:~$ install -m 600 sshkey.private /tmp/tmp.Jr3k6uRfVo/my_key
bandit13@bandit:~$ cd /tmp/tmp.Jr3k6uRfVo
bandit13@bandit:/tmp/tmp.Jr3k6uRfVo$ dir
my_key
bandit13@bandit:/tmp/tmp.Jr3k6uRfVo$ cat my_key 
-----BEGIN OPENSSH PRIVATE KEY-----

```
well it fucking worked upuntill this command.
Now to passthis using the identity symbol 
```bash
bandit13@bandit:/tmp/tmp.Jr3k6uRfVo$ ssh -i my_key -p 2220 bandit.labs.overthewire.org -l bandit14
The authenticity of host '[bandit.labs.overthewire.org]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is: SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

```
This didnot work, google fucking lied to me fucker. SBut since, i have full access to the file i can use scp to get it in my local linux

Fuckk, I didnot save the scp command, letme look it up, but letme try it without looking it up from memory. well i forgot
```shell
bandit13@bandit:/tmp/tmp.Jr3k6uRfVo$ scp -P 2220 bandit13@bandit.labs.overthewire.org:/tmp/tmp.Jr3k6uRfVo/my_key /home/dibij/projects/CyberSecurity-Learning
The authenticity of host '[bandit.labs.overthewire.org]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is: SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? Y
Please type 'yes', 'no' or the fingerprint: yes
Could not create directory '/home/bandit13/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit13/.ssh/known_hosts).
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

!!! You are trying to log into this SSH server from localhost.
!!! Connecting from/to localhost is blocked to conserve resources.
!!! Please log out and log in again, directly from your client machine.

backend: gibson-1
Received disconnect from 127.0.0.1 port 2220:2: no authentication methods enabled
Disconnected from 127.0.0.1 port 2220
scp: Connection closed
bandit13@bandit:/tmp/tmp.Jr3k6uRfVo$ 

```
even this didnot work ? maybe because i am inside bandit servers? letme try it outside in my local machine for once.
Ok i got this 
```shell
bandit13@bandit:/tmp/tmp.Jr3k6uRfVo$ exit
logout
Connection to bandit.labs.overthewire.org closed.
dibij@Dibij:~/projects/CyberSecurity-Learning$ scp -P 2220 bandit13@bandit.labs.overthewire.org:/tmp/tmp.Jr3k6uRfVo/my_key /home/dibij/projects/CyberSecurity-Learning/
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-1
bandit13@bandit.labs.overthewire.org's password: 
Permission denied, please try again.
bandit13@bandit.labs.overthewire.org's password: 
my_key                                                                    100% 2602     4.2KB/s   00:00    
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls -la
total 32
drwxr-xr-x 1 dibij dibij 4096 Oct 17 19:28  .
drwxr-xr-x 1 dibij dibij    0 Oct 15 16:41  ..
drwxr-xr-x 1 dibij dibij 4096 Oct 17 18:08  .git
-rwxr-xr-x 1 dibij dibij  233 Oct 17 18:04  .gitignore
drwxr-xr-x 1 dibij dibij 4096 Oct 15 18:57  .obsidian
drwxr-xr-x 1 dibij dibij    0 Oct 15 16:47  '00 - Dashboard'
drwxr-xr-x 1 dibij dibij 4096 Oct 17 17:57  '01 - Journal'
drwxr-xr-x 1 dibij dibij 4096 Oct 16 21:26  '02 - Fundamentals'
drwxr-xr-x 1 dibij dibij    0 Oct 16 21:24  '03 - Tools'
drwxr-xr-x 1 dibij dibij    0 Oct 16 21:23  '04 - Labs and Experiments'
drwxr-xr-x 1 dibij dibij    0 Oct 16 21:27  '05 - Projects'
drwxr-xr-x 1 dibij dibij 4096 Oct 16 21:28  '06 - Templates'
-rwxr-xr-x 1 dibij dibij 1530 Oct 17 18:07  README.md
drwxr-xr-x 1 dibij dibij    0 Oct 17 18:04  _secrets
-rwxr-xr-x 1 dibij dibij 2602 Oct 17 19:28  my_key
drwxr-xr-x 1 dibij dibij    0 Oct 17 18:30  pass
```
Now letme pass this file to next level

now what new iisue is this ?? 
```shell 
dibij@Dibij:~/projects/CyberSecurity-Learning$ ssh -i my_key -p 2220 bandit.labs.overthewire.org -l bandit14
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-1
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0755 for 'my_key' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "my_key": bad permissions
bandit14@bandit.labs.overthewire.org's password: 
```
Since i dont know the password, nor the mode identifiers to make this only accessible by me, we probably either use chmod or umask so lemme look up the syntax
Apparetnyl chmod 600 locks the file so only the owner can view it, this should be secure enough.

Well even `chmod 600 my_key` didnot work because this project is basically a symlink project from windows d drive to this linux, and apparently windows NTFS so i will create a linux based file at /tmp
Finally motherfucker
```bash
ibij@Dibij:~/projects/CyberSecurity-Learning$ mv my_key  /tmp/random_key_for_bandit 
dibij@Dibij:~/projects/CyberSecurity-Learning$ dir /tmp/
mcp-PzuQsM
node-compile-cache
random_key_for_bandit
snap-private-tmp
systemd-private-59b68d1cda0e4bbd98118394a28f0442-ModemManager.service-itJKZs
systemd-private-59b68d1cda0e4bbd98118394a28f0442-bluetooth.service-G5WYCr
systemd-private-59b68d1cda0e4bbd98118394a28f0442-chrony.service-YG2EbM
systemd-private-59b68d1cda0e4bbd98118394a28f0442-colord.service-2SlYtc
systemd-private-59b68d1cda0e4bbd98118394a28f0442-fwupd.service-ICdvGf
systemd-private-59b68d1cda0e4bbd98118394a28f0442-polkit.service-KanVSc
systemd-private-59b68d1cda0e4bbd98118394a28f0442-power-profiles-daemon.service-xP2LlY
systemd-private-59b68d1cda0e4bbd98118394a28f0442-switcheroo-control.service-z2L6i9
systemd-private-59b68d1cda0e4bbd98118394a28f0442-systemd-logind.service-kBuFQd
systemd-private-59b68d1cda0e4bbd98118394a28f0442-upower.service-xWIpPp
unleash-repo-schema-v1-codeium-language-server.json
vscode-ah-be523e38b7f6
dibij@Dibij:~/projects/CyberSecurity-Learning$ chmod 600 /tmp/random_key_for_bandit 
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls -la /tmp
total 472
drwxrwxrwt 20 root  root     480 Oct 17 19:39 .
drwxr-xr-x 20 root  root    4096 Sep  8 01:56 ..
drwxrwxrwt  2 root  root      40 Oct 17  2026 .ICE-unix
-r--r--r--  1 dibij dibij     11 Oct 17 17:51 .X0-lock
-r--r--r--  1 dibij dibij     11 Oct 17 17:51 .X1-lock
drwxrwxrwt  2 root  root      80 Oct 17 17:51 .X11-unix
drwxrwxrwt  2 root  root      40 Oct 17  2026 .XIM-unix
drwxrwxrwt  2 root  root      40 Oct 17  2026 .font-unix
drwx------  2 dibij dibij     60 Oct 17 18:02 mcp-PzuQsM
drwxrwxr-x  3 dibij dibij     60 Oct 17 18:02 node-compile-cache
-rw-------  1 dibij dibij   2602 Oct 17 19:28 random_key_for_bandit
drwx------  6 root  root     120 Oct 17 18:00 snap-private-tmp
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-ModemManager.service-itJKZs
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-bluetooth.service-G5WYCr
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-chrony.service-YG2EbM
drwx------  3 root  root      60 Oct 17 17:51 systemd-private-59b68d1cda0e4bbd98118394a28f0442-colord.service-2SlYtc
drwx------  3 root  root      60 Oct 17 19:24 systemd-private-59b68d1cda0e4bbd98118394a28f0442-fwupd.service-ICdvGf
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-polkit.service-KanVSc
drwx------  3 root  root      60 Oct 17 17:51 systemd-private-59b68d1cda0e4bbd98118394a28f0442-power-profiles-daemon.service-xP2LlY
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-switcheroo-control.service-z2L6i9
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-systemd-logind.service-kBuFQd
drwx------  3 root  root      60 Oct 17  2026 systemd-private-59b68d1cda0e4bbd98118394a28f0442-upower.service-xWIpPp
-rw-rw-r--  1 dibij dibij 463641 Oct 17 18:02 unleash-repo-schema-v1-codeium-language-server.json
drwx------  2 dibij dibij     60 Oct 17 18:01 vscode-ah-be523e38b7f6
dibij@Dibij:~/projects/CyberSecurity-Learning$ ssh -i /tmp/random_key_for_bandit -p 2220 bandit.labs.overthewire.org -l bandit14
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-1

      ,----..            ,----,          .---.
     /   /   \         ,/   .`|         /. ./|
    /   .     :      ,`   .'  :     .--'.  ' ;
   .   /   ;.  \   ;    ;     /    /__./ \ : |
  .   ;   /  ` ; .'___,/    ,' .--'.  '   \' .
  ;   |  ; \ ; | |    :     | /___/ \ |    ' '
  |   :  | ; | ' ;    |.';  ; ;   \  \;      :
  .   |  ' ' ' : `----'  |  |  \   ;  `      |
  '   ;  \; /  |     '   :  ;   .   \    .\  ;
   \   \  ',  /      |   |  '    \   \   ' \ |
    ;   :    /       '   :  |     :   '  |--"
     \   \ .'        ;   |.'       \   \ ;
  www. `---` ver     '---' he       '---" ire.org


Welcome to OverTheWire!

If you find any problems, please report them to the #wargames channel on
discord or IRC.

--[ Playing the games ]--

  This machine might hold several wargames.
  If you are playing "somegame", then:

    * USERNAMES are somegame0, somegame1, ...
    * Most LEVELS are stored in /somegame/.
    * PASSWORDS for each level are stored in /etc/somegame_pass/.

  Write-access to homedirectories is disabled. It is advised to create a
  working directory with a hard-to-guess name in /tmp/.  You can use the
  command "mktemp -d" in order to generate a random and hard to guess
  directory in /tmp/.  Read-access to both /tmp/ is disabled and to /proc
  restricted so that users cannot snoop on eachother. Files and directories
  with easily guessable or short names will be periodically deleted! The /tmp
  directory is regularly wiped.
  Please play nice:

    * don't leave orphan processes running
    * don't leave exploit-files laying around
    * don't annoy other players
    * don't post passwords or spoilers
    * again, DONT POST SPOILERS!
      This includes writeups of your solution on your blog or website!

--[ Tips ]--

  This machine has a 64bit processor and many security-features enabled
  by default, although ASLR has been switched off.  The following
  compiler flags might be interesting:

    -m32                    compile for 32bit
    -fno-stack-protector    disable ProPolice
    -Wl,-z,norelro          disable relro

  In addition, the execstack tool can be used to flag the stack as
  executable on ELF binaries.

  Finally, network-access is limited for most levels by a local
  firewall.

--[ Tools ]--

 For your convenience we have installed a few useful tools which you can find
 in the following locations:

    * gef (https://github.com/hugsy/gef) in /opt/gef/
    * pwndbg (https://github.com/pwndbg/pwndbg) in /opt/pwndbg/
    * gdbinit (https://github.com/gdbinit/Gdbinit) in /opt/gdbinit/
    * pwntools (https://github.com/Gallopsled/pwntools)
    * radare2 (http://www.radare.org/)

--[ More information ]--

  For more information regarding individual wargames, visit
  http://www.overthewire.org/wargames/

  For support, questions or comments, contact us on discord or IRC.

  Enjoy your stay!

bandit14@bandit:~$ 


```
I have finally logged into bandit14 dayumm.
Now to get the password
 I got the password and saved it at [[Bandit Passwords]]

> [!tip] Quick Solution & Key Lessons
> 1. **Copy key to client (outside server):**
>    ```bash
>    scp -P 2220 bandit13@bandit.labs.overthewire.org:/tmp/tmp.Jr3k6uRfVo/my_key /home/dibij/projects/CyberSecurity-Learning/
>    ```
> 2. **WSL / Windows NTFS Gotcha:**
>    NTFS partitions mounted in WSL ignore standard Linux `chmod` file permission modes, leaving the file at `0755` (`WARNING: UNPROTECTED PRIVATE KEY FILE!`).
>    **Fix:** Move the key to a native Linux path like `/tmp/` and set strict permissions:
>    ```bash
>    mv my_key /tmp/random_key_for_bandit
>    chmod 600 /tmp/random_key_for_bandit
>    ```
> 3. **Login with Identity File (`-i`):**
>    ```bash
>    ssh -i /tmp/random_key_for_bandit -p 2220 bandit.labs.overthewire.org -l bandit14
>    ```
> 4. **Retrieve Password:**
>    ```bash
>    cat /etc/bandit_pass/bandit14
>    ```

---

## Level 15
**Objective:** The password for the next level can be retrieved by submitting the password of the current level to **port 30000 on localhost**.

Useful commands to investigate: `nc` (netcat), `ncat`, `telnet`, `openssl`, `s_client`.

---

## Current Position

**Last completed:** Bandit Level 14 objective.

**Next:** Connect to localhost port 30000, send the Bandit 14 password, and retrieve the Bandit 15 password.

**Learning approach:** Attempt each challenge independently before consulting walkthroughs.

**Related sessions:**
- [[2026-10-17 - Bandit - Session]]
- [[2026-10-17 - DNS - Session]]
- [[2026-10-16 - Cybersecurity Learning Session]]
