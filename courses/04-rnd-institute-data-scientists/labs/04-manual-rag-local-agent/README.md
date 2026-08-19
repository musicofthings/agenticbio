# Lab 04 — Synthetic lab-manual RAG, local retrieve

**Module:** 5 (cohort 4)  
**Timebox:** 2–3 hours async  
**Data:** `data/manuals/` only. Invented ops notes. Not a real institute SOP dump. No wet-lab recipes.

## Objective

Given a query file, retrieve the top snippets from a **local** markdown corpus using token overlap. No embedding APIs. No network.

## Constraints

- Do not replace the fixtures with real manuals.
- Do not call OpenAI / Gemini / hosted vector databases.
- A human must approve any write-back into a live SOP tree.

## What to run

```bash
python3 retrieve.py --corpus data/manuals --query data/query.txt --out outputs/hits.md --k 3
```

Optional: run inside the cohort 1 lab 02 image with bind mounts. `outputs/` is gitignored — do not commit retrieval hits.

## Week 6 — bounded fail / patch

Canonical `data/query.txt` stays untouched. Run the **broken** query (tokens that do not appear in the corpus):

```bash
python3 retrieve.py --corpus data/manuals --query data/broken-query.txt --out outputs/hits-broken.md --k 3
```

Expect no useful hits. Propose a query rewrite, get a human yes, write `outputs/query-fixed.txt` and re-run. Do not merge a generated paragraph into a live SOP. Max three iterations.

## Acceptance criteria

- [ ] `outputs/hits.md` lists source filenames and scored snippets
- [ ] Hits come from the local corpus (or an explicit “no hit”) — not from the internet
- [ ] README states the manuals are synthetic teaching data

## ClassroomIO

Attach this folder to Module 5. Assignment: `outputs/hits.md` plus one paragraph on why uploading SOPs to a vendor RAG is out of scope.
