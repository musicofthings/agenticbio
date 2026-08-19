#!/usr/bin/env python3
"""Fill a grant outline from invented teaching abstracts. No network."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FIELD_RE = re.compile(r"^(id|title|claim|gap|section):\s*(.+)$")


def parse_abstract(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {"source": path.name}
    for line in path.read_text().splitlines():
        match = FIELD_RE.match(line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def main() -> None:
    p = argparse.ArgumentParser(description="Local synthetic grant outline fill")
    p.add_argument("--abstracts", type=Path, required=True)
    p.add_argument("--template", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    records = [parse_abstract(path) for path in sorted(args.abstracts.glob("*.md"))]
    by_section: dict[str, list[dict[str, str]]] = {}
    for rec in records:
        by_section.setdefault(rec.get("section", "Need and rationale"), []).append(rec)

    lines = [
        "# Synthetic grant outline",
        "",
        "Invented teaching abstracts only. Not a BioE3 filing. Not a medical device.",
        "",
    ]
    current_heading: str | None = None
    for raw in args.template.read_text().splitlines():
        if raw.startswith("## "):
            current_heading = raw[3:].strip()
            lines += [raw, ""]
            for rec in by_section.get(current_heading, []):
                abs_id = rec.get("id", rec["source"])
                title = rec.get("title", "")
                claim = rec.get("claim", "")
                gap = rec.get("gap", "")
                lines.append(f"- **{abs_id}** ({title}): {claim} Gap: {gap}")
            if current_heading not in by_section:
                lines.append("- _No local abstract mapped to this heading._")
            lines.append("")
        elif raw.startswith("# "):
            continue
        elif raw.strip():
            lines += [raw, ""]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines).rstrip() + "\n")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
