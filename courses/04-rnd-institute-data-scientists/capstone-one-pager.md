# Capstone — architecture one-pager (cohort 4, local manual retrieve)

Copy into a PDF or ClassroomIO assignment. One page. No real institute SOP dump.

## System name

## Trust boundary
What may leave (how retrieval is gated), what must not (manual bodies, internal hostnames, unpublished figures), and where logs live.

## Data flow
Synthetic manuals + query in → agent plan → Nextflow process(es) → scored hits out → human gate before write-back to a live SOP tree.

## Execution plane
Which steps are Nextflow processes vs agent-only. Name the container image tag. Retrieval is keyword overlap on disk — no embedding API.

## Failure modes
Two realistic failures (empty/vague query; a hit that cannot cite a path) and the human action. Week 6 uses `data/broken-query.txt` on purpose.

## What this is not
Not a medical device. Synthetic teaching manuals only. No vendor RAG upload. No auto-merge into a live SOP.
