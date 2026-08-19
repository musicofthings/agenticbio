#!/usr/bin/env python3
"""Invite a test fellow to a Fellowship course and wait for Mailpit.

Usage:

  python3 deploy/scripts/invite_fellow.py
  python3 deploy/scripts/invite_fellow.py --email fellow@agenticbio.local
  python3 deploy/scripts/invite_fellow.py --slug agentic-bio-fellowship-biopharma-ds
  python3 deploy/scripts/invite_fellow.py --title 'The Agentic Bio Fellowship: Offline Multiomic Analysis for Biopharma Data Science'
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / "deploy" / ".env"
API_BASE = os.environ.get("CLASSROOMIO_API_URL", "http://localhost:3081")
MAILPIT = os.environ.get("MAILPIT_URL", "http://localhost:8025")
DEFAULT_SLUG = "agentic-bio-fellowship-bioinformatics"
DEFAULT_EMAIL = "fellow@agenticbio.local"

KNOWN_SLUGS = (
    "agentic-bio-fellowship-bioinformatics",
    "agentic-bio-fellowship-biopharma-ds",
    "agentic-bio-fellowship-clinical",
    "agentic-bio-fellowship-rnd-rag",
    "agentic-bio-fellowship-academic-grants",
)


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def http_json(method: str, url: str, headers: dict[str, str], body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"error": raw[:500]}
        return exc.code, parsed


def mailpit_messages() -> list[dict]:
    status, payload = http_json("GET", f"{MAILPIT}/api/v1/messages", {"Accept": "application/json"})
    if status != 200:
        raise SystemExit(f"Mailpit API failed ({status}). Is http://localhost:8025 up?")
    return payload.get("messages") or []


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


def find_course_id(slug: str, title: str) -> str:
    if title:
        escaped = title.replace("'", "''")
        course_id = psql(f"SELECT id FROM course WHERE title = '{escaped}' LIMIT 1;")
        if not course_id:
            raise SystemExit(f"Course not found by title: {title}")
        return course_id
    escaped = slug.replace("'", "''")
    course_id = psql(f"SELECT id FROM course WHERE slug = '{escaped}' LIMIT 1;")
    if not course_id:
        known = ", ".join(KNOWN_SLUGS)
        raise SystemExit(f"Course not found by slug: {slug}. Known slugs: {known}")
    return course_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Invite a test fellow via ClassroomIO public API")
    parser.add_argument("--email", default=DEFAULT_EMAIL)
    parser.add_argument("--slug", default=DEFAULT_SLUG, help="Course slug (default: cohort 1)")
    parser.add_argument("--title", default="", help="Look up by exact course title instead of slug")
    parser.add_argument(
        "--skip-mailpit",
        action="store_true",
        help="Do not wait for captured mail (use when Mailpit is not running)",
    )
    args = parser.parse_args()
    email = args.email.strip().lower()

    env = load_dotenv(ENV_PATH)
    token = os.environ.get("CLASSROOMIO_API_KEY") or env.get("CLASSROOMIO_API_KEY", "")
    if not token:
        print("CLASSROOMIO_API_KEY missing. Run deploy/scripts/seed_cohort1.py first.", file=sys.stderr)
        return 1

    course_id = find_course_id(args.slug.strip(), args.title.strip())
    before: set[str] = set()
    if not args.skip_mailpit:
        before = {msg.get("ID") for msg in mailpit_messages() if msg.get("ID")}

    status, payload = http_json(
        "POST",
        f"{API_BASE}/public-api/v1/audience",
        {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        {"email": email, "courseIds": [course_id], "sendEmail": True},
    )
    if status not in (200, 201):
        print(f"Invite failed ({status}): {payload.get('error', payload)}", file=sys.stderr)
        return 1
    print(f"Invited {email} to course {course_id}")

    if args.skip_mailpit:
        print("Skipped Mailpit wait (--skip-mailpit).")
        return 0

    deadline = time.time() + 25
    while time.time() < deadline:
        for msg in mailpit_messages():
            if msg.get("ID") in before:
                continue
            to_addrs = " ".join(
                (item.get("Address") or "") for item in (msg.get("To") or [])
            ).lower()
            if email in to_addrs:
                subject = msg.get("Subject") or "(no subject)"
                print(f"Mailpit captured invite: {subject}")
                print(f"Open {MAILPIT} to read the message.")
                return 0
        time.sleep(1)

    print("Invite API succeeded but no new Mailpit message yet.", file=sys.stderr)
    print("Check docker compose logs jobs, then open http://localhost:8025", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
