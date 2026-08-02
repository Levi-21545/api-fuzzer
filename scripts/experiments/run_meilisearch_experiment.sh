#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
RUNNER="${SCRIPT_DIR}/run_experiment.sh"
DEDUPLICATOR="${SCRIPT_DIR}/deduplicate_run.py"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

IMAGE="getmeili/meilisearch@sha256:ac40212f9e5a7526d8007586e3e46fb0441d29dd36c7b02fa2341d2c9a1f6493"
IMAGE_VERSION="v1.45.1"
CONTRACT_URL="https://github.com/meilisearch/meilisearch/releases/download/v1.45.1/meilisearch-openapi.json"
CONTRACT_SHA256="f4eaf26d91dfea9acde4eb113c0df796865bb6ee67cb5f3fb0e4148ea2f5b2cc"
CONTAINER="api-fuzzer-meilisearch-experiment"
PORT="${HOST_PORT:-19093}"
BASE_URL="http://127.0.0.1:${PORT}"
MASTER_KEY="api-fuzzer-meilisearch-local-key"
EXPERIMENT_ID="${EXPERIMENT_ID:-TCC-CONFIRMATORY-001}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/output/experiments/${EXPERIMENT_ID}/meilisearch}"
REPETITIONS="${REPETITIONS:-5}"

TEMP_DIR="$(mktemp -d /tmp/api-fuzzer-meilisearch.XXXXXX)"
CONTRACT="${TEMP_DIR}/meilisearch-openapi.json"
AUTH_CONFIG="${TEMP_DIR}/auth.yaml"
CURRENT_RUN_DIR=""

# Paths are excluded at the same granularity supported by the fuzzer CLI.
# Reasons are structural: unsupported input encoding, unresolved resources,
# external integrations, or mutation of the deterministic seed itself.
EXCLUDED_PATHS=(
  '/batches'
  '/chats'
  '/chats/{workspace_uid}'
  '/chats/{workspace_uid}/chat/completions'
  '/chats/{workspace_uid}/settings'
  '/dynamic-search-rules/{uid}'
  '/indexes/{index_uid}'
  '/indexes/{index_uid}/documents'
  '/indexes/{index_uid}/documents/{document_id}'
  '/indexes/{index_uid}/search'
  '/indexes/{index_uid}/settings/distinct-attribute'
  '/indexes/{index_uid}/settings/facet-search'
  '/indexes/{index_uid}/settings/search-cutoff-ms'
  '/indexes/{index_uid}/similar'
  '/indexes/{index_uid}/stats'
  '/keys/{key}'
  '/logs/stderr'
  '/logs/stream'
  '/network'
  '/network/control'
  '/stats'
  '/tasks'
  '/tasks/cancel'
  '/tasks/{task_id}/documents'
  '/webhooks'
  '/webhooks/{uuid}'
)

stop_target() {
  docker rm --force "${CONTAINER}" >/dev/null 2>&1 || true
}

collect_target_artifacts() {
  if [[ -z "${CURRENT_RUN_DIR}" || ! -d "${CURRENT_RUN_DIR}" ]]; then
    return
  fi
  mkdir -p "${CURRENT_RUN_DIR}/data"
  docker logs "${CONTAINER}" >"${CURRENT_RUN_DIR}/data/target_container.log" 2>&1 || true
  docker image inspect "${IMAGE}" >"${CURRENT_RUN_DIR}/data/target_image.json" 2>/dev/null || true
  cp "${CONTRACT}" "${CURRENT_RUN_DIR}/data/target_contract.json"
}

cleanup() {
  local exit_code=$?
  set +e
  collect_target_artifacts
  stop_target
  rm -rf -- "${TEMP_DIR}"
  exit "${exit_code}"
}
trap cleanup EXIT

wait_ready() {
  local ready=0
  for _attempt in {1..30}; do
    if curl --fail --silent "${BASE_URL}/health" >/dev/null 2>&1; then
      ready=1
      break
    fi
    if [[ "$(docker inspect --format '{{.State.Running}}' "${CONTAINER}" 2>/dev/null)" != "true" ]]; then
      break
    fi
    sleep 1
  done
  if [[ "${ready}" -ne 1 ]]; then
    docker logs --tail 100 "${CONTAINER}" >&2 || true
    return 1
  fi
}

wait_task() {
  local task_uid="$1"
  local task_state=""
  local task_file="${TEMP_DIR}/task-${task_uid}.json"
  for _attempt in {1..30}; do
    curl --fail --silent \
      --header "Authorization: Bearer ${MASTER_KEY}" \
      "${BASE_URL}/tasks/${task_uid}" >"${task_file}"
    task_state="$(jq -r '.status' "${task_file}")"
    if [[ "${task_state}" == "succeeded" ]]; then
      return 0
    fi
    if [[ "${task_state}" == "failed" || "${task_state}" == "canceled" ]]; then
      jq . "${task_file}" >&2
      return 1
    fi
    sleep 1
  done
  echo "Task ${task_uid} did not finish in time" >&2
  return 1
}

