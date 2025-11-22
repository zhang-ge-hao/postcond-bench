

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
    parser.add_argument("--port", type=str, default=None)
    parser.add_argument("--generate_num", type=int, default=5)
    parser.add_argument("--w_code", type=str)
    parser.add_argument("--lang", type=str, default=None)
    parser.add_argument("--prompting", type=str, default=None)
    parser.add_argument("--custom_root", type=str, default=None)
    args = parser.parse_args()

    assert args.task_num is not None and isinstance(args.task_num, int)
    assert args.task_idx is not None and isinstance(args.task_idx, int)
    assert args.model_name is not None and isinstance(args.model_name, str)
    assert args.generate_num is not None and isinstance(args.generate_num, int)
    assert args.w_code in ["False", "True"]
    assert args.task_num > args.task_idx

    model_name = args.model_name
    port = args.port
    generate_num = args.generate_num
    task_num = args.task_num
    task_idx = args.task_idx
    lang = args.lang
    w_code = args.w_code == "True"
    prompting = args.prompting
    custom_root = args.custom_root

    folder_name = model_name + "--" + ("w_code" if w_code else "wo_code")
    if prompting is not None:
        folder_name += f"--{prompting}"
    output_dir = f"data/step/9.{folder_name}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if custom_root is None:
        input_dir = "data/step/8.benchmark"
    else:
        input_dir = f"{custom_root}/9.{folder_name}"

    postcond_generation_pool(
        input_dir=input_dir,
        output_dir=output_dir,
        model_name=model_name,
        port=port,
        generate_num=generate_num,
        w_code=w_code,
        task_num=task_num,
        task_idx=task_idx,
        lang=lang,
        prompting=prompting
    )
