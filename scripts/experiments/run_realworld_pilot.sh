#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_experiment.sh"
DEDUPLICATOR="${SCRIPT_DIR}/deduplicate_run.py"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

MOCK_ROOT="${MOCK_ROOT:-${REPO_ROOT}/../mock-projects}"
SPEC_ROOT="${REALWORLD_SPEC_ROOT:-${MOCK_ROOT}/realworld}"
BACKEND_ROOT="${REALWORLD_BACKEND_ROOT:-${MOCK_ROOT}/realworld-django-ninja}"
SPEC_ROOT="$(cd -- "${SPEC_ROOT}" && pwd)"
BACKEND_ROOT="$(cd -- "${BACKEND_ROOT}" && pwd)"
SCHEMA="${SPEC_ROOT}/specs/api/openapi.yml"
COMPOSE_FILE="${BACKEND_ROOT}/docker-compose.yml"

PORT="${HOST_PORT:-18080}"
BASE_URL="http://127.0.0.1:${PORT}/api"
RUN_ID="${RUN_ID:-realworld-pilot-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/output/experiments/TCC-PILOT-001/realworld}"
RUN_DIR="${OUTPUT_ROOT}/${RUN_ID}"
PROJECT_SUFFIX="$(printf '%s' "${RUN_ID}" | tr '[:upper:]_' '[:lower:]-' | tr -cd 'a-z0-9-')"
COMPOSE_PROJECT="${COMPOSE_PROJECT:-api-fuzzer-realworld-${PROJECT_SUFFIX}}"

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/api-fuzzer-realworld.XXXXXX")"
OVERRIDE_FILE="${TEMP_DIR}/compose.override.yml"
BOOTSTRAP_LOG="${TEMP_DIR}/bootstrap.log"
AUTH_CONFIG="${TEMP_DIR}/auth.yml"
AUTH_RESULT="${TEMP_DIR}/authentication.json"
LOGIN_RESPONSE="${TEMP_DIR}/login.json"
PHASE="environment_check"

for required in "${SCHEMA}" "${COMPOSE_FILE}" "${RUNNER}" "${DEDUPLICATOR}"; do
  if [[ ! -f "${required}" ]]; then
    echo "Required file not found: ${required}" >&2
    exit 1
  fi
done

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Python environment not found: ${PYTHON_BIN}" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Required command not found: jq" >&2
  exit 1
fi

if [[ -e "${RUN_DIR}" ]]; then
  echo "Run already exists; refusing to overwrite: ${RUN_DIR}" >&2
  exit 1
fi

SPEC_COMMIT="$(git -C "${SPEC_ROOT}" rev-parse HEAD)"
BACKEND_COMMIT="$(git -C "${BACKEND_ROOT}" rev-parse HEAD)"

# Remove the target's fixed port and source bind mount. The image is built from
# the target checkout, but the running container cannot write back into it.
cat >"${OVERRIDE_FILE}" <<EOF
services:
  realword-app:
    ports: !override
      - "127.0.0.1:${PORT}:8000"
    volumes: !override []
EOF

compose() {
  docker compose \
    --project-name "${COMPOSE_PROJECT}" \
    --project-directory "${BACKEND_ROOT}" \
    --file "${COMPOSE_FILE}" \
    --file "${OVERRIDE_FILE}" \
    "$@"
}

cleanup() {
  if [[ -d "${RUN_DIR}" ]]; then
    compose logs --no-color >"${RUN_DIR}/data/target_stack.log" 2>&1 || true
    cp "${BOOTSTRAP_LOG}" "${RUN_DIR}/data/bootstrap.log" 2>/dev/null || true
    cp "${AUTH_RESULT}" "${RUN_DIR}/data/authentication.json" 2>/dev/null || true
  fi
  compose down --volumes --remove-orphans >/dev/null 2>&1 || true
}

on_exit() {
  local exit_code="$1"
  set +e
  if [[ "${exit_code}" -ne 0 ]]; then
    echo "RealWorld pilot failed during ${PHASE} (exit ${exit_code})." >&2
    compose ps >&2 || true
    compose logs --no-color --tail 150 >&2 || true
  fi
  cleanup
  rm -rf "${TEMP_DIR}"
}
trap 'on_exit $?' EXIT

docker info >/dev/null 2>&1 || {
  echo "Docker is unavailable. Start OrbStack and try again." >&2
  exit 1
}
docker compose version >/dev/null
compose config >/dev/null

PHASE="database_start"
echo "Starting isolated PostgreSQL"
compose down --volumes --remove-orphans >/dev/null 2>&1 || true
compose up --detach db >"${BOOTSTRAP_LOG}" 2>&1

