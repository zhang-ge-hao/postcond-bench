from __future__ import annotations

import asyncio
from typing import Optional, Any, AsyncIterator

from autogen_agentchat.agents import AssistantAgent

from src.ds import Method
from src.util import read_code  # read_code(path) -> (code_str, code_bytes)
from src.agent.proto_v2.models import client  # your vLLM client factory


DIAGNOSIS_SYSTEM_PROMPT = """\
You are a code specification assistant.

You will be given:
- A Python method (source code).
- A set of icontract postconditions (decorator lines) suspected of being incorrect or incomplete.

Definitions:
- Correctness: the postconditions must hold after the correct method executes normally.
- Completeness: the postconditions should reject (be violated by) at least one plausible buggy implementation that changes the intended behavior.

Procedure:
1. Construct several representative input/pre-state situations (2~4), grounded in the given code and types.
2. For each situation, reason about the correct method's behavior and whether the postconditions would hold.
3. If you find any situation where the postconditions would be violated by the correct method, stop and report suspected incorrectness.
4. Otherwise, create one plausible buggy implementation by making an atomized change (exactly one local edit: replace/insert/delete a single line), keeping the signature unchanged and the code runnable.
5. Pick one representative situation and reason about the buggy behavior and whether the postconditions would still hold.
6. If the postconditions would still hold for the buggy implementation, stop and report suspected incompleteness.
7. Otherwise, output exactly: No issues found.

Hard constraints:
- If context is missing, make conservative assumptions and state them briefly in the trace.
- Do not output extra sections beyond the required report format.

Response format:
- If incorrectness:
  Input situation: (3~4 sentences)
  Trace: (3~4 sentences)
  Issue: (3~4 sentences explaining why this indicates incorrectness)
- If incompleteness:
  Input situation: (3~4 sentences)
  Buggy implementation: (show only the changed line in a small snippet)
  Trace: (3~4 sentences)
  Issue: (3~4 sentences explaining why this indicates incompleteness)
- Otherwise: one sentence only: No issues found.
"""

def diagnosis_assistant() -> AssistantAgent:
    model_client = client("Qwen/Qwen3-32B", 
                          thinking=True, 
                          presence_penalty=1.5)

    agent = AssistantAgent(
        name="diagnosis_assistant",
        model_client=model_client,
        system_message=DIAGNOSIS_SYSTEM_PROMPT,
    )
    return agent

