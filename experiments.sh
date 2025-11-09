#!/usr/bin/env bash

TASK_NUM=$1
TASK_IDX=$2
PORT=$3

# MODELS=("gpt-4.1" "gpt-4o-mini")
# MODELS=("claude-sonnet-4")
# MODELS=("claude-3-5-haiku")
# MODELS=("Qwen3-8B")
# MODELS=("Qwen3-32B")
# MODELS=("Llama-3.1-70B")
# MODELS=("deepseek-coder-v2")
MODELS=("phi-4")
# MODELS=("gemma-3-4b")
# MODELS=("gemma-3-27b")
WCODES=("True" "False")

PROMPTS=("")

for model in "${MODELS[@]}"; do
  for wcode in "${WCODES[@]}"; do
    for prompt in "${PROMPTS[@]}"; do
      # 组装命令（空 prompt 不加 --prompting）
      cmd=(poetry run python src/job/postcond_generation.py
           --model_name "$model"
           --generate_num 5
           --w_code "$wcode"
           --task_num $TASK_NUM
           --task_idx $TASK_IDX
           --port $PORT)

      if [[ -n "$prompt" ]]; then
        cmd+=(--prompting "$prompt")
      fi

      echo ">>> Running: ${cmd[@]}"
      "${cmd[@]}"
    done
  done
done


PROMPTS=("fsl_1" "fsl_3" "fsl_5" "no_gram")
# PROMPTS=("no_gram")
# PROMPTS=("fsl_1" "fsl_3" "fsl_5")

for prompt in "${PROMPTS[@]}"; do
  for model in "${MODELS[@]}"; do
    for wcode in "${WCODES[@]}"; do
      # 组装命令（空 prompt 不加 --prompting）
      cmd=(poetry run python src/job/postcond_generation.py
           --model_name "$model"
           --generate_num 1
           --w_code "$wcode"
           --task_num $TASK_NUM
           --task_idx $TASK_IDX
           --port $PORT)

      if [[ -n "$prompt" ]]; then
        cmd+=(--prompting "$prompt")
      fi

      echo ">>> Running: ${cmd[@]}"
      "${cmd[@]}"
    done
  done
done