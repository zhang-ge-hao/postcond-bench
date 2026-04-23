#!/bin/bash

set -euo pipefail

INPUT_DIR="data/step/8.benchmark"
OUTPUT_DIR=""
WORKDIR="$(pwd)"
CHECKPOINT_PATH=""
TASK_NUM=""
TASK_IDX=""
LANG=""
GITHUB_PATH=""
RLID=""
LIMIT=""
PROCESSES=1
APPTAINER_IMAGE="${HOME}/image/apptainer/sbpy.sif"
VLLM_START_SCRIPT="src/reasoning/eval/start_vllm.sh"
VLLM_HOST="127.0.0.1"
VLLM_PORT=""
VLLM_SERVER_URL=""
VLLM_MODEL_NAME="placeholder-vllm-model"
PROMPT_MODE="baseline"
GENERATE_NUM=1
STARTUP_TIMEOUT_SEC=600
HEALTHCHECK_INTERVAL_SEC=5
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: bash src/reasoning/eval/run_in_apptainer.sh [options]

Options:
  --input_dir PATH
  --output_dir PATH
  --workdir PATH
  --checkpoint_path PATH
  --task_num N
  --task_idx N
  --lang LANG
  --github_path OWNER/REPO
  --rlid METHOD_ID
  --limit N
  --processes N
  --apptainer_image PATH
  --vllm_start_script PATH
  --vllm_host HOST
  --vllm_port PORT
  --vllm_server_url URL
  --vllm_model_name NAME
  --prompt_mode MODE
  --generate_num N
  --startup_timeout_sec N
  --healthcheck_interval_sec N
  --dry_run
  -h, --help
EOF
}

compute_vllm_port() {
  local seed="$1"

  python - <<'PY' "$seed"
import hashlib
import sys

seed = sys.argv[1]
low = 20000
high = 59999
span = high - low + 1
common_ports = {
    20022,
    23000,
    23717,
    23719,
    25565,
    27017,
    28080,
    30000,
    33060,
    40400,
    42000,
    50051,
}
value = int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16)

for offset in range(span):
    candidate = low + ((value + offset) % span)
    if candidate not in common_ports:
        print(candidate)
        break
else:
    raise RuntimeError("failed to derive a usable vLLM port")
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input_dir)
      INPUT_DIR="$2"
      shift 2
      ;;
    --output_dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --workdir)
      WORKDIR="$2"
      shift 2
      ;;
    --checkpoint_path)
      CHECKPOINT_PATH="$2"
      shift 2
      ;;
    --task_num)
      TASK_NUM="$2"
      shift 2
      ;;
    --task_idx)
      TASK_IDX="$2"
      shift 2
      ;;
    --lang)
      LANG="$2"
      shift 2
      ;;
    --github_path)
      GITHUB_PATH="$2"
      shift 2
      ;;
    --rlid)
      RLID="$2"
      shift 2
      ;;
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --processes)
      PROCESSES="$2"
      shift 2
      ;;
    --apptainer_image)
      APPTAINER_IMAGE="$2"
      shift 2
      ;;
    --vllm_start_script)
      VLLM_START_SCRIPT="$2"
      shift 2
      ;;
    --vllm_host)
      VLLM_HOST="$2"
      shift 2
      ;;
    --vllm_port)
      VLLM_PORT="$2"
      shift 2
      ;;
    --vllm_server_url)
      VLLM_SERVER_URL="$2"
      shift 2
      ;;
    --vllm_model_name)
      VLLM_MODEL_NAME="$2"
      shift 2
      ;;
    --prompt_mode)
      PROMPT_MODE="$2"
      shift 2
      ;;
    --generate_num)
      GENERATE_NUM="$2"
      shift 2
      ;;
    --startup_timeout_sec)
      STARTUP_TIMEOUT_SEC="$2"
      shift 2
      ;;
    --healthcheck_interval_sec)
      HEALTHCHECK_INTERVAL_SEC="$2"
      shift 2
      ;;
    --dry_run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$OUTPUT_DIR" ]]; then
  echo "--output_dir is required" >&2
  exit 1
fi

if [[ -z "$CHECKPOINT_PATH" ]]; then
  echo "--checkpoint_path is required" >&2
  exit 1
fi

