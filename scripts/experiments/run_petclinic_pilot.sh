#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_experiment.sh"
DEDUPLICATOR="${SCRIPT_DIR}/deduplicate_run.py"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

PETCLINIC_ROOT="${PETCLINIC_ROOT:-${REPO_ROOT}/../mock-projects/spring-petclinic-rest}"
SCHEMA="${PETCLINIC_ROOT}/src/main/resources/openapi.yml"
IMAGE="springcommunity/spring-petclinic-rest:4.0.2"
CONTAINER="api-fuzzer-petclinic-pilot"
PORT="${HOST_PORT:-9966}"
BASE_URL="http://127.0.0.1:${PORT}/petclinic/api"
HEALTH_URL="http://127.0.0.1:${PORT}/petclinic/actuator/health"
RUN_ID="${RUN_ID:-petclinic-pilot-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/output/experiments/TCC-PILOT-001/petclinic}"
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
    docker logs "${CONTAINER}" >"${RUN_DIR}/data/target_container.log" 2>&1 \
      || true
    image_id="$(docker inspect --format '{{.Image}}' "${CONTAINER}" 2>/dev/null || true)"
    if [[ -n "${image_id}" ]]; then
      docker image inspect "${image_id}" \
        >"${RUN_DIR}/data/target_image.json" 2>/dev/null || true
    fi
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

trap cleanup EXIT

echo "Starting Spring Petclinic REST 4.0.2 at ${BASE_URL}"
docker run --detach \
  --name "${CONTAINER}" \
  --publish "127.0.0.1:${PORT}:9966" \
  "${IMAGE}" >/dev/null

ready=0
for _attempt in {1..60}; do
  if curl --fail --silent "${HEALTH_URL}" >/dev/null 2>&1; then
    ready=1
    break
  fi
  container_state="$(
    docker inspect --format '{{.State.Status}}' "${CONTAINER}" 2>/dev/null || true
  )"
  if [[ "${container_state}" == "exited" || "${container_state}" == "dead" ]]; then
    break
  fi
  sleep 5
done

if [[ "${ready}" -ne 1 ]]; then
  echo "Spring Petclinic did not become ready. Recent logs:" >&2
  docker logs --tail 150 "${CONTAINER}" >&2 || true
  exit 1
fi

API_FUZZER_TARGET_IMAGE="${IMAGE}; see target_image.json" \
RUN_ID="${RUN_ID}" \
OUTPUT_ROOT="${OUTPUT_ROOT}" \
"${RUNNER}" \
  "${SCHEMA}" \
  "${BASE_URL}" \
  TCC-PILOT-001 \
  petclinic \
  "${RUN_NUMBER:-0}" \
  --all \
  --exclude-path /oops \
  --no-deduplicate

cleanup
trap - EXIT
PYTHONPATH="${REPO_ROOT}/src" "${PYTHON_BIN}" "${DEDUPLICATOR}" "${RUN_DIR}"

echo "Spring Petclinic pilot completed: ${RUN_DIR}"
