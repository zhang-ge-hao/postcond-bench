from __future__ import annotations

import asyncio
from typing import Optional, Any, AsyncIterator

from autogen_agentchat.agents import AssistantAgent

from src.ds import Method
from src.util import read_code  # read_code(path) -> (code_str, code_bytes)
from src.agent.proto_v2.models import client  # your vLLM client factory


# ============================================================
# Prompt (hard-coded for: lang=python, prompting=v2-all)
# ============================================================

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

def grammar_agent() -> AssistantAgent:
    model_client = client("Qwen/Qwen3-32B", thinking=False)

    agent = AssistantAgent(
        name="grammar_assistant",
        model_client=model_client,
        system_message=GRAMMAR_SYSTEM_PROMPT,
    )
    return agent

