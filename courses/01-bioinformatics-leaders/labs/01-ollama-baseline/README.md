# Lab 01 — Local Ollama baseline

**Module:** 1  
**Timebox:** 90 minutes async  
**Data:** fixture text only (`fixtures/governance-note.txt`). No genomic payloads.

## Objective

Run a local instruct model through Ollama (or compatible) and produce one completion that restates a **process** constraint — never a clinical or genomic payload. You should be able to point at the trust boundary in one paragraph.

## Constraints

- Inference stays on localhost (or a VM you control). No OpenAI/Anthropic/Google calls in this lab.
- Do not paste VCF, BAM, FASTQ, or identifiable clinical text into the prompt.
- If Ollama cannot be installed (corporate laptop), document the blocker and run `scripts/offline_stub.py` so the rest of the Fellowship can continue.

## What to run

```bash
# If Docker is available (optional — Ollama usually runs on the host):
# brew install ollama   # or follow https://ollama.com

ollama pull llama3.2:1b
./scripts/run_local_prompt.sh
```

Offline fallback:

```bash
python3 scripts/offline_stub.py
```

## Acceptance criteria

- [ ] `outputs/completion.txt` exists and is derived from `fixtures/governance-note.txt`
- [ ] `outputs/boundary.md` states: what may leave the machine, what must not, and how you would log a violation
- [ ] No API keys in the repo or in shell history for this exercise

## ClassroomIO

Attach this README as the lesson resource for Module 1, Lesson 1.3. Fellows upload `outputs/boundary.md` as the assignment.
