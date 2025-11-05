#!/usr/bin/env bash

MODEL_NAME=$1
TASK_IDX=$2

source /modules/opt/linux-ubuntu24.04-x86_64/miniforge3/24.7.1/etc/profile.d/conda.sh
conda activate ~/conda/envs/vllm

########################################
# 自动检测可用 GPU 数量
########################################

GPU_NUM=1

if [[ -n "$CUDA_VISIBLE_DEVICES" ]]; then
  # 如果用户手动设置了 CUDA_VISIBLE_DEVICES，就以它为准
  IFS=',' read -ra DEVICES <<< "$CUDA_VISIBLE_DEVICES"
  GPU_NUM=${#DEVICES[@]}
elif command -v nvidia-smi &>/dev/null; then
  # 否则通过 nvidia-smi 检测可见的 GPU 数量
  GPU_NUM=$(nvidia-smi -L | wc -l)
fi

# 如果有多张卡，就在多张卡上 tensor parallel
TP_ARGS=()
if (( GPU_NUM > 1 )); then
  TP_ARGS=(--tensor-parallel-size "$GPU_NUM")
fi

########################################
# 启动 vLLM
########################################

if [[ "$MODEL_NAME" == *Qwen3* ]]; then
  # Qwen3 系列模型：开启 yarn rope scaling，放大 context length
  vllm serve "$MODEL_NAME" \
    --port "1999$TASK_IDX" \
    "${TP_ARGS[@]}" \
    --rope-scaling '{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}' \
    --max-model-len 131072
else
  # 其他模型：保持原来的启动方式 + 自动 TP
  vllm serve "$MODEL_NAME" \
    --port "1999$TASK_IDX" \
    "${TP_ARGS[@]}"
fi
