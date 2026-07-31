#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -lt 5 ]]; then
  echo "Usage: $0 SCHEMA BASE_URL EXPERIMENT_ID TARGET_ID RUN_NUMBER [FUZZER_ARGS...]" >&2
  exit 2
fi

SCHEMA="$1"
BASE_URL="$2"
EXPERIMENT_ID="$3"
TARGET_ID="$4"
RUN_NUMBER="$5"
shift 5

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"
RUN_ID="${RUN_ID:-${TARGET_ID}-$(date -u +%Y%m%dT%H%M%SZ)}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/output/experiments/${EXPERIMENT_ID}/${TARGET_ID}}"

if [[ ! -f "${SCHEMA}" ]]; then
  echo "OpenAPI contract not found: ${SCHEMA}" >&2
  exit 1
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Python environment not found: ${PYTHON_BIN}" >&2
  exit 1
fi

if [[ -e "${OUTPUT_ROOT}/${RUN_ID}" ]]; then
  echo "Run already exists; refusing to overwrite: ${OUTPUT_ROOT}/${RUN_ID}" >&2
  exit 1
fi

echo "Experiment: ${EXPERIMENT_ID}"
echo "Target: ${TARGET_ID}"
echo "Run: ${RUN_ID}"

cd "${REPO_ROOT}"
PYTHONPATH="${REPO_ROOT}/src" \
"${PYTHON_BIN}" -m fuzzer.main "${SCHEMA}" \
  --base-url "${BASE_URL}" \
  --level "${LEVEL:-1}" \
  --max "${MAX_MUTATIONS:-20}" \
  --concurrency "${CONCURRENCY:-1}" \
  --delay "${DELAY_MS:-250}" \
  --timeout "${TIMEOUT_SECONDS:-10}" \
  --output-dir "${OUTPUT_ROOT}" \
  --run-id "${RUN_ID}" \
  --experiment-id "${EXPERIMENT_ID}" \
  --target-id "${TARGET_ID}" \
  --run-number "${RUN_NUMBER}" \
  "$@"