if [[ -n "$TASK_NUM" && -z "$TASK_IDX" ]] || [[ -z "$TASK_NUM" && -n "$TASK_IDX" ]]; then
  echo "--task_num and --task_idx must be set together" >&2
  exit 1
fi

if [[ ! -d "$CHECKPOINT_PATH" ]]; then
  echo "Checkpoint directory not found: $CHECKPOINT_PATH" >&2
  exit 1
fi

if [[ -n "$VLLM_SERVER_URL" ]]; then
  URL_PORT="$(python - <<'PY' "$VLLM_SERVER_URL"
from urllib.parse import urlparse
import sys

parsed = urlparse(sys.argv[1])
print(parsed.port or "")
PY
)"
  if [[ -z "$VLLM_PORT" ]]; then
    VLLM_PORT="$URL_PORT"
  elif [[ -n "$URL_PORT" && "$VLLM_PORT" != "$URL_PORT" ]]; then
    echo "--vllm_port and --vllm_server_url disagree on port" >&2
    exit 1
  fi
fi

if [[ -z "$VLLM_PORT" ]]; then
  if [[ -n "${SLURM_JOB_ID:-}" ]]; then
    VLLM_PORT="$(compute_vllm_port "$SLURM_JOB_ID")"
  else
    VLLM_PORT="$(compute_vllm_port "local-${USER:-unknown}-${HOSTNAME:-unknown}-${PPID}")"
  fi
fi

if [[ -z "$VLLM_SERVER_URL" ]]; then
  VLLM_SERVER_URL="http://${VLLM_HOST}:${VLLM_PORT}/v1"
fi

WORKDIR_ABS="$(python - <<'PY' "$WORKDIR"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"
OUTPUT_DIR_ABS="$(python - <<'PY' "$OUTPUT_DIR"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"
CHECKPOINT_PATH_ABS="$(python - <<'PY' "$CHECKPOINT_PATH"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"
VLLM_START_SCRIPT_ABS="$(python - <<'PY' "$VLLM_START_SCRIPT"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"

PYTHON_CMD=(PYTHONPATH=. poetry run python src/reasoning/eval/__main__.py
  --input_dir "$INPUT_DIR"
  --output_dir "$OUTPUT_DIR_ABS"
  --processes "$PROCESSES"
  --vllm_server_url "$VLLM_SERVER_URL"
  --model_name "$VLLM_MODEL_NAME"
  --prompt_mode "$PROMPT_MODE"
  --generate_num "$GENERATE_NUM")

if [[ -n "$TASK_NUM" ]]; then
  PYTHON_CMD+=(--task_num "$TASK_NUM" --task_idx "$TASK_IDX")
fi
if [[ -n "$LANG" ]]; then
  PYTHON_CMD+=(--lang "$LANG")
fi
if [[ -n "$GITHUB_PATH" ]]; then
  PYTHON_CMD+=(--github_path "$GITHUB_PATH")
fi
if [[ -n "$RLID" ]]; then
  PYTHON_CMD+=(--rlid "$RLID")
fi
if [[ -n "$LIMIT" ]]; then
  PYTHON_CMD+=(--limit "$LIMIT")
fi

printf -v PYTHON_CMD_STR '%q ' "${PYTHON_CMD[@]}"
PYTHON_CMD_STR="${PYTHON_CMD_STR% }"

mkdir -p "$OUTPUT_DIR_ABS"
VLLM_LOG_PATH="$OUTPUT_DIR_ABS/vllm_server.log"

if [[ "$DRY_RUN" -eq 1 ]]; then
  printf '%s\n' "cd $(printf '%q' "$WORKDIR_ABS")"
  printf '%s\n' "HOST=$(printf '%q' "$VLLM_HOST") PORT=$(printf '%q' "$VLLM_PORT") VLLM_BASE_URL=$(printf '%q' "$VLLM_SERVER_URL") SERVED_MODEL_NAME=$(printf '%q' "$VLLM_MODEL_NAME") bash $(printf '%q' "$VLLM_START_SCRIPT_ABS") $(printf '%q' "$CHECKPOINT_PATH_ABS") > $(printf '%q' "$VLLM_LOG_PATH") 2>&1 &"
  printf '%s\n' "wait for $(printf '%q' "$VLLM_SERVER_URL/models") up to ${STARTUP_TIMEOUT_SEC}s"
  printf '%s\n' "apptainer exec --cleanenv ... $(printf '%q' "$APPTAINER_IMAGE") bash -lc $(printf '%q' "$PYTHON_CMD_STR")"
  exit 0
