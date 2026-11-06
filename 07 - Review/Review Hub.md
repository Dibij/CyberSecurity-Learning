---
title: "Review Hub"
type: dashboard
tags:
  - review
  - recall
---

# Review Hub

> Technical questions generated from the notes, stored locally, and pulled out
> on demand. No model is called while you quiz.

Related: [[Cyber-Security Home]] · [[Lab Tracker]]

---

## The loop

1. You (or Antigravity) finish a session and write/update a note.
2. A cron entry runs every minute. It notices the new or changed note by hash.
3. The local Ollama model turns the note into question/answer cards.
4. Each card is stored in `.quiz/quiz.db` with a cited line from the note.
5. Whenever you want, you pull due cards and grade yourself. The SRS schedule
   decides when each card comes back.

| Stage | Command |
|---|---|
| Quiz due cards | `python3 .quiz/quiz.py` |
| More cards | `python3 .quiz/quiz.py --count 20` |
| One topic | `python3 .quiz/quiz.py --topic xss` |
| Never seen | `python3 .quiz/quiz.py --new` |
| Ignore schedule | `python3 .quiz/quiz.py --all` |
| Bank stats | `python3 .quiz/quiz.py --stats` |

**Grades:** `a` = again (10 min) · `h` = hard (1 day) · `g` = good (next box) ·
`e` = easy (skip 2 boxes) · `s` = skip · `q` = quit.

---

## Reading mode in Obsidian

```bash
python3 .quiz/quiz.py --note
```

Writes `07 - Review/Daily/YYYY-MM-DD.md` with every due question and a folded
`<details>` answer. Add `--all` for the whole bank, or `--topic xss` to focus.
Works in reading view; answers stay hidden until you unfold them. The exported
note is a snapshot — grading (and therefore the spaced-repetition schedule) still
happens in the terminal quiz.

---

## What gets ingested

Included: `01 - Journal`, `02 - Fundamentals`, `03 - Tools`, `04 - Labs and
Experiments`, `05 - Projects`.

Excluded: `06 - Templates`, `00 - Dashboard`, `07 - Review`, `_secrets`, and
anything in a dot-folder. Notes under 350 characters of body are skipped.

Cards never ask "what did you do today". The prompt targets definitions,
mechanisms, comparisons, payload/command mechanics, gotchas, and defenses.

---

## Maintenance

```bash
crontab -l                                  # confirm the watcher is installed
tail -f .quiz/logs/ingest.log               # watch generation
python3 .quiz/ingest.py --path "01 - Journal/2026-10-20 - PortSwigger DOM XSS Session.md" --force
rm .quiz/quiz.db && python3 .quiz/ingest.py --scan --force   # full rebuild
```

- Model lives in `.quiz/config.json` (`ollama.model`). Default:
  `gemma4:31b-cloud` (free tier). Offline fallback: `qwen2.5:1.5b`, weaker.
- The DB is git-ignored. Copy `.quiz/quiz.db` if you want to back up progress.
- If a note changes, its old cards stay and only genuinely new questions are
  added, so review history is never thrown away.
