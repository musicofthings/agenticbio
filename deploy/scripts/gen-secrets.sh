#!/usr/bin/env bash
# Fill empty BETTER_AUTH_SECRET and PRIVATE_SERVER_KEY in deploy/.env.
# Existing non-empty values are never overwritten.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}"
  echo "Run: cp .env.example .env"
  exit 1
fi

upsert_if_empty() {
  local key="$1"
  local value="$2"
  local current
  current="$(grep -E "^${key}=" "${ENV_FILE}" | tail -n1 | cut -d= -f2- || true)"

  if [[ -n "${current}" ]]; then
    echo "Keeping existing ${key}"
    return
  fi

  if grep -qE "^${key}=" "${ENV_FILE}"; then
    if [[ "$(uname)" == "Darwin" ]]; then
      sed -i '' "s|^${key}=.*|${key}=${value}|" "${ENV_FILE}"
    else
      sed -i "s|^${key}=.*|${key}=${value}|" "${ENV_FILE}"
    fi
  else
    printf '\n%s=%s\n' "${key}" "${value}" >> "${ENV_FILE}"
  fi
  echo "Wrote ${key}"
}

upsert_if_empty BETTER_AUTH_SECRET "$(openssl rand -hex 32)"
upsert_if_empty PRIVATE_SERVER_KEY "$(openssl rand -hex 32)"

echo "Secrets ready in ${ENV_FILE}"
echo "Do not commit .env"
