from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable

from src.ds import Method


DEFAULT_MUTATION_DIR = Path("data/step/6.mutation")
DEFAULT_BENCHMARK_DIR = Path("data/step/8.benchmark")
TARGET_LANGUAGES = ("python", "java")


def iter_methods(directory: Path) -> Iterable[Method]:
    for path in sorted(directory.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            yield Method.from_dict(json.load(handle))
    for path in sorted(directory.glob("*.jsonl")):
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                yield Method.from_dict(json.loads(line.strip()))


def collect_repositories(directory: Path) -> set[str]:
    return {method.repo.github_path for method in iter_methods(directory)}


def summarize_mutation_pool(
    raw_data_dir: Path = DEFAULT_MUTATION_DIR,
    benchmark_dir: Path = DEFAULT_BENCHMARK_DIR,
) -> Dict[str, Dict[str, int]]:
    excluded_repositories = collect_repositories(benchmark_dir)
    methods_by_language: dict[str, int] = defaultdict(int)
    repositories_by_language: dict[str, set[str]] = defaultdict(set)

    for method in iter_methods(raw_data_dir):
        language = method.repo.language.lower()
        if language not in TARGET_LANGUAGES:
            continue
        if method.repo.github_path in excluded_repositories:
            continue
        methods_by_language[language] += 1
        repositories_by_language[language].add(method.repo.github_path)

    summary: Dict[str, Dict[str, int]] = {}
    for language in TARGET_LANGUAGES:
        summary[language] = {
            "method_count": methods_by_language[language],
            "repository_count": len(repositories_by_language[language]),
            "excluded_repository_count": len(excluded_repositories),
        }
    for _, repos in repositories_by_language.items():
        for repo in repos:
            print(repo)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Count methods and repositories in data/step/6.mutation after excluding "
            "repositories that appear in data/step/8.benchmark."
        )
    )
    parser.add_argument(
        "--raw-data-dir",
        type=Path,
        default=DEFAULT_MUTATION_DIR,
        help="Directory containing mutation-stage method JSON files.",
    )
    parser.add_argument(
        "--benchmark-dir",
        type=Path,
        default=DEFAULT_BENCHMARK_DIR,
        help="Directory containing benchmark-stage method JSON files.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the summary as JSON.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = summarize_mutation_pool(
        raw_data_dir=args.raw_data_dir,
        benchmark_dir=args.benchmark_dir,
    )

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    excluded_repositories = collect_repositories(args.benchmark_dir)
    print(
        "Excluded repositories from benchmark:",
        len(excluded_repositories),
    )
    for language in TARGET_LANGUAGES:
        stats = summary[language]
        print(f"{language.capitalize()} methods: {stats['method_count']}")
        print(f"{language.capitalize()} repositories: {stats['repository_count']}")


if __name__ == "__main__":
    main()