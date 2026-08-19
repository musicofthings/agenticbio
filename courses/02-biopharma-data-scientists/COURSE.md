# The Agentic Bio Fellowship — Data Scientist Teams at Biopharma

ClassroomIO-ready outline for **cohort 2**. Same technical core as cohort 1 (local LLM, Docker, Nextflow as execution plane). Different skin: discovery and multiomic analysis **behind the firewall**, not clinical-genomics pipeline language.

**LMS title:** The Agentic Bio Fellowship: Offline Multiomic Analysis for Biopharma Data Science  
**Duration:** 6–8 weeks (live sessions + async labs + recordings)  
**Tracks:** Individual Innovator ₹1.5L · Enterprise Team ₹5L (3–5 seats + 60-min architecture review)

Do not launch this cohort until cohort 1 is filling. Shared labs live in [`../01-bioinformatics-leaders/labs/`](../01-bioinformatics-leaders/labs/).

## Positioning

Privacy-first **local** multi-agent orchestration for discovery and multiomic tables. Agents plan; **Nextflow (DSL2) executes**. No public cloud LLM APIs for expression matrices, assay exports, or unpublished figures.

## Audience

**For:** data-science leads on discovery, translational, or multiomic teams inside biopharma who already work in Python/R and need an agent layer that never leaves the company network.

**Not for:** prompt-engineering beginners, or teams whose only goal is a cloud notebook copilot on licensed assay data.

## Learning outcomes

By the capstone, a fellow can:

1. Run a local LLM (Ollama) with an explicit data-governance boundary for discovery artifacts.
2. Ship a Dockerized Python + R analysis image (same image as cohort 1).
3. Treat Nextflow as the execution plane and an agent as a planner that never shells around the workflow engine.
4. Join a **synthetic** multiomic matrix to a local annotation table, with human review before any write.
5. Run a self-correcting EDA loop that stops for a human gate on failure.
6. Deliver one autonomous local pipeline on a synthetic discovery cohort, documented as an architecture one-pager.

## Delivery in ClassroomIO

Live sessions: weekly 90 minutes. Recordings uploaded to the course. Labs 1–3 are the cohort 1 folders (clone this repo). Lab 4 is the multiomic fixture in this directory. Enterprise architecture calls are scheduled outside the LMS after week 3.

## Module map

| Week | Module | Lab |
|---|---|---|
| 1 | Local LLM baseline for discovery notes | [`../01-bioinformatics-leaders/labs/01-ollama-baseline`](../01-bioinformatics-leaders/labs/01-ollama-baseline) |
| 2 | Dockerized R + Python environments | [`../01-bioinformatics-leaders/labs/02-container-r-python`](../01-bioinformatics-leaders/labs/02-container-r-python) |
| 3 | Nextflow DSL2 as the execution plane | [`../01-bioinformatics-leaders/labs/03-nextflow-execution-plane`](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane) |
| 4 | Agent loops over assay files, not chat | (uses labs 1–3; week-4 tool map) |
| 5 | Multiomic matrix join on-box | [`labs/04-multiomic-local-agent`](labs/04-multiomic-local-agent) |
| 6 | Self-correcting EDA agents with human review gates | lab 4 `data/broken-expression.tsv` |
| 7–8 | Capstone: one autonomous local pipeline on a synthetic discovery cohort | [`capstone-one-pager.md`](capstone-one-pager.md) |

---

## Module 1 — Local LLM baseline for discovery

**Lesson 1.1 — Why cloud APIs fail licensed assay data**  
Public model endpoints and unpublished expression tables, figure drafts, or partner-data use terms. “The vendor is SOC2” is not permission to leave the firewall.

**Lesson 1.2 — Ollama as the on-box inference plane**  
Same lab as cohort 1: one completion against a non-clinical fixture.

**Lesson 1.3 — Boundary contract**  
What may leave (process questions). What must not (matrices, sample IDs, unpublished figures). Logging.

**Lab:** [01-ollama-baseline](../01-bioinformatics-leaders/labs/01-ollama-baseline/README.md)

---

## Module 2 — Dockerized analysis environments

Same image contract as cohort 1. Discovery teams still pin Python + R rather than “it works on my laptop.”

**Lesson 2.1 — One image, two languages**  
**Lesson 2.2 — What belongs in the image vs bind-mounted assays**

**Lab:** [02-container-r-python](../01-bioinformatics-leaders/labs/02-container-r-python/README.md)

---

## Module 3 — Nextflow DSL2 as the execution plane

Agents plan; Nextflow runs. The workflow file is the audit trail for a discovery pipeline, not a chat log.

**Lesson 3.1 — Agents plan; Nextflow runs**  
**Lesson 3.2 — Channels, processes, containers**

**Lab:** [03-nextflow-execution-plane](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane/README.md)

---

## Module 4 — Agent loop over assay files

**Lesson 4.1 — Tool-using agents vs chat UIs**  
File in → plan → Nextflow/process → file out → critic. Human gate on writes.

**Lesson 4.2 — OpenClaw (or equivalent) on local tools**  
Map tools to `list_dir`, `read_file`, `run_nextflow`, `run_container`. Deny network except trusted package mirrors.

---

## Module 5 — Multiomic matrix on-box

**Lesson 5.1 — A matrix is a contract**  
Gene × sample table. Teaching data is **synthetic only** (`SYNTH-DS-001`). Not from a trial, not from a public GEO series used as a stand-in for a partner dataset.

**Lesson 5.2 — Join locally**  
No Enrichr, no STRING, no “just this once” REST. Fixture TSV only.

**Lab:** [04-multiomic-local-agent](labs/04-multiomic-local-agent/README.md)

---

## Module 6 — Self-correcting EDA with human gates

**Lesson 6.1 — Fail, patch, re-run**  
Run `data/broken-expression.tsv`. Agent proposes a pandas or R fix; human approves; container re-runs; max three iterations.

**Lesson 6.2 — What never auto-merges**  
Never auto-merge into a LIMS, a board deck with real sample IDs, or a production Nextflow `-resume` on licensed assays.

---

## Module 7–8 — Capstone

**Deliverable:** one local pipeline on the synthetic matrix in lab 4:

- Ollama (or stub) drafts a run plan
- Nextflow executes containerized join + summary
- Human signs the architecture one-pager ([`capstone-one-pager.md`](capstone-one-pager.md))

**Enterprise extra:** 60-minute architecture review (their data lake, GxP zone, or HPC vs this pattern). Not a lab in git.

## Load checklist (admin)

1. Start ClassroomIO ([`../../deploy/README.md`](../../deploy/README.md)).
2. Import this cohort:

   ```bash
   python3 deploy/scripts/seed_cohort1.py \
     --draft courses/02-biopharma-data-scientists/classroomio-draft.json \
     --slug agentic-bio-fellowship-biopharma-ds
   ```

3. Confirm the course sits **next to** cohort 1 in Agentic Bio Labs — do not replace it.
4. Invite fellows only after cohort 1 has a fill date.

## Constraints (non-negotiable)

- Synthetic or public teaching data only. No real assay exports in this repo or in ClassroomIO uploads for labs.
- No dual-use pathogen, enhancement, or wet-lab protocol content.
- Not a medical device. Not clinical advice.
