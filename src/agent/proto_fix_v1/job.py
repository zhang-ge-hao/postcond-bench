

from src.agent.proto_fix_v1.gen import (
    postcond_generation_v2_pool
)
from src.ds import *
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_num", type=int)
    parser.add_argument("--task_idx", type=int)
    parser.add_argument("--lang", type=str, default=None)
    args = parser.parse_args()

    assert args.task_num is not None and isinstance(args.task_num, int)
    assert args.task_idx is not None and isinstance(args.task_idx, int)
    
    input_dir = "data/step/9.Qwen3-32B-reason--v2-all"
    output_dir = "data/step/9.Qwen3-32B-agent--v2-all"
    task_num = args.task_num
    task_idx = args.task_idx
    lang = args.lang

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    postcond_generation_v2_pool(
        input_dir=input_dir,
        output_dir=output_dir,
        task_num=task_num,
        task_idx=task_idx,
        lang=lang,
    )
