#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${ROOT}/outputs"
PROMPT="$(cat "${ROOT}/fixtures/governance-note.txt")

Restate the rule in three bullet points for a bioinformatics lead. Do not invent sample data."

if ! command -v ollama >/dev/null 2>&1; then
  echo "ollama not on PATH — use scripts/offline_stub.py" >&2
  exit 1
fi

ollama run llama3.2:1b "${PROMPT}" | tee "${ROOT}/outputs/completion.txt"
