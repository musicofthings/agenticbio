# The Agentic Bio Fellowship — Academic Scientists (ICMR, CSIR, DBT)

ClassroomIO-ready outline for **cohort 5**. Same technical core as cohort 1. Skin: **literature synthesis and grant architecture** (e.g. BioE3-style sections) on a machine you control. Teaching abstracts are invented; we do not copy publisher PDFs.

**LMS title:** The Agentic Bio Fellowship: Local Literature Synthesis and Grant Architecture  
**Duration:** 6–8 weeks (live sessions + async labs + recordings)  
**Tracks:** Individual Innovator ₹1.5L · Enterprise Team ₹5L (3–5 seats + 60-min architecture review)

Do not launch this cohort until earlier tracks are filling. Shared labs live in [`../01-bioinformatics-leaders/labs/`](../01-bioinformatics-leaders/labs/).

## Positioning

Privacy-first **local** synthesis of notes you already hold (institute reports, your own drafts, teaching abstracts). Agents plan; **Nextflow (DSL2) executes**. No “upload the unpublished manuscript to a cloud writer.” Grant *structure* is the product; the agency portal stays a human submit.

## Audience

**For:** PIs and senior scientists at ICMR, CSIR, DBT labs and university groups who already write grants and literature notes and need a local loop that does not leak unpublished text.

**Not for:** students hunting a chatbot to rewrite a real paper, or anyone expecting the Fellowship to file a BioE3 proposal for them.

## Learning outcomes

By the capstone, a fellow can:

1. Run a local LLM with an explicit boundary for unpublished manuscripts and institute reports.
2. Ship a Dockerized Python + R image (same as cohort 1).
3. Treat Nextflow as the execution plane.
4. Synthesize a **synthetic** abstract set into a grant-outline skeleton (BioE3-style headings) on disk.
5. Run a self-correcting outline loop that stops for a human gate before any portal paste.
6. Deliver one autonomous local pipeline on the synthetic corpus, documented as an architecture one-pager.

## Delivery in ClassroomIO

Labs 1–3 are the cohort 1 folders. Lab 4 is the grant-synthesis fixture in this directory.

## Module map

| Week | Module | Lab |
|---|---|---|
| 1 | Local LLM baseline for unpublished text | [`../01-bioinformatics-leaders/labs/01-ollama-baseline`](../01-bioinformatics-leaders/labs/01-ollama-baseline) |
| 2 | Dockerized R + Python environments | [`../01-bioinformatics-leaders/labs/02-container-r-python`](../01-bioinformatics-leaders/labs/02-container-r-python) |
| 3 | Nextflow DSL2 as the execution plane | [`../01-bioinformatics-leaders/labs/03-nextflow-execution-plane`](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane) |
| 4 | Agent loops over notes, not chat | (uses labs 1–3; week-4 tool map) |
| 5 | Grant outline from synthetic abstracts | [`labs/04-grant-synth-local-agent`](labs/04-grant-synth-local-agent) |
| 6 | Self-correcting outline with human gates | lab 4 `data/broken-abstracts/` |
| 7–8 | Capstone: one autonomous local pipeline on the synthetic set | [`capstone-one-pager.md`](capstone-one-pager.md) |

---

## Module 1 — Local LLM baseline for unpublished text

**Lesson 1.1 — Why cloud writers fail grant and manuscript drafts**  
Unpublished text, reviewer comments, and institute reports are not public. A “research copilot” that ships them off-box is a leak.

**Lesson 1.2 — Ollama as the on-box inference plane**  
Same lab as cohort 1.

**Lesson 1.3 — Boundary contract**  
What may leave: how an outline is gated. What must not: manuscript bodies, real budget lines, reviewer identities.

**Lab:** [01-ollama-baseline](../01-bioinformatics-leaders/labs/01-ollama-baseline/README.md)

---

## Module 2 — Dockerized analysis environments

**Lab:** [02-container-r-python](../01-bioinformatics-leaders/labs/02-container-r-python/README.md)

---

## Module 3 — Nextflow DSL2 as the execution plane

The workflow file is the audit trail for which abstract files were read. Chat is not a submission record.

**Lab:** [03-nextflow-execution-plane](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane/README.md)

---

## Module 4 — Agent loop over notes

File in → plan → synthesize → file out → critic. Human gate before any paste into an agency portal.

---

## Module 5 — Grant outline on-box

**Lesson 5.1 — Abstracts as a contract**  
Teaching abstracts are **invented** (`SYNTH-ABS-*`). We do not copy publisher PDFs. BioE3 is named as a *section pattern*, not as a filing service.

**Lesson 5.2 — Fill locally**  
Join claims into the outline template on disk. No cloud writer.

**Lab:** [04-grant-synth-local-agent](labs/04-grant-synth-local-agent/README.md)

---

## Module 6 — Self-correcting outline with human gates

**Lesson 6.1 — Fail, patch, re-run**  
Run `data/broken-abstracts/`. Agent proposes a section rewrite; human approves; max three iterations.

**Lesson 6.2 — What never auto-submits**  
Never auto-submit. Paste into an agency portal is a human act.

---

## Module 7–8 — Capstone

**Deliverable:** one local pipeline on the synthetic abstracts in lab 4. Use [`capstone-one-pager.md`](capstone-one-pager.md).

## Load checklist (admin)

```bash
python3 deploy/scripts/seed_cohort1.py \
  --draft courses/05-academic-scientists/classroomio-draft.json \
  --slug agentic-bio-fellowship-academic-grants
```

## Constraints (non-negotiable)

- Invented teaching abstracts only. No copyrighted paper text in this repo.
- No dual-use pathogen, enhancement, or wet-lab protocol content.
- Not a medical device. The Fellowship does not file grants.
