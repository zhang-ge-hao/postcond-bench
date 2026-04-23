#!/usr/bin/env bash
set -euo pipefail

CONDA_MODULE=${CONDA_MODULE:-conda/latest}
VLLM_CONDA_ENV_PATH=${VLLM_CONDA_ENV_PATH:-${PI_WORKDIR:-}/conda/envs/vllm}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
MAX_MODEL_LEN=${MAX_MODEL_LEN:-262144}
ENABLE_REASONING=${ENABLE_REASONING:-true}
REASONING_PARSER=${REASONING_PARSER:-deepseek_r1}

usage() {
    cat <<'EOF' >&2
Usage: serve_vllm_checkpoint.sh CHECKPOINT_PATH [additional vllm serve args...]

Environment overrides:
    CONDA_MODULE         Module name used to load conda. Default: conda/latest
    VLLM_CONDA_ENV_PATH  Path to the vllm conda env. Default: $PI_WORKDIR/conda/envs/vllm
    HOST                 Host passed to vllm serve. Default: 0.0.0.0
    PORT                 Port passed to vllm serve. Default: 8000
    MAX_MODEL_LEN        Passed to --max-model-len. Default: 262144
    ENABLE_REASONING     Whether to add --enable-reasoning. Default: true
    REASONING_PARSER     Passed to --reasoning-parser when reasoning is enabled. Default: deepseek_r1
EOF
    exit 1
}

detect_gpu_count() {
    local gpu_count=""

    if [[ -n "${CUDA_VISIBLE_DEVICES:-}" ]]; then
        IFS=',' read -r -a cuda_devices <<< "${CUDA_VISIBLE_DEVICES}"
        gpu_count=${#cuda_devices[@]}
    elif command -v nvidia-smi >/dev/null 2>&1; then
        gpu_count=$(nvidia-smi --list-gpus | wc -l | tr -d ' ')
    fi

    if [[ -z "${gpu_count}" || "${gpu_count}" -lt 1 ]]; then
        echo "Unable to detect a usable GPU. Set CUDA_VISIBLE_DEVICES or run on a GPU node." >&2
        exit 1
    fi

    printf '%s\n' "${gpu_count}"
}

if [[ $# -lt 1 ]]; then
    usage
fi

CHECKPOINT_PATH=$1
shift

if [[ ! -d "${CHECKPOINT_PATH}" ]]; then
    echo "Checkpoint directory not found: ${CHECKPOINT_PATH}" >&2
    exit 1
fi

if [[ ! -d "${VLLM_CONDA_ENV_PATH}" ]]; then
    echo "vllm conda environment not found: ${VLLM_CONDA_ENV_PATH}" >&2
    exit 1
fi

module load "${CONDA_MODULE}"
CONDA_BASE=$(conda info --base)
source "${CONDA_BASE}/etc/profile.d/conda.sh"
conda activate "${VLLM_CONDA_ENV_PATH}"

if ! command -v vllm >/dev/null 2>&1; then
    echo "vllm is not available in environment: ${VLLM_CONDA_ENV_PATH}" >&2
    exit 1
fi

GPU_COUNT=$(detect_gpu_count)
SERVED_MODEL_NAME=${SERVED_MODEL_NAME:-$(basename "${CHECKPOINT_PATH}")}
VLLM_ARGS=(
    --host "${HOST}"
    --port "${PORT}"
    --served-model-name "${SERVED_MODEL_NAME}"
    --tensor-parallel-size "${GPU_COUNT}"
    --max-model-len "${MAX_MODEL_LEN}"
)

case "${ENABLE_REASONING}" in
    1|true|TRUE|True|yes|YES|Yes|on|ON|On)
        VLLM_ARGS+=(
            --enable-reasoning
            --reasoning-parser "${REASONING_PARSER}"
        )
        ;;
esac

echo "Serving checkpoint: ${CHECKPOINT_PATH}"
echo "Using vllm environment: ${VLLM_CONDA_ENV_PATH}"
echo "Detected GPUs: ${GPU_COUNT}"
echo "Starting vllm serve on ${HOST}:${PORT}"

exec vllm serve "${CHECKPOINT_PATH}" \
    "${VLLM_ARGS[@]}" \
    "$@"