

from src.postcond import (
    postcond_generation_pool
)
from src.ds import *
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_num", type=int)
    parser.add_argument("--task_idx", type=int)
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--generate_num", type=int, default=5)
    parser.add_argument("--w_code", type=bool)
    args = parser.parse_args()

    assert args.task_num is not None and isinstance(args.task_num, int)
    assert args.task_idx is not None and isinstance(args.task_idx, int)
    assert args.model_name is not None and isinstance(args.model_name, str)
    assert args.generate_num is not None and isinstance(args.generate_num, int)
    assert args.w_code is not None and isinstance(args.w_code, bool)
    assert args.task_num > args.task_idx

    folder_name = (
        args.model_name + "--"
        "w_code" if args.w_code else "wo_code"
    )
    output_dir = f"data/step/9.{folder_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    postcond_generation_pool(
        input_dir="data/step/8.benchmark",
        output_dir=output_dir,
        model_name=args.model_name,
        generate_num=args.generate_num,
        w_code=args.w_code,
        task_num=args.task_num,
        task_idx=args.task_idx,
    )
