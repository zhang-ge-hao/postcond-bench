from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.agent.conf_sum.config import PrototypeConfig, default_conference_config
from src.agent.conf_sum.export import export_csv, export_jsonl, export_xlsx
from src.agent.conf_sum.resolvers.fse import FseResolver
from src.agent.conf_sum.resolvers.icml import IcmlResolver
from src.agent.conf_sum.resolvers.iclr import IclrResolver
from src.agent.conf_sum.resolvers.icse import IcseResolver
from src.agent.conf_sum.resolvers.neurips import NeuripsResolver


def _build_resolver(config: PrototypeConfig):
    conference_key = config.conference.name.casefold()
    if conference_key == "iclr":
        return IclrResolver(
            conference=config.conference,
            timeout_seconds=config.timeout_seconds,
            user_agent=config.user_agent,
            show_progress=config.show_progress,
        )
    if conference_key == "icml":
        return IcmlResolver(
            conference=config.conference,
            timeout_seconds=config.timeout_seconds,
            user_agent=config.user_agent,
            show_progress=config.show_progress,
        )
    if conference_key == "neurips":
        return NeuripsResolver(
            conference=config.conference,
            timeout_seconds=config.timeout_seconds,
            user_agent=config.user_agent,
            show_progress=config.show_progress,
        )
    if conference_key == "fse":
        return FseResolver(
            conference=config.conference,
            timeout_seconds=config.timeout_seconds,
            user_agent=config.user_agent,
            show_progress=config.show_progress,
        )
    if conference_key == "icse":
        return IcseResolver(
            conference=config.conference,
            timeout_seconds=config.timeout_seconds,
            user_agent=config.user_agent,
            show_progress=config.show_progress,
        )
    raise ValueError(f"Unsupported conference: {config.conference.name}")


def run_conference_latest_sample(config: PrototypeConfig) -> dict[str, str]:
    effective_config = config
    sample_size = None if effective_config.crawl_all else effective_config.sample_size
    output_stem = "all_papers" if effective_config.crawl_all else "latest_sample"
    resolver = _build_resolver(effective_config)
    result = resolver.resolve_latest_sample(sample_size=sample_size)

    output_dir = effective_config.output_dir
    csv_path = output_dir / f"{output_stem}.csv"
    jsonl_path = output_dir / f"{output_stem}.jsonl"
    xlsx_path = output_dir / f"{output_stem}.xlsx"
    run_log_path = output_dir / "run_log.json"

    export_csv(result.records, csv_path)
    export_jsonl(result.records, jsonl_path)
    export_xlsx(result.records, xlsx_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    run_log_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")

    return {
        "csv": str(csv_path),
        "jsonl": str(jsonl_path),
        "xlsx": str(xlsx_path),
        "run_log": str(run_log_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the conference summary prototype.")
    parser.add_argument("--conference", choices=["iclr", "icml", "neurips", "fse", "icse"], default="iclr")
    parser.add_argument("--sample-size", type=int, default=10)
    parser.add_argument("--all", action="store_true", help="Crawl all listed papers instead of sampling.")
    parser.add_argument("--no-progress", action="store_true", help="Disable the crawl progress bar.")
    parser.add_argument("--output-dir", default="data/conf_sum")
    args = parser.parse_args()

    config = default_conference_config(conference_key=args.conference, sample_size=args.sample_size, crawl_all=args.all)
    config = PrototypeConfig(
        conference=config.conference,
        sample_size=config.sample_size,
        crawl_all=config.crawl_all,
        timeout_seconds=config.timeout_seconds,
        user_agent=config.user_agent,
        show_progress=not args.no_progress,
        output_dir=Path(args.output_dir),
    )
    outputs = run_conference_latest_sample(config)
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()