from __future__ import annotations

import asyncio
from typing import Optional, Any, AsyncIterator

from autogen_agentchat.agents import AssistantAgent

from src.ds import Method
from src.util import read_code  # read_code(path) -> (code_str, code_bytes)
from src.agent.proto_v2.models import client  # your vLLM client factory


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

def completion_assistant() -> AssistantAgent:
    model_client = client("Qwen/Qwen3-32B", 
                          thinking=True, 
                          presence_penalty=1.5)

    agent = AssistantAgent(
        name="completion_assistant",
        model_client=model_client,
        system_message=COMPLETION_SYSTEM_PROMPT,
    )
    return agent

