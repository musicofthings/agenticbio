#!/usr/bin/env python3
"""Load cohort 1 into local ClassroomIO via the public API.

Creates (or reuses) an org API key in Postgres, then:

  POST /public-api/v1/courses
  PUT  /public-api/v1/courses/{id}/structure
  PUT  /public-api/v1/courses/{id}   (publish + landing copy)

Idempotent: if a course with the draft title already exists, landing
fields are updated and lesson HTML is applied in place. Structure PUT
runs only when the course has no lessons yet — re-merge with a new
idempotency key would duplicate lessons (ClassroomIO matches on UUID,
not draft externalId).

Usage (from repo root or deploy/):

  python3 deploy/scripts/seed_cohort1.py
  python3 deploy/scripts/seed_cohort1.py --draft courses/02-biopharma-data-scientists/classroomio-draft.json \\
    --slug agentic-bio-fellowship-biopharma-ds
  python3 deploy/scripts/seed_cohort1.py --draft courses/03-clinical-healthcare/classroomio-draft.json \\
    --slug agentic-bio-fellowship-clinical
  python3 deploy/scripts/seed_cohort1.py --draft courses/04-rnd-institute-data-scientists/classroomio-draft.json \\
    --slug agentic-bio-fellowship-rnd-rag
  python3 deploy/scripts/seed_cohort1.py --draft courses/05-academic-scientists/classroomio-draft.json \\
    --slug agentic-bio-fellowship-academic-grants
"""

import argparse
import hashlib
import json
import os
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEPLOY_DIR = REPO_ROOT / "deploy"
ENV_PATH = DEPLOY_DIR / ".env"
DRAFT_PATH = (
    REPO_ROOT / "courses" / "01-bioinformatics-leaders" / "classroomio-draft.json"
)
API_BASE = os.environ.get("CLASSROOMIO_API_URL", "http://localhost:3081")
ORG_ID = "ef37c25c-3cba-45e9-ab5f-300713b1c566"
PROFILE_ID = "712b29e2-02f1-4dc1-bc53-9481656786ea"
ENV_KEY_NAME = "CLASSROOMIO_API_KEY"
COURSE_SLUG = "agentic-bio-fellowship-bioinformatics"


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


def append_dotenv(path: Path, key: str, value: str) -> None:
    existing = path.read_text() if path.exists() else ""
    if not existing.endswith("\n"):
        existing += "\n"
    path.write_text(
        existing + f"\n# Local ClassroomIO public API key (do not commit)\n{key}={value}\n"
    )


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


def ensure_api_key(env: dict[str, str]) -> str:
    secret = os.environ.get(ENV_KEY_NAME) or env.get(ENV_KEY_NAME, "")
    if secret:
        return secret

    secret = "cio_api_" + secrets.token_urlsafe(24)
    digest = hashlib.sha256(secret.encode()).hexdigest()
    prefix = secret[:16]
    sql = (
        "INSERT INTO organization_api_key "
        "(organization_id, created_by_profile_id, type, label, "
        "secret_prefix, secret_hash, scopes) VALUES ("
        f"'{ORG_ID}', '{PROFILE_ID}', 'api', 'Local cohort seed', "
        f"'{prefix}', '{digest}', '[\"public_api:*\"]'::jsonb"
        ");"
    )
    psql(sql)
    append_dotenv(ENV_PATH, ENV_KEY_NAME, secret)
    print(f"Created org API key and wrote {ENV_KEY_NAME} to deploy/.env")
    return secret


def api(method: str, path: str, token: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"error": raw}
        return exc.code, parsed


def find_course_id(title: str) -> str | None:
    escaped = title.replace("'", "''")
    row = psql(f"SELECT id FROM course WHERE title = '{escaped}' LIMIT 1;")
    return row or None


def lesson_count(course_id: str) -> int:
    row = psql(f"SELECT count(*) FROM lesson WHERE course_id = '{course_id}';")
    return int(row or 0)


def payload_keys(payload: object) -> str:
    if not isinstance(payload, dict):
        return type(payload).__name__
    data = payload.get("data")
    extra = ""
    if isinstance(data, dict):
        extra = f" data.keys={sorted(data)}"
    return f"keys={sorted(payload)}{extra}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Load a Fellowship draft into ClassroomIO")
    parser.add_argument("--draft", type=Path, default=DRAFT_PATH)
    parser.add_argument("--slug", default=COURSE_SLUG)
    args = parser.parse_args()
    draft_path = args.draft if args.draft.is_absolute() else REPO_ROOT / args.draft
    course_slug = args.slug

    if not draft_path.is_file():
        print(f"Missing draft: {draft_path}", file=sys.stderr)
        return 1

    draft = json.loads(draft_path.read_text())
    title = draft["course"]["title"]
    description = draft["course"]["description"]
    course_type = draft["course"]["type"]
    metadata = draft["course"].get("metadata") or {}

    env = load_dotenv(ENV_PATH)
    token = ensure_api_key(env)

    existing_id = find_course_id(title)
    if existing_id:
        course_id = existing_id
        print(f"Reusing course {course_id}")
    else:
        status, payload = api(
            "POST",
            "/public-api/v1/courses",
            token,
            {
                "title": title,
                "description": description,
                "type": course_type,
            },
        )
        if status not in (200, 201):
            print(
                f"Create course failed ({status}): {payload_keys(payload)} {payload}",
                file=sys.stderr,
            )
            return 1
        course_id = find_course_id(title)
        if not course_id:
            print(f"Course created but id not found ({payload_keys(payload)})", file=sys.stderr)
            return 1
        print(f"Created course {course_id}")

    if lesson_count(course_id) > 0:
        print("Course already has lessons; skipping structure PUT (would duplicate).")
        print("Apply lesson HTML with: python3 deploy/scripts/enrich_lesson_content.py --apply")
    else:
        status, payload = api(
            "PUT",
            f"/public-api/v1/courses/{course_id}/structure",
            token,
            {
                "mode": "merge",
                "idempotencyKey": f"seed-{course_slug}-v1",
                "summary": {
                    "source": str(draft_path.relative_to(REPO_ROOT)),
                    "slug": course_slug,
                },
                "draft": draft,
            },
        )
        if status != 200:
            err = payload.get("error") if isinstance(payload, dict) else payload
            print(f"Update structure failed ({status}): {err}", file=sys.stderr)
            return 1
        print("Synced sections, lessons, and exercises")

    status, payload = api(
        "PUT",
        f"/public-api/v1/courses/{course_id}",
        token,
        {
            "title": title,
            "description": description,
            "type": course_type,
            "slug": course_slug,
            "overview": metadata.get("description") or description,
            "metadata": metadata,
            "isPublished": True,
            "cost": 0,
            "currency": "USD",
        },
    )
    if status != 200:
        err = payload.get("error") if isinstance(payload, dict) else payload
        print(f"Publish/landing update failed ({status}): {err}", file=sys.stderr)
        return 1
    print(f"Published: http://localhost:3082/courses/{course_id}")

    enrich = REPO_ROOT / "deploy/scripts/enrich_lesson_content.py"
    if enrich.is_file():
        print("Applying lesson HTML, YouTube placeholders, and prev/next…")
        subprocess.run(
            [sys.executable, str(enrich), "--apply", "--slug", course_slug],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
