#!/usr/bin/env python3
"""Core engine for the vault recall question bank.

Notes are the source of truth. Cards live in SQLite so the daily quiz never
needs to wait for a model. Only stdlib is used.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

QUIZ_DIR = Path(__file__).resolve().parent
VAULT = QUIZ_DIR.parent
CONFIG_PATH = QUIZ_DIR / "config.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


CFG = load_config()
if os.environ.get("QUIZ_MODEL"):
    CFG["ollama"]["model"] = os.environ["QUIZ_MODEL"]
if os.environ.get("QUIZ_OLLAMA_URL"):
    CFG["ollama"]["url"] = os.environ["QUIZ_OLLAMA_URL"]
DB_PATH = VAULT / CFG["db_path"]
OLLAMA = CFG["ollama"]
GEN = CFG["generation"]
SRS = CFG["srs"]


# ---------------------------------------------------------------- time helpers

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


# ------------------------------------------------------------------- database

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    path        TEXT PRIMARY KEY,
    title       TEXT,
    kind        TEXT,
    hash        TEXT,
    size        INTEGER,
    mtime       REAL,
    ingested_at TEXT,
    card_count  INTEGER NOT NULL DEFAULT 0,
    status      TEXT NOT NULL DEFAULT 'ok',
    error       TEXT
);

CREATE TABLE IF NOT EXISTS cards (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    note_path     TEXT NOT NULL REFERENCES notes(path) ON DELETE CASCADE,
    question      TEXT NOT NULL,
    answer        TEXT NOT NULL,
    evidence      TEXT,
    kind          TEXT,
    difficulty    TEXT,
    tags          TEXT,
    qkey          TEXT,
    created_at    TEXT NOT NULL,
    box           INTEGER NOT NULL DEFAULT 0,
    due           TEXT NOT NULL,
    last_reviewed TEXT,
    reviews       INTEGER NOT NULL DEFAULT 0,
    lapses        INTEGER NOT NULL DEFAULT 0,
    suspended     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reviews (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id    INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
    ts         TEXT NOT NULL,
    grade      TEXT NOT NULL,
    box_before INTEGER,
    box_after  INTEGER
);

CREATE INDEX IF NOT EXISTS idx_cards_due  ON cards(due);
CREATE INDEX IF NOT EXISTS idx_cards_note ON cards(note_path);
CREATE INDEX IF NOT EXISTS idx_reviews_ts ON reviews(ts);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(SCHEMA)
    columns = {row["name"] for row in con.execute("PRAGMA table_info(cards)")}
    if "evidence" not in columns:
        con.execute("ALTER TABLE cards ADD COLUMN evidence TEXT")
    con.commit()
    return con


# --------------------------------------------------------------- note parsing

FM_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n?", re.S)
WIKILINK_RE = re.compile(r"!?\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

SKIP_SECTIONS = re.compile(
    r"related notes?|next session|next steps|further reading|references|resources|^links$",
    re.I,
)


def _scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    meta: dict = {"tags": []}
    body = raw
    match = FM_RE.match(raw)
    if not match:
        return meta, body
    block = match.group(1)
    body = raw[match.end():]
    in_tags = False
    for line in block.splitlines():
        if re.match(r"^tags\s*:", line, re.I):
            in_tags = True
            inline = line.split(":", 1)[1].strip()
            if inline.startswith("["):
                meta["tags"] = [
                    _scalar(t) for t in inline.strip("[]").split(",") if _scalar(t)
                ]
            elif inline:
                meta["tags"] = [_scalar(t) for t in inline.split(",") if _scalar(t)]
            continue
        if in_tags:
            item = re.match(r"^\s*-\s+(.+)$", line)
            if item:
                meta["tags"].append(_scalar(item.group(1)))
                continue
            if line.strip():
                in_tags = False
        key = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.+)$", line)
        if key and not line.startswith((" ", "\t")):
            meta[key.group(1)] = _scalar(key.group(2))
    return meta, body


def clean_text(body: str) -> str:
    body = COMMENT_RE.sub("", body)
    body = WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1), body)
    body = re.sub(
        r"(?im)^(related|see also)\s+notes?\s*:?\s*\n(?:[ \t]*[-*].*\n?)*", "", body
    )
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def note_title(meta: dict, body: str, path: Path) -> str:
    if meta.get("title"):
        return meta["title"]
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def split_sections(body: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, text) chunks on level-2 headings."""
    sections: list[tuple[str, str]] = []
    heading, buf = "", []
    for line in body.splitlines():
        if line.startswith("## "):
            if "\n".join(buf).strip():
                sections.append((heading, "\n".join(buf).strip()))
            heading, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if "\n".join(buf).strip():
        sections.append((heading, "\n".join(buf).strip()))
    return [(h, t) for h, t in sections if not SKIP_SECTIONS.search(h)]


