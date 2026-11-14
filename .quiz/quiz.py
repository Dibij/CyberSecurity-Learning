#!/usr/bin/env python3
"""Quiz yourself from the local question bank, or export a review note."""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import quizgen as qg

GRADES = {
    "a": "again",
    "again": "again",
    "h": "hard",
    "hard": "hard",
    "g": "good",
    "good": "good",
    "e": "easy",
    "easy": "easy",
}

GRADE_HELP = """
How to grade (grade difficulty, not just correctness):

  a  again   You blanked or were wrong. Card returns in 10 minutes.
  h  hard    You got there late, needed a hint, or guessed. Back tomorrow.
  g  good    You recalled it correctly. Interval grows: 1 → 3 → 7 → 16 → 35 days.
  e  easy    Instant, no hesitation. Skips two boxes.
  s  skip    Don't touch the schedule.
  q  quit    Save what you've done and stop.

Be honest: a card you "sort of" knew is a hard, not a good.
"""


def local_time(value: str | None) -> str:
    dt = qg.parse_iso(value)
    if not dt:
        return "?"
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")


def fetch_cards(
    con: sqlite3.Connection,
    *,
    count: int,
    topic: str | None = None,
    include_all: bool = False,
    new_only: bool = False,
) -> list[sqlite3.Row]:
    sql = """SELECT c.*, n.title AS note_title
             FROM cards c JOIN notes n ON n.path = c.note_path
             WHERE c.suspended = 0"""
    params: list = []
    if new_only:
        sql += " AND c.box = 0"
    elif not include_all:
        sql += " AND c.due <= ?"
        params.append(qg.iso(qg.now_utc()))
    if topic:
        needle = f"%{topic}%"
        sql += " AND (c.question LIKE ? OR c.answer LIKE ? OR c.tags LIKE ? OR n.title LIKE ? OR c.note_path LIKE ?)"
        params.extend([needle] * 5)
    sql += " ORDER BY c.due ASC, RANDOM() LIMIT ?"
    params.append(count)
    return list(con.execute(sql, params))


def print_header(index: int, total: int, card: sqlite3.Row) -> None:
    print()
    print("─" * 72)
    print(
        f"[{index}/{total}]  {card['note_title']}  ·  {card['kind']}  ·  {card['difficulty']}"
    )
    print("─" * 72)
    print(f"\n{card['question']}\n")


