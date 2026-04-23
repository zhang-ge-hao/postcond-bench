#!/bin/bash

set -euo pipefail

INPUT_DIR="data/step/8.benchmark"
OUTPUT_DIR=""
WORKDIR="$(pwd)"
TASK_NUM=""
TASK_IDX=""
LANG=""
GITHUB_PATH=""
RLID=""
LIMIT=""
PROCESSES=1
APPTAINER_IMAGE="${HOME}/image/apptainer/sbpy.sif"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: bash src/reasoning/eval_gt/run_in_apptainer.sh [options]

Options:
  --input_dir PATH
  --output_dir PATH
  --workdir PATH
  --task_num N
  --task_idx N
  --lang LANG
  --github_path OWNER/REPO
  --rlid METHOD_ID
  --limit N
  --processes N
  --apptainer_image PATH
  --dry_run
  -h, --help
EOF
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

if [[ -n "$TASK_NUM" && -z "$TASK_IDX" ]] || [[ -z "$TASK_NUM" && -n "$TASK_IDX" ]]; then
  echo "--task_num and --task_idx must be set together" >&2
  exit 1
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

PYTHON_CMD=(PYTHONPATH=. poetry run python src/reasoning/eval_gt/__main__.py
  --input_dir "$INPUT_DIR"
  --output_dir "$OUTPUT_DIR_ABS"
  --processes "$PROCESSES")

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

if [[ "$DRY_RUN" -eq 1 ]]; then
  printf '%s\n' "cd $(printf '%q' "$WORKDIR_ABS")"
  printf '%s\n' "apptainer exec --cleanenv ... $(printf '%q' "$APPTAINER_IMAGE") bash -lc $(printf '%q' "$PYTHON_CMD_STR")"
  exit 0
fi

mkdir -p "$OUTPUT_DIR_ABS"
cd "$WORKDIR_ABS"

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
  "$APPTAINER_IMAGE" \
  bash -lc "$PYTHON_CMD_STR"