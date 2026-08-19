#!/usr/bin/env python3
"""Keyword-overlap retrieve over a local markdown corpus. No network."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def score(query: set[str], doc: set[str]) -> float:
    if not query:
        return 0.0
    return len(query & doc) / len(query)


def main() -> None:
    p = argparse.ArgumentParser(description="Local synthetic manual retrieve")
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--query", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--k", type=int, default=3)
    args = p.parse_args()

    query_text = args.query.read_text()
    q = tokens(query_text)
    ranked: list[tuple[float, Path, str]] = []
    for path in sorted(args.corpus.glob("*.md")):
        body = path.read_text()
        ranked.append((score(q, tokens(body)), path, body.strip()))
    ranked.sort(key=lambda row: (-row[0], str(row[1])))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Local retrieval hits",
        "",
        "Synthetic teaching corpus. No network. Not a real institute SOP dump.",
        "",
        f"Query file: `{args.query.name}`",
        "",
    ]
    hits = [row for row in ranked if row[0] > 0][: args.k]
    if not hits:
        lines.append("No overlap with the local corpus.")
    for rank, (sc, path, body) in enumerate(hits, start=1):
        snippet = " ".join(body.split())[:280]
        lines += [
            f"## {rank}. `{path.name}` (overlap={sc:.2f})",
            "",
            snippet,
            "",
        ]
    args.out.write_text("\n".join(lines))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
