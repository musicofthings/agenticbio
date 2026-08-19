# Capstone — architecture one-pager (cohort 5, grant outline)

Copy into a PDF or ClassroomIO assignment. One page. No unpublished manuscripts or real budgets.

## System name

## Trust boundary
What may leave (how an outline is gated), what must not (manuscript bodies, real budget lines, reviewer identities), and where logs live.

## Data flow
Synthetic abstracts + BioE3-style template in → agent plan → Nextflow process(es) → filled outline out → human gate before any portal paste.

## Execution plane
Which steps are Nextflow processes vs agent-only. Name the container image tag. Each filled bullet must cite a local `SYNTH-ABS-*` id.

## Failure modes
Two realistic failures (abstract missing a `section:` field; empty template heading) and the human action. Week 6 uses `data/broken-abstracts/` on purpose.

## What this is not
Not a medical device. Invented teaching abstracts only. The Fellowship does not file grants. No cloud writer. No auto-submit.
