#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_experiment.sh"
SCHEMA="${MOCK_ROOT:-${REPO_ROOT}/../mock-projects}/VAmPI/openapi_specs/openapi3.yml"

IMAGE="erev0s/vampi@sha256:0a5a224b6e14ae7da6a6ea265178ff71286ff903aec74adee98f660bb0e4ca12"
CONTAINER="api-fuzzer-vampi-pilot"
PORT="${HOST_PORT:-5002}"
RUN_ID="${RUN_ID:-vampi-pilot-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/output/experiments/TCC-PILOT-001/vampi}"
RUN_DIR="${OUTPUT_ROOT}/${RUN_ID}"

if [[ ! -f "${SCHEMA}" ]]; then
  echo "OpenAPI contract not found: ${SCHEMA}" >&2
  exit 1
fi

if [[ -e "${RUN_DIR}" ]]; then
  echo "Run already exists; refusing to overwrite: ${RUN_DIR}" >&2
  exit 1
fi

cleanup() {
  if [[ -d "${RUN_DIR}" ]]; then
    docker logs "${CONTAINER}" >"${RUN_DIR}/target_container.log" 2>&1 || true
  fi
  docker rm -f "${CONTAINER}" >/dev/null 2>&1 || true
}

docker info >/dev/null 2>&1 || {
  echo "Docker is unavailable. Start OrbStack and try again." >&2
  exit 1
}

docker container inspect "${CONTAINER}" >/dev/null 2>&1 && {
  echo "Container already exists: ${CONTAINER}" >&2
  exit 1
}

echo "Starting VAmPI at http://127.0.0.1:${PORT}"
docker run -d \
  --name "${CONTAINER}" \
  --env vulnerable=1 \
  --publish "127.0.0.1:${PORT}:5000" \
  "${IMAGE}" >/dev/null

trap cleanup EXIT

ready=0
for _attempt in {1..30}; do
  if curl --fail --silent "http://127.0.0.1:${PORT}/" >/dev/null 2>&1; then
    ready=1
    break
  fi
  if [[ "$(docker inspect --format '{{.State.Running}}' "${CONTAINER}" 2>/dev/null)" != "true" ]]; then
    break
  fi
  sleep 2
done

if [[ "${ready}" -ne 1 ]]; then
  echo "VAmPI did not become ready. Recent logs:" >&2
  docker logs --tail 100 "${CONTAINER}" >&2 || true
  exit 1
fi

if ! curl --fail --silent "http://127.0.0.1:${PORT}/createdb" >/dev/null; then
  echo "VAmPI database initialization failed. Recent logs:" >&2
  docker logs --tail 100 "${CONTAINER}" >&2 || true
  exit 1
fi

API_FUZZER_TARGET_IMAGE="${IMAGE}" \
RUN_ID="${RUN_ID}" \
OUTPUT_ROOT="${OUTPUT_ROOT}" \
"${RUNNER}" \
  "${SCHEMA}" \
  "http://127.0.0.1:${PORT}" \
  TCC-PILOT-001 \
  vampi \
  "${RUN_NUMBER:-0}" \
  --all \
  --exclude-path /createdb \
  --auto-auth

echo "Pilot completed: ${RUN_DIR}"
