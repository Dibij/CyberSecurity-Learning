# Question bank engine

The notes are the source of truth. This folder turns them into spaced-repetition
flashcards stored in SQLite, so quizzing never waits for a model.

```
.quiz/
├── config.json     model, chunk sizes, SRS intervals, included folders
├── quizgen.py      shared engine: parsing, Ollama calls, DB, SRS math
├── ingest.py       scan notes → generate cards (run by cron every minute)
├── quiz.py         terminal quiz, stats, Obsidian note export
├── run.sh          cron entry point (lock + log rotation)
├── quiz.db         runtime data (git-ignored)
└── logs/           ingest log (git-ignored)
```

## How a card is made

1. `ingest.py --scan` walks the folders listed in `config.json`.
2. A note is processed when its SHA-256 hash differs from the last run.
3. The body is split into ~2400-char chunks by `##` section.
4. The chunk is numbered sentence by sentence and sent to Ollama with a JSON
   schema (`question`, `answer`, `source`, `kind`, `difficulty`).
5. `source` must point at a real numbered sentence; the card stores that
   sentence as `evidence`. Cards with an out-of-range citation are dropped.
6. Questions are de-duplicated against everything already in the bank.

Notes that fail mid-way get status `partial` and are retried on the next scan.

## Common commands

```bash
python3 .quiz/ingest.py --scan                  # what cron runs
python3 .quiz/ingest.py --path "01 - Journal/….md" --force
python3 .quiz/ingest.py --path "…" --dry-run    # print cards, save nothing
python3 .quiz/quiz.py                           # due cards
python3 .quiz/quiz.py --stats
python3 .quiz/quiz.py --note                    # export to 07 - Review/Daily/
```

## Model

Default is `gemma4:31b-cloud` (free Ollama cloud plan): fast, and good enough to
produce technically correct cards. `qwen2.5:1.5b` is installed as an offline
fallback but produced wrong/echoing answers in testing.

Switch with either:

```bash
# temporary
QUIZ_MODEL=qwen2.5:1.5b python3 .quiz/quiz.py --stats

# permanent
# edit .quiz/config.json → ollama.model
```

## Reset / rebuild

```bash
rm .quiz/quiz.db
python3 .quiz/ingest.py --scan --force
```

Deleting the DB only removes cards and review history; notes are untouched.
