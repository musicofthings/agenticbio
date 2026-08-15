# Capstone — architecture one-pager template

Copy into a PDF or ClassroomIO assignment. One page. No sample-level data.

## System name

## Trust boundary
What may leave the machine, what must not, and where logs live.

## Data flow
Fixture in → agent plan → Nextflow process(es) → TSV/report out → human gate.

## Execution plane
Which steps are Nextflow processes vs agent-only (read/plan). Name the container image tag.

## Failure modes
Two realistic failures (model hallucination of a variant row; Nextflow process non-zero) and the human action.

## What this is not
Not a medical device. Synthetic data only. No production LIMS write-back.
