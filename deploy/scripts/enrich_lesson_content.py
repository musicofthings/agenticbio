#!/usr/bin/env python3
"""Expand Fellowship lesson HTML, add YouTube placeholders and prev/next nav.

Writes classroomio-draft.json for all five cohorts, then (with --apply) updates
the running local ClassroomIO database in place. Structure PUT is not used:
re-importing with a new idempotency key would duplicate lessons.

Usage (from repo root):

  python3 deploy/scripts/enrich_lesson_content.py --write
  python3 deploy/scripts/enrich_lesson_content.py --write --apply
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GH = "https://github.com/musicofthings/agenticbio"
LAB01 = f"{GH}/tree/main/courses/01-bioinformatics-leaders/labs/01-ollama-baseline"
LAB02 = f"{GH}/tree/main/courses/01-bioinformatics-leaders/labs/02-container-r-python"
LAB03 = f"{GH}/tree/main/courses/01-bioinformatics-leaders/labs/03-nextflow-execution-plane"
LAB04_BIO = f"{GH}/tree/main/courses/01-bioinformatics-leaders/labs/04-vcf-local-agent"
LAB04_DS = f"{GH}/tree/main/courses/02-biopharma-data-scientists/labs/04-multiomic-local-agent"
LAB04_CLIN = f"{GH}/tree/main/courses/03-clinical-healthcare/labs/04-ethics-packet-local-agent"
LAB04_RAG = f"{GH}/tree/main/courses/04-rnd-institute-data-scientists/labs/04-manual-rag-local-agent"
LAB04_GRANT = f"{GH}/tree/main/courses/05-academic-scientists/labs/04-grant-synth-local-agent"
CAPSTONE = f"{GH}/blob/main/courses/01-bioinformatics-leaders/capstone-one-pager.md"

COURSES = [
    {
        "draft": REPO_ROOT / "courses/01-bioinformatics-leaders/classroomio-draft.json",
        "slug": "agentic-bio-fellowship-bioinformatics",
        "slot": "BIO",
    },
    {
        "draft": REPO_ROOT / "courses/02-biopharma-data-scientists/classroomio-draft.json",
        "slug": "agentic-bio-fellowship-biopharma-ds",
        "slot": "DS",
    },
    {
        "draft": REPO_ROOT / "courses/03-clinical-healthcare/classroomio-draft.json",
        "slug": "agentic-bio-fellowship-clinical",
        "slot": "CLIN",
    },
    {
        "draft": REPO_ROOT / "courses/04-rnd-institute-data-scientists/classroomio-draft.json",
        "slug": "agentic-bio-fellowship-rnd-rag",
        "slot": "RAG",
    },
    {
        "draft": REPO_ROOT / "courses/05-academic-scientists/classroomio-draft.json",
        "slug": "agentic-bio-fellowship-academic-grants",
        "slot": "GRANT",
    },
]

NAV_START = "<!--cio-lesson-nav-->"
NAV_END = "<!--/cio-lesson-nav-->"
YT_START = "<!--cio-youtube-placeholder-->"
YT_END = "<!--/cio-youtube-placeholder-->"


def slugify(title: str) -> str:
    text = title.lower().replace("—", "-").replace("–", "-")
    text = text.replace(".", "-")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def youtube_block(slot: str) -> str:
    return (
        f"{YT_START}"
        "<h3>Live session recording</h3>"
        f"<p><strong>YouTube placeholder — {slot}</strong></p>"
        "<p>The 90-minute live session recording will be embedded here after class. "
        "Faculty: open this lesson → <em>Videos</em> → paste the YouTube URL. "
        "Do not put a raw iframe in the lesson body (the dashboard Content-Security-Policy "
        "blocks YouTube frames). Completion stays <em>manual</em>, so fellows can mark the "
        "lesson complete before the recording is up.</p>"
        f"<p><em>[ YouTube player will appear above this text once {slot} is added ]</em></p>"
        f"{YT_END}"
    )


def nav_block(
    *,
    prev_title: str | None,
    prev_hrefs: list[tuple[str, str]],
    next_title: str | None,
    next_hrefs: list[tuple[str, str]],
) -> str:
    parts = [NAV_START, "<h3>Continue to the next lesson</h3>"]
    if prev_title and prev_hrefs:
        links = " · ".join(f'<a href="{href}">{label}</a>' for href, label in prev_hrefs)
        parts.append(f"<p>← Previous: {prev_title} — {links}</p>")
    else:
        parts.append("<p>This is the first lesson in the course.</p>")
    if next_title and next_hrefs:
        links = " · ".join(f'<a href="{href}">{label}</a>' for href, label in next_hrefs)
        parts.append(f"<p>Next: {next_title} → {links}</p>")
    else:
        parts.append("<p>This is the last lesson. Submit the capstone when you are ready.</p>")
    parts.append(
        "<p>Fellows signed in as students also get Previous / Next in the lesson header. "
        "Teachers: use <em>View as student</em> in the course header to see that bar, "
        "or use the links above.</p>"
    )
    parts.append(NAV_END)
    return "".join(parts)


def strip_markers(html: str) -> str:
    html = re.sub(re.escape(YT_START) + r".*?" + re.escape(YT_END), "", html, flags=re.S)
    html = re.sub(re.escape(NAV_START) + r".*?" + re.escape(NAV_END), "", html, flags=re.S)
    return html


def disclaimer() -> str:
    return (
        "<p><strong>Not a medical device. Not clinical advice.</strong> "
        "Labs use synthetic teaching data only.</p>"
    )


def how_live() -> str:
    return (
        "<h3>How the live session runs</h3>"
        "<p>Ninety minutes on the week’s contract, then the lab is async. "
        "Bring a machine you control (or a written blocker plus the offline stub). "
        "We will not paste real payloads into a prompt in class.</p>"
    )


def ollama_lab() -> str:
    return (
        "<h3>What to run</h3>"
        f"<p>Lab folder: <a href=\"{LAB01}\">labs/01-ollama-baseline</a>.</p>"
        "<pre><code>ollama pull llama3.2:1b\n./scripts/run_local_prompt.sh</code></pre>"
        "<p>If Ollama cannot be installed (corporate laptop, no local daemon), document "
        "the blocker and continue with the stub so the rest of the Fellowship is unblocked:</p>"
        "<pre><code>python3 scripts/offline_stub.py</code></pre>"
        "<h3>Acceptance</h3>"
        "<ul>"
        "<li><code>outputs/completion.txt</code> exists and is derived from "
        "<code>fixtures/governance-note.txt</code></li>"
        "<li>No API keys in the repo or in shell history for this exercise</li>"
        "</ul>"
    )


def docker_lab() -> str:
    return (
        "<h3>What to run</h3>"
        f"<p>Lab folder: <a href=\"{LAB02}\">labs/02-container-r-python</a>.</p>"
        "<pre><code>docker build -t agenticbio-lab02:local .\n"
        'docker run --rm -v "$PWD/data:/data" -v "$PWD/outputs:/outputs" '
        "agenticbio-lab02:local python /opt/lab/summarize.py\n"
        'docker run --rm -v "$PWD/data:/data" -v "$PWD/outputs:/outputs" '
        "agenticbio-lab02:local Rscript /opt/lab/summarize.R</code></pre>"
        "<h3>Acceptance</h3>"
        "<ul>"
        "<li>Image builds on your machine (amd64 or arm64)</li>"
        "<li><code>outputs/python_summary.txt</code> and <code>outputs/r_summary.txt</code> exist</li>"
        "<li>Host <code>python3</code> / <code>R</code> are not required to produce those files</li>"
        "<li>The Dockerfile pins a digest or a major tag you could defend in an audit</li>"
        "</ul>"
    )


def nextflow_lab() -> str:
    return (
        "<h3>What to run</h3>"
        f"<p>Lab folder: <a href=\"{LAB03}\">labs/03-nextflow-execution-plane</a>.</p>"
        "<pre><code>nextflow run main.nf -c nextflow.config</code></pre>"
        "<p>Or:</p>"
        "<pre><code>docker run --rm -v \"$PWD\":/work -w /work "
        "nextflow/nextflow:24.10.0 nextflow run main.nf</code></pre>"
        "<h3>Acceptance</h3>"
        "<ul>"
        "<li><code>results/summary.txt</code> exists after a clean run</li>"
        "<li><code>main.nf</code> has at least two processes wired by a channel</li>"
        "<li>You can explain the audit-trail rule in two sentences</li>"
        "</ul>"
    )


def body_bio() -> dict[str, str]:
    return {
        "les-1-1": (
            "<h3>The failure mode</h3>"
            "<p>Public model endpoints and VCF or protocol text do not mix. "
            "“The vendor says the model is HIPAA-eligible” is not the same as "
            "<em>your</em> institutional governance allowing genomic payloads off-box. "
            "The question is not whether a brochure lists a certification. The question "
            "is whether this payload leaves a machine you control.</p>"
            "<p>Clinical genomics already has a chain of custody: sequencer → pipeline → "
            "report → sign-out. Inserting a cloud LLM in that chain without a DPA, a DPIA, "
            "and an explicit allow-list is how programs get paused by legal, not how they "
            "get faster.</p>"
            "<h3>Local-only rule for this Fellowship</h3>"
            "<ul>"
            "<li>No public cloud LLM APIs for VCF, BAM-derived tables, or protocol text.</li>"
            "<li>Agents may talk about <em>process</em> (how a pipeline is gated). They may "
            "not be given the payload.</li>"
            "<li>If a vendor dashboard would make the run easier, it is still out of scope.</li>"
            "</ul>"
            "<h3>Who this week is for</h3>"
            "<p>Bioinformatics leads, computational biologists, and infrastructure owners "
            "who already write pipelines. Not for prompt-engineering beginners or teams "
            "whose only goal is a cloud copilot on PHI.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-1-2": (
            "<h3>Ollama as the inference plane</h3>"
            "<p>Install Ollama on a machine you control. Pull a small instruct model. "
            "Run one completion against a <strong>non-clinical</strong> fixture file. "
            "The point is not model quality. The point is that inference has a home "
            "you can point at in an audit: this host, this binary, this model tag.</p>"
            "<p>Treat the local daemon as infrastructure, not as a chatbot. Later weeks "
            "will call it from an agent loop. This week you prove it runs without a "
            "cloud key.</p>"
            + ollama_lab()
            + how_live()
        ),
        "les-1-3": (
            "<h3>What may leave the machine</h3>"
            "<p>Prompts about <em>process</em>: how a human gate works, which Nextflow "
            "process failed, whether a container tag is pinned. Never the payload. "
            "A useful test: if the email would still make sense with every sample id "
            "redacted, it may leave. If it would not, it stays.</p>"
            "<h3>What must not leave</h3>"
            "<ul>"
            "<li>VCF, BAM, FASTQ, or identifiable clinical narrative</li>"
            "<li>Sample IDs from a real cohort</li>"
            "<li>Protocol text that is not already public</li>"
            "</ul>"
            "<h3>Logging</h3>"
            "<p>Write down where prompts and completions are stored, who can read them, "
            "and how you would log a violation. That paragraph is the assignment "
            "(<code>outputs/boundary.md</code>).</p>"
            f"<p>Lab folder: <a href=\"{LAB01}\">labs/01-ollama-baseline</a>.</p>"
            + how_live()
        ),
        "les-2-1": (
            "<h3>One image, two languages</h3>"
            "<p>Python and R in one reproducible image. Pin versions. "
            "“It works on my HPC login node” is not an audit trail. The fellow who "
            "joins in month six should be able to rebuild the same runtime from the "
            "Dockerfile, not from your <code>$HOME</code>.</p>"
            "<p>Analysis code runs <em>in the container</em>, not on the host Python or R. "
            "Bind-mount inputs and outputs. Do not bake unpublished or licensed clinical "
            "datasets into the image.</p>"
            + docker_lab()
            + how_live()
        ),
        "les-2-2": (
            "<h3>What belongs in the image</h3>"
            "<p>Interpreters, Bioconductor packages, pinned system libraries. Anything a "
            "second fellow would need to reproduce the run without your <code>$HOME</code>. "
            "If a package is only on your laptop because you compiled it last year, it "
            "belongs in the image or it does not belong in the pipeline.</p>"
            "<h3>What is bind-mounted</h3>"
            "<p>Input tables and outputs. Do not bake unpublished or licensed clinical "
            "datasets into the image. This lab’s <code>data/counts.csv</code> is teaching "
            "data only.</p>"
            "<h3>Network</h3>"
            "<p>Image <em>build</em> may use a package mirror. Analysis scripts must not "
            "call the network. No Ensembl, no ClinVar, no “just this once” REST annotation.</p>"
            f"<p>Lab folder: <a href=\"{LAB02}\">labs/02-container-r-python</a>.</p>"
            + how_live()
        ),
        "les-3-1": (
            "<h3>The audit-trail rule</h3>"
            "<p>Never let the agent invoke ad-hoc <code>bash</code> as the source of truth "
            "for a pipeline. The workflow file is the audit trail. An agent may "
            "<em>propose</em> <code>nextflow run</code>; it must not replace the workflow "
            "with a shell script and call that the pipeline.</p>"
            "<p>Two sentences you should be able to say to a PI:</p>"
            "<ol>"
            "<li>The agent plans which process to run and with which params.</li>"
            "<li>Nextflow (DSL2) is the only runner that writes the work directory, "
            "the report, and the resume state.</li>"
            "</ol>"
            f"<p>Lab folder: <a href=\"{LAB03}\">labs/03-nextflow-execution-plane</a>.</p>"
            + how_live()
        ),
        "les-3-2": (
            "<h3>Minimal DSL2</h3>"
            "<p>Two processes wired by a channel: count lines, then write a summary. "
            "Use <code>-c nextflow.config</code> so the container image is explicit. "
            "If the agent cannot see which image tag ran, you do not have an audit trail.</p>"
            "<p>Channels are the contract between processes. Do not reach into another "
            "process’s work directory from a side script. That is how “helpful” agents "
            "destroy <code>-resume</code>.</p>"
            + nextflow_lab()
            + how_live()
        ),
        "les-4-1": (
            "<h3>File in → plan → execute → file out → critic</h3>"
            "<p>Chat UIs are not the product. The loop is: read a file, propose a Nextflow "
            "or container command, run it, read the output, stop for a human before any "
            "write that would mutate inputs or a LIMS.</p>"
            "<h3>Human gate on writes</h3>"
            "<p>The agent may create files under <code>outputs/</code> or <code>results/</code>. "
            "It may not rewrite the input VCF, the workflow file, or a production "
            "<code>-resume</code> work directory without an explicit human yes.</p>"
            "<p>This week has no extra lab stub. Reuse labs 1–3 as the tool surface.</p>"
            + how_live()
        ),
        "les-4-2": (
            "<h3>Map tools, deny network</h3>"
            "<p>On OpenClaw or an equivalent local runtime, map tools to:</p>"
            "<ul>"
            "<li><code>list_dir</code></li>"
            "<li><code>read_file</code></li>"
            "<li><code>run_nextflow</code></li>"
            "<li><code>run_container</code></li>"
            "</ul>"
            "<p>Deny network except optional package mirrors you already trust. Do not "
            "give the agent a general <code>bash</code> tool that can <code>curl</code> ClinVar.</p>"
            "<h3>Implementation</h3>"
            "<p>The implementation is the fellow’s own agent runtime using labs 1–3. "
            "Paste a short architecture note (tools allowed, tools denied, where the "
            "human gate sits) into the week-4 assignment.</p>"
            + how_live()
        ),
        "les-5-1": (
            "<h3>VCFv4.2 as a contract</h3>"
            "<p>Header, INFO, FORMAT. Teaching data is <strong>synthetic only</strong> — "
            "invented sites and sample id <code>SYNTH-001</code>. Not from a patient, "
            "not from a public disease study. Do not replace the fixture with a real "
            "cohort export “just to see if it works.”</p>"
            f"<p>Lab folder: <a href=\"{LAB04_BIO}\">labs/04-vcf-local-agent</a>.</p>"
            "<h3>Non-negotiable</h3>"
            "<ul>"
            "<li>Do not replace <code>synthetic.vcf</code> with a real cohort export</li>"
            "<li>Do not call external REST annotation services</li>"
            "<li>A future agent may propose the parse command; a human must approve "
            "any rewrite of the VCF</li>"
            "</ul>"
            + how_live()
            + disclaimer()
        ),
        "les-5-2": (
            "<h3>On disk, not over HTTPS</h3>"
            "<p>Parse the fixture, emit a TSV of CHROM/POS/REF/ALT/QUAL, and join a local "
            "annotation table. No Ensembl, ClinVar, or other network annotation APIs. "
            "If the local TSV has no row, the annotation is <code>NA</code> — not a second "
            "try against the internet.</p>"
            "<pre><code>python3 parse_vcf.py --vcf data/synthetic.vcf "
            "--annot data/annotation.tsv --out outputs/variants.tsv</code></pre>"
            "<p>Optional: run the same script inside the lab 02 image with bind mounts.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_BIO}\">labs/04-vcf-local-agent</a>.</p>"
            "<h3>Acceptance</h3>"
            "<ul>"
            "<li><code>outputs/variants.tsv</code> has a header and one row per variant "
            "record (not header lines)</li>"
            "<li>Annotation column is filled from the local TSV (or <code>NA</code> if "
            "missing) — not from the internet</li>"
            "<li>A paragraph on why ClinVar-over-HTTPS is out of scope for the lab</li>"
            "</ul>"
            + how_live()
        ),
        "les-6-1": (
            "<h3>Fail, patch, re-run</h3>"
            "<p>The agent proposes a pandas or R fix. A human approves. The container "
            "re-runs. Max N iterations, then stop. Extend lab 2 (the image) and lab 4 "
            "(the TSV). Do not invent a new cloud notebook.</p>"
            "<h3>What “self-correcting” is not</h3>"
            "<p>It is not unbounded retries against a production Nextflow work dir. It is "
            "a bounded loop with a human signature on each patch that changes analysis "
            "code. If you cannot point at the yes, the patch did not happen.</p>"
            + how_live()
        ),
        "les-6-2": (
            "<h3>Never auto-merge</h3>"
            "<ul>"
            "<li>Anything that would touch a LIMS</li>"
            "<li>A clinical report or sign-out artifact</li>"
            "<li>A production Nextflow <code>-resume</code> on real samples</li>"
            "<li>Rewrites of input VCFs</li>"
            "</ul>"
            "<p>If the patch would do any of those, the loop ends and a human writes the "
            "next ticket. That is the whole lesson. Speed is not a reason to skip the gate.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-7-1": (
            "<h3>Deliverable</h3>"
            "<p>One local pipeline on the synthetic cohort in lab 4:</p>"
            "<ul>"
            "<li>Ollama (or the offline stub) drafts a run plan</li>"
            "<li>Nextflow executes containerized parse + summary</li>"
            "<li>A human signs the architecture one-pager</li>"
            "</ul>"
            "<h3>One-pager (one page, no sample-level data)</h3>"
            "<ul>"
            "<li>System name</li>"
            "<li>Trust boundary — what may leave, what must not, where logs live</li>"
            "<li>Data flow — fixture in → agent plan → Nextflow → TSV/report out → human gate</li>"
            "<li>Execution plane — which steps are Nextflow processes vs agent-only; "
            "name the container image tag</li>"
            "<li>Failure modes — two realistic failures and the human action</li>"
            "<li>What this is not — not a medical device; synthetic data only; "
            "no production LIMS write-back</li>"
            "</ul>"
            f"<p>Template: <a href=\"{CAPSTONE}\">capstone-one-pager.md</a>.</p>"
            "<h3>Enterprise extra</h3>"
            "<p>60-minute architecture review of their HPC/LIMS/Batch vs this pattern. "
            "Scheduled outside the LMS after week 3. Not a lab in git.</p>"
            + disclaimer()
        ),
    }


def body_ds() -> dict[str, str]:
    return {
        "les-1-1": (
            "<h3>The failure mode</h3>"
            "<p>Public model endpoints and unpublished expression tables, figure drafts, "
            "or partner-data use terms do not mix. “The vendor is SOC2” is not permission "
            "to leave the firewall. Partner contracts often forbid exactly this kind of "
            "off-box processing even when the rows look de-identified to you.</p>"
            "<h3>Local-only rule</h3>"
            "<ul>"
            "<li>No public cloud LLM APIs for matrices, assay exports, or unpublished figures.</li>"
            "<li>Agents may talk about <em>process</em>. They may not be given the payload.</li>"
            "</ul>"
            "<p>This track uses the same technical core as cohort 1 (Ollama, Docker, Nextflow). "
            "The skin is discovery and multiomic analysis behind the firewall — not "
            "clinical-genomics pipeline language.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-1-2": (
            "<h3>Same lab as cohort 1</h3>"
            "<p>Install Ollama (or run the offline stub). One completion against a "
            "non-clinical fixture. The fixture is about process, not about an assay. "
            "Do not paste a real matrix into the prompt to “make it more realistic.”</p>"
            + ollama_lab()
            + how_live()
        ),
        "les-1-3": (
            "<h3>What may leave</h3>"
            "<p>Prompts about process: how a human gate works, which Nextflow process "
            "failed, whether a container tag is pinned.</p>"
            "<h3>What must not</h3>"
            "<ul>"
            "<li>Expression matrices, sample IDs, unpublished figures</li>"
            "<li>Partner-data tables even if “de-identified enough”</li>"
            "</ul>"
            "<p>Assignment: <code>outputs/boundary.md</code> from the cohort 1 Ollama lab, "
            "written in discovery language.</p>"
            + how_live()
        ),
        "les-2-1": (
            "<h3>Pin the image</h3>"
            "<p>Python and R in one reproducible image. Discovery teams still do not "
            "ship “it works on my laptop.” The image is the runtime you could defend "
            "to QA or to a partner auditor.</p>"
            + docker_lab()
            + how_live()
        ),
        "les-3-1": (
            "<h3>The audit-trail rule</h3>"
            "<p>The workflow file is the audit trail for a discovery pipeline, not a "
            "chat log. An agent may propose <code>nextflow run</code>; it must not "
            "replace the workflow with ad-hoc bash. If a board later asks which image "
            "produced a figure, the answer is in Nextflow’s report, not in Slack.</p>"
            + nextflow_lab()
            + how_live()
        ),
        "les-4-1": (
            "<h3>File in → plan → execute → file out → critic</h3>"
            "<p>Map tools to <code>list_dir</code>, <code>read_file</code>, "
            "<code>run_nextflow</code>, <code>run_container</code>. Deny network except "
            "trusted package mirrors. Human gate on any write that would mutate inputs "
            "or a LIMS.</p>"
            "<p>Chat is for planning. Files are for evidence. If the only record of a "
            "join is a paste from a chatbot, you do not have a discovery pipeline.</p>"
            + how_live()
        ),
        "les-5-1": (
            "<h3>A matrix is a contract</h3>"
            "<p>Gene × sample table. Teaching data is <strong>synthetic only</strong> — "
            "invented gene ids and sample id <code>SYNTH-DS-001</code>. Not from a trial, "
            "not from GEO-as-proxy for partner data.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_DS}\">labs/04-multiomic-local-agent</a>.</p>"
            "<p>Do not replace <code>expression.tsv</code> with a real assay export. "
            "A future agent may propose the join command; a human must approve any "
            "rewrite of the matrix.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-5-2": (
            "<h3>On disk, not over HTTPS</h3>"
            "<pre><code>python3 join_matrix.py --expr data/expression.tsv "
            "--annot data/annotation.tsv --out outputs/joined.tsv</code></pre>"
            "<p>No Enrichr, STRING, or other network enrichment APIs. Annotation comes "
            "from the local TSV or <code>NA</code>.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_DS}\">labs/04-multiomic-local-agent</a>.</p>"
            "<h3>Acceptance</h3>"
            "<ul>"
            "<li><code>outputs/joined.tsv</code> has a header and one row per gene</li>"
            "<li>Annotation columns are filled from the local TSV (or <code>NA</code>)</li>"
            "<li>One paragraph on why Enrichr-over-HTTPS is out of scope</li>"
            "</ul>"
            + how_live()
        ),
        "les-6-1": (
            "<h3>Bounded loop</h3>"
            "<p>The agent proposes a pandas or R fix. A human approves. The container "
            "re-runs. Max N iterations, then stop. Never auto-merge into a LIMS, a board "
            "deck with real sample IDs, or a production Nextflow <code>-resume</code> on "
            "licensed assays.</p>"
            + how_live()
        ),
        "les-7-1": (
            "<h3>Deliverable</h3>"
            "<p>One local pipeline on the synthetic matrix in lab 4. Ollama (or stub) "
            "drafts a run plan. Nextflow executes containerized join + summary. A human "
            "signs the architecture one-pager (reuse the cohort 1 template; swap VCF "
            "language for matrix).</p>"
            f"<p>Template: <a href=\"{CAPSTONE}\">capstone-one-pager.md</a>.</p>"
            + disclaimer()
        ),
    }


def body_clin() -> dict[str, str]:
    return {
        "les-1-1": (
            "<h3>The failure mode</h3>"
            "<p>Public model endpoints and identifiable notes, imaging reports, or live "
            "IEC packets do not mix. “HIPAA-eligible vendor” is not your DPA. Hospital "
            "legal will ask where the text went, who can read the logs, and whether a "
            "subprocessor in another country saw a name.</p>"
            "<h3>What this track is not</h3>"
            "<p>Not diagnosis, triage, or treatment. Documentation workflow only — "
            "ethics-committee packets and protocol administration. We do not teach "
            "scribes that write into the EHR.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-1-2": (
            "<h3>Same lab as cohort 1</h3>"
            "<p>One completion against a non-clinical fixture. Do not paste a real note, "
            "imaging report, or consent form into the prompt. The fixture is about "
            "process language: how a packet is gated, not what a patient said.</p>"
            + ollama_lab()
            + how_live()
        ),
        "les-1-3": (
            "<h3>What may leave</h3>"
            "<p>Prompts about how a packet is gated: which checklist item is missing, "
            "whether the container tag is pinned, who must sign before filing.</p>"
            "<h3>What must not</h3>"
            "<ul>"
            "<li>Names, MRNs, report text</li>"
            "<li>Real consent forms or live IEC packets</li>"
            "</ul>"
            "<p>Assignment: <code>outputs/boundary.md</code> written for clinical "
            "documents (process only).</p>"
            + how_live()
        ),
        "les-2-1": (
            "<h3>Pin the image</h3>"
            "<p>Clinical IT still pins the runtime rather than “it works on the ward PC.” "
            "The image is what you would show to infosec when they ask how document "
            "assembly is reproduced.</p>"
            + docker_lab()
            + how_live()
        ),
        "les-3-1": (
            "<h3>Audit trail</h3>"
            "<p>The workflow file is the audit trail for document assembly, not a chat "
            "log. If an IEC secretariat later asks which checklist version was indexed, "
            "the answer is in Nextflow’s report.</p>"
            + nextflow_lab()
            + how_live()
        ),
        "les-4-1": (
            "<h3>Human gate before filing</h3>"
            "<p>Map tools to <code>list_dir</code>, <code>read_file</code>, "
            "<code>run_nextflow</code>, <code>run_container</code>. Deny network. "
            "Never auto-file to an IEC portal, EHR, or PACS.</p>"
            "<p>The agent may list gaps. It may not invent CVs, insurance text, or "
            "signatures. Filing is a human act.</p>"
            + how_live()
        ),
        "les-5-1": (
            "<h3>A packet is a contract</h3>"
            "<p>Checklist + administrative cover. Trial id <code>SYNTH-TRIAL-001</code>. "
            "No patients, no dosing, no wet-lab methods. Do not replace fixtures with "
            "a real IEC packet.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_CLIN}\">labs/04-ethics-packet-local-agent</a>.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-5-2": (
            "<h3>Assemble locally</h3>"
            "<pre><code>python3 extract_packet.py --checklist data/iec-checklist.md "
            "--cover data/synthetic-protocol-admin.md --out outputs/packet-index.md</code></pre>"
            "<p>The agent may list gaps. It may not invent CVs or insurance text. Cover "
            "fields (trial id, title, site) come from the local file — not from the internet.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_CLIN}\">labs/04-ethics-packet-local-agent</a>.</p>"
            "<h3>Acceptance</h3>"
            "<ul>"
            "<li><code>outputs/packet-index.md</code> lists each checklist item as present or missing</li>"
            "<li>One paragraph on why a cloud scribe on identifiable notes is out of scope</li>"
            "</ul>"
            + how_live()
        ),
        "les-6-1": (
            "<h3>Bounded loop</h3>"
            "<p>Agent proposes a checklist fix; human approves; container re-runs; max N "
            "iterations. Never auto-file to an IEC portal, EHR, or PACS. If the next "
            "step would look like a submission, the loop ends.</p>"
            + how_live()
        ),
        "les-7-1": (
            "<h3>Deliverable</h3>"
            "<p>One local pipeline on the synthetic packet. Ollama (or stub) drafts a run "
            "plan; Nextflow executes containerized extract; a human signs the architecture "
            "one-pager (reuse the cohort 1 template; swap VCF language for packet).</p>"
            f"<p>Template: <a href=\"{CAPSTONE}\">capstone-one-pager.md</a>.</p>"
            + disclaimer()
        ),
    }


def body_rag() -> dict[str, str]:
    return {
        "les-1-1": (
            "<h3>The failure mode</h3>"
            "<p>Vendor knowledge bases that require uploading SOPs. Historical research "
            "stores often include unpublished methods filenames and internal path "
            "conventions even when the science is not secret. Uploading the folder is "
            "still a leak of how the institute is organized.</p>"
            "<p>This track is offline retrieval over manuals you already have on disk. "
            "No public embedding APIs. No “upload the SOP to a vendor.”</p>"
            + how_live()
            + disclaimer()
        ),
        "les-1-2": (
            "<h3>Same lab as cohort 1</h3>"
            "<p>Prove local inference before you retrieve. Do not paste a real manual "
            "body into the prompt this week. The fixture is process language.</p>"
            + ollama_lab()
            + how_live()
        ),
        "les-1-3": (
            "<h3>What may leave</h3>"
            "<p>How retrieval is gated: which corpus was searched, which k, who must "
            "approve a write-back.</p>"
            "<h3>What must not</h3>"
            "<ul>"
            "<li>Manual bodies</li>"
            "<li>Internal hostnames</li>"
            "<li>Unpublished figure files</li>"
            "</ul>"
            + how_live()
        ),
        "les-2-1": (
            "<h3>Pin the image</h3>"
            "<p>Retrieval jobs still need a pinned runtime. The image is how a second "
            "informatics lead reproduces the search without your laptop.</p>"
            + docker_lab()
            + how_live()
        ),
        "les-3-1": (
            "<h3>Audit trail</h3>"
            "<p>The workflow file records which corpus was searched. Chat is not a "
            "citation. If a PI asks “where did that paragraph come from?”, the answer "
            "is a path on disk plus a Nextflow report.</p>"
            + nextflow_lab()
            + how_live()
        ),
        "les-4-1": (
            "<h3>Cite the path</h3>"
            "<p>File in → retrieve → file out → critic. Human gate before write-back "
            "into the live SOP tree. Deny network except trusted package mirrors. "
            "A generated paragraph that cannot point at a source file is not a hit; "
            "it is a hallucination with formatting.</p>"
            + how_live()
        ),
        "les-5-1": (
            "<h3>A corpus is a contract</h3>"
            "<p>Synthetic ops notes: freezer logs, run-folder naming, handover. Not "
            "wet-lab recipes. Not a real institute SOP dump. Do not replace the "
            "fixtures with live manuals.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_RAG}\">labs/04-manual-rag-local-agent</a>.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-5-2": (
            "<h3>Retrieve locally</h3>"
            "<pre><code>python3 retrieve.py --corpus data/manuals --query data/query.txt "
            "--out outputs/hits.md --k 3</code></pre>"
            "<p>Keyword overlap. No OpenAI embeddings, no hosted vector DB. Hits come "
            "from the local corpus or an explicit “no hit.”</p>"
            f"<p>Lab folder: <a href=\"{LAB04_RAG}\">labs/04-manual-rag-local-agent</a>.</p>"
            "<h3>Acceptance</h3>"
            "<ul>"
            "<li><code>outputs/hits.md</code> lists source filenames and scored snippets</li>"
            "<li>One paragraph on why uploading SOPs to a vendor RAG is out of scope</li>"
            "</ul>"
            + how_live()
        ),
        "les-6-1": (
            "<h3>Bounded loop</h3>"
            "<p>Agent proposes a query rewrite; human approves; container re-runs. "
            "Never auto-merge a generated paragraph into the live manual. A wrong "
            "cite stops the loop.</p>"
            + how_live()
        ),
        "les-7-1": (
            "<h3>Deliverable</h3>"
            "<p>One local pipeline on the synthetic corpus. Reuse the cohort 1 "
            "architecture one-pager; swap VCF language for manual corpus.</p>"
            f"<p>Template: <a href=\"{CAPSTONE}\">capstone-one-pager.md</a>.</p>"
            + disclaimer()
        ),
    }


def body_grant() -> dict[str, str]:
    return {
        "les-1-1": (
            "<h3>The failure mode</h3>"
            "<p>Unpublished text, reviewer comments, and institute reports are not "
            "public. A research copilot that ships them off-box is a leak. Grant "
            "<em>structure</em> is the product; the agency portal stays a human submit.</p>"
            "<p>The Fellowship does not file grants. Teaching abstracts are invented; "
            "we do not copy publisher PDFs.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-1-2": (
            "<h3>Same lab as cohort 1</h3>"
            "<p>Prove local inference before you synthesize. Do not paste an unpublished "
            "manuscript or a real budget line into the prompt this week.</p>"
            + ollama_lab()
            + how_live()
        ),
        "les-1-3": (
            "<h3>What may leave</h3>"
            "<p>How an outline is gated: which template heading is empty, who must "
            "approve a portal paste.</p>"
            "<h3>What must not</h3>"
            "<ul>"
            "<li>Manuscript bodies</li>"
            "<li>Real budget lines</li>"
            "<li>Reviewer identities</li>"
            "</ul>"
            + how_live()
        ),
        "les-2-1": (
            "<h3>Pin the image</h3>"
            "<p>Synthesis still needs a pinned runtime. The image is how a co-PI "
            "reproduces the outline job without your laptop Python.</p>"
            + docker_lab()
            + how_live()
        ),
        "les-3-1": (
            "<h3>Audit trail</h3>"
            "<p>The workflow file records which abstract files were read. Chat is not "
            "a submission record. If a funding desk asks which notes fed a section, "
            "the answer is a path plus a Nextflow report.</p>"
            + nextflow_lab()
            + how_live()
        ),
        "les-4-1": (
            "<h3>Human gate before the portal</h3>"
            "<p>File in → synthesize → file out → critic. Never auto-submit to an "
            "agency portal. Deny network except trusted package mirrors. Paste is a "
            "human act, even when the outline looks finished.</p>"
            + how_live()
        ),
        "les-5-1": (
            "<h3>Abstracts as a contract</h3>"
            "<p><code>SYNTH-ABS-*</code> teaching files. We do not copy publisher PDFs. "
            "BioE3 is a section pattern, not a filing service. Do not paste copyrighted "
            "paper text into <code>data/abstracts/</code>.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_GRANT}\">labs/04-grant-synth-local-agent</a>.</p>"
            + how_live()
            + disclaimer()
        ),
        "les-5-2": (
            "<h3>Fill locally</h3>"
            "<pre><code>python3 synthesize.py --abstracts data/abstracts "
            "--template data/bioe3-outline.md --out outputs/grant-outline.md</code></pre>"
            "<p>Each filled bullet must cite a local <code>SYNTH-ABS-*</code> id. "
            "No cloud writer.</p>"
            f"<p>Lab folder: <a href=\"{LAB04_GRANT}\">labs/04-grant-synth-local-agent</a>.</p>"
            "<h3>Acceptance</h3>"
            "<ul>"
            "<li><code>outputs/grant-outline.md</code> has every template heading</li>"
            "<li>Each filled bullet cites a <code>SYNTH-ABS-*</code> id</li>"
            "<li>One paragraph on why uploading an unpublished manuscript to a cloud "
            "writer is out of scope</li>"
            "</ul>"
            + how_live()
        ),
        "les-6-1": (
            "<h3>Bounded loop</h3>"
            "<p>Agent proposes a section rewrite; human approves; container re-runs. "
            "Never auto-submit. If the next step is a portal paste, the loop ends.</p>"
            + how_live()
        ),
        "les-7-1": (
            "<h3>Deliverable</h3>"
            "<p>One local pipeline on the synthetic abstracts. Reuse the cohort 1 "
            "architecture one-pager; swap VCF language for grant outline. The "
            "Fellowship does not file grants.</p>"
            f"<p>Template: <a href=\"{CAPSTONE}\">capstone-one-pager.md</a>.</p>"
            + disclaimer()
        ),
    }


BODIES = {
    "agentic-bio-fellowship-bioinformatics": body_bio,
    "agentic-bio-fellowship-biopharma-ds": body_ds,
    "agentic-bio-fellowship-clinical": body_clin,
    "agentic-bio-fellowship-rnd-rag": body_rag,
    "agentic-bio-fellowship-academic-grants": body_grant,
}


def week_slot(prefix: str, lesson_external_id: str) -> str:
    # les-1-1 → W1-L1
    parts = lesson_external_id.split("-")
    if len(parts) >= 3:
        return f"{prefix}-W{parts[1]}-L{parts[2]}"
    return f"{prefix}-{lesson_external_id}"


def assemble_content(
    slug: str,
    slot_prefix: str,
    lessons: list[dict],
    *,
    lms_ids: dict[str, str] | None = None,
    course_id: str | None = None,
) -> dict[str, str]:
    bodies = BODIES[slug]()
    by_id = {item["externalId"]: item for item in lessons}
    ordered = sorted(
        lessons,
        key=lambda item: (item["sectionExternalId"], item["order"]),
    )
    out: dict[str, str] = {}
    for index, lesson in enumerate(ordered):
        ext = lesson["externalId"]
        body = bodies.get(ext)
        if not body:
            raise KeyError(f"Missing body for {slug} {ext}")
        prev_lesson = ordered[index - 1] if index else None
        next_lesson = ordered[index + 1] if index + 1 < len(ordered) else None

        def hrefs(item: dict | None) -> list[tuple[str, str]]:
            if not item:
                return []
            public = f"/course/{slug}/lesson/{slugify(item['title'])}"
            links = [(public, "public page")]
            if lms_ids and course_id and item["externalId"] in lms_ids:
                lid = lms_ids[item["externalId"]]
                links.insert(0, (f"/courses/{course_id}/lessons/{lid}", "classroom"))
            return links

        html = (
            youtube_block(week_slot(slot_prefix, ext))
            + body
            + nav_block(
                prev_title=prev_lesson["title"] if prev_lesson else None,
                prev_hrefs=hrefs(prev_lesson),
                next_title=next_lesson["title"] if next_lesson else None,
                next_hrefs=hrefs(next_lesson),
            )
        )
        out[ext] = html
        _ = by_id
    return out


def enrich_draft(path: Path, slug: str, slot_prefix: str) -> dict:
    draft = json.loads(path.read_text())
    for lesson in draft["lessons"]:
        lesson["isUnlocked"] = True
        lesson["public"] = True
    assembled = assemble_content(slug, slot_prefix, draft["lessons"])
    by_ext = {row["lessonExternalId"]: row for row in draft["lessonLanguages"]}
    for ext, html in assembled.items():
        if ext not in by_ext:
            draft["lessonLanguages"].append(
                {"lessonExternalId": ext, "locale": "en", "content": html}
            )
        else:
            by_ext[ext]["content"] = html
    return draft


def psql(sql: str) -> str:
    result = subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            "cio-postgres",
            "psql",
            "-U",
            "postgres",
            "-d",
            "classroomio",
            "-tAc",
            sql,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def psql_script(sql: str) -> None:
    subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            "cio-postgres",
            "psql",
            "-U",
            "postgres",
            "-d",
            "classroomio",
            "-v",
            "ON_ERROR_STOP=1",
        ],
        check=True,
        capture_output=True,
        text=True,
        input=sql,
    )


def find_course_id(title: str) -> str | None:
    escaped = title.replace("'", "''")
    row = psql(f"SELECT id FROM course WHERE title = '{escaped}' LIMIT 1;")
    return row or None


def db_lessons(course_id: str) -> list[tuple[str, str, str]]:
    sql = (
        "SELECT l.id, l.title, COALESCE(l.slug, '') "
        "FROM lesson l JOIN course_section s ON s.id = l.section_id "
        f"WHERE l.course_id = '{course_id}' "
        'ORDER BY s."order", l."order";'
    )
    rows = psql(sql)
    if not rows:
        return []
    out = []
    for line in rows.splitlines():
        lesson_id, title, slug = line.split("|", 2)
        out.append((lesson_id, title, slug))
    return out


def apply_draft(draft: dict, slug: str, slot_prefix: str) -> None:
    title = draft["course"]["title"]
    course_id = find_course_id(title)
    if not course_id:
        print(f"Skip apply (course not in DB): {title}", file=sys.stderr)
        return

    rows = db_lessons(course_id)
    by_title = {name: lid for lid, name, _ in rows}
    lms_ids: dict[str, str] = {}
    missing = []
    for lesson in draft["lessons"]:
        lid = by_title.get(lesson["title"])
        if not lid:
            missing.append(lesson["title"])
        else:
            lms_ids[lesson["externalId"]] = lid
    if missing:
        raise SystemExit(f"{slug}: lessons not found in DB: {missing}")

    assembled = assemble_content(
        slug,
        slot_prefix,
        draft["lessons"],
        lms_ids=lms_ids,
        course_id=course_id,
    )

    statements = [
        f"UPDATE lesson SET public = true, is_unlocked = true, "
        f"completion_policy = 'manual' WHERE course_id = '{course_id}';"
    ]
    for ext, html in assembled.items():
        lid = lms_ids[ext]
        quoted = "$cio$" + html + "$cio$"
        statements.append(
            f"UPDATE lesson_language SET content = {quoted} "
            f"WHERE lesson_id = '{lid}' AND locale = 'en';"
        )
        statements.append(
            f"UPDATE lesson SET note = {quoted}, updated_at = now() "
            f"WHERE id = '{lid}';"
        )
    psql_script("\n".join(statements))
    print(f"Applied {len(assembled)} lessons → {slug} ({course_id})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand lesson HTML and optionally apply to local LMS")
    parser.add_argument("--write", action="store_true", help="Write classroomio-draft.json files")
    parser.add_argument("--apply", action="store_true", help="Update lesson HTML in local Postgres")
    parser.add_argument("--slug", help="Only process this course slug")
    args = parser.parse_args()
    if not args.write and not args.apply:
        args.write = True

    for spec in COURSES:
        if args.slug and spec["slug"] != args.slug:
            continue
        path: Path = spec["draft"]
        slug: str = spec["slug"]
        slot: str = spec["slot"]
        draft = enrich_draft(path, slug, slot)
        if args.write:
            path.write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n")
            print(f"Wrote {path.relative_to(REPO_ROOT)}")
        if args.apply:
            apply_draft(draft, slug, slot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
