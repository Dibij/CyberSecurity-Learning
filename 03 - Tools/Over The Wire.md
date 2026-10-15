# OverTheWire: Bandit Learning Journal

Related notes:
- [[Linux Fundamentals]]
- [[Lab Tracker]]
- [[Learning Roadmap]]
- [[2026-10-15 - Cybersecurity Learning Session]]

So, OverTheWire has different levels it wants you to complete. I am starting from Level 0.

In Level 0, it showed me that `man <command>` displays the user guide or documentation for a command, where you can type `/` to search for a specific keyword.

But for shell-builtin commands, you need to use `help <command>`.

So, **Level 0** had me SSH into their machine with the command:

```
ssh -p 2220 bandit.labs.overthewire.org -l bandit0
```

With the password:

```
bandit0
```

Now I am moving to **Level 1**.

Level 1 has you working with a few commands:

|Command|Description|
|---|---|
|`ls`|To list files in the directory|
|`cd`|To move into a folder or out of one|
|`cat`|To print the content of the file in the terminal|
|`file`|To know the type and format of the file from the content itself|
|`du`|To know the amount of storage used by the file/folder|
|`find`|Find files|

> **NOTE:** [[note_file_OTW]] stores passwords, as apparently I may need it.

---

## Level 1

The password for the next level is stored in a file called **`readme`**, located in the home directory. Use this password to log into `bandit1` using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

### Steps I took to clear this level

I just did `ls`, and the file `readme` was just there. The password I got from it using `cat` was:

```
<see note_file_OTW>
```

So I am exiting out of `bandit0` and logging into **`bandit1`** using this password.

I am inside `bandit1`.

---

## Level 2

The password for the next level is stored in a file called **`-`**, located in the home directory.

For this, those same commands are given as "commands you may need to solve this level," but it needs us to find a file named `-`. Looking for _dashed filenames_ in Google.

Since CLI programs use the dash (`-`) to specify flags and options, we have two ways to bypass this issue.

- **The path prefix `./`:** Adding a relative path, for example, `./-`.
    
    ```
    bandit1@bandit:~$ cat ./-
    <see note_file_OTW>
    ```
    
- **The End-Of-Options Delimiter `--`:** Typing double-dash tells the command that all subsequent arguments are strictly filenames. (Google said this works, but it did not work for me.)
    
- But `cat < -` worked, as it gave me this:
    
    ```
    bandit1@bandit:~$ cat < -
    <see note_file_OTW>
    ```
    

---

## Level 3

The password for the next level is stored in a file called **`--spaces in this filename--`**, located in the home directory.

For this level, however, `cat ./ --spaces in this filename--` does not work, as this command does not like spaces in commands.

I also tried this:

```
cat "--spaces in this filename--"
```

It also did not work.

Neither did this:

```
cat > --spaces\ in\ this\ filename--
```

BUT...

This worked:

```
bandit2@bandit:~$ cat -- "--spaces in this filename--"
<see note_file_OTW>
```

AND... this worked too:

```
bandit2@bandit:~$ cat "./--spaces in this filename--"
<see note_file_OTW>
```

Since the filename contained both "dashes" and "spaces", it made the previous commands confused. But passing the command inside quotation marks passes the exact string literal, and since we used `--` in the first instance of it working, Bash knows that whatever comes after it, which was a literal string, was a filename. And similarly, adding `./` made it so that the command `cat` knew that whatever the string literal contained was a filename.

---

## Level 4

The password for the next level is stored in a hidden file in the **`inhere`** directory.

So I was able to cheese through this level because I knew of the command `ls -la`.

It gave this result:

```
bandit3@bandit:~/inhere$ ls -la
total 12
drwxr-xr-x 2 root    root    4096 Sep 26 21:53 .
drwxr-xr-x 3 root    root    4096 Sep 26 21:53 ..
-rw-r----- 1 bandit4 bandit3   33 Sep 26 21:53 ...Hiding-From-You
bandit3@bandit:~/inhere$ cat ...Hiding-From-You
<see note_file_OTW>
```

Here, I was logged in as `bandit3`, and as you can see from this line:

```
-rw-r----- 1 bandit4 bandit3   33 Sep 26 21:53 ...Hiding-From-You
```

Here, the first `-rw` corresponds to the first username after `1`, which is `bandit4`, and this is a permission list which means `bandit4` can read or write. As I am `bandit3`, I have read access, as shown by `-r---`.

