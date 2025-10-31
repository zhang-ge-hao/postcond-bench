# llmorpheus_mutator.py
import re
import ast
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set

from src.util import get_language_and_parser, parse_code, read_code
from src.clone import repository_reproduct
from src.ds import Method  # Repo is referenced within Method
from copy import deepcopy

from openai import OpenAI

from src.mutation.llm.find_lines import (
    find_placeholder_lines_python,
    find_placeholder_lines_java
)


PLACEHOLDER = "<PLACEHOLDER>"

# ------------------------------
# Prompt (adapted to method-level span, full-file context)
# ------------------------------
SYSTEM_PROMPT = (
    "You are an expert in mutation testing for software."
)

USER_PROMPT_TEMPLATE = (
    "```\n{code}```\n"
    "Above is a {lang} source code with one `<PLACEHOLDER>` marker. "
    "A `<PLACEHOLDER>` masks one line. "
    "Suppose we replace `<PLACEHOLDER>` to `{original}`, "
    "the code will be correct. "
    "Please generate exactly {per_site} alternative code lines. "
    "Each of them can play a similar role as the correct line `{original}`, "
    "but introduces defects. "
    "Note that after applying the returned code lines, the code "
    "should have buggy behavior "
    "but does NOT raise any compile error or exception during the "
    "`<PLACEHOLDER>` belonging method runs.\n"
    "The response template:\n"
    "```\n<alternative code line 1>\n```\n"
    "```\n<alternative code line 2>\n```\n"
    "```\n<alternative code line 3>\n```\n"
    "..."
)


# ------------------------------
# OpenAI client
# ------------------------------
class LLMClient:
    def __init__(self, model):
        self.client = OpenAI()
        self.model = model

    def gen_replacements(
            self, 
            lang: str, 
            code_w_ph: str, 
            orig_snippet: str,
            per_site=3) -> List[str]:
        user_prompt = USER_PROMPT_TEMPLATE.format(
            lang=lang,
            code=code_w_ph,
            original=orig_snippet,
            per_site=per_site
        )
        # # ===== DEBUG: prompt =====
        # print("===== DEBUG: prompt =====")
        # print(user_prompt)
        # # ===== END DEBUG =====
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )
        text = resp.choices[0].message.content or ""
        # # ===== DEBUG: response =====
        # print("===== DEBUG: response =====")
        # print(text)
        # # ===== END DEBUG =====
        ret = extract_code_fences(text)
        return ret


# ------------------------------
# Parse fences
# ------------------------------
def extract_code_fences(s: str) -> List[str]:
    ret = []
    closed = True
    for l in s.split("\n"):
        if l.startswith("```") and closed:
            ret.append([])
            closed = False
        elif l.startswith("```") and not closed:
            closed = True
        elif len(ret) > 0:
            ret[-1].append(l)
    return ["\n".join(r) for r in ret]

# ------------------------------
# Public API: mutate using Method (returns METHOD-LEVEL mutants)
# ------------------------------
def generate_mutants_for_method(
        method: Method, 
        per_site: int = 5, 
        model: str = "gpt-4o-mini") -> List[str]:
    """
    Given a Method object, returns METHOD-LEVEL mutants (List[str]).
    Flow:
      1) Parse method.content with tree-sitter and collect mutation spans (method scope only).
      2) For each span, apply <PLACEHOLDER> to the METHOD code (method_with_ph).
      3) Build prompts using the FULL FILE:
         - original_full_file = the original file text
         - context_full_with_ph = original full file with lines [start_line, end_line] replaced by method_with_ph
      4) Ask LLM for replacements; for each, replace <PLACEHOLDER> inside the METHOD-only text to obtain mutated_method.
      5) Validate by splicing mutated_method into the full file and parsing the whole file.
      6) Return unique mutated METHOD strings.
    """
    lang = method.repo.language.lower()
    if lang not in ("python", "java"):
        raise ValueError("repo.language must be 'python' or 'java'")

    # Load full file
    with repository_reproduct(method.repo) as repo_dir:
        file_code_str, _ = read_code(method.file)
    code_lines = file_code_str.split("\n")

    # LLM
    llm = LLMClient(model=model)

    mutants: List[str] = []

    if lang == "python":
        lines = find_placeholder_lines_python(file_code_str)
    elif lang == "java":
        lines = find_placeholder_lines_java(file_code_str)

    for line_idx_0b in lines:

        if not (line_idx_0b + 1 <= method.end_line \
                and line_idx_0b + 1 >= method.body_start_line):
            continue

        rep_code_lines = deepcopy(code_lines)
        ori_line = rep_code_lines[line_idx_0b]
        ori_indent = ori_line[: len(ori_line) - len(ori_line.lstrip())]
        ori_line_content = ori_line.lstrip()
        rep_code_lines[line_idx_0b] = ori_indent + PLACEHOLDER
        full_with_ph = "\n".join(rep_code_lines)

        if len([ch for ch in ori_line_content if ch.isalpha()]) == 0:
            continue

        replacements = llm.gen_replacements(
            lang=lang,
            code_w_ph=full_with_ph,
            orig_snippet=ori_line_content,
            per_site=per_site
        )

        for r in replacements[:per_site]:
            r = r.strip()
            mutant_code_lines = deepcopy(rep_code_lines)
            mutant_code_lines[line_idx_0b] = \
                mutant_code_lines[line_idx_0b].replace(PLACEHOLDER, r, 1)

            mutated_method = "\n".join(
                mutant_code_lines[method.start_line - 1: method.end_line])

            if mutated_method.strip() == method.content.strip():
                continue

            mutants.append(mutated_method)

    return mutants

