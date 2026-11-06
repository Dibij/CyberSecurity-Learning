#!/usr/bin/env python3
"""Scan the vault for new or changed notes and turn them into question cards.

Intended to be run from cron every minute; it is cheap when nothing changed.
"""
from __future__ import annotations

import argparse
import fcntl
import fnmatch
import sys
import time
from pathlib import Path

import quizgen as qg


def excluded(rel: str) -> bool:
    if any(part.startswith(".") for part in Path(rel).parts):
        return True
    return any(fnmatch.fnmatch(rel, pattern) for pattern in qg.CFG["ingest"]["exclude_globs"])


def iter_notes() -> list[Path]:
    files: list[Path] = []
    for folder in qg.CFG["ingest"]["include_dirs"]:
        root = qg.VAULT / folder
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            rel = path.relative_to(qg.VAULT).as_posix()
            if not excluded(rel):
                files.append(path)
    files.sort(key=lambda p: p.stat().st_mtime)
    return files


def record_error(con, path: Path, message: str) -> None:
    rel = path.relative_to(qg.VAULT).as_posix()
    con.execute(
        """INSERT INTO notes(path,title,kind,hash,size,mtime,ingested_at,card_count,status,error)
           VALUES(?,?,?,?,?,?,?,0,'error',?)
           ON CONFLICT(path) DO UPDATE SET status='error', error=excluded.error,
             ingested_at=excluded.ingested_at""",
        (
            rel,
            path.stem,
            "unknown",
            "",
            path.stat().st_size,
            path.stat().st_mtime,
            qg.iso(qg.now_utc()),
            message[:500],
        ),
    )
    con.commit()


def prune_missing(con, log) -> None:
    """Drop cards for notes that no longer exist (rename or delete)."""
    for row in con.execute("SELECT path FROM notes").fetchall():
        if not (qg.VAULT / row["path"]).exists():
            con.execute("DELETE FROM notes WHERE path = ?", (row["path"],))
            log(f"[prune] {row['path']} no longer exists")
    con.commit()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate question cards from vault notes.")
    parser.add_argument("--scan", action="store_true", help="scan every configured note (default)")
    parser.add_argument("--path", metavar="NOTE", help="ingest a single note")
    parser.add_argument("--force", action="store_true", help="regenerate even when the file is unchanged")
    parser.add_argument("--dry-run", action="store_true", help="print cards without saving anything")
    parser.add_argument("--limit", type=int, default=0, help="process at most N notes this run")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    def log(message: str = "") -> None:
        if not args.quiet:
            print(message, flush=True)

    lock_handle = open(qg.QUIZ_DIR / ".ingest.lock", "w")
    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log("another ingest is already running; skipping this pass")
        return 0

    if not qg.ollama_up():
        log(f"ollama is not responding at {qg.OLLAMA['url']}; will retry next pass")
        return 0

    con = qg.connect()

    if not args.path and not args.dry_run:
        prune_missing(con, log)

    if args.path:
        target = Path(args.path)
        if not target.is_absolute():
            target = (qg.VAULT / target).resolve()
        if not target.is_file():
            log(f"no such note: {target}")
            return 1
        targets = [target]
    else:
        targets = iter_notes()

    settle = float(qg.CFG["ingest"]["settle_seconds"])
    processed = created = skipped = 0
    consecutive_failures = 0
    started = time.time()

    for path in targets:
        if args.limit and processed >= args.limit:
            break
        if not args.path and time.time() - path.stat().st_mtime < settle:
            log(f"[wait] {path.name} is still being written")
            continue
        rel = path.relative_to(qg.VAULT).as_posix()
        note_started = time.time()
        try:
            result = qg.ingest_note(
                con, path, force=args.force, dry_run=args.dry_run, log=(lambda m: log(m)) if not args.quiet else (lambda m: None)
            )
        except qg.OllamaError as exc:
            log(f"[error] {rel}: {exc}")
            if not args.dry_run:
                record_error(con, path, str(exc))
            consecutive_failures += 1
            if consecutive_failures >= 3:
                log("three notes failed in a row; stopping this pass")
                break
            continue
        except Exception as exc:  # keep the watcher alive on a single bad note
            log(f"[error] {rel}: {exc.__class__.__name__}: {exc}")
            if not args.dry_run:
                record_error(con, path, f"{exc.__class__.__name__}: {exc}")
            continue

        consecutive_failures = 0
        if result["skipped"]:
            skipped += 1
            continue

        processed += 1
        created += result["new"]
        elapsed = time.time() - note_started
        log(f"[new] {rel}: {result['new']} cards from {result['chunks']} chunks in {elapsed:.0f}s")

    if processed or args.path:
        log(
            f"done: {processed} note(s) processed, {created} new card(s), "
            f"{skipped} unchanged, {time.time() - started:.0f}s"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
