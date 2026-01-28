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


def generation_agent() -> AssistantAgent:
    model_client = client("Qwen/Qwen3-32B", 
                          thinking=True, 
                          presence_penalty=1.5)

    agent = AssistantAgent(
        name="generation_assistant",
        model_client=model_client,
        system_message=GENERATION_SYSTEM_PROMPT,
    )
    return agent

