#!/usr/bin/env bash

TASK_NUM=$1
TASK_IDX=$2

# MODELS=("gpt-4.1" "gpt-4o-mini")
# MODELS=("claude-sonnet-4" "claude-3-5-haiku")
# MODELS=("claude-3-5-haiku")
MODELS=("Qwen3-32B")
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
           --task_idx $TASK_IDX)

      if [[ -n "$prompt" ]]; then
        cmd+=(--prompting "$prompt")
      fi

      echo ">>> Running: ${cmd[@]}"
      "${cmd[@]}"
    done
  done
done


PROMPTS=("no_gram" "fsl_1" "fsl_3" "fsl_5")
# PROMPTS=("no_gram")
# PROMPTS=("fsl_1" "fsl_3" "fsl_5")

for model in "${MODELS[@]}"; do
  for wcode in "${WCODES[@]}"; do
    for prompt in "${PROMPTS[@]}"; do
      # 组装命令（空 prompt 不加 --prompting）
      cmd=(poetry run python src/job/postcond_generation.py
           --model_name "$model"
           --generate_num 1
           --w_code "$wcode"
           --task_num $TASK_NUM
           --task_idx $TASK_IDX)

      if [[ -n "$prompt" ]]; then
        cmd+=(--prompting "$prompt")
      fi

      echo ">>> Running: ${cmd[@]}"
      "${cmd[@]}"
    done
  done
done