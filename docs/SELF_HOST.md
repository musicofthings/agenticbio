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

The ClassroomIO login page always shows **Login with Google**. That is not configured until you put a real OAuth Web client in `.env`. Placeholder values (`docker-local-client-id`) produce Google **Error 401: invalid_client**.

Until then, use **email and password** (`admin@agenticbio.local` locally).

To enable Google:

1. [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials) → Create credentials → OAuth client ID → **Web application**.
2. Authorized JavaScript origins:
   - `http://localhost:3082`
   - `https://learn.agenticbio.in` (later)
3. Authorized redirect URIs (Better Auth, dashboard origin):
   - `http://localhost:3082/api/auth/callback/google`
   - `https://learn.agenticbio.in/api/auth/callback/google` (later)
4. Paste into `deploy/.env`:

```env
GOOGLE_CLIENT_ID=....apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=....
```

5. Recreate the API: `cd deploy && docker compose up -d --force-recreate api`

## Production later (not enabled in this repo)

Local `deploy/docker-compose.override.yml` publishes host ports and Mailpit. Do **not** copy that overlay to a public server.

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

### Cloudflare Tunnel overlay (sketch)

Add a service; omit host `ports:` on `api` and `dashboard`:

```yaml
  cloudflared:
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    command: tunnel --no-autoupdate run
    environment:
      TUNNEL_TOKEN: ${CLOUDFLARE_TUNNEL_TOKEN}
```

Zero Trust public hostname:

- Hostname: `learn.agenticbio.in`
- Service type: HTTP
- URL: `dashboard:3082`

Optional second route for media if you keep MinIO: path `/media` on the same hostname → `http://minio:9000` (or move objects to R2 and set `OBJECT_STORAGE_MEDIA_PUBLIC_BASE_URL` to the R2 public URL).

Do not put Cloudflare Access OTP in front of `learn.agenticbio.in`. That would block new paying students. If you want an extra perimeter, apply Access only to staff surfaces (for example `admin.agenticbio.in`). Learners authenticate with ClassroomIO BetterAuth.

### Cloudflare R2 instead of MinIO

Run without MinIO, set `OBJECT_STORAGE_*` to the R2 endpoint, keys, and public media base URL. Buckets still need to exist (`videos`, `documents`, `media`).

### HTTPS

ClassroomIO production expects `DASHBOARD_ORIGIN` to be `https://`. Tunnel or Caddy/Traefik terminates TLS. This local stack is HTTP on localhost by design.
