# Agentic Bio Classroom — local deploy

Self-hosted [ClassroomIO](https://github.com/classroomio/classroomio) for The Agentic Bio Fellowship. This directory is the runnable stack. It uses **official Docker Hub images**, not the generic `ghcr.io/classroomio/*` compose circulating online.

## Prerequisites

- Docker Desktop (Mac) or Docker Engine + Compose v2
- 4 GB RAM minimum (8 GB recommended — the jobs worker spikes during video/AI work)
- 2 vCPUs
- Ports free: `3081`, `3082`, `5432`, `6379`, `8025`, `9000`, `9001`

Images `classroomio/api:1.0.0`, `dashboard`, and `jobs` publish **amd64 and arm64**, so Apple Silicon works without QEMU.

Do **not** build ClassroomIO from source here. A dashboard build needs ~8 GB RAM and the full upstream monorepo.

## Start

```bash
cd deploy
cp .env.example .env
chmod +x scripts/gen-secrets.sh
./scripts/gen-secrets.sh
docker compose up -d
docker compose ps
```

`gen-secrets.sh` writes `BETTER_AUTH_SECRET` and `PRIVATE_SERVER_KEY` if they are empty. Compose refuses to start if either is blank.

## URLs (local)

| Service | URL |
|---|---|
| Dashboard (learners / admins) | http://localhost:3082 |
| API (debug only — the dashboard proxies this) | http://localhost:3081 |
| Mailpit (captured email) | http://localhost:8025 |
| MinIO console | http://localhost:9001 (`minioadmin` / `minioadmin`) |
| MinIO S3 API | http://localhost:9000 |

Verify:

```bash
curl -sS http://localhost:3081/    # API JSON
curl -I  http://localhost:3082/    # dashboard 200
```

## First-admin checklist

1. Open http://localhost:3082 and create the first organization account (email/password — Google login is optional and off until you add a real `GOOGLE_CLIENT_ID`; see [`../docs/SELF_HOST.md`](../docs/SELF_HOST.md)).
2. Confirm the verification email in [Mailpit](http://localhost:8025). Local Mailpit needs dummy SMTP auth (`SMTP_USER=mailpit`) and a STARTTLS cert (`./mailpit-certs`, see compose override). Without that, signup looks successful but verification mail never delivers.
3. Create the course **The Agentic Bio Fellowship — Bioinformatics & Computational Biology** using [`../courses/01-bioinformatics-leaders/COURSE.md`](../courses/01-bioinformatics-leaders/COURSE.md).
4. Attach each lab `README.md` as a lesson resource.

Optional demo seed (ClassroomIO sample org, not Agentic Bio content):

```bash
docker exec cio-api pnpm --filter @cio/db db:setup:seed
```

## Everyday commands

```bash
docker compose ps
docker compose logs -f api dashboard jobs
docker compose restart api dashboard
docker compose down              # stop; keep volumes
docker compose down -v           # DESTROYS Postgres, Redis, MinIO data
```

Backup Postgres:

```bash
docker exec cio-postgres pg_dump -U postgres classroomio > backup-$(date +%F).sql
```

## What not to change

- **Jobs worker is required.** If `cio-jobs` is down, uploads stay on “processing” and most emails never send.
- Browsers should hit the **dashboard** origin. Do not point learners at `:3081`.
- Pin `CIO_VERSION` in `.env`. Current pin: **1.0.0**. `latest` is a rolling `main` build.

## Production (not this overlay)

Local `docker-compose.override.yml` publishes host ports and Mailpit. Do not ship that file to a public server. See [`../docs/SELF_HOST.md`](../docs/SELF_HOST.md) for Cloudflare Tunnel on **`learn.agenticbio.in`**, SMTP (`noreply@agenticbio.in`), and media URLs.
