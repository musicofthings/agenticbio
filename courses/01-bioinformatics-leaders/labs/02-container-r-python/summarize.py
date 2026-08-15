#!/usr/bin/env python3
from pathlib import Path

data = Path("/data")
out = Path("/outputs")
out.mkdir(parents=True, exist_ok=True)
files = sorted(p.name for p in data.iterdir() if p.is_file())
(out / "python_summary.txt").write_text(
    "python files=" + ",".join(files) + f" count={len(files)}\n"
)
