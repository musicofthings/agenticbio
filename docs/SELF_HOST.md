# Self-host runbook

## Local (this Mac)

Full steps live in [`../deploy/README.md`](../deploy/README.md). Short version:

```bash
cd deploy
cp .env.example .env
./scripts/gen-secrets.sh
docker compose up -d
```

- Dashboard: http://localhost:3082
- Mailpit: http://localhost:8025
- MinIO console: http://localhost:9001

Schema setup runs inside `cio-api` on start. Do not set `SKIP_DB_SETUP=true` unless you are running multiple API replicas.

### Troubleshooting

| Symptom | Likely cause |
|---|---|
| Compose exits immediately citing `PRIVATE_SERVER_KEY` / `BETTER_AUTH_SECRET` | `.env` secrets empty — run `./scripts/gen-secrets.sh` |
| Signup succeeds, no email | Mailpit/jobs down — `docker compose logs jobs` and open `:8025` |
| Upload stuck on “processing” | `cio-jobs` not running |
| Dashboard 502 / “API upstream not configured” | `PRIVATE_SERVER_URL` must be `http://api:3081` |
| Postgres `57P03` recovery | Wait for healthcheck; api starts only after `SELECT 1` |
| Image pull fails for `ghcr.io/classroomio/...` | Wrong compose — this repo uses Docker Hub `classroomio/...` |
| Google **Error 401: invalid_client** | `GOOGLE_CLIENT_ID` is empty or a placeholder (`docker-local-client-id`). Use email/password, or create a real OAuth client (see below). |

Port conflicts:

```bash
lsof -nP -iTCP:3081 -sTCP:LISTEN
lsof -nP -iTCP:3082 -sTCP:LISTEN
```

### Backup

```bash
docker exec cio-postgres pg_dump -U postgres classroomio > backup-$(date +%F).sql
```

`docker compose down -v` deletes Postgres, Redis, and MinIO volumes.

### Google login (optional)

Deferred. Full steps: [`GOOGLE_OAUTH.md`](GOOGLE_OAUTH.md). Until then use email/password. Do not click **Login with Google** — it will 401 until a real client ID is in `deploy/.env`.

## Production (Cloudflare Tunnel — files ready, not enabled)

Local `deploy/docker-compose.override.yml` publishes host ports and Mailpit. Do **not** copy that overlay to a public server. Use:

- [`../deploy/docker-compose.prod.yml`](../deploy/docker-compose.prod.yml)
- [`../deploy/.env.production.example`](../deploy/.env.production.example)

```bash
cd deploy
cp .env.production.example .env.production
./scripts/gen-secrets.sh .env.production
# fill SMTP_*, CLOUDFLARE_TUNNEL_TOKEN, POSTGRES_PASSWORD, MINIO_ROOT_PASSWORD
./scripts/prod-up.sh
```

You still need: Cloudflare nameservers on **`agenticbio.in`**, a Zero Trust tunnel token, real SMTP (`noreply@agenticbio.in` + SPF/DKIM), and the public hostname below. The token is not in this repo. `prod-up.sh` never merges the local override (host ports + Mailpit).

### Go-live checklist

1. Point `agenticbio.in` nameservers at Cloudflare.
2. Create a Zero Trust **token** tunnel. Public hostname `learn.agenticbio.in` → `http://dashboard:3082`. Optional `/media*` → `http://minio:9000`.
3. Paste the token into `.env.production` as `CLOUDFLARE_TUNNEL_TOKEN`.
4. Real SMTP + SPF/DKIM for `noreply@agenticbio.in`. Mailpit is local-only.
5. Change `POSTGRES_PASSWORD` and MinIO keys from the example placeholders.
6. Google login remains optional — [`GOOGLE_OAUTH.md`](GOOGLE_OAUTH.md) — set the production origin/redirect on the same client, then put the id/secret in `.env.production`.
7. Do **not** copy `docker-compose.override.yml` to the server. Do **not** put Cloudflare Access OTP in front of learner login.

### Domain and routing

Registered domain: **`agenticbio.in`**. Point the zone at Cloudflare (nameservers) before creating the tunnel. Do not publish a separate public API hostname.

| Hostname | Role | Tunnel service |
|---|---|---|
| `learn.agenticbio.in` | LMS (learners + faculty) | `http://dashboard:3082` |
| `agenticbio.in` / `www.agenticbio.in` | Marketing site later (not this stack) | — |
| `admin.agenticbio.in` | Optional staff-only (MinIO console / ops) | only if Access-gated |

Set in production `.env`:

```env
DASHBOARD_ORIGIN=https://learn.agenticbio.in
ORIGIN=https://learn.agenticbio.in
PUBLIC_SERVER_URL=https://learn.agenticbio.in
PRIVATE_SERVER_URL=http://api:3081
OBJECT_STORAGE_PUBLIC_ENDPOINT=https://learn.agenticbio.in
OBJECT_STORAGE_MEDIA_PUBLIC_BASE_URL=https://learn.agenticbio.in/media
SMTP_SENDER=noreply@agenticbio.in
```

You still need a reverse-proxy or tunnel path that serves `/media` from MinIO (or switch to Cloudflare R2 / S3 and drop MinIO).

Do not expose `api`, Postgres, Redis, or MinIO on the host. The dashboard proxies the API on the Docker network.

### SMTP is mandatory

Replace Mailpit with a real provider (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_SENDER=noreply@agenticbio.in`). Cloudflare Access OTP does **not** send ClassroomIO verification, password-reset, or invite mail. SPFs/DKIM should be on the `agenticbio.in` zone in Cloudflare.

### Cloudflare Tunnel overlay

The service lives in [`../deploy/docker-compose.prod.yml`](../deploy/docker-compose.prod.yml) (`cloudflare/cloudflared:2026.8.2`, overridable via `CLOUDFLARED_VERSION`). Do not merge it with `docker-compose.override.yml`. Start with [`../deploy/scripts/prod-up.sh`](../deploy/scripts/prod-up.sh).

Zero Trust public hostname:

- Hostname: `learn.agenticbio.in`
- Service type: HTTP
- URL: `http://dashboard:3082`

Optional second route for media if you keep MinIO: path `/media*` on the same hostname → `http://minio:9000` (or move objects to R2 and set `OBJECT_STORAGE_MEDIA_PUBLIC_BASE_URL` to the R2 public URL).

Do not put Cloudflare Access OTP in front of `learn.agenticbio.in`. That would block new paying students. If you want an extra perimeter, apply Access only to staff surfaces (for example `admin.agenticbio.in`). Learners authenticate with ClassroomIO BetterAuth.

### Cloudflare R2 instead of MinIO

Run without MinIO, set `OBJECT_STORAGE_*` to the R2 endpoint, keys, and public media base URL. Buckets still need to exist (`videos`, `documents`, `media`).

### HTTPS

ClassroomIO production expects `DASHBOARD_ORIGIN` to be `https://`. Tunnel or Caddy/Traefik terminates TLS. This local stack is HTTP on localhost by design.
