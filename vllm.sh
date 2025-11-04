#!/usr/bin/env bash

MODEL_NAME=$1
PORT=$2

source /modules/opt/linux-ubuntu24.04-x86_64/miniforge3/24.7.1/etc/profile.d/conda.sh
conda activate ~/conda/envs/vllm

if [[ "$MODEL_NAME" == *Qwen3* ]]; then
  # Qwen3 系列模型：开启 yarn rope scaling，放大 context length
  vllm serve "$MODEL_NAME" \
    --port "$PORT" \
    --rope-scaling '{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}' \
    --max-model-len 131072
else
  # 其他模型：保持原来的启动方式
  vllm serve "$MODEL_NAME" --port "$PORT"
fi
