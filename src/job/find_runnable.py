from src.repo import reproduce_pool, reproduce
from src.ds import Repo
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_num", type=int)
    parser.add_argument("--task_idx", type=int)
    args = parser.parse_args()

    assert args.task_num is not None and isinstance(args.task_num, int)
    assert args.task_idx is not None and isinstance(args.task_idx, int)
    assert args.task_num > args.task_idx

    reproduce_pool(input_dir="data/step/1.biglist", 
                   output_dir="data/step/2.runnable",
                   task_num=args.task_num,
                   task_idx=args.task_idx)