fi

cleanup() {
  if [[ -n "${VLLM_PID:-}" ]] && kill -0 "$VLLM_PID" 2>/dev/null; then
    kill "$VLLM_PID" 2>/dev/null || true
    wait "$VLLM_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT

cd "$WORKDIR_ABS"

HOST="$VLLM_HOST" \
PORT="$VLLM_PORT" \
VLLM_BASE_URL="$VLLM_SERVER_URL" \
SERVED_MODEL_NAME="$VLLM_MODEL_NAME" \
VLLM_OUTPUT_DIR="$OUTPUT_DIR_ABS" \
VLLM_LOG_PATH="$VLLM_LOG_PATH" \
bash "$VLLM_START_SCRIPT_ABS" "$CHECKPOINT_PATH_ABS" >"$VLLM_LOG_PATH" 2>&1 &
VLLM_PID=$!

echo "Started vLLM launcher with PID $VLLM_PID"
echo "Using checkpoint: $CHECKPOINT_PATH_ABS"
echo "Using vLLM port: $VLLM_PORT"
echo "Waiting for vLLM at ${VLLM_SERVER_URL}/models"

START_TIME=$SECONDS
while true; do
  if python - <<'PY' "$VLLM_SERVER_URL"
import sys
from urllib import error, request

url = sys.argv[1].rstrip("/") + "/models"
try:
    with request.urlopen(url, timeout=5) as response:
        sys.exit(0 if 200 <= response.status < 300 else 1)
except (OSError, error.URLError, error.HTTPError):
    sys.exit(1)
PY
  then
    break
  fi

  if ! kill -0 "$VLLM_PID" 2>/dev/null; then
    wait "$VLLM_PID"
    echo "vLLM launcher exited before the service became reachable. See $VLLM_LOG_PATH" >&2
    exit 1
  fi

  if (( SECONDS - START_TIME >= STARTUP_TIMEOUT_SEC )); then
    echo "Timed out after ${STARTUP_TIMEOUT_SEC}s waiting for vLLM at ${VLLM_SERVER_URL}/models" >&2
    exit 1
  fi

  sleep "$HEALTHCHECK_INTERVAL_SEC"
done

PATH_STR=/root/.cargo/bin
PATH_STR="$PATH_STR:/opt/maven/bin"
PATH_STR="$PATH_STR:/root/.local/bin"
PATH_STR="$PATH_STR:/root/.pyenv/bin"
PATH_STR="$PATH_STR:/root/.pyenv/shims"
PATH_STR="$PATH_STR:/usr/local/sbin"
PATH_STR="$PATH_STR:/usr/local/bin"
PATH_STR="$PATH_STR:/usr/sbin"
PATH_STR="$PATH_STR:/usr/bin"
PATH_STR="$PATH_STR:/sbin"
PATH_STR="$PATH_STR:/bin"

apptainer exec --cleanenv \
  --env JAVA_HOME=/usr \
  --env SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
  --env PYTHONPATH=. \
  --env LC_ALL=C.UTF-8 \
  --env LANG=C.UTF-8 \
  --env PATH="$PATH_STR" \
  --env PI_WORKDIR="${PI_WORKDIR:-$PWD}" \
  --env OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
  --env ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}" \
  --env DASHSCOPE_API_KEY="${DASHSCOPE_API_KEY:-}" \
  --env DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-}" \
  --env AWS_BEARER_TOKEN_BEDROCK="${AWS_BEARER_TOKEN_BEDROCK:-}" \
  --env GITHUB_TOKEN="${GITHUB_TOKEN:-}" \
  --env HF_HOME="${HF_HOME:-}" \
  --env HF_TOKEN="${HF_TOKEN:-}" \
  --env VLLM_BASE_URL="$VLLM_SERVER_URL" \
  --env VLLM_MODEL_NAME="$VLLM_MODEL_NAME" \
  "$APPTAINER_IMAGE" \
  bash -lc "$PYTHON_CMD_STR"