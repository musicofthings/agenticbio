# Lab 03 — Nextflow DSL2 as the execution plane

**Module:** 3  
**Timebox:** 2 hours async  
**Data:** `data/input.txt` (plain text). The agent is not the runner.

## Objective

Run a two-process DSL2 pipeline: (1) count lines, (2) write a JSON-ish summary. The workflow file is the audit trail. An agent may *propose* a `nextflow run` command; it must not replace the workflow with ad-hoc bash.

## Constraints

- `main.nf` is the source of truth. Do not “fix” a failed run by copying commands into a shell script and calling that the pipeline.
- Use `-c nextflow.config` so the container image is explicit.
- Teaching data only.

## What to run

```bash
# nextflow 24+ on PATH, or:
# docker run --rm -v "$PWD":/work -w /work nextflow/nextflow:24.10.0 nextflow run main.nf

nextflow run main.nf -c nextflow.config
```

## Acceptance criteria

- [ ] `results/summary.txt` exists after a clean run
- [ ] `main.nf` has at least two processes wired by a channel
- [ ] You can explain to a PI, in two sentences, why the agent must not `docker run` analysis steps behind Nextflow’s back

## ClassroomIO

Zip this folder onto Module 3. Assignment: attach `results/summary.txt` and a 5-line comment on the audit-trail rule.