def _pack(parts: list[str], limit: int) -> list[str]:
    out: list[str] = []
    cur: list[str] = []
    size = 0
    for part in parts:
        extra = len(part) + 2
        if cur and size + extra > limit:
            out.append("\n\n".join(cur))
            cur, size = [], 0
        cur.append(part)
        size += extra
    if cur:
        out.append("\n\n".join(cur))
    return out


def make_chunks(sections: list[tuple[str, str]], limit: int) -> list[str]:
    parts: list[str] = []
    for heading, text in sections:
        block = (f"## {heading}\n" if heading else "") + text.strip()
        if len(block) <= limit:
            parts.append(block)
            continue
        for para in re.split(r"\n{2,}", block):
            para = para.strip()
            if para:
                parts.extend(_pack([para], limit))
    return _pack(parts, limit)


# --------------------------------------------------------------------- ollama

class OllamaError(RuntimeError):
    pass


CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "source": {"type": "integer"},
                    "kind": {
                        "type": "string",
                        "enum": [
                            "definition",
                            "mechanism",
                            "application",
                            "comparison",
                            "gotcha",
                            "command",
                            "defense",
                        ],
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"],
                    },
                },
                "required": ["question", "answer", "source", "kind", "difficulty"],
            },
        }
    },
    "required": ["cards"],
}


def ollama_up() -> bool:
    try:
        with urllib.request.urlopen(
            OLLAMA["url"].rstrip("/") + "/api/tags", timeout=3
        ) as response:
            return response.status == 200
    except Exception:
        return False


