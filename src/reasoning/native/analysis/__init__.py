import os
import random
from typing import Dict, List

from src.reasoning.native import (
    NO_REASONING_TRACE,
    _iter_method_files,
    _load_method_file,
)


def _sanitize_flag(flag: str) -> str:
    if flag is None:
        return "unknown"
    return flag.replace("/", "_").replace(" ", "_")


def _sanitize_name(value: str) -> str:
    return value.replace("/", "--")


def _trace_output_name(item: Dict) -> str:
    corr_flag = _sanitize_flag(item["corr_flag"])
    repo_name = _sanitize_name(item["repo_name"])
    method_id = _sanitize_name(item["method_id"])
    candidate_idx = item["candidate_idx"]
    return f"{corr_flag}__{repo_name}--{method_id}__cand{candidate_idx}.md"


def _trace_text(item: Dict) -> str:
    sections = [
        "# Trace Sample",
        "",
        "## Metadata",
        f"- repo: {item['repo_name']}",
        f"- method_id: {item['method_id']}",
        f"- github_url: {item['github_url']}",
        f"- candidate_idx: {item['candidate_idx']}",
        f"- corr_flag: {item['corr_flag']}",
        "",
        "## Trace",
        "```text",
        item["thought"] or "",
        "```",
    ]

    if item.get("response"):
        sections.extend([
            "",
            "## Response",
            "```text",
            item["response"],
            "```",
        ])

    sections.extend([
        "",
        "## Incorr Msg",
        "```text",
        item["incorr_msg"] or "",
        "```",
    ])

    sections.extend([
        "",
        "## Reference",
        "```text",
        item["reference"] or "",
        "```",
    ])

    return "\n".join(sections).rstrip() + "\n"


def _collect_trace_items(work_dir: str, lang: str = None) -> List[Dict]:
    items: List[Dict] = []
    for method_path in _iter_method_files(work_dir):
        method = _load_method_file(method_path)
        if lang is not None and method.repo.language != lang:
            continue
        if method.postcond_corr is None:
            continue
        if method.thoughts is None:
            thoughts = [NO_REASONING_TRACE] * len(method.postcond_corr)
        else:
            thoughts = method.thoughts
        if method.responses is None:
            responses = [None] * len(method.postcond_corr)
        else:
            responses = method.responses
        if method.incorr_msgs is None:
            incorr_msgs = [None] * len(method.postcond_corr)
        else:
            incorr_msgs = method.incorr_msgs
        reference = method.ref_postcond
        for candidate_idx, (corr_flag, thought, response, incorr_msg) in enumerate(
            zip(method.postcond_corr, thoughts, responses, incorr_msgs)
        ):
            if thought is None or corr_flag is None:
                continue
            items.append({
                "repo_name": method.repo.github_path,
                "method_id": method.rlid,
                "github_url": method.github_url,
                "candidate_idx": candidate_idx,
                "corr_flag": corr_flag,
                "thought": thought,
                "incorr_msg": incorr_msg,
                "response": response,
                "reference": reference
            })
    return items


def sample_trace_workflow(
        work_dir: str,
        output_dir: str,
        passed_num: int = 10,
        failed_num: int = 10,
    lang: str = None,
        seed: int = 0) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    removed_files = []
    for file_name in os.listdir(output_dir):
        if not file_name.endswith(".txt") and not file_name.endswith(".md"):
            continue
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            removed_files.append(file_path)

    items = _collect_trace_items(work_dir, lang=lang)
    passed_items = [item for item in items if item["corr_flag"] == "passed"]
    non_passed_items = [item for item in items if item["corr_flag"] != "passed"]

    if len(passed_items) < passed_num:
        raise RuntimeError(f"Not enough passed traces: need {passed_num}, got {len(passed_items)}")
    if len(non_passed_items) < failed_num:
        raise RuntimeError(
            f"Not enough non-passed traces: need {failed_num}, got {len(non_passed_items)}"
        )

    rng = random.Random(seed)
    selected_passed = rng.sample(passed_items, passed_num)
    selected_non_passed = rng.sample(non_passed_items, failed_num)
    selected_items = selected_passed + selected_non_passed

    written_files = []
    for item in selected_items:
        output_name = _trace_output_name(item)
        output_path = os.path.join(output_dir, output_name)
        with open(output_path, "w") as file:
            file.write(_trace_text(item))
        written_files.append(output_path)

    written_files.sort()
    return {
        "work_dir": work_dir,
        "output_dir": output_dir,
        "lang": lang,
        "seed": seed,
        "passed_count": passed_num,
        "non_passed_count": failed_num,
        "removed_files": sorted(removed_files),
        "written_files": written_files,
    }