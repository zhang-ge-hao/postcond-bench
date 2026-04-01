import argparse
import json

from src.reasoning.native import default_work_dir
from src.reasoning.native.analysis import sample_trace_workflow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="deepseek-reasoner")
    parser.add_argument("--work_dir", type=str, default=None)
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
    )
    parser.add_argument("--passed_num", type=int, default=10)
    parser.add_argument("--non_passed_num", type=int, default=10)
    parser.add_argument("--lang", type=str, default=None)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    work_dir = args.work_dir or default_work_dir(args.model_name)
    output_dir = args.output_dir or f"{work_dir}/analysis"

    result = sample_trace_workflow(
        work_dir=work_dir,
        output_dir=output_dir,
        passed_num=args.passed_num,
        failed_num=args.non_passed_num,
        lang=args.lang,
        seed=args.seed,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()