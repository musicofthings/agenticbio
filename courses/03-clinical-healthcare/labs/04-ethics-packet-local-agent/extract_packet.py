#!/usr/bin/env python3
"""Index a synthetic IEC checklist against an admin cover. No network."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

CHECK_RE = re.compile(r"^- \[([ xX])\] (.+)$")
FIELD_RE = re.compile(r"^\| ([^|]+) \| ([^|]+) \|$")


def parse_checklist(path: Path) -> list[tuple[bool, str]]:
    items: list[tuple[bool, str]] = []
    for line in path.read_text().splitlines():
        match = CHECK_RE.match(line.strip())
        if match:
            items.append((match.group(1).lower() == "x", match.group(2).strip()))
    return items


def parse_cover_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text().splitlines():
        match = FIELD_RE.match(line.strip())
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip()
        if key.lower() == "field":
            continue
        if set(key) <= {"-"}:
            continue
        fields[key] = value
    return fields


def main() -> None:
    p = argparse.ArgumentParser(description="Local synthetic IEC packet index")
    p.add_argument("--checklist", type=Path, required=True)
    p.add_argument("--cover", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    items = parse_checklist(args.checklist)
    fields = parse_cover_fields(args.cover)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Synthetic packet index",
        "",
        "Teaching data only. Not a real IEC filing. Not a medical device.",
        "",
        "## Cover fields (from local file)",
        "",
    ]
    for key, value in fields.items():
        lines.append(f"- **{key}:** {value}")
    lines += ["", "## Checklist", ""]
    missing = 0
    for present, label in items:
        mark = "present" if present else "MISSING"
        if not present:
            missing += 1
        lines.append(f"- [{mark}] {label}")
    lines += [
        "",
        f"Missing items: {missing}. A human must supply files; do not invent them.",
        "",
    ]
    args.out.write_text("\n".join(lines))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
