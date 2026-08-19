# Capstone — architecture one-pager (cohort 2, discovery / matrix)

Copy into a PDF or ClassroomIO assignment. One page. No sample-level assay data.

## System name

## Trust boundary
What may leave the machine (process questions), what must not (matrices, sample IDs, unpublished figures, partner tables), and where prompts/logs live.

## Data flow
Synthetic matrix in → agent plan → Nextflow process(es) → joined TSV out → human gate.

## Execution plane
Which steps are Nextflow processes vs agent-only (read/plan). Name the container image tag.

## Failure modes
Two realistic failures (malformed TSV row; Nextflow process non-zero) and the human action. Week 6 uses `data/broken-expression.tsv` on purpose.

## What this is not
Not a medical device. Synthetic teaching data only. No LIMS write-back. No Enrichr-over-HTTPS.
