# Lab 04 — Synthetic multiomic matrix, local join

**Module:** 5 (cohort 2)  
**Timebox:** 2–3 hours async  
**Data:** `data/expression.tsv` only. Invented gene ids and sample ids (`SYNTH-DS-001`). Not from a trial, not from GEO-as-proxy for partner data.

## Objective

Join a gene × sample matrix **on disk** to a local annotation table (`data/annotation.tsv`). No Enrichr, STRING, or other network enrichment APIs.

## Constraints

- Do not replace `expression.tsv` with a real assay export.
- Do not call external REST annotation or enrichment services.
- A future agent may propose the join command; a human must approve any rewrite of the matrix.

## What to run

```bash
python3 join_matrix.py --expr data/expression.tsv --annot data/annotation.tsv --out outputs/joined.tsv
```

Optional: run the same script inside the cohort 1 lab 02 image with bind mounts. `outputs/` is gitignored — do not commit joined matrices.

## Week 6 — bounded fail / patch

Canonical `data/expression.tsv` stays untouched. Run the **broken** copy (commas, not tabs):

```bash
python3 join_matrix.py --expr data/broken-expression.tsv --annot data/annotation.tsv --out outputs/joined-broken.tsv
```

Gene ids will not match the annotation table. Propose a TSV patch, get a human yes, write under `outputs/`. Max three iterations.

## Acceptance criteria

- [ ] `outputs/joined.tsv` has a header and one row per gene
- [ ] Annotation columns are filled from the local TSV (or `NA` if missing) — not from the internet
- [ ] README or comments state that this file is synthetic teaching data

## ClassroomIO

Attach this folder to Module 5. Assignment: `outputs/joined.tsv` plus one paragraph on why Enrichr-over-HTTPS is out of scope for the lab.
