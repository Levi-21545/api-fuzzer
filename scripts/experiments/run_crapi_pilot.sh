#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_experiment.sh"
DEDUPLICATOR="${SCRIPT_DIR}/deduplicate_run.py"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

CRAPI_ROOT="${CRAPI_ROOT:-${REPO_ROOT}/../mock-projects/crAPI}"
DEPLOY_DIR="${CRAPI_ROOT}/deploy/docker"
COMPOSE_FILE="${DEPLOY_DIR}/docker-compose.yml"
MINIMAL_FILE="${DEPLOY_DIR}/docker-compose.minimal.yml"
SCHEMA="${CRAPI_ROOT}/openapi-spec/crapi-openapi-spec.json"

CRAPI_SOURCE_VERSION="$(tr -d '[:space:]' <"${CRAPI_ROOT}/VERSION")"
CRAPI_IMAGE_TAG="${CRAPI_IMAGE_TAG:-main}"
COMPOSE_PROJECT="api-fuzzer-crapi-pilot"
BASE_URL="http://127.0.0.1:8888"
RUN_ID="${RUN_ID:-crapi-pilot-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/output/experiments/TCC-PILOT-001/crapi}"
RUN_DIR="${OUTPUT_ROOT}/${RUN_ID}"
BOOTSTRAP_LOG="${OUTPUT_ROOT}/${RUN_ID}-bootstrap.log"

if [[ ! -f "${SCHEMA}" ]]; then
  echo "OpenAPI contract not found: ${SCHEMA}" >&2
  exit 1
fi

if [[ ! -f "${COMPOSE_FILE}" || ! -f "${MINIMAL_FILE}" ]]; then
  echo "crAPI Compose files were not found under: ${DEPLOY_DIR}" >&2
  exit 1
fi

if [[ -e "${RUN_DIR}" ]]; then
  echo "Run already exists; refusing to overwrite: ${RUN_DIR}" >&2
  exit 1
fi

mkdir -p "${OUTPUT_ROOT}"

compose() {
  env \
    VERSION="${CRAPI_IMAGE_TAG}" \
    LISTEN_IP="127.0.0.1" \
    docker compose \
      --env-file /dev/null \
      --project-name "${COMPOSE_PROJECT}" \
      --project-directory "${DEPLOY_DIR}" \
      --file "${COMPOSE_FILE}" \
      --file "${MINIMAL_FILE}" \
      --compatibility \
      "$@"
}

cleanup() {
  if [[ -d "${RUN_DIR}" ]]; then
    compose logs --no-color >"${RUN_DIR}/data/target_stack.log" 2>&1 || true
    compose images --quiet \
      | sort -u \
      | xargs docker image inspect \
        >"${RUN_DIR}/data/target_images.json" 2>/dev/null \
      || true
    if [[ -f "${BOOTSTRAP_LOG}" ]]; then
      mv "${BOOTSTRAP_LOG}" "${RUN_DIR}/data/bootstrap.log"
    fi
  fi
  compose down --volumes --remove-orphans >/dev/null 2>&1 || true
}

docker info >/dev/null 2>&1 || {
  echo "Docker is unavailable. Start OrbStack and try again." >&2
  exit 1
}

for container in \
  crapi-web \
  crapi-identity \
  crapi-community \
  crapi-workshop \
  crapi-chatbot \
  chromadb \
  postgresdb \
  mongodb \
  mailhog
do
  if docker container inspect "${container}" >/dev/null 2>&1; then
    echo "Container already exists; refusing to interfere: ${container}" >&2
    exit 1
  fi
done

trap cleanup EXIT

echo "Starting crAPI source ${CRAPI_SOURCE_VERSION} with image tag ${CRAPI_IMAGE_TAG}"
echo "Target URL: ${BASE_URL}"
compose up --detach --pull missing crapi-chatbot crapi-web >"${BOOTSTRAP_LOG}" 2>&1

ready=0
for _attempt in {1..60}; do
  if curl --fail --silent "${BASE_URL}/health" >/dev/null 2>&1; then
    ready=1
    break
  fi
  web_state="$(docker inspect --format '{{.State.Status}}' crapi-web 2>/dev/null || true)"
  if [[ "${web_state}" == "exited" || "${web_state}" == "dead" ]]; then
    break
  fi
  sleep 5
done

if [[ "${ready}" -ne 1 ]]; then
  echo "crAPI did not become ready. Current stack state:" >&2
  compose ps >&2 || true
  compose logs --no-color --tail 150 >&2 || true
  exit 1
fi

API_FUZZER_TARGET_IMAGE="crAPI source ${CRAPI_SOURCE_VERSION}; images ${CRAPI_IMAGE_TAG}; see target_images.json" \
RUN_ID="${RUN_ID}" \
OUTPUT_ROOT="${OUTPUT_ROOT}" \
"${RUNNER}" \
  "${SCHEMA}" \
  "${BASE_URL}" \
  TCC-PILOT-001 \
  crapi \
  "${RUN_NUMBER:-0}" \
  --all \
  --auto-auth \
  --auth-probe \
  --no-deduplicate

cleanup
trap - EXIT
PYTHONPATH="${REPO_ROOT}/src" "${PYTHON_BIN}" "${DEDUPLICATOR}" "${RUN_DIR}"

echo "crAPI pilot completed: ${RUN_DIR}"
