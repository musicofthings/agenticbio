#!/usr/bin/env python3
"""Deterministic fallback when Ollama is not installed. Not a model."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text = (root / "fixtures" / "governance-note.txt").read_text()
out = root / "outputs"
out.mkdir(exist_ok=True)
(out / "completion.txt").write_text(
    "OFFLINE STUB (no LLM invoked)\n\n"
    "- Keep genomic and clinical files on local disk.\n"
    "- Ask models only about pipeline process and gates.\n"
    "- Never paste VCF records, sample IDs, or identifiable narrative.\n\n"
    f"Source fixture:\n{text}"
)
(out / "boundary.md").write_text(
    "# Trust boundary (stub)\n\n"
    "- May leave the machine: anonymized process descriptions, Docker/Nextflow snippets.\n"
    "- Must not leave: VCF/BAM/FASTQ, sample IDs, protocol text with identifiers.\n"
    "- Violation log: timestamp, destination, file class, operator id — stored locally.\n"
)
print(f"Wrote {out / 'completion.txt'} and {out / 'boundary.md'}")
