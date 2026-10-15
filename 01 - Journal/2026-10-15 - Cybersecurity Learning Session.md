# Cybersecurity Learning Session — 2026-10-15

**Session:** 001
**Focus:** Linux fundamentals and OverTheWire Bandit
**Status:** Completed for today

## What I worked on

### OverTheWire: Bandit

Today, I progressed through the early Bandit levels.

I practised and learned about:

- `man` and `help` for command documentation.
- `ls` and `ls -la` for inspecting directory contents.
- `cat` for reading files.
- `./filename` for handling filenames that resemble command options.
- Quoting filenames containing spaces.
- `file` for identifying file types.
- `find` for searching by file properties.
- `grep` for searching text.
- File ownership, groups, and permissions.
- Handling permission-denied messages during filesystem searches.

See [[Over The Wire]] for my detailed walkthrough.

## What I learned

- The shell interprets spaces as argument separators unless quoting or escaping changes that behaviour.
- Command options and filenames can sometimes be confused if a filename begins with a dash.
- The exact path returned by `find` can be passed to another command.
- Permission-denied messages do not necessarily mean a search has failed.
- Reading command output carefully is an important debugging skill.

## What I still need to understand

- Unix file permissions and ownership.
- The difference between command options and arguments.
- How to interpret `ls -l` output confidently.
- How to redirect standard output and errors.
- How to build useful `find` expressions independently.

These are topics to revisit as they become relevant.

## Next session

1. Log into Bandit as `bandit8`.
2. Read the next level's objective carefully.
3. Identify the constraints and consider which commands might help.
4. Attempt a solution independently.
5. Consult documentation when necessary.
6. Record my reasoning, mistakes, and discoveries in [[Over The Wire]].
7. Update [[Lab Tracker]].

## Handover

**Current position:** Ready to continue from Bandit Level 8.

**Next objective:** Solve the next challenge independently where possible.

**Approach:** Read, reason, predict, test, inspect the output, and explain what I learned.

**Reminder:** Keep passwords out of public notes and Git-tracked files.

## Related notes

- [[Over The Wire]]
- [[Lab Tracker]]
- [[Linux Fundamentals]]
- [[Learning Roadmap]]
- [[Starting Point]]
- [[Cyber-Security Home]]
