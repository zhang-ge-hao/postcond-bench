

from src.curator import (
    ref_gen_pool
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

    ref_gen_pool(
        input_dir="data/step/6.mutation",
        output_dir="data/step/7.reference",
        task_num=args.task_num,
        task_idx=args.task_idx
    )
