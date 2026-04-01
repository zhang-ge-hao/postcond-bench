import argparse
import json

from src.reasoning.native import (
    default_work_dir,
    evaluate_workflow,
    merge_batch_outputs,
    metric_workflow,
    prompt_workflow,
)
from src.reasoning.native.analysis import sample_trace_workflow


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    prompt_parser = subparsers.add_parser("prompt")
    prompt_parser.add_argument("--model_name", type=str, required=True)
    prompt_parser.add_argument("--task_num", type=int, default=1)
    prompt_parser.add_argument("--task_idx", type=int, default=0)
    prompt_parser.add_argument("--lang", type=str, default=None)
    prompt_parser.add_argument("--limit", type=int, default=None)
    prompt_parser.add_argument("--input_dir", type=str, default="data/reasoning/8.benchmark")
    prompt_parser.add_argument("--work_dir", type=str, default=None)

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("--work_dir", type=str, required=True)
    merge_parser.add_argument("--batch_output_path", type=str, required=True)

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("--work_dir", type=str, required=True)

    metric_parser = subparsers.add_parser("metric")
    metric_parser.add_argument("--work_dir", type=str, required=True)
    metric_parser.add_argument("--lang", type=str, default=None)

    sample_trace_parser = subparsers.add_parser("sample-traces")
    sample_trace_parser.add_argument("--work_dir", type=str, required=True)
    sample_trace_parser.add_argument("--output_dir", type=str, required=True)
    sample_trace_parser.add_argument("--passed_num", type=int, default=10)
    sample_trace_parser.add_argument("--non_passed_num", type=int, default=10)
    sample_trace_parser.add_argument("--lang", type=str, default=None)
    sample_trace_parser.add_argument("--seed", type=int, default=0)

    args = parser.parse_args()

    if args.command == "prompt":
        work_dir = args.work_dir or default_work_dir(args.model_name)
        result = prompt_workflow(
            input_dir=args.input_dir,
            work_dir=work_dir,
            model_name=args.model_name,
            task_num=args.task_num,
            task_idx=args.task_idx,
            lang=args.lang,
            limit=args.limit,
        )
    elif args.command == "merge":
        result = merge_batch_outputs(
            work_dir=args.work_dir,
            batch_output_path=args.batch_output_path,
        )
    elif args.command == "evaluate":
        result = evaluate_workflow(
            work_dir=args.work_dir,
        )
    elif args.command == "metric":
        result = metric_workflow(
            work_dir=args.work_dir,
            lang=args.lang,
        )
    elif args.command == "sample-traces":
        result = sample_trace_workflow(
            work_dir=args.work_dir,
            output_dir=args.output_dir,
            passed_num=args.passed_num,
            failed_num=args.non_passed_num,
            lang=args.lang,
            seed=args.seed,
        )
    else:
        raise NotImplementedError()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()