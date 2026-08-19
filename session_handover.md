# Session Handover
_Generated: 2026-08-19T09:50:00+05:30_
_Branch: main_
_Trigger: user request (lesson content, nav, YouTube placeholders)_

---

## 🎯 Active Task
**What we're building/fixing:**
Expanded all five Fellowship courses in local ClassroomIO: real lesson bodies, YouTube placeholders, and lesson-to-lesson Continue links. Native Previous/Next in the header only shows for students; teachers use the in-body links or **View as student**.

**Phase:** Curriculum content in LMS
**Next action:** Open a lesson at http://localhost:3082, confirm copy + Continue links, then paste YouTube URLs after live sessions.

---

## ✅ Completed This Session
- [x] Expanded lesson HTML for all 5 cohorts (14 + 4×10 lessons)
- [x] YouTube placeholders with slot ids (`BIO-W1-L1`, `DS-W1-L1`, …)
- [x] Prev/next Continue links (classroom UUID path + public slug path)
- [x] Set `public=true` and `is_unlocked=true` on every lesson
- [x] Applied in place via SQL (no duplicate lessons)
- [x] Seed skips structure PUT when lessons already exist

---

## 🔄 In Progress (Exact Resume Point)
**Branch:** `main`
**Last commit:** `39549ea Fix local ClassroomIO mail and stop fake Google OAuth.`
**Next immediate action:** Spot-check cohort 1 lesson 1.1 in the dashboard; add real YouTube URLs later via Videos tab.

---

## 📋 Remaining Work
1. Paste live-session YouTube URLs into each lesson’s Videos tab after class
2. Configuration later: Google OAuth, Cloudflare tunnel, SMTP, Razorpay
3. Market one live cohort at a time (start with 1)

---

## 🏗 Architecture Decisions Made
| Decision | Rationale | Date |
|----------|-----------|------|
| Apply lesson HTML via SQL, not structure PUT | CIO merge keys on lesson UUID; a second import duplicates lessons | 2026-08-19 |
| YouTube as HTML placeholder, not `videos` jsonb | Empty/fake YouTube links break the player; CSP blocks iframes in lesson HTML | 2026-08-19 |
| Keep `completionPolicy=manual` | Placeholders must not block Mark complete | 2026-08-19 |
| In-body Continue links + public=true | Admin/edit view hides CIO’s header prev/next (`isStudentExperience` only) | 2026-08-19 |

---

## 🔧 Commands to Resume
```bash
cd ~/projects/agenticbio/deploy && docker compose up -d
python3 deploy/scripts/enrich_lesson_content.py --write --apply
# Login: admin@agenticbio.local / LocalTest!2026abc  (do not click Google)
```

---

## 📁 Files Modified This Session
| File | Status |
|------|--------|
| deploy/scripts/enrich_lesson_content.py | added |
| deploy/scripts/seed_cohort1.py | modified |
| courses/0{1-5}-*/classroomio-draft.json | modified |
| courses/01-bioinformatics-leaders/COURSE.md | modified |
| README.md | modified |

---

## 🌿 Git Context
Lots of uncommitted curriculum/docs. Do **not** commit `deploy/.env`, `.env.production`, or `mailpit-certs/`. Do **not** `docker compose down -v`. Do **not** re-run `gen-secrets.sh`.