start_and_seed_target() {
  local task_uid
  docker run --detach \
    --name "${CONTAINER}" \
    --env "MEILI_MASTER_KEY=${MASTER_KEY}" \
    --env MEILI_ENV=development \
    --env MEILI_NO_ANALYTICS=true \
    --publish "127.0.0.1:${PORT}:7700" \
    "${IMAGE}" >/dev/null
  wait_ready

  curl --fail --silent \
    --request POST \
    --header "Authorization: Bearer ${MASTER_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{"uid":"A","primaryKey":"id"}' \
    "${BASE_URL}/indexes" >"${TEMP_DIR}/seed-index.json"
  task_uid="$(jq -er '.taskUid' "${TEMP_DIR}/seed-index.json")"
  wait_task "${task_uid}"

  curl --fail --silent \
    --request POST \
    --header "Authorization: Bearer ${MASTER_KEY}" \
    --header 'Content-Type: application/json' \
    --data '[{"id":"A","title":"A"}]' \
    "${BASE_URL}/indexes/A/documents" >"${TEMP_DIR}/seed-documents.json"
  task_uid="$(jq -er '.taskUid' "${TEMP_DIR}/seed-documents.json")"
  wait_task "${task_uid}"

  for fixture_path in /indexes/A /indexes/A/documents/A /tasks/0 /batches/0; do
    curl --fail --silent \
      --header "Authorization: Bearer ${MASTER_KEY}" \
      "${BASE_URL}${fixture_path}" >/dev/null
  done
}

append_target_artifacts_to_manifest() {
  local manifest="${CURRENT_RUN_DIR}/run_manifest.json"
  local updated="${CURRENT_RUN_DIR}/run_manifest.updated.json"
  jq '
    .artifacts += [
      "data/target_container.log",
      "data/target_contract.json",
      "data/target_image.json"
    ]
    | .artifacts |= unique
  ' "${manifest}" >"${updated}"
  mv "${updated}" "${manifest}"
}

for command in curl docker jq shasum; do
  if ! command -v "${command}" >/dev/null 2>&1; then
    echo "Required command not found: ${command}" >&2
    exit 1
  fi
done
[[ -x "${PYTHON_BIN}" ]] || {
  echo "Python environment not found: ${PYTHON_BIN}" >&2
  exit 1
}
[[ "${REPETITIONS}" =~ ^[1-9][0-9]*$ ]] || {
  echo "REPETITIONS must be a positive integer" >&2
  exit 1
}
if docker container inspect "${CONTAINER}" >/dev/null 2>&1; then
  echo "Container already exists; refusing to interfere: ${CONTAINER}" >&2
  exit 1
fi

curl --fail --silent --show-error --location "${CONTRACT_URL}" --output "${CONTRACT}"
actual_contract_sha256="$(shasum -a 256 "${CONTRACT}" | awk '{print $1}')"
if [[ "${actual_contract_sha256}" != "${CONTRACT_SHA256}" ]]; then
  echo "Unexpected OpenAPI SHA-256: ${actual_contract_sha256}" >&2
  exit 1
fi

printf 'auth:\n  enabled: true\n  inject:\n    headers:\n      Authorization: "Bearer %s"\n' \
  "${MASTER_KEY}" >"${AUTH_CONFIG}"
chmod 600 "${AUTH_CONFIG}"

FUZZER_ARGS=(--all --auth "${AUTH_CONFIG}" --auth-probe --no-deduplicate)
for excluded_path in "${EXCLUDED_PATHS[@]}"; do
  FUZZER_ARGS+=(--exclude-path "${excluded_path}")
done

mkdir -p "${OUTPUT_ROOT}"
for ((run_number = 1; run_number <= REPETITIONS; run_number++)); do
  run_id="meilisearch-r${run_number}-$(date -u +%Y%m%dT%H%M%SZ)"
  CURRENT_RUN_DIR="${OUTPUT_ROOT}/${run_id}"
  echo "Starting repetition ${run_number}/${REPETITIONS}: ${run_id}"

  start_and_seed_target
  API_FUZZER_TARGET_IMAGE="Meilisearch ${IMAGE_VERSION} ${IMAGE}" \
  LEVEL=2 \
  MAX_MUTATIONS=20 \
  MAX_PAIRS=10 \
  CONCURRENCY=1 \
  DELAY_MS=250 \
  TIMEOUT_SECONDS=10 \
  RUN_ID="${run_id}" \
  OUTPUT_ROOT="${OUTPUT_ROOT}" \
  "${RUNNER}" \
    "${CONTRACT}" \
    "${BASE_URL}" \
    "${EXPERIMENT_ID}" \
    meilisearch \
    "${run_number}" \
    "${FUZZER_ARGS[@]}"

  jq -e '
    .status == "completed"
    and .counts.selected_endpoints == 85
    and .counts.planned_requests == 477
    and .counts.completed_requests == 477
  ' "${CURRENT_RUN_DIR}/run_manifest.json" >/dev/null

  collect_target_artifacts
  stop_target
  PYTHONPATH="${REPO_ROOT}/src" \
    "${PYTHON_BIN}" "${DEDUPLICATOR}" "${CURRENT_RUN_DIR}"
  append_target_artifacts_to_manifest
  echo "Completed repetition ${run_number}/${REPETITIONS}: ${CURRENT_RUN_DIR}"
  CURRENT_RUN_DIR=""
done

trap - EXIT
rm -rf -- "${TEMP_DIR}"
echo "Completed ${REPETITIONS} Meilisearch repetitions in ${OUTPUT_ROOT}"
