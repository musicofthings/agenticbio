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
| [`docs/SELF_HOST.md`](docs/SELF_HOST.md) | Local ops + production Cloudflare Tunnel notes (not enabled yet) |
| [`docs/FELLOWSHIP.md`](docs/FELLOWSHIP.md) | Offer, INR pricing, five cohorts, backend funnel |
| [`docs/LAUNCH.md`](docs/LAUNCH.md) | Sequence: posts → webinar → Fellowship → implementation |
| [`docs/MARKETING.md`](docs/MARKETING.md) | First three LinkedIn/X posts |
| [`docs/JUSTIFICATION.md`](docs/JUSTIFICATION.md) | Manager justification one-pager for finance |
| [`courses/01-bioinformatics-leaders/`](courses/01-bioinformatics-leaders/) | Cohort 1 outline + lab stubs to paste into ClassroomIO |

## Architecture (short)

Learners use the **dashboard** origin only. The dashboard proxies the API on the Docker network. Do not send browsers to the API port in production.

Production domain (bought, Cloudflare stage not enabled): **`agenticbio.in`**. LMS hostname will be `https://learn.agenticbio.in`. Apex/www stay free for a marketing site later.

Pinned image tag: **ClassroomIO 1.0.0** (`classroomio/api`, `dashboard`, `jobs`). Not `ghcr.io/classroomio/*`.

## Cohort 1

**Bioinformatics & Computational Biology Leaders** — Nextflow DSL2 as the execution plane, Ollama on-box, Dockerized Python/R, synthetic VCF only.

Load into ClassroomIO with the checklist in [`courses/01-bioinformatics-leaders/COURSE.md`](courses/01-bioinformatics-leaders/COURSE.md).

Cohorts 2–5 are named in [`docs/FELLOWSHIP.md`](docs/FELLOWSHIP.md) and are **not** built yet.

## Out of scope (this MVP)

- Cloudflare Tunnel, DNS, Access OTP
- Payment checkout
- Building ClassroomIO from source
- Custom LMS frontend beyond env branding vars

Not a medical device. Labs use synthetic teaching data only.
