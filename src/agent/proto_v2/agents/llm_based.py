from __future__ import annotations

import asyncio
from typing import Optional, Any, AsyncIterator

from autogen_agentchat.agents import AssistantAgent

from src.ds import Method
from src.util import read_code  # read_code(path) -> (code_str, code_bytes)
from src.agent.proto_v2.models import client  # your vLLM client factory


GENERATION_SYSTEM_PROMPT = """\
You are an expert formal specification writer for Python.

You must generate ONE candidate set of icontract postconditions for the given target method.

Hard constraints:
- Your response MUST contain ONLY decorator lines starting with:
  @icontract.snapshot(...)
  @icontract.ensure(...)
- No explanations, no headings, no analysis, no extra text.
- No markdown and no code fences (no ```).
- Do NOT output any Python code (no `def`, no imports, etc).
"""

DIAGNOSIS_SYSTEM_PROMPT = """\
You are a code specification assistant.

Input:
- A Python method (source code).
- A set of icontract postconditions (decorator lines).

Task:
Write a 3-part response.

1) Buggy implementation:
- Create ONE plausible buggy version of the method by making EXACTLY ONE local edit: replace OR insert OR delete a single line.
- Keep the same signature, keep the code runnable.
- Output the full buggy method code (only the method; no extra text).

2) Analysis:
- Construct 2~4 representative input/pre-state situations grounded in the code and types (state any conservative assumptions if needed).
- For each situation, explain the expected behavior of the original method (normal return only) and whether the given postconditions would hold.
- Pick ONE of those situations and compare original vs buggy behavior.
- Decide whether the postconditions' satisfaction outcome changes between original and buggy (i.e., passes vs fails).

3) Conclusion:
- If the satisfaction outcome CHANGES between original and buggy, output exactly: No issues found.
- If the satisfaction outcome DOES NOT CHANGE, output exactly: Suspected incomplete.

Hard constraints:
- Put the reasoning explicitly in Analysis.
- Do not add any extra sections besides Buggy implementation/Analysis/Conclusion.
- Keep the Analysis concise but complete enough to justify the conclusion.
- The Conclusion can only be "No issues found" or "Suspected incomplete".
"""

COMPLETION_SYSTEM_PROMPT = """\
You are a code specification assistant.

You will be given (from icontract lint):
- a Python method
- a set of icontract postconditions (decorator lines) that is suspected of being incorrect or incomplete
- a report from a postcondition diagnose assistant

Definitions:
- Correctness: the postconditions must hold after the correct method executes normally.
- Completeness: the postconditions should reject (be violated by) at least one plausible buggy implementation that changes the intended behavior.

Goal:
Modify the current postcondition set. 
You should response a complete postcondition set.

Hard constraints:
- Your response MUST contain ONLY decorator lines starting with:
  @icontract.snapshot(...)
  @icontract.ensure(...)
- No explanations, no headings, no analysis, no extra text.
- No markdown and no code fences (no ```).
- Do NOT output any Python code (no `def`, no imports, etc).
"""

GRAMMAR_SYSTEM_PROMPT = """\
You are a code specification assistant.

You will be given (from icontract lint):
- a Python method
- a set of icontract postconditions (decorator lines) that have API usage / grammar problems
- an error message from icontract lint

Goal:
Fix ONLY icontract API usage / grammar problems in the postconditions.

Hard constraints:
- Your response MUST contain ONLY decorator lines starting with:
  @icontract.snapshot(...)
  @icontract.ensure(...)
- No explanations, no headings, no analysis, no extra text.
- No markdown and no code fences (no ```).
- Do NOT output any Python code (no `def`, no imports, etc).
- Keep the intended semantics the same as much as possible; change only what is necessary to fix grammar/API usage.
"""

SYSTEM_PROMPT_MAP = {
    "generation_assistant": GENERATION_SYSTEM_PROMPT,
    "diagnosis_assistant": DIAGNOSIS_SYSTEM_PROMPT,
    "completion_assistant": COMPLETION_SYSTEM_PROMPT,
    "grammar_assistant": GRAMMAR_SYSTEM_PROMPT,
}

def get_llm_based_agent(name: str, model: str, thinking: bool) -> AssistantAgent:
    system_prompt = SYSTEM_PROMPT_MAP[name]
    if model == "Qwen/Qwen3-32B":
        model_client = client(
            "Qwen/Qwen3-32B", 
            thinking=thinking, 
            presence_penalty=1.5 if thinking else 0.0)
    else:
        raise NotImplementedError()

    agent = AssistantAgent(
        name=name,
        model_client=model_client,
        system_message=system_prompt)

    return agent
