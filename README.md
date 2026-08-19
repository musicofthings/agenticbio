# Agentic Bio Classroom

Self-hosted LMS and curriculum for **The Agentic Bio Fellowship** — a 6–8 week program on privacy-first, local multi-agent orchestration for life sciences.

The classroom software is [ClassroomIO](https://github.com/classroomio/classroomio), pulled as official Docker Hub images. This repo does **not** vendor the ClassroomIO monorepo.

## Quick start (local)

Requires Docker Desktop and ~4 GB RAM (8 GB recommended).

```bash
cd deploy
cp .env.example .env
./scripts/gen-secrets.sh
docker compose up -d
```

Then open:

- Dashboard: http://localhost:3082
- Mailpit (signup/invite mail): http://localhost:8025
- MinIO console: http://localhost:9001

Full runbook: [`deploy/README.md`](deploy/README.md).

## What’s in this repo

| Path | Purpose |
|---|---|
| [`deploy/`](deploy/) | Compose stack: Postgres 16, Redis, MinIO, API `:3081`, dashboard `:3082`, jobs worker, Mailpit |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Request path, auth, why jobs/SMTP matter |
| [`docs/SELF_HOST.md`](docs/SELF_HOST.md) | Local ops + production Cloudflare Tunnel (overlay ready, token not in repo) |
| [`docs/GOOGLE_OAUTH.md`](docs/GOOGLE_OAUTH.md) | Google login setup (deferred) |
| [`docs/FELLOWSHIP.md`](docs/FELLOWSHIP.md) | Offer, INR pricing, five cohorts, backend funnel |
| [`docs/LAUNCH.md`](docs/LAUNCH.md) | Sequence: posts → webinar → Fellowship → implementation |
| [`docs/MARKETING.md`](docs/MARKETING.md) | First three LinkedIn/X posts |
| [`docs/JUSTIFICATION.md`](docs/JUSTIFICATION.md) | Manager justification one-pager ([PDF](docs/justification-one-pager.pdf)) |
| [`courses/01-bioinformatics-leaders/`](courses/01-bioinformatics-leaders/) | Cohort 1 outline, labs, and ClassroomIO import draft |
| [`courses/02-biopharma-data-scientists/`](courses/02-biopharma-data-scientists/) | Cohort 2 outline (shared labs 1–3 + multiomic lab 4) |
| [`courses/03-clinical-healthcare/`](courses/03-clinical-healthcare/) | Cohort 3 outline (IEC packet lab; not diagnosis) |
| [`courses/04-rnd-institute-data-scientists/`](courses/04-rnd-institute-data-scientists/) | Cohort 4 outline (offline RAG over synthetic manuals) |
| [`courses/05-academic-scientists/`](courses/05-academic-scientists/) | Cohort 5 outline (synthetic abstracts → grant skeleton) |

## Architecture (short)

Learners use the **dashboard** origin only. The dashboard proxies the API on the Docker network. Do not send browsers to the API port in production.

Production domain (bought, Cloudflare stage not enabled): **`agenticbio.in`**. LMS hostname will be `https://learn.agenticbio.in`. Apex/www stay free for a marketing site later.

Pinned image tag: **ClassroomIO 1.0.0** (`classroomio/api`, `dashboard`, `jobs`). Not `ghcr.io/classroomio/*`.

## Cohort 1

**Bioinformatics & Computational Biology Leaders** — Nextflow DSL2 as the execution plane, Ollama on-box, Dockerized Python/R, synthetic VCF only.

Load into ClassroomIO:

```bash
python3 deploy/scripts/seed_cohort1.py
```

Checklist and lesson copy: [`courses/01-bioinformatics-leaders/COURSE.md`](courses/01-bioinformatics-leaders/COURSE.md). LMS HTML: [`classroomio-draft.json`](courses/01-bioinformatics-leaders/classroomio-draft.json).

After editing lesson bodies, apply them in place (does not duplicate lessons):

```bash
python3 deploy/scripts/enrich_lesson_content.py --write --apply
```

Each lesson has a **YouTube placeholder** (slot id like `BIO-W1-L1`). Paste the real URL in the lesson **Videos** tab after class — do not iframe YouTube in the HTML. Fellows signed in as students get Previous / Next in the header; every lesson body also has Continue links. Teachers: **View as student** in the course header.

Cohort 2–5 outlines (same core labs, different audience skin): see [`docs/FELLOWSHIP.md`](docs/FELLOWSHIP.md). Do not market tracks 2–5 until cohort 1 fills.

## Out of scope (this MVP)

- Live Cloudflare Tunnel / DNS (compose overlay is in `deploy/`; token not in repo)
- Payment checkout
- Building ClassroomIO from source
- Custom LMS frontend beyond env branding vars

Not a medical device. Labs use synthetic teaching data only.
