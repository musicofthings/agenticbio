# Session Handover
_Generated: 2026-08-19T19:30:00+05:30_
_Branch: main_
_Trigger: continue curriculum content (14-lesson spine, week-6 fixtures, capstones)_

---

## 🎯 Active Task
**What we're building/fixing:**
Fellowship teaching content: cohorts 2–5 now match cohort 1’s 14-lesson / 6-assignment spine, with audience-skinned copy, capstone one-pagers, and week-6 broken fixtures.

**Phase:** Curriculum content (uncommitted)
**Next action:** Commit when you want this on `main`. Existing local LMS courses that already have 10 lessons will **not** pick up the four new lessons via `seed_cohort1.py` (structure PUT is skipped to avoid duplicates). Fresh import or a one-off add is needed for those.

---

## ✅ Completed This Session
- [x] Pin `cloudflared` to `2026.8.2`; add `deploy/scripts/prod-up.sh` (never merges local override)
- [x] `gen-secrets.sh` accepts `.env.production`
- [x] `invite_fellow.py` looks up by `--slug` / `--title`; `--skip-mailpit` for hosts without Mailpit
- [x] Self-host go-live checklist; OAuth production recreate via `prod-up.sh`
- [x] Justification HTML + one-page PDF with webinar-date placeholder
- [x] Cohort 2–5 lab 4 scripts run on fixtures (join / packet index / retrieve / grant outline)
- [x] Cohorts 2–5: 14 lessons + 6 exercises (added 2.2, 3.2, 4.2, 6.2)
- [x] Skinned capstone one-pagers for cohorts 2–5
- [x] Week-6 broken fixtures on every lab 4 (VCF / commas / asterisk checklist / no-hit query / unmapped abstract)

---

## 🔄 In Progress (Exact Resume Point)
**Branch:** `main` (ahead with `fe8c479`; leftover files still unstaged)
**Last pushed commit:** `fe8c479` Expand LMS lessons…
**Next immediate action:** `git add` the leftover deploy/docs/lab files and commit if desired. Do not commit `deploy/.env` or `.env.production`.

---

## 📋 Remaining Work
1. Paste live-session YouTube URLs into each lesson’s Videos tab after class
2. Webinar date on the justification PDF header
3. Google OAuth client (follow `docs/GOOGLE_OAUTH.md`) when you want the button
4. Cloudflare nameservers + tunnel token + real SMTP, then `./scripts/prod-up.sh`
5. Market one live cohort at a time (start with 1)
6. Checkout (Razorpay etc.)

---

## 🏗 Architecture Decisions Made
| Decision | Rationale | Date |
|----------|-----------|------|
| Explicit `-f` list / `prod-up.sh` | Auto-merged `override.yml` would publish Postgres and Mailpit on a public host | 2026-08-19 |
| Pin `cloudflare/cloudflared:2026.8.2` | Same reason as pinning ClassroomIO 1.0.0 — no `:latest` on a live LMS | 2026-08-19 |
| Invite by course slug | Five courses in one org; cohort 1 title must not be hardcoded | 2026-08-19 |
| Audience lab 4 only; labs 1–3 stay in cohort 1 | Shared core; different skin and fixtures per track | 2026-08-17 |

---

## 🔧 Commands to Resume
```bash
cd ~/projects/agenticbio/deploy && docker compose up -d
python3 deploy/scripts/invite_fellow.py
# Login: admin@agenticbio.local / LocalTest!2026abc  (do not click Google)
```

Production (when token and SMTP exist):

```bash
cd deploy
cp .env.production.example .env.production
./scripts/gen-secrets.sh .env.production
./scripts/prod-up.sh
```

---

## 📁 Files Modified This Session
Leftover unstaged set (do **not** commit `.env` / `.env.production` / `mailpit-certs/`):

| File | Status |
|------|--------|
| deploy/docker-compose.prod.yml | added/updated |
| deploy/.env.production.example | added/updated |
| deploy/scripts/prod-up.sh | added |
| deploy/scripts/invite_fellow.py | added/updated |
| deploy/scripts/gen-secrets.sh | modified |
| docs/GOOGLE_OAUTH.md, SELF_HOST.md, JUSTIFICATION.md, … | modified |
| docs/justification-one-pager.html + .pdf | added/updated |
| courses/02–05 COURSE.md + labs/04-* | added |

---

## 🌿 Git Context
Lots of uncommitted deploy/docs/labs. Do **not** commit `deploy/.env`, `.env.production`, or `mailpit-certs/`. Do **not** `docker compose down -v`. Do **not** re-run `gen-secrets.sh` on the local `.env` unless secrets are empty.
