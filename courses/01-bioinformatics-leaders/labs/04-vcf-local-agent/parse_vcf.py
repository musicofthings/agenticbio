#!/usr/bin/env python3
"""Parse a VCFv4.2 fixture and join a local annotation TSV. No network."""
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


def parse_vcf(path: Path) -> list[list[str]]:
    records: list[list[str]] = []
    with path.open() as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 8:
                continue
            chrom, pos, vid, ref, alt, qual = parts[:6]
            records.append([chrom, pos, vid, ref, alt, qual])
    return records


def main() -> None:
    p = argparse.ArgumentParser(description="Local synthetic VCF parse")
    p.add_argument("--vcf", type=Path, required=True)
    p.add_argument("--annot", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    annot = load_annot(args.annot)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as fh:
        fh.write("chrom\tpos\tid\tref\talt\tqual\tgene_symbol\tnote\n")
        for rec in parse_vcf(args.vcf):
            gene, note = annot.get(rec[2], ("NA", "no local annotation"))
            fh.write("\t".join(rec + [gene, note]) + "\n")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