---
## Level 5
The password for the next level is stored in the only human-readable file in the **inhere** directory. Tip: if your terminal is messed up, try the “reset” command.
Apparently human-readable file meant an ASCII or a UNICODE file. Since the " file " commands shows you the file type by the actual content, i was able to find out the only ASCII file out of the existing 10 files
```
bandit4@bandit:~/inhere$ ls -la
total 48
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file00
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file01
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file02
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file03
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file04
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file05
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file06
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file07
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file08
-rw-r----- 1 bandit5 bandit4   33 Sep 26 21:53 -file09
drwxr-xr-x 2 root    root    4096 Sep 26 21:53 .
drwxr-xr-x 3 root    root    4096 Sep 26 21:53 ..
bandit4@bandit:~/inhere$ file ./-file00
./-file00: data
bandit4@bandit:~/inhere$ file ./-file01
./-file01: data
bandit4@bandit:~/inhere$ file ./-file02
./-file02: data
bandit4@bandit:~/inhere$ file ./-file04
./-file04: data
bandit4@bandit:~/inhere$ file ./-file03
./-file03: data
bandit4@bandit:~/inhere$ file ./-file05
./-file05: data
bandit4@bandit:~/inhere$ file ./-file06
./-file06: data
bandit4@bandit:~/inhere$ file ./-file07
./-file07: ASCII text
bandit4@bandit:~/inhere$ file ./-file08
./-file08: data
bandit4@bandit:~/inhere$ file ./-file09
./-file09: data
bandit4@bandit:~/inhere$ cat ./-file07
<see note_file_OTW>

```
so the password is ``` <see note_file_OTW> ```

---
## Level 6
The password for the next level is stored in a file somewhere under the **inhere** directory and has all of the following properties:
- human-readable
- 1033 bytes in size
- not executable

Before starting this challenge, here is what i think of it, we have the *files* command, that can look at a file and tell me if or not it is human readable, a *du* command that tells me the size of the file, and for not executable, ill google it, and there are several way we could check if a file is executable or not but the easiest one is *ls -la*, for a file to be executable there should be an x.
So here are my command outputs
```
bandit5@bandit:~/inhere$ dir
maybehere00  maybehere03  maybehere06  maybehere09  maybehere12	 maybehere15  maybehere18
maybehere01  maybehere04  maybehere07  maybehere10  maybehere13	 maybehere16  maybehere19
maybehere02  maybehere05  maybehere08  maybehere11  maybehere14	 maybehere17
bandit5@bandit:~/inhere$ find . -type f -size 1033c ! -executable -exec file {} + | grep text
./maybehere07/.file2: ASCII text, with very long lines (1000)
bandit5@bandit:~/inhere$ cat maybehere07/.file
cat: maybehere07/.file: No such file or directory
bandit5@bandit:~/inhere$ cat maybehere07/.file2
<see note_file_OTW>


```

The explanation for this was, i looked around google, and first thought of writing a for-loop. but found out that the intended and much faster way was using the command 
```
find . -type f -size 1033c ! -executable -exec file {} + | grep text
```
 where 
 ```
 find -  the base utility for finding files
 . - tells the command to start searching in the current directory
 -type f - restricts the search to strictly regular files 
 -size 1033c - searcher for exactly 1033 bytes in files size
 ! -executable - matches for a file that is not executable
 -exec - tells "find" to run an  external linux command on any files it finds
 file - its the command being executed after -exec to check the actual file type
 {} - a placeholder that find automatically replaces with the paths of the files it located
 + - passes all the found files to the find command at once
 | - takes the output generated by the " file " command and sends it as input to the next command
 grep text - filters the incoming text and only displays lines containing the word "text".
 ```

---
## Level 7 
The password for the next level is stored **somewhere on the server** and has all of the following properties:

- owned by user bandit7
- owned by group bandit6
- 33 bytes in size
Just like previously i need make small  piped shell command pipeline that fulfill all commands. 
Wait, misconception changed, instead of the piped shell command, i was able to do all of this with just flags in the find command. 
```
bandit6@bandit:/$ find -user bandit7 -group bandit6 -size 33c

```
It gave some long reports, but 
```
./var/lib/dpkg/info/bandit7.password
bandit6@bandit:/$ cat ./var/lib/dpkg/info/bandit7.password 
<see note_file_OTW>
```
I was able to get Level 7's password. 

---
## Level 8
The password for the next level is stored in the file **data.txt** next to the word **millionth**

```
Commands I may need to use to solve this: 
grep - 
sort -
uniq - 
strings - 
base64 - 
tr -
tar -
gzip -
bzip2 -
xxd - 
```
Before even looking up all these commands i just ran this 
```
cat data.txt | grep millionth
```
and it gave this output
```
millionth	<see note_file_OTW>
```
I hope this works 
 And it did work. 
I am stopping for today here. Use this command to get inside the terminal again 
``` 
ssh -p 2220 bandit.labs.overthewire.org -l bandit8

```
the password is the most recent one 


---
## Current Position

**Last completed:** Bandit Level 8 objective.

**Next:** Continue with Bandit Level 8.

**Learning approach:** Attempt each challenge independently before consulting walkthroughs.

**Related session:** [[2026-10-15 - Cybersecurity Learning Session]]
