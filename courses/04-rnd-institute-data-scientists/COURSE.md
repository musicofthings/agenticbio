# The Agentic Bio Fellowship — Data Scientists in R&D Institutes

ClassroomIO-ready outline for **cohort 4**. Same technical core as cohort 1. Skin: **offline RAG** over lab manuals and historical research stores that must not leave the institute network.

**LMS title:** The Agentic Bio Fellowship: Offline RAG over Institute Lab Manuals  
**Duration:** 6–8 weeks (live sessions + async labs + recordings)  
**Tracks:** Individual Innovator ₹1.5L · Enterprise Team ₹5L (3–5 seats + 60-min architecture review)

Do not launch this cohort until earlier tracks are filling. Shared labs live in [`../01-bioinformatics-leaders/labs/`](../01-bioinformatics-leaders/labs/).

## Positioning

Privacy-first **local** retrieval over manuals you already have on disk. Agents plan; **Nextflow (DSL2) executes**. No public embedding APIs, no “upload the SOP to a vendor.” Historical run folders and instrument manuals stay inside the institute.

## Audience

**For:** data scientists and informatics leads at CSIR/DBT/ICMR labs, university cores, and public R&D institutes who already keep SOPs in Git or shared drives and need retrieval that never phones home.

**Not for:** teams whose only goal is ChatGPT over a public PDF dump, or prompt-engineering beginners.

## Learning outcomes

By the capstone, a fellow can:

1. Run a local LLM with an explicit boundary for institute manuals (process questions may leave; manual text must not).
2. Ship a Dockerized Python + R image (same as cohort 1).
3. Treat Nextflow as the execution plane.
4. Retrieve from a **synthetic** local manual store with keyword overlap (no network embeddings).
5. Run a self-correcting retrieval loop that stops for a human gate on a wrong cite.
6. Deliver one autonomous local pipeline on the synthetic store, documented as an architecture one-pager.

## Delivery in ClassroomIO

Labs 1–3 are the cohort 1 folders. Lab 4 is the local-manual RAG fixture in this directory.

## Module map

| Week | Module | Lab |
|---|---|---|
| 1 | Local LLM baseline for institute stores | [`../01-bioinformatics-leaders/labs/01-ollama-baseline`](../01-bioinformatics-leaders/labs/01-ollama-baseline) |
| 2 | Dockerized R + Python environments | [`../01-bioinformatics-leaders/labs/02-container-r-python`](../01-bioinformatics-leaders/labs/02-container-r-python) |
| 3 | Nextflow DSL2 as the execution plane | [`../01-bioinformatics-leaders/labs/03-nextflow-execution-plane`](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane) |
| 4 | Agent loops over manuals, not chat | (uses labs 1–3; week-4 tool map) |
| 5 | Local RAG over synthetic manuals | [`labs/04-manual-rag-local-agent`](labs/04-manual-rag-local-agent) |
| 6 | Self-correcting retrieval with human gates | lab 4 `data/broken-query.txt` |
| 7–8 | Capstone: one autonomous local pipeline on the synthetic store | [`capstone-one-pager.md`](capstone-one-pager.md) |

---

## Module 1 — Local LLM baseline for institute stores

**Lesson 1.1 — Why cloud RAG fails institute manuals**  
Vendor “knowledge bases” that require uploading SOPs. Historical research stores often include unpublished methods *filenames* and internal path conventions even when the science is not secret.

**Lesson 1.2 — Ollama as the on-box inference plane**  
Same lab as cohort 1.

**Lesson 1.3 — Boundary contract**  
What may leave: how retrieval is gated. What must not: manual bodies, internal hostnames, unpublished figure files.

**Lab:** [01-ollama-baseline](../01-bioinformatics-leaders/labs/01-ollama-baseline/README.md)

---

## Module 2 — Dockerized analysis environments

**Lab:** [02-container-r-python](../01-bioinformatics-leaders/labs/02-container-r-python/README.md)

---

## Module 3 — Nextflow DSL2 as the execution plane

Retrieval jobs still need an audit trail. The workflow file, not the chat, is the record of which corpus was searched.

**Lab:** [03-nextflow-execution-plane](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane/README.md)

---

## Module 4 — Agent loop over manuals

File in → plan → retrieve/process → file out → critic. Cite the source path. Human gate before any write-back into the live SOP tree.

---

## Module 5 — Local RAG on-box

**Lesson 5.1 — A corpus is a contract**  
Teaching manuals are **synthetic** ops notes (freezer logs, run-folder naming). Not a real institute SOP dump. Not wet-lab recipes.

**Lesson 5.2 — Retrieve locally**  
Keyword overlap on disk. No OpenAI embeddings, no hosted vector DB.

**Lab:** [04-manual-rag-local-agent](labs/04-manual-rag-local-agent/README.md)

---

## Module 6 — Self-correcting retrieval with human gates

**Lesson 6.1 — Fail, patch, re-run**  
Run `data/broken-query.txt`. Agent proposes a query rewrite; human approves; max three iterations.

**Lesson 6.2 — What never auto-merges into a live SOP**  
Never auto-merge a generated paragraph into the live manual.

---

## Module 7–8 — Capstone

**Deliverable:** one local pipeline on the synthetic corpus in lab 4. Use [`capstone-one-pager.md`](capstone-one-pager.md).

## Load checklist (admin)

```bash
python3 deploy/scripts/seed_cohort1.py \
  --draft courses/04-rnd-institute-data-scientists/classroomio-draft.json \
  --slug agentic-bio-fellowship-rnd-rag
```

## Constraints (non-negotiable)

- Synthetic teaching manuals only. No real institute SOP dumps in this repo.
- No dual-use pathogen, enhancement, or wet-lab protocol content.
- Not a medical device.
