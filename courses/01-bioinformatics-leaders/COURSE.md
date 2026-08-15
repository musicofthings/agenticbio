# The Agentic Bio Fellowship — Bioinformatics & Computational Biology Leaders

ClassroomIO-ready outline for **cohort 1**. Copy modules and lessons into the dashboard course builder. Attach each lab `README.md` as a lesson resource.

**LMS title:** The Agentic Bio Fellowship: Local Multi-Agent Orchestration for Bioinformatics  
**Duration:** 6–8 weeks (live sessions + async labs + recordings)  
**Tracks:** Individual Innovator ₹1.5L · Enterprise Team ₹5L (3–5 seats + 60-min architecture review)

## Positioning

Privacy-first **local** multi-agent orchestration for clinical and genomic workflows. Agents plan; **Nextflow (DSL2) executes**. No public cloud LLM APIs for VCF, BAM-derived tables, or protocol text.

## Audience

**For:** bioinformatics leads, computational biologists, and infrastructure owners who already write pipelines (Nextflow, Snakemake, R, Python) and need an agent layer that stays behind the firewall.

**Not for:** prompt-engineering beginners, no-code “ChatGPT for science” tourists, or teams whose only goal is a cloud copilot on PHI.

## Learning outcomes

By the capstone, a fellow can:

1. Run a local LLM (Ollama) with an explicit data-governance boundary.
2. Ship a Dockerized Python + R/Bioconductor analysis image.
3. Treat Nextflow as the execution plane and an agent as a planner that never shells around the workflow engine.
4. Parse and reshape a **synthetic** VCF v4.2 locally, with human review before any write.
5. Run a self-correcting EDA loop (Python or R) that stops for a human gate on failure.
6. Deliver one autonomous local pipeline on a synthetic cohort, documented as an architecture one-pager.

## Delivery in ClassroomIO

Live sessions: weekly 90 minutes. Recordings uploaded to the course. Labs are Git folders in this repo. Enterprise architecture calls are scheduled outside the LMS after week 3.

## Module map

| Week | Module | Lab |
|---|---|---|
| 1 | Local LLM baseline and data-governance constraints | [`labs/01-ollama-baseline`](labs/01-ollama-baseline) |
| 2 | Dockerized R/Bioconductor + Python environments | [`labs/02-container-r-python`](labs/02-container-r-python) |
| 3 | Nextflow DSL2 as the execution plane | [`labs/03-nextflow-execution-plane`](labs/03-nextflow-execution-plane) |
| 4 | Agent loops over files (OpenClaw or equivalent) | (uses labs 1–3; no extra stub) |
| 5 | VCF v4.2 parse / reformat / annotation, on-box | [`labs/04-vcf-local-agent`](labs/04-vcf-local-agent) |
| 6 | Self-correcting EDA agents with human review gates | extend lab 2 + 4 |
| 7–8 | Capstone: one autonomous local pipeline on a synthetic cohort | architecture one-pager |

---

## Module 1 — Local LLM baseline and data-governance

**Lesson 1.1 — Why cloud APIs fail clinical genomics**  
Public model endpoints and VCF/protocol text. Institutional governance vs “the model is HIPAA-eligible.” Local-only rule for this Fellowship.

**Lesson 1.2 — Ollama as the on-box inference plane**  
Install, pull a small instruct model, one completion against a **non-clinical** fixture file.

**Lesson 1.3 — Boundary contract**  
What may leave the machine (prompts about *process*, never payloads). Logging. No telemetry to public APIs.

**Lab:** [01-ollama-baseline](labs/01-ollama-baseline/README.md)

---

## Module 2 — Dockerized analysis environments

**Lesson 2.1 — One image, two languages**  
Python + R in one reproducible image. Pin versions. No “it works on my HPC login node.”

**Lesson 2.2 — Bioconductor without host pollution**  
What belongs in the image vs bind-mounted data.

**Lab:** [02-container-r-python](labs/02-container-r-python/README.md)

---

## Module 3 — Nextflow DSL2 as the execution plane

**Lesson 3.1 — Agents plan; Nextflow runs**  
Never let the agent invoke ad-hoc `bash` as the source of truth for a pipeline. The workflow file is the audit trail.

**Lesson 3.2 — Channels, processes, containers**  
Minimal DSL2 pipeline that calls the Module 2 image.

**Lab:** [03-nextflow-execution-plane](labs/03-nextflow-execution-plane/README.md)

---

## Module 4 — Agent loop over files, not chat

**Lesson 4.1 — Tool-using agents vs chat UIs**  
File in → plan → Nextflow/process → file out → critic. Human gate on writes.

**Lesson 4.2 — OpenClaw (or equivalent) on local tools**  
Map tools to: `list_dir`, `read_file`, `run_nextflow`, `run_container`. Deny network except optional package mirrors you already trust.

Paste this lesson body into ClassroomIO; the implementation is the fellow’s own agent runtime using labs 1–3.

---

## Module 5 — VCF v4.2 on-box

**Lesson 5.1 — VCFv4.2 as a contract**  
Header, INFO, FORMAT. Teaching data is **synthetic only**.

**Lesson 5.2 — Parse, reshape, annotate locally**  
No external annotation APIs in the lab. Fixture TSV only.

**Lab:** [04-vcf-local-agent](labs/04-vcf-local-agent/README.md)

---

## Module 6 — Self-correcting EDA with human gates

**Lesson 6.1 — Fail, patch, re-run**  
Agent proposes a pandas or R fix; human approves; container re-runs; max N iterations.

**Lesson 6.2 — What never auto-merges**  
Anything that would touch a LIMS, a clinical report, or a production Nextflow `-resume` on real samples.

---

## Module 7–8 — Capstone

**Deliverable:** one local pipeline on the synthetic cohort in lab 4:

- Ollama (or stub) drafts a run plan
- Nextflow executes containerized parse + summary
- Human signs the architecture one-pager (one page: data flow, trust boundary, failure modes)

**Enterprise extra:** 60-minute architecture review (their HPC/LIMS/Batch vs this pattern). Not a lab in git.

## Other deliverables

- Session recordings in ClassroomIO
- This `labs/` tree (fellows clone or download as a zip from the course)
- Architecture one-pager template (capstone)

## Load checklist (admin)

1. Start ClassroomIO ([`../../deploy/README.md`](../../deploy/README.md)).
2. Create organization **Agentic Bio Labs**.
3. Create course with the LMS title above; set it to paid/invite as you prefer (checkout is out of band for this MVP).
4. Create seven modules; paste lesson titles and bodies from this file.
5. Upload each lab folder as a downloadable resource (or link the git tree once the repo is remote).
6. Add a “Capstone” assignment: upload the one-pager PDF.
7. Invite the first fellow; confirm the invite appears in Mailpit (`http://localhost:8025`).

## Constraints (non-negotiable)

- Synthetic or public teaching data only. No real patient VCFs in this repo or in ClassroomIO uploads for labs.
- No dual-use pathogen, enhancement, or wet-lab protocol content.
- Not a medical device. Not clinical advice.
