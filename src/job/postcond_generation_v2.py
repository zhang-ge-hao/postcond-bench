

from src.postcond import (
    postcond_generation_v2_pool
)
from src.ds import *
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_num", type=int)
    parser.add_argument("--task_idx", type=int)
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--port", type=str, default=None)
    parser.add_argument("--generate_num", type=int, default=5)
    parser.add_argument("--prompting", type=str, default=None)
    parser.add_argument("--lang", type=str, default=None)
    args = parser.parse_args()

    assert args.task_num is not None and isinstance(args.task_num, int)
    assert args.task_idx is not None and isinstance(args.task_idx, int)
    assert args.model_name is not None and isinstance(args.model_name, str)
    assert args.generate_num is not None and isinstance(args.generate_num, int)
    assert args.prompting is not None and isinstance(args.prompting, str)
    assert args.task_num > args.task_idx

    model_name = args.model_name
    port = args.port
    generate_num = args.generate_num
    task_num = args.task_num
    task_idx = args.task_idx
    lang = args.lang
    prompting = args.prompting

    input_dir = "data/step/8.benchmark"

    folder_name = model_name + "--" + prompting
    output_dir = f"data/step/9.{folder_name}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    postcond_generation_v2_pool(
        input_dir=input_dir,
        output_dir=output_dir,
        model_name=model_name,
        port=port,
        generate_num=generate_num,
        prompting=prompting,
        task_num=task_num,
        task_idx=task_idx,
        lang=lang,
    )
