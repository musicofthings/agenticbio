# Capstone — architecture one-pager (cohort 3, IEC packet)

Copy into a PDF or ClassroomIO assignment. One page. No identifiable notes or live packets.

## System name

## Trust boundary
What may leave (how a packet is gated), what must not (names, MRNs, report text, real consent forms), and where logs live.

## Data flow
Synthetic checklist + admin cover in → agent plan → Nextflow process(es) → packet index out → human gate before any filing.

## Execution plane
Which steps are Nextflow processes vs agent-only. Name the container image tag.

## Failure modes
Two realistic failures (checklist items not parsed; missing cover field) and the human action. Week 6 uses `data/broken-iec-checklist.md` on purpose.

## What this is not
Not a medical device. Not diagnosis or treatment. Synthetic teaching documents only. No IEC portal submit. No invented CVs or signatures.
