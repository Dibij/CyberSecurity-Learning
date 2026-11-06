#!/usr/bin/env bash
# Cron entry point. Cheap no-op when no note changed.
set -uo pipefail

QUIZ_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname -- "$QUIZ_DIR")"
LOG="$QUIZ_DIR/logs/ingest.log"
mkdir -p "$QUIZ_DIR/logs"

# keep the log from growing forever
if [[ -f "$LOG" ]] && (( $(stat -c%s "$LOG") > 2000000 )); then
  tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

cd "$ROOT" || exit 1
exec /usr/bin/python3 "$QUIZ_DIR/ingest.py" --scan >>"$LOG" 2>&1
