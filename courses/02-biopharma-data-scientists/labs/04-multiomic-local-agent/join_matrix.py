#!/usr/bin/env python3
"""Join a synthetic gene×sample matrix to a local annotation TSV. No network."""
from __future__ import annotations

import argparse
from pathlib import Path


def load_annot(path: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    with path.open() as fh:
        header = fh.readline()
        if not header:
            return rows
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            rows[parts[0]] = (parts[1], parts[2])
    return rows


def main() -> None:
    p = argparse.ArgumentParser(description="Local synthetic multiomic join")
    p.add_argument("--expr", type=Path, required=True)
    p.add_argument("--annot", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    annot = load_annot(args.annot)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.expr.open() as src, args.out.open("w") as out:
        header = src.readline().rstrip("\n")
        out.write(header + "\tsymbol\tpathway_note\n")
        for line in src:
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0]:
                continue
            symbol, note = annot.get(parts[0], ("NA", "no local annotation"))
            out.write("\t".join(parts + [symbol, note]) + "\n")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