def run_quiz(con: sqlite3.Connection, cards: list[sqlite3.Row]) -> int:
    answered = 0
    print(
        "grade: a=again · h=hard · g=good · e=easy · s=skip · q=quit"
        "   (type ? at the prompt for help)\n"
    )
    for index, card in enumerate(cards, start=1):
        print_header(index, len(cards), card)
        try:
            reveal = input("press Enter to reveal the answer (q to quit) ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if reveal.strip().lower() == "q":
            print("\nstopped early.")
            break
        print(f"\nAnswer: {card['answer']}\n")
        if card["evidence"]:
            print(f"Evidence: \"{card['evidence']}\"\n")

        while True:
            try:
                raw = input("grade  [a]gain  [h]ard  [g]ood  [e]asy  [s]kip  [q]uit  (? help) > ")
            except (EOFError, KeyboardInterrupt):
                raw = "q"
            raw = raw.strip().lower()
            if raw == "?":
                print(GRADE_HELP)
                continue
            if raw == "q":
                print("\nstopped early.")
                break
            if raw == "s":
                break
            grade = GRADES.get(raw)
            if not grade:
                print("  enter a, h, g, e, s, q, or ? for help")
                continue
            new_box, due = qg.apply_grade(card["box"], grade)
            now = qg.iso(qg.now_utc())
            con.execute(
                """UPDATE cards SET box=?, due=?, last_reviewed=?, reviews=reviews+1,
                         lapses=lapses+? WHERE id=?""",
                (new_box, qg.iso(due), now, 1 if grade == "again" else 0, card["id"]),
            )
            con.execute(
                """INSERT INTO reviews(card_id, ts, grade, box_before, box_after)
                   VALUES(?,?,?,?,?)""",
                (card["id"], now, grade, card["box"], new_box),
            )
            con.commit()
            answered += 1
            next_review = due.astimezone().strftime("%Y-%m-%d %H:%M")
            print(f"  → box {new_box}, next review {next_review}")
            break

        if raw == "q":
            break

    due_count = con.execute(
        "SELECT COUNT(*) AS n FROM cards WHERE suspended=0 AND due <= ?",
        (qg.iso(qg.now_utc()),),
    ).fetchone()["n"]
    print(f"\nReviewed {answered} card(s). {due_count} card(s) still due.\n")
    return answered


def cmd_stats(con: sqlite3.Connection) -> None:
    total = con.execute("SELECT COUNT(*) AS n FROM cards WHERE suspended=0").fetchone()["n"]
    due = con.execute(
        "SELECT COUNT(*) AS n FROM cards WHERE suspended=0 AND due <= ?",
        (qg.iso(qg.now_utc()),),
    ).fetchone()["n"]
    new = con.execute(
        "SELECT COUNT(*) AS n FROM cards WHERE suspended=0 AND box=0"
    ).fetchone()["n"]
    notes = con.execute("SELECT COUNT(*) AS n FROM notes WHERE card_count > 0").fetchone()["n"]

    midnight = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    today = con.execute(
        "SELECT COUNT(*) AS n FROM reviews WHERE ts >= ?", (qg.iso(midnight),)
    ).fetchone()["n"]
    lifetime = con.execute("SELECT COUNT(*) AS n FROM reviews").fetchone()["n"]

    print(f"Question bank — {total} cards from {notes} notes")
    print(f"  due now {due} · new {new} · reviewed today {today} · lifetime reviews {lifetime}")

    rows = con.execute(
        """SELECT n.title, n.path, COUNT(c.id) AS total,
                  SUM(CASE WHEN c.due <= ? THEN 1 ELSE 0 END) AS due
           FROM notes n JOIN cards c ON c.note_path = n.path
           GROUP BY n.path ORDER BY due DESC, total DESC""",
        (qg.iso(qg.now_utc()),),
    ).fetchall()
    if rows:
        print("\n  by note:")
        for row in rows:
            print(f"    {row['total']:>3} cards · {row['due']:>3} due · {row['title']}")

    next_due = con.execute(
        "SELECT MIN(due) AS d FROM cards WHERE suspended=0 AND due > ?",
        (qg.iso(qg.now_utc()),),
    ).fetchone()["d"]
    if next_due:
        print(f"\n  next scheduled review: {local_time(next_due)}")


def note_stem(path: str) -> str:
    return Path(path).stem


def write_review_note(con: sqlite3.Connection, cards: list[sqlite3.Row], out: Path) -> Path:
    today = datetime.now().astimezone().strftime("%Y-%m-%d")
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "---",
        f'title: "Review — {today}"',
        "type: review",
        f"date: {today}",
        "tags:",
        "  - review",
        "---",
        "",
        f"# Review — {today}",
        "",
        f"> {len(cards)} questions pulled from the vault question bank.",
        "> Answers are folded. Unfold only after answering out loud.",
        "",
    ]

    grouped: dict[str, list[sqlite3.Row]] = {}
    for card in cards:
        grouped.setdefault(card["note_path"], []).append(card)

    question_number = 0
    for note_path, note_cards in grouped.items():
        title = note_cards[0]["note_title"]
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"Source: [[{note_stem(note_path)}]]")
        lines.append("")
        for card in note_cards:
            question_number += 1
            lines.append(
                f"### Q{question_number} · {card['kind']} · {card['difficulty']}"
            )
            lines.append("")
            lines.append(card["question"])
            lines.append("")
            lines.append("<details><summary>Answer</summary>")
            lines.append("")
            lines.append(card["answer"])
            if card["evidence"]:
                lines.append("")
                lines.append(f"> **Evidence:** \"{card['evidence']}\"")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Quiz yourself from the local question bank.")
    parser.add_argument("--count", type=int, default=qg.SRS["default_count"])
    parser.add_argument("--topic", help="only cards matching this word (e.g. xss, dns, bandit)")
    parser.add_argument("--all", action="store_true", help="include cards that are not due yet")
    parser.add_argument("--new", action="store_true", help="only cards that were never reviewed")
    parser.add_argument("--stats", action="store_true", help="show bank statistics")
    parser.add_argument(
        "--note",
        nargs="?",
        const="",
        metavar="PATH",
        help="export the selected questions to an Obsidian note instead of quizzing",
    )
    args = parser.parse_args()

    con = qg.connect()

    if args.stats:
        cmd_stats(con)
        return 0

    cards = fetch_cards(
        con,
        count=args.count,
        topic=args.topic,
        include_all=args.all,
        new_only=args.new,
    )

    if not cards:
        print("No cards match. Try --new, --all, or --topic.")
        return 0

    if args.note is not None:
        today = datetime.now().astimezone().strftime("%Y-%m-%d")
        out = (
            Path(args.note).expanduser()
            if args.note
            else qg.VAULT / "07 - Review" / "Daily" / f"{today}.md"
        )
        path = write_review_note(con, cards, out)
        print(f"wrote {len(cards)} questions to {path}")
        return 0

    run_quiz(con, cards)
    return 0


if __name__ == "__main__":
    sys.exit(main())