def chat(messages: list[dict], json_mode: bool = True, timeout: int | None = None, retry: bool = False) -> str:
    payload = {
        "model": OLLAMA["model"],
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.15 if retry else GEN["temperature"],
            "num_ctx": GEN["num_ctx"],
            "num_predict": min(600, GEN["num_predict"]) if retry else GEN["num_predict"],
            "repeat_penalty": 1.25 if retry else 1.08,
            "repeat_last_n": 256,
        },
    }
    if json_mode:
        payload["format"] = CARD_SCHEMA
    request = urllib.request.Request(
        OLLAMA["url"].rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=timeout or OLLAMA.get("timeout", 600)
        ) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise OllamaError(f"ollama HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise OllamaError(f"ollama unreachable at {OLLAMA['url']}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise OllamaError(f"ollama returned non-JSON envelope: {exc}") from exc
    content = (data.get("message") or {}).get("content", "")
    if not content:
        raise OllamaError("ollama returned an empty message")
    return content


SYSTEM_PROMPT = (
    "You are a cybersecurity instructor who writes retrieval-practice questions. "
    "You are technically precise, you use only the supplied note, and you never "
    "invent facts that are not in it."
)


def build_prompt(title: str, tags: list[str], passage: str, count: int, sentence_count: int = 0) -> str:
    return f"""Read the PASSAGE from a student's cybersecurity note and write {count} question/answer pairs for retrieval practice.

The PASSAGE is split into numbered sentences like "[3] ...". Cite the sentence that proves each answer.

RULES
1. Test technical understanding: definitions, how a mechanism works, why it matters, how to apply it, differences between concepts, common gotchas, and defenses.
2. Never ask about the student's activities or the study session. Do not ask "what did you do", "which lab did you solve", "what payload did you try", "what did you learn today", or for a summary.
3. Every question must be answerable from the PASSAGE alone.
4. One fact per question. The question must end with "?".
5. The answer is 1-2 precise sentences, in your own words. Do not say "the passage says" and do not use first person ("I", "we").
6. source is the number of the single sentence that most directly supports the answer. It must be an integer between 1 and {sentence_count or "the last number"}.
7. kind is one of: definition, mechanism, application, comparison, gotcha, command, defense.
8. difficulty is one of: easy, medium, hard.
9. Write every question and answer in English.
10. Do not ask about other notes, links, or this document, and do not ask generic language trivia (for example "what does CSS control") unless the passage ties it directly to exploitation.
11. Prefer a few high-value questions about the core security concept over many shallow ones.

NOTE TITLE: {title}
NOTE TAGS: {", ".join(tags) if tags else "(none)"}

PASSAGE:
---
{passage}
---

Return JSON only, in exactly this shape:
{{"cards":[{{"question":"...","answer":"...","source":3,"kind":"definition","difficulty":"easy"}}]}}"""


BAD_QUESTION = re.compile(
    r"\b(what did (you|i|we)|which lab|what lab|this session|today i|this note|the note|"
    r"related note|in relation to this|in this document|the document|the student|"
    r"source sentence|in this lab|in the provided lab|"
    r"what (specific )?payload (was|did)|which payload|"
    r"according to the (note|passage|text|document)|"
    r"the (note|passage|text|document) (says|states|mentions)|lab \d+)\b"
    r"|^\[\d+\]"
    r"|\b(topic|summary)\b[^?]*\b(session|note|notes|document)\b"
    r"|\b(session|note|notes|document)\b[^?]*\b(described|covered|discussed)\b",
    re.I,
)


def parse_cards(raw: str) -> list[dict]:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    data = None
    try:
        data = json.loads(text)
    except Exception:
        starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
        if starts:
            try:
                data, _ = json.JSONDecoder().raw_decode(text[min(starts):])
            except Exception:
                data = None
    if data is None:
        return []
    if isinstance(data, dict):
        for key in ("cards", "questions", "items"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
        else:
            data = [data] if ("question" in data or "q" in data) else []
    if not isinstance(data, list):
        return []

    cards: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question") or item.get("q") or "").strip()
        answer = str(item.get("answer") or item.get("a") or "").strip()
        try:
            source = int(item.get("source") or 0)
        except (TypeError, ValueError):
            source = 0
        kind = str(item.get("kind") or "concept").strip().lower()
        difficulty = str(item.get("difficulty") or "medium").strip().lower()
        question = re.sub(r"\s+", " ", question)
        answer = re.sub(r"\s+", " ", answer)
        if not (12 <= len(question) <= 240):
            continue
        if not (15 <= len(answer) <= 700):
            continue
        if source < 1:
            continue
        if not question.endswith("?"):
            question = question.rstrip(".") + "?"
        if BAD_QUESTION.search(question):
            continue
        if re.search(r"\b(I|we|my|our|had to|I'd|we'd)\b", answer):
            continue
        if not re.search(r"[.!?`'\"\)\]]$", answer):
            continue  # truncated generation
        if kind not in {"definition", "mechanism", "application", "comparison", "gotcha", "command", "defense"}:
            kind = "concept"
        if difficulty not in {"easy", "medium", "hard"}:
            difficulty = "medium"
        cards.append(
            {
                "question": question,
                "answer": answer,
                "source": source,
                "kind": kind,
                "difficulty": difficulty,
            }
        )
    return cards


SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _passage_sentences(passage: str) -> list[str]:
    found: list[str] = []
    for line in passage.splitlines():
        line = line.strip().lstrip("->*#").strip()
        line = re.sub(r"^\d+[.)]\s+", "", line)
        if not line or set(line) <= set("-| "):
            continue
        for part in SENTENCE_SPLIT.split(line):
            part = part.strip(" |")
            if 20 <= len(part) <= 400:
                found.append(part)
    return found


STOPWORDS = set(
    "a an the is are was were be been of to in on for and or with that this it as by "
    "from can do does what why how when which who whom whose would should could "
    "you your i we our they them their there here at into about than then".split()
)
WORD_RE = re.compile(r"[a-z0-9]+")


def q_tokens(question: str) -> set[str]:
    return {
        w for w in WORD_RE.findall(question.lower()) if w not in STOPWORDS and len(w) > 2
    }


def is_duplicate(question: str, existing: list[tuple[set[str], str]], threshold: float = 0.62) -> bool:
    tokens = q_tokens(question)
    if not tokens:
        return True
    lowered = question.lower()
    for other_tokens, other_question in existing:
        if other_tokens:
            overlap = len(tokens & other_tokens) / len(tokens | other_tokens)
            if overlap >= threshold:
                return True
        if difflib.SequenceMatcher(None, lowered, other_question).ratio() >= 0.8:
            return True
    return False


# ------------------------------------------------------------------ ingestion

def note_kind(meta: dict, rel: str) -> str:
    if meta.get("type"):
        return meta["type"]
    return "journal" if rel.startswith("01 - Journal/") else "concept"


def ingest_note(
    con: sqlite3.Connection,
    path: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
    log=print,
) -> dict:
    rel = path.relative_to(VAULT).as_posix()
    raw = path.read_text(encoding="utf-8", errors="replace")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    stat = path.stat()

    row = con.execute(
        "SELECT hash, status FROM notes WHERE path = ?", (rel,)
    ).fetchone()
    if row and row["hash"] == digest and row["status"] in {"ok", "empty", "short"} and not force:
        return {"path": rel, "skipped": True, "new": 0, "chunks": 0}

    meta, body = parse_frontmatter(raw)
    body = clean_text(body)
    title = note_title(meta, body, path)
    tags = [str(t) for t in meta.get("tags", [])]
    kind = note_kind(meta, rel)

    # journals open with date/topic metadata; only the sections below matter
    if kind == "journal":
        cut = body.find("\n## ")
        if cut > 0:
            body = body[cut + 1:]

    if len(body) < CFG["ingest"]["min_chars"] and not force:
        if not dry_run:
            con.execute(
                """INSERT INTO notes(path,title,kind,hash,size,mtime,ingested_at,card_count,status)
                   VALUES(?,?,?,?,?,?,?,0,'short')
                   ON CONFLICT(path) DO UPDATE SET hash=excluded.hash,size=excluded.size,
                     mtime=excluded.mtime,ingested_at=excluded.ingested_at,status='short'""",
                (rel, title, kind, digest, stat.st_size, stat.st_mtime, iso(now_utc())),
            )
            con.commit()
        log(f"[skip] {rel}: only {len(body)} chars of body")
        return {"path": rel, "skipped": True, "new": 0, "chunks": 0}

    chunks = make_chunks(split_sections(body), GEN["chunk_chars"])
    if not chunks:
        chunks = [body[: GEN["chunk_chars"]]]

    existing = [
        (q_tokens(r["question"]), r["question"].lower())
        for r in con.execute(
            "SELECT question FROM cards WHERE note_path = ?", (rel,)
        )
    ]
    collected: list[dict] = []
    failures = 0
    per_chunk = GEN["cards_per_chunk"]

    for index, chunk in enumerate(chunks, start=1):
        sentences = _passage_sentences(chunk)
        if len(sentences) < 2:
            continue
        numbered = "\n".join(f"[{i}] {s}" for i, s in enumerate(sentences, 1))
        needed = min(per_chunk, GEN["max_cards_per_note"] - len(collected))
        if needed <= 0:
            break
        prompt = build_prompt(title, tags, numbered, needed, len(sentences))
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        try:
            raw_out = chat(messages)
        except OllamaError as exc:
            log(f"  chunk {index} failed ({exc}); retrying with tighter sampling")
            try:
                raw_out = chat(messages, retry=True)
            except OllamaError as exc2:
                log(f"  chunk {index} failed again ({exc2}); skipping it")
                failures += 1
                continue
        for card in parse_cards(raw_out):
            source = card.pop("source", 0)
            if not (1 <= source <= len(sentences)):
                continue
            card["evidence"] = sentences[source - 1]
            if is_duplicate(card["question"], existing):
                continue
            existing.append((q_tokens(card["question"]), card["question"].lower()))
            collected.append(card)
            if len(collected) >= GEN["max_cards_per_note"]:
                break
        log(f"  chunk {index}/{len(chunks)} -> {len(collected)} cards so far")

    if dry_run:
        for card in collected:
            log(f"    Q: {card['question']}\n       A: {card['answer']}\n       E: {card['evidence']}")
        return {"path": rel, "skipped": False, "new": len(collected), "chunks": len(chunks)}

    if failures and not collected:
        raise OllamaError(f"every chunk failed for {rel}")

    timestamp = iso(now_utc())
    con.execute(
        """INSERT INTO notes(path,title,kind,hash,size,mtime,ingested_at,card_count,status,error)
           VALUES(?,?,?,?,?,?,?,?,? ,NULL)
           ON CONFLICT(path) DO UPDATE SET title=excluded.title,kind=excluded.kind,
             hash=excluded.hash,size=excluded.size,mtime=excluded.mtime,
             ingested_at=excluded.ingested_at,card_count=excluded.card_count,
             status=excluded.status,error=NULL""",
        (
            rel,
            title,
            kind,
            digest,
            stat.st_size,
            stat.st_mtime,
            timestamp,
            len(collected),
            "partial" if failures else ("ok" if collected else "empty"),
        ),
    )
    for card in collected:
        con.execute(
            """INSERT INTO cards(note_path,question,answer,evidence,kind,difficulty,tags,qkey,
                                 created_at,box,due)
               VALUES(?,?,?,?,?,?,?,?,?,0,?)""",
            (
                rel,
                card["question"],
                card["answer"],
                card.get("evidence"),
                card["kind"],
                card["difficulty"],
                json.dumps(tags),
                " ".join(sorted(q_tokens(card["question"]))),
                timestamp,
                timestamp,
            ),
        )
    con.commit()
    return {"path": rel, "skipped": False, "new": len(collected), "chunks": len(chunks)}


# ------------------------------------------------------------------------ SRS

def apply_grade(box: int, grade: str) -> tuple[int, datetime]:
    """Return (new_box, due_datetime_utc)."""
    max_box = SRS["max_box"]
    intervals = SRS["intervals_days"]
    now = now_utc()
    if grade == "again":
        return 0, now + timedelta(minutes=SRS["again_minutes"])
    if grade == "hard":
        new_box = max(1, box)
        return new_box, now + timedelta(days=1)
    if grade == "good":
        new_box = min(max_box, box + 1)
    elif grade == "easy":
        new_box = min(max_box, box + 2)
    else:
        raise ValueError(f"unknown grade: {grade}")
    return new_box, now + timedelta(days=intervals[new_box])
