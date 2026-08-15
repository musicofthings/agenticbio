# Lab 02 — Dockerized Python + R

**Module:** 2  
**Timebox:** 2 hours async  
**Data:** none beyond the image itself.

## Objective

Build one image that can run a tiny Python summary and a tiny R summary on the same bind-mounted `data/` directory. Pin versions. Do not install Bioconductor packages on the host.

## Constraints

- Analysis code runs **in the container**, not on the host Python/R.
- No network calls from the analysis scripts (image build may use a package mirror).
- Do not add unpublished or licensed clinical datasets to `data/`.

## What to run

```bash
docker build -t agenticbio-lab02:local .
docker run --rm -v "$PWD/data:/data" -v "$PWD/outputs:/outputs" agenticbio-lab02:local python /opt/lab/summarize.py
docker run --rm -v "$PWD/data:/data" -v "$PWD/outputs:/outputs" agenticbio-lab02:local Rscript /opt/lab/summarize.R
```

## Acceptance criteria

- [ ] Image builds on your machine (amd64 or arm64)
- [ ] `outputs/python_summary.txt` and `outputs/r_summary.txt` exist
- [ ] Host `python3` / `R` are not required to produce those files
- [ ] `Dockerfile` pins a digest or a major tag you could defend in an audit

## ClassroomIO

Attach this folder (zip) to Module 2. Assignment: paste the `docker build` image id and both output files.
