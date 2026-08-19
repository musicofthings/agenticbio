# Google OAuth (do later)

Google login is **not enabled** yet. Use ClassroomIO email/password until this is done.

The login page always shows **Login with Google**. Clicking it without a real OAuth client produces Google **Error 401: invalid_client**. Do not use placeholder IDs such as `docker-local-client-id`.

## Status

| Environment | Google OAuth |
|---|---|
| Local (`http://localhost:3082`) | Off — `GOOGLE_CLIENT_ID` empty in `deploy/.env` |
| Production (`https://learn.agenticbio.in`) | Off — Cloudflare stage not enabled |

## Create the OAuth client

1. Open [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials).
2. If prompted, configure the OAuth consent screen (External or Internal). App name: **Agentic Bio Classroom**. Add your Google account as a test user while the app is in Testing.
3. Create credentials → **OAuth client ID** → Application type **Web application**. Name: `agenticbio-classroom-web`.
4. Authorized JavaScript origins:

   | When | Origin |
   |---|---|
   | Local now | `http://localhost:3082` |
   | Production later | `https://learn.agenticbio.in` |

5. Authorized redirect URIs (Better Auth on the **dashboard** origin; the dashboard proxies `/api/auth/*`):

   | When | Redirect URI |
   |---|---|
   | Local now | `http://localhost:3082/api/auth/callback/google` |
   | Production later | `https://learn.agenticbio.in/api/auth/callback/google` |

   Do **not** register `http://localhost:3081/...` or `https://api.agenticbio.in/...`. Learners never hit the API host.

6. Copy the client ID (`….apps.googleusercontent.com`) and client secret.

## Wire it into ClassroomIO

In `deploy/.env` (never commit this file):

```env
GOOGLE_CLIENT_ID=....apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=....
```

Recreate the API so it picks up the new values:

```bash
cd deploy
docker compose up -d --force-recreate api
```

Confirm:

```bash
docker exec cio-api sh -c 'if [ -z "$GOOGLE_CLIENT_ID" ]; then echo empty; else echo set; fi'
```

Then retry **Login with Google** at http://localhost:3082/login.

When production is live, add the `learn.agenticbio.in` origin and redirect URI on the **same** OAuth client (or a second Web client). Put the id and secret in `deploy/.env.production` (not `.env`), keep `DASHBOARD_ORIGIN=https://learn.agenticbio.in`, and recreate `api` on the server:

```bash
cd deploy
./scripts/prod-up.sh --force-recreate api
```

## If it still fails

| Error | Likely cause |
|---|---|
| **401: invalid_client** | Wrong or empty client ID, or still using a placeholder |
| **redirect_uri_mismatch** | URI not exactly `/api/auth/callback/google` on the dashboard origin (scheme, host, port, path) |
| **Access blocked: this app isn’t verified** | Consent screen in Testing — add the Google account under Test users |
| Button works, then loops to login | `DASHBOARD_ORIGIN` does not match the URL in the browser |

Email/password remains the supported login until this file’s steps are completed.
