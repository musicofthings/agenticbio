# Lab 04 — Synthetic VCF v4.2, local parse

**Module:** 5  
**Timebox:** 2–3 hours async  
**Data:** `data/synthetic.vcf` only. Invented sites and sample ids (`SYNTH-001`). Not from a patient, not from a public disease study.

## Objective

Parse a VCFv4.2 fixture **on disk**, emit a TSV of CHROM/POS/REF/ALT/QUAL, and join a local annotation table (`data/annotation.tsv`). No Ensembl, ClinVar, or other network annotation APIs.

## Constraints

- Do not replace `synthetic.vcf` with a real cohort export.
- Do not call external REST annotation services.
- A future agent may propose the parse command; a human must approve any rewrite of the VCF.

## What to run

```bash
python3 parse_vcf.py --vcf data/synthetic.vcf --annot data/annotation.tsv --out outputs/variants.tsv
```

Optional: run the same script inside the lab 02 image with bind mounts.

## Acceptance criteria

- [ ] `outputs/variants.tsv` has a header and one row per variant record (not header lines)
- [ ] Annotation column is filled from the local TSV (or `NA` if missing) — not from the internet
- [ ] README or comments state that this file is synthetic teaching data

## ClassroomIO

Attach this folder to Module 5. Assignment: `outputs/variants.tsv` plus one paragraph on why ClinVar-over-HTTPS is out of scope for the lab.
