

from src.mutation import (
    mutant_generation_pool
)
from src.ds import *
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_num", type=int)
    parser.add_argument("--task_idx", type=int)
    args = parser.parse_args()

    assert args.task_num is not None and isinstance(args.task_num, int)
    assert args.task_idx is not None and isinstance(args.task_idx, int)
    assert args.task_num > args.task_idx

    mutant_generation_pool(
        input_dir="data/step/5.exec_check",
        output_dir="data/step/6.mutation",
        task_num=args.task_num,
        task_idx=args.task_idx
    )
