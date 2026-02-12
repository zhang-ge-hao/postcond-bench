from __future__ import annotations

from typing import List, Tuple
import random

from src.ds import Method
from src.mutation.mutmut import generate_mutants_for_method


def _splitlines_keepends(s: str) -> List[str]:
    # Like str.splitlines(True) but guarantees at least [] for empty.
    return s.splitlines(True)


def _ensure_trailing_newline_like(original_lines: List[str], replacement: str) -> str:
    """
    If the original replaced region ended with a newline, keep that property.
    This helps keep the file formatting stable.
    """
    if not original_lines:
        return replacement
    orig_ended_with_nl = original_lines[-1].endswith("\n") or original_lines[-1].endswith("\r\n")
    rep_ended_with_nl = replacement.endswith("\n") or replacement.endswith("\r\n")
    if orig_ended_with_nl and not rep_ended_with_nl:
        return replacement + "\n"
    return replacement


def _replace_line_range(
    file_content: str,
    start_line: int,  # 1-based inclusive
    end_line: int,    # 1-based inclusive
    replacement_block: str,
) -> str:
    lines = _splitlines_keepends(file_content)

    if start_line < 1 or end_line < start_line:
        raise ValueError(f"Invalid line range: start_line={start_line}, end_line={end_line}")
    if end_line > len(lines):
        raise ValueError(
            f"Line range out of bounds: start_line={start_line}, end_line={end_line}, "
            f"file has {len(lines)} lines"
        )

    # Convert to 0-based slice
    s = start_line - 1
    e = end_line  # exclusive

    original_slice = lines[s:e]
    replacement_block = _ensure_trailing_newline_like(original_slice, replacement_block)

    replacement_lines = _splitlines_keepends(replacement_block)

    new_lines = lines[:s] + replacement_lines + lines[e:]
    return "".join(new_lines)


def load_mutation(method: Method) -> None:
    """
    Populate:
      - method.file_content
      - method.mut_file_contents
      - method.mut_line_ranges

    Semantics:
      mut_file_contents[i] is file_content with method.content replaced by mutants[i]
      mut_line_ranges[i] is (start_line, end_line) of the mutant block inside mut_file_contents[i]
    """
    with open(method.file, "r", encoding="utf-8") as f:
        method.file_content = f.read()

    # Generate mutant blocks for the method code (assumed to be the same region as method.content)
    mutants: List[str] = list(generate_mutants_for_method(method.content))

    # filter out mutantion that applied on header part
    ignore_line_num = method.body_start_line - method.start_line
    src_lines = method.content.split("\n")[: ignore_line_num]
    for mut_idx in reversed(list(range(len(mutants)))):
        tgt_lines = mutants[mut_idx].split("\n")[: ignore_line_num]
        if src_lines != tgt_lines:
            mutants.pop(mut_idx)

    start_line = method.start_line
    end_line = method.end_line

    mut_file_contents: List[str] = []
    mut_line_ranges: List[Tuple[int, int]] = []

    for mut in mutants:
        new_file = _replace_line_range(
            file_content=method.file_content,
            start_line=start_line,
            end_line=end_line,
            replacement_block=mut,
        )
        mut_file_contents.append(new_file)

        mut_lines = mut.splitlines()
        new_end_line = start_line + len(mut_lines) - 1
        # Special case: mut == "" -> 0 lines; treat as empty block sitting on start_line-1
        # but usually mutants won’t be empty; keep a sensible invariant anyway.
        if len(mut_lines) == 0:
            new_end_line = start_line - 1

        mut_line_ranges.append((start_line, new_end_line))

    method.mutants_4a = mutants
    method.mut_files_4a = mut_file_contents
    method.mut_lines_4a = mut_line_ranges
