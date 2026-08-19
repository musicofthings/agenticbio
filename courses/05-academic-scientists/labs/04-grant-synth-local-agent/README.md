# Lab 04 — Synthetic abstracts → grant outline, local synth

**Module:** 5 (cohort 5)  
**Timebox:** 2–3 hours async  
**Data:** `data/abstracts/` invented teaching abstracts (`SYNTH-ABS-*`). Not publisher PDFs. Not a real BioE3 filing.

## Objective

Read local teaching abstracts plus a BioE3-style outline skeleton, emit a filled outline whose claims are sourced from those files. No cloud writer. No network.

## Constraints

- Do not paste copyrighted paper text into `data/abstracts/`.
- Do not call a public LLM API for this lab (use the files + script; Ollama is optional later).
- A human must approve any paste into an agency portal.

## What to run

```bash
python3 synthesize.py --abstracts data/abstracts --template data/bioe3-outline.md --out outputs/grant-outline.md
```

Optional: run inside the cohort 1 lab 02 image with bind mounts. `outputs/` is gitignored — do not commit grant outlines.

## Week 6 — bounded fail / patch

Canonical `data/abstracts/` stays untouched. Run the **broken** one-file corpus (no `section:` field):

```bash
python3 synthesize.py --abstracts data/broken-abstracts --template data/bioe3-outline.md --out outputs/grant-outline-broken.md
```

Most template headings will be empty. Propose adding a `section:` line, get a human yes, write a patched copy under `outputs/`. Do not auto-submit. Max three iterations.

## Acceptance criteria

- [ ] `outputs/grant-outline.md` has every template heading
- [ ] Each filled bullet cites a `SYNTH-ABS-*` id from the local files
- [ ] README states abstracts are invented teaching material

## ClassroomIO

Attach this folder to Module 5. Assignment: `outputs/grant-outline.md` plus one paragraph on why uploading an unpublished manuscript to a cloud writer is out of scope.
