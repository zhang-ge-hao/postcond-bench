#!/bin/bash

set -euo pipefail

INPUT_DIR="data/step/8.benchmark"
OUTPUT_DIR=""
RUN_ID=""
WORKDIR="$(pwd)"
TASK_NUM=""
TASK_IDX=""
LANG=""
GITHUB_PATH=""
RLID=""
LIMIT=""
JOB_NAME="postcond-gt-eval"
PARTITION="superpod-a100"
ACCOUNT=""
QOS=""
CONSTRAINT=""
GRES="gpu:a100:1"
TIME_LIMIT="08:00:00"
MEMORY="256g"
CPUS_PER_TASK=32
PROCESSES=""
APPTAINER_IMAGE="${HOME}/image/apptainer/sbpy.sif"
DRY_RUN=0
RUN_SCRIPT="src/reasoning/eval_gt/run_in_apptainer.sh"

usage() {
  cat <<'EOF'
Usage: bash src/reasoning/eval_gt/submit_slurm.sh [options]

Options:
  --input_dir PATH
  --output_dir PATH
  --run_id ID
  --workdir PATH
  --task_num N
  --task_idx N
  --lang LANG
  --github_path OWNER/REPO
  --rlid METHOD_ID
  --limit N
  --job_name NAME
  --partition NAME
  --account NAME
  --qos NAME
  --constraint EXPR
  --gres SPEC
  --time HH:MM:SS
  --mem SIZE
  --cpus_per_task N
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
    --run_id)
      RUN_ID="$2"
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
    --job_name)
      JOB_NAME="$2"
      shift 2
      ;;
    --partition)
      PARTITION="$2"
      shift 2
      ;;
    --account)
      ACCOUNT="$2"
      shift 2
      ;;
    --qos)
      QOS="$2"
      shift 2
      ;;
    --constraint)
      CONSTRAINT="$2"
      shift 2
      ;;
    --gres)
      GRES="$2"
      shift 2
      ;;
    --time)
      TIME_LIMIT="$2"
      shift 2
      ;;
    --mem)
      MEMORY="$2"
      shift 2
      ;;
    --cpus_per_task)
      CPUS_PER_TASK="$2"
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

if [[ -n "$TASK_NUM" && -z "$TASK_IDX" ]] || [[ -z "$TASK_NUM" && -n "$TASK_IDX" ]]; then
  echo "--task_num and --task_idx must be set together" >&2
  exit 1
fi

if [[ -z "$PROCESSES" ]]; then
  PROCESSES="$CPUS_PER_TASK"
fi

if [[ -z "$RUN_ID" ]]; then
  RUN_ID="$(date +%Y%m%d_%H%M%S)"
fi

if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR="data/reasoning/eval_gt/${RUN_ID}/results"
fi

OUTPUT_DIR_ABS="$(python - <<'PY' "$OUTPUT_DIR"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"
WORKDIR_ABS="$(python - <<'PY' "$WORKDIR"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"
SUBMIT_DIR="$(dirname "$OUTPUT_DIR_ABS")"
SLURM_DIR="${SUBMIT_DIR}/slurm"
mkdir -p "$SLURM_DIR"

RUNNER_CMD=(bash "$RUN_SCRIPT"
  --workdir "$WORKDIR_ABS"
  --input_dir "$INPUT_DIR"
  --output_dir "$OUTPUT_DIR_ABS"
  --processes "$PROCESSES"
  --apptainer_image "$APPTAINER_IMAGE")

if [[ -n "$TASK_NUM" ]]; then
  RUNNER_CMD+=(--task_num "$TASK_NUM" --task_idx "$TASK_IDX")
fi
if [[ -n "$LANG" ]]; then
  RUNNER_CMD+=(--lang "$LANG")
fi
if [[ -n "$GITHUB_PATH" ]]; then
  RUNNER_CMD+=(--github_path "$GITHUB_PATH")
fi
if [[ -n "$RLID" ]]; then
  RUNNER_CMD+=(--rlid "$RLID")
fi
if [[ -n "$LIMIT" ]]; then
  RUNNER_CMD+=(--limit "$LIMIT")
fi

printf -v RUNNER_CMD_STR '%q ' "${RUNNER_CMD[@]}"
RUNNER_CMD_STR="${RUNNER_CMD_STR% }"

SBATCH_SCRIPT="${SLURM_DIR}/submit-${RUN_ID}.sbatch"
STDOUT_PATH="${SLURM_DIR}/%x-%j.out"
STDERR_PATH="${SLURM_DIR}/%x-%j.err"

cat > "$SBATCH_SCRIPT" <<EOF
#!/bin/bash
#SBATCH --job-name=${JOB_NAME}
#SBATCH --output=${STDOUT_PATH}
#SBATCH --error=${STDERR_PATH}
#SBATCH --nodes=1
#SBATCH --cpus-per-task=${CPUS_PER_TASK}
#SBATCH --mem=${MEMORY}
#SBATCH --time=${TIME_LIMIT}
EOF

if [[ -n "$PARTITION" ]]; then
  echo "#SBATCH --partition=${PARTITION}" >> "$SBATCH_SCRIPT"
fi
if [[ -n "$ACCOUNT" ]]; then
  echo "#SBATCH --account=${ACCOUNT}" >> "$SBATCH_SCRIPT"
fi
if [[ -n "$QOS" ]]; then
  echo "#SBATCH --qos=${QOS}" >> "$SBATCH_SCRIPT"
fi
if [[ -n "$CONSTRAINT" ]]; then
  echo "#SBATCH --constraint=${CONSTRAINT}" >> "$SBATCH_SCRIPT"
fi
if [[ -n "$GRES" ]]; then
  echo "#SBATCH --gres=${GRES}" >> "$SBATCH_SCRIPT"
fi

cat >> "$SBATCH_SCRIPT" <<EOF

set -euo pipefail
mkdir -p $(printf '%q' "$OUTPUT_DIR_ABS")
cd $(printf '%q' "$WORKDIR_ABS")
$(printf '%s' "$RUNNER_CMD_STR")
EOF

METADATA_PATH="${SUBMIT_DIR}/submit.json"

if [[ "$DRY_RUN" -eq 1 ]]; then
  cat > "$METADATA_PATH" <<EOF
{
  "job_id": null,
  "submit_stdout": "",
  "submit_stderr": "",
  "script_path": "${SBATCH_SCRIPT}",
  "output_dir": "${OUTPUT_DIR_ABS}",
  "workdir": "${WORKDIR_ABS}",
  "command": "${RUNNER_CMD_STR}",
  "apptainer_image": "${APPTAINER_IMAGE}",
  "dry_run": true
}
EOF
  cat "$METADATA_PATH"
  exit 0
fi

SBATCH_OUTPUT="$(sbatch "$SBATCH_SCRIPT")"
JOB_ID="$(echo "$SBATCH_OUTPUT" | awk '/Submitted batch job/ {print $4}')"

cat > "$METADATA_PATH" <<EOF
{
  "job_id": "${JOB_ID}",
  "submit_stdout": "${SBATCH_OUTPUT}",
  "submit_stderr": "",
  "script_path": "${SBATCH_SCRIPT}",
  "output_dir": "${OUTPUT_DIR_ABS}",
  "workdir": "${WORKDIR_ABS}",
  "command": "${RUNNER_CMD_STR}",
  "apptainer_image": "${APPTAINER_IMAGE}",
  "dry_run": false
}
EOF

cat "$METADATA_PATH"