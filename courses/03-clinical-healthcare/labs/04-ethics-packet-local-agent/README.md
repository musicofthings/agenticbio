# Lab 04 — Synthetic IEC packet index, local extract

**Module:** 5 (cohort 3)  
**Timebox:** 2–3 hours async  
**Data:** `data/` fixtures only. Invented trial id `SYNTH-TRIAL-001`. Administrative cover + checklist. No patients, no dosing, no wet-lab methods.

## Objective

Read a synthetic IEC checklist and a synthetic protocol **admin** cover, emit a packet index that lists required documents vs what is present on disk. No cloud protocol copilots. No network.

## Constraints

- Do not replace fixtures with a real IEC packet.
- Do not add interventional methods, pathogen work, or identifiable clinical narrative.
- A human must approve any rewrite of the checklist or cover before it would be treated as a filing.

## What to run

```bash
python3 extract_packet.py --checklist data/iec-checklist.md --cover data/synthetic-protocol-admin.md --out outputs/packet-index.md
```

Optional: run the same script inside the cohort 1 lab 02 image with bind mounts. `outputs/` is gitignored — do not commit packet indexes.

## Week 6 — bounded fail / patch

Canonical `data/iec-checklist.md` stays untouched. Run the **broken** copy (asterisk bullets the parser ignores):

```bash
python3 extract_packet.py --checklist data/broken-iec-checklist.md --cover data/synthetic-protocol-admin.md --out outputs/packet-index-broken.md
```

The index will list no checklist items. Propose a patch to `- [ ]` syntax, get a human yes, write under `outputs/`. Do not invent CVs. Max three iterations.

## Acceptance criteria

- [ ] `outputs/packet-index.md` lists each checklist item as present or missing
- [ ] Cover fields (trial id, title, site) appear in the index from the local file — not from the internet
- [ ] README states this packet is synthetic teaching data

## ClassroomIO

Attach this folder to Module 5. Assignment: `outputs/packet-index.md` plus one paragraph on why a cloud scribe on identifiable notes is out of scope.
