import argparse
import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.clone import repository_reproduct
from src.ds import Method
from src.reasoning.eval.__main__ import build_prompt, generate_postcondition_responses


def read_benchmark(input_dir: str) -> list[Method]:
    methods: list[Method] = []
    for file_name in sorted(os.listdir(input_dir)):
        if not file_name.endswith(".json"):
            continue
        file_path = os.path.join(input_dir, file_name)
        with open(file_path) as file:
            methods.append(Method.from_dict(json.load(file)))
    return methods


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Construct real baseline prompts and print vLLM reasoning/response outputs.",
    )
    parser.add_argument("--input_dir", default="data/step/8.benchmark")
    parser.add_argument("--server_url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model_name", default="placeholder-vllm-model")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--generate_num", type=int, default=1)
    parser.add_argument("--lang", default="python")
    parser.add_argument("--github_path", default=None)
    parser.add_argument("--rlid", default=None)
    return parser


def select_methods(
    input_dir: str,
    lang: str | None,
    github_path: str | None,
    rlid: str | None,
    limit: int,
) -> list[Method]:
    selected = []
    for method in read_benchmark(input_dir):
        if lang is not None and method.repo.language != lang:
            continue
        if github_path is not None and method.repo.github_path != github_path:
            continue
        if rlid is not None and method.rlid != rlid:
            continue
        selected.append(method)
        if len(selected) >= limit:
            break
    return selected


def main() -> None:
    args = build_parser().parse_args()
    methods = select_methods(
        input_dir=args.input_dir,
        lang=args.lang,
        github_path=args.github_path,
        rlid=args.rlid,
        limit=args.limit,
    )

    if not methods:
        raise SystemExit("No matching methods found.")

    for index, method in enumerate(methods, start=1):
        method.generate_num = args.generate_num
        with repository_reproduct(method.repo):
            method.prompt = build_prompt(method, "baseline")

        responses = generate_postcondition_responses(
            method=method,
            server_url=args.server_url,
            model_name=args.model_name,
        )

        print(f"===== Method {index} =====")
        print(f"repo: {method.repo.github_path}")
        print(f"rlid: {method.rlid}")
        print(f"model: {method.model_name}")
        print(f"prompt_chars: {len(method.prompt)}")
        print("----- Prompt Prefix -----")
        print(method.prompt[:1200])

        for sample_idx, (thought, response) in enumerate(zip(method.thoughts or [], responses), start=1):
            print(f"----- Sample {sample_idx} Reasoning -----")
            print(thought)
            print(f"----- Sample {sample_idx} Response -----")
            print(response)


if __name__ == "__main__":
    main()