db_ready=0
for _attempt in {1..60}; do
  if compose exec --no-TTY db pg_isready -U postgres >/dev/null 2>&1; then
    db_ready=1
    break
  fi
  db_state="$(compose ps --all --format json db 2>/dev/null || true)"
  if [[ "${db_state}" == *'"State":"exited"'* || "${db_state}" == *'"State":"dead"'* ]]; then
    break
  fi
  sleep 2
done

if [[ "${db_ready}" -ne 1 ]]; then
  echo "PostgreSQL did not become ready." >&2
  exit 1
fi

PHASE="application_start"
echo "Building and starting RealWorld at ${BASE_URL}"
compose up --detach --build realword-app >>"${BOOTSTRAP_LOG}" 2>&1

ready=0
for _attempt in {1..90}; do
  if curl --fail --silent "${BASE_URL}/tags" >/dev/null 2>&1; then
    ready=1
    break
  fi
  app_state="$(compose ps --all --format json realword-app 2>/dev/null || true)"
  if [[ "${app_state}" == *'"State":"exited"'* || "${app_state}" == *'"State":"dead"'* ]]; then
    break
  fi
  sleep 2
done

if [[ "${ready}" -ne 1 ]]; then
  echo "RealWorld did not become ready." >&2
  exit 1
fi

PHASE="authentication"
AUTH_SUFFIX="$(date -u +%Y%m%d%H%M%S)-$$"
AUTH_USERNAME="fuzzer-${AUTH_SUFFIX}"
AUTH_EMAIL="${AUTH_USERNAME}@test.com"
AUTH_PASSWORD="RealworldPilot123!"

register_status="$(curl --silent --show-error --output /dev/null \
  --write-out '%{http_code}' \
  --header 'Content-Type: application/json' \
  --data "{\"user\":{\"username\":\"${AUTH_USERNAME}\",\"email\":\"${AUTH_EMAIL}\",\"password\":\"${AUTH_PASSWORD}\"}}" \
  "${BASE_URL}/users")"
if [[ "${register_status}" != "201" ]]; then
  echo "Registration failed with HTTP ${register_status}." >&2
  exit 1
fi

login_status="$(curl --silent --show-error --output "${LOGIN_RESPONSE}" \
  --write-out '%{http_code}' \
  --header 'Content-Type: application/json' \
  --data "{\"user\":{\"email\":\"${AUTH_EMAIL}\",\"password\":\"${AUTH_PASSWORD}\"}}" \
  "${BASE_URL}/users/login")"
if [[ "${login_status}" != "200" ]]; then
  echo "Login failed with HTTP ${login_status}." >&2
  exit 1
fi

JWT_TOKEN="$(jq --exit-status --raw-output \
  '.user.token | select(type == "string" and (split(".") | length == 3))' \
  "${LOGIN_RESPONSE}")" || {
  echo "Login response did not contain a JWT-shaped user.token." >&2
  exit 1
}

current_user_status="$(curl --silent --show-error --output /dev/null \
  --write-out '%{http_code}' \
  --header "Authorization: Token ${JWT_TOKEN}" \
  "${BASE_URL}/user")"
if [[ "${current_user_status}" != "200" ]]; then
  echo "Token authentication failed with HTTP ${current_user_status}." >&2
  exit 1
fi

cat >"${AUTH_RESULT}" <<EOF
{
  "registration_status": ${register_status},
  "login_status": ${login_status},
  "authenticated_request_status": ${current_user_status},
  "authorization_header": "Token <REDACTED>"
}
EOF
cat >"${AUTH_CONFIG}" <<EOF
auth:
  enabled: true
  inject:
    headers:
      Authorization: "Token ${JWT_TOKEN}"
EOF

PHASE="fuzzer_campaign"
API_FUZZER_TARGET_IMAGE="RealWorld backend ${BACKEND_COMMIT}; canonical contract ${SPEC_COMMIT}" \
RUN_ID="${RUN_ID}" \
OUTPUT_ROOT="${OUTPUT_ROOT}" \
"${RUNNER}" \
  "${SCHEMA}" \
  "${BASE_URL}" \
  TCC-PILOT-001 \
  realworld \
  "${RUN_NUMBER:-0}" \
  --all \
  --auth "${AUTH_CONFIG}" \
  --auth-probe \
  --no-deduplicate

PHASE="cleanup"
cleanup
trap - EXIT
rm -rf "${TEMP_DIR}"

PHASE="deduplication"
PYTHONPATH="${REPO_ROOT}/src" "${PYTHON_BIN}" "${DEDUPLICATOR}" "${RUN_DIR}"

echo "RealWorld pilot completed: ${RUN_DIR}"
