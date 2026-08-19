# The Agentic Bio Fellowship — Clinical & Healthcare

ClassroomIO-ready outline for **cohort 3**. Same technical core as cohort 1 (local LLM, Docker, Nextflow as execution plane). Skin: reclaiming documentation hours for MDs, nursing, radiology, and pathology — ethics-committee **packets** and protocol **administration**, not diagnosis.

**LMS title:** The Agentic Bio Fellowship: Local Agents for Clinical Documentation Hours  
**Duration:** 6–8 weeks (live sessions + async labs + recordings)  
**Tracks:** Individual Innovator ₹1.5L · Enterprise Team ₹5L (3–5 seats + 60-min architecture review)

Do not launch this cohort until earlier tracks are filling. Shared labs live in [`../01-bioinformatics-leaders/labs/`](../01-bioinformatics-leaders/labs/).

## Positioning

Privacy-first **local** multi-agent orchestration for clinical *documentation workflow*. Agents plan; **Nextflow (DSL2) executes**. No public cloud LLM APIs for identifiable notes, imaging reports, or live ethics packets.

This track does **not** teach diagnosis, triage, or treatment. It teaches how to keep document assembly behind the hospital firewall with a human gate before anything is filed.

## Audience

**For:** clinical directors, nurse educators, radiology/pathology leads, and quality officers who already own SOPs and IEC/IRB packets and need an agent layer that never leaves the campus network.

**Not for:** prompt-engineering beginners, consumer “AI scribe” tourists, or teams whose only goal is a cloud copilot on the EHR.

## Learning outcomes

By the capstone, a fellow can:

1. Run a local LLM (Ollama) with an explicit boundary for clinical *documents* (process, never payloads).
2. Ship a Dockerized Python + R analysis image (same image as cohort 1).
3. Treat Nextflow as the execution plane; the agent never shells around it.
4. Assemble a **synthetic** IEC packet index from a checklist + admin fixture, with human review before any “submit.”
5. Run a self-correcting document loop that stops for a human gate on failure.
6. Deliver one autonomous local pipeline on the synthetic packet, documented as an architecture one-pager.

## Delivery in ClassroomIO

Live sessions: weekly 90 minutes. Labs 1–3 are the cohort 1 folders. Lab 4 is the ethics-packet fixture in this directory. Enterprise architecture calls (HIS/LIS/PACS vs this pattern) are scheduled outside the LMS after week 3.

## Module map

| Week | Module | Lab |
|---|---|---|
| 1 | Local LLM baseline for clinical documents | [`../01-bioinformatics-leaders/labs/01-ollama-baseline`](../01-bioinformatics-leaders/labs/01-ollama-baseline) |
| 2 | Dockerized R + Python environments | [`../01-bioinformatics-leaders/labs/02-container-r-python`](../01-bioinformatics-leaders/labs/02-container-r-python) |
| 3 | Nextflow DSL2 as the execution plane | [`../01-bioinformatics-leaders/labs/03-nextflow-execution-plane`](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane) |
| 4 | Agent loops over packet files, not chat | (uses labs 1–3; week-4 tool map) |
| 5 | IEC packet index on-box | [`labs/04-ethics-packet-local-agent`](labs/04-ethics-packet-local-agent) |
| 6 | Self-correcting document loops with human gates | lab 4 `data/broken-iec-checklist.md` |
| 7–8 | Capstone: one autonomous local pipeline on a synthetic packet | [`capstone-one-pager.md`](capstone-one-pager.md) |

---

## Module 1 — Local LLM baseline for clinical documents

**Lesson 1.1 — Why cloud APIs fail hospital documentation**  
Public model endpoints and identifiable notes, imaging reports, or live IEC packets. “HIPAA-eligible vendor” is not your DPA.

**Lesson 1.2 — Ollama as the on-box inference plane**  
Same lab as cohort 1: one completion against a non-clinical fixture.

**Lesson 1.3 — Boundary contract**  
What may leave (how a packet is gated). What must not (names, MRNs, report text, real consent forms). Logging.

**Lab:** [01-ollama-baseline](../01-bioinformatics-leaders/labs/01-ollama-baseline/README.md)

---

## Module 2 — Dockerized analysis environments

Same image contract as cohort 1. Clinical IT still pins the runtime rather than “it works on the ward PC.”

**Lab:** [02-container-r-python](../01-bioinformatics-leaders/labs/02-container-r-python/README.md)

---

## Module 3 — Nextflow DSL2 as the execution plane

The workflow file is the audit trail for document assembly, not a chat log.

**Lab:** [03-nextflow-execution-plane](../01-bioinformatics-leaders/labs/03-nextflow-execution-plane/README.md)

---

## Module 4 — Agent loop over packet files

File in → plan → Nextflow/process → file out → critic. Human gate before any write that would look like a filing. Map tools to `list_dir`, `read_file`, `run_nextflow`, `run_container`. Deny network.

---

## Module 5 — IEC packet index on-box

**Lesson 5.1 — A packet is a contract**  
Checklist + administrative protocol cover. Teaching data is **synthetic only** (`SYNTH-TRIAL-001`). No real patient identifiers, no interventional methods, no wet-lab recipes.

**Lesson 5.2 — Assemble locally**  
No cloud “protocol copilot.” Fixture markdown only.

**Lab:** [04-ethics-packet-local-agent](labs/04-ethics-packet-local-agent/README.md)

---

## Module 6 — Self-correcting document loops with human gates

**Lesson 6.1 — Fail, patch, re-run**  
Run `data/broken-iec-checklist.md`. Agent proposes a checklist fix; human approves; max three iterations.

**Lesson 6.2 — What never auto-files**  
Never auto-file to an IEC portal, EHR, or PACS. Do not invent CVs or signatures.

---

## Module 7–8 — Capstone

**Deliverable:** one local pipeline on the synthetic packet in lab 4. Ollama (or stub) drafts a run plan; Nextflow executes containerized extract; a human signs the architecture one-pager ([`capstone-one-pager.md`](capstone-one-pager.md)).

**Enterprise extra:** 60-minute architecture review of their HIS/LIS vs this pattern. Not a lab in git.

## Load checklist (admin)

```bash
python3 deploy/scripts/seed_cohort1.py \
  --draft courses/03-clinical-healthcare/classroomio-draft.json \
  --slug agentic-bio-fellowship-clinical
```

Do not market this track until cohort 1 is filling.

## Constraints (non-negotiable)

- Synthetic teaching documents only. No real notes, images, or live IEC packets in this repo or in ClassroomIO uploads.
- No dual-use pathogen, enhancement, or wet-lab protocol content. No diagnosis or treatment advice.
- Not a medical device. Not clinical advice.
