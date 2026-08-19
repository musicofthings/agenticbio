#!/usr/bin/env bash
# Start the production stack without docker-compose.override.yml.
# That local overlay publishes Postgres/Redis/MinIO/API ports and Mailpit.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

ENV_FILE="${ROOT}/.env.production"
if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}"
  echo "Run: cp .env.production.example .env.production"
  echo "Then fill secrets, SMTP, and CLOUDFLARE_TUNNEL_TOKEN (./scripts/gen-secrets.sh .env.production)."
  exit 1
fi

if [[ -f "${ROOT}/docker-compose.override.yml" ]]; then
  echo "Note: docker-compose.override.yml is present but will not be merged."
  echo "This script uses an explicit -f list so host ports and Mailpit stay off."
fi

exec docker compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  --env-file "${ENV_FILE}" \
  up -d "$@"
