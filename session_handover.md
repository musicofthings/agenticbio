# Session Handover
_Generated: 2026-08-15_
_Branch: (uncommitted MVP)_
_Trigger: AgenticBio Classroom MVP implementation_

---

## Active Task

**What we're building:** Agentic Bio Classroom — local ClassroomIO + Fellowship product docs + cohort 1 labs.

**Phase:** Local MVP files in repo. Stack not necessarily running until `docker compose up` in `deploy/`.

**Next action:** `cd deploy && cp .env.example .env && ./scripts/gen-secrets.sh && docker compose up -d`, then create the first org at http://localhost:3082 and paste cohort 1 from `courses/01-bioinformatics-leaders/COURSE.md`.

---

## Completed This Session

- [x] `deploy/` official ClassroomIO 1.0.0 compose (Docker Hub, not ghcr), Mailpit override, `.env.example`, `scripts/gen-secrets.sh`
- [x] Docs: ARCHITECTURE, SELF_HOST, FELLOWSHIP, LAUNCH, MARKETING, JUSTIFICATION
- [x] Cohort 1 COURSE.md + labs 01–04 + capstone one-pager template
- [x] Root README and this handover

---

## Remaining Work

1. Start the local stack and create the first ClassroomIO admin/org
2. Paste cohort 1 modules into the LMS; attach lab zips
3. Production later: add `agenticbio.in` to Cloudflare, Tunnel public hostname `learn.agenticbio.in` → `dashboard:3082`, real SMTP (`noreply@agenticbio.in`), media public URLs on that host
4. Webinar date + PDF export of `docs/JUSTIFICATION.md`
5. Checkout (Razorpay etc.) — not started
6. Cohorts 2–5 curriculum — not started
7. Backend offers (fractional / DFY / consortium) — copy only, no delivery ops yet

---

## Architecture Decisions Made

| Decision | Rationale | Date |
|----------|-----------|------|
| Official Docker Hub `classroomio/{api,dashboard,jobs}:1.0.0` | Pasted ghcr compose and `:3000` ports do not match ClassroomIO; 1.0.0 is the current immutable v1 tag (amd64+arm64) | 2026-08-15 |
| Single dashboard origin; API stays internal | CIO dashboard proxies API; no `PUBLIC_API_URL` | 2026-08-15 |
| Mailpit locally; real SMTP in prod | Access OTP is not CIO email and would block new students | 2026-08-15 |
| Cloudflare Tunnel documented, not enabled | User chose local-first (`localhost:3082`) | 2026-08-15 |
| Production domain `agenticbio.in` | Bought; LMS will be `learn.agenticbio.in` via Cloudflare Tunnel. No public `api.` hostname. Apex/www reserved for marketing later | 2026-08-15 |
| Jobs worker required | Video, AI gen, most email never drain without it | 2026-08-15 |
| Fellowship naming + ₹1.5L / ₹5L | Mid-funnel; not a $1k workshop | 2026-08-15 |
| Launch cohort 1 only (bioinformatics leaders) | Sequence, do not sync five tracks | 2026-08-15 |
| Synthetic VCF only in labs | No real patient data in git or teaching uploads | 2026-08-15 |

---

## Commands to Resume

```bash
cd /Users/theranosis_dx/projects/agenticbio/deploy
cp -n .env.example .env
./scripts/gen-secrets.sh
docker compose up -d
docker compose ps
docker compose logs -f api dashboard jobs
```

Dashboard: http://localhost:3082  
Mailpit: http://localhost:8025  
MinIO: http://localhost:9001 (`minioadmin` / `minioadmin`)

---

## Files Modified This Session

| Path | Status |
|------|--------|
| `README.md` | added |
| `.gitignore` | added |
| `deploy/**` | added |
| `docs/**` | added |
| `courses/01-bioinformatics-leaders/**` | added |
| `session_handover.md` | updated |

---

## Critical Rules

- Never commit `.env` or generated auth secrets
- Do not put Cloudflare Access OTP in front of learner login
- Do not use `docker compose down -v` unless you intend to wipe the LMS database
- Labs: synthetic data only; not a medical device

---

## Bioinformatics Context

- Teaching reference: GRCh38 placeholder in synthetic VCF header only
- No real cohorts, no ACMG classification in labs
