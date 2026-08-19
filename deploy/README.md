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
3. Import cohort 1 (creates the course, seven modules, lessons, and assignments):

   ```bash
   python3 scripts/seed_cohort1.py
   ```

   Draft JSON: [`../courses/01-bioinformatics-leaders/classroomio-draft.json`](../courses/01-bioinformatics-leaders/classroomio-draft.json). Re-run after editing the draft; the script merges into the existing course. Lab folders stay in git — lesson bodies link to GitHub.
4. Invite a test fellow and confirm Mailpit:

   ```bash
   python3 scripts/invite_fellow.py
   python3 scripts/invite_fellow.py --slug agentic-bio-fellowship-biopharma-ds
   ```

   Default address `fellow@agenticbio.local` is captured at http://localhost:8025. Use `--skip-mailpit` if Mailpit is not running.

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

## Production (Cloudflare Tunnel)

Local `docker-compose.override.yml` publishes host ports and Mailpit. Do **not** copy that overlay to a public server.

Production files in this directory:

- [`docker-compose.prod.yml`](docker-compose.prod.yml) — `cloudflared` only; no host ports
- [`.env.production.example`](.env.production.example) — `learn.agenticbio.in` URLs and SMTP placeholders

```bash
cp .env.production.example .env.production
./scripts/gen-secrets.sh .env.production
# fill SMTP_*, CLOUDFLARE_TUNNEL_TOKEN, and change default passwords
./scripts/prod-up.sh
```

`prod-up.sh` uses an explicit `-f` list so `docker-compose.override.yml` is not merged. Do not copy that override to a public server. Point the zone at Cloudflare, create a token tunnel, public hostname `learn.agenticbio.in` → `http://dashboard:3082`. Optional path `/media*` → `http://minio:9000`. Full notes: [`../docs/SELF_HOST.md`](../docs/SELF_HOST.md).
