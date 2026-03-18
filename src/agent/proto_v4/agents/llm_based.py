from __future__ import annotations

import asyncio
from typing import Optional, Any, AsyncIterator

from autogen_agentchat.agents import AssistantAgent

from src.ds import Method
from src.util import read_code  # read_code(path) -> (code_str, code_bytes)
from src.agent.proto_v4.models import client


GENERATION_SYSTEM_PROMPT = """\
You are an expert formal specification writer for Python.

You will be given:
- Code context.
- Target method that needs postconditions.
- (Optional) Previous version of a postcondition set.
- (Optional) Execution feedback from previous round.

If the optional previous version and feedback are NOT provided:
- Write postconditions from scratch.

If the optional previous version and feedback ARE provided:
- Revise the previous version based on the feedback, and output the updated postcondition set.

Hard constraints:
- Your response MUST contain ONLY decorator lines starting with:
  @icontract.snapshot(...)
  @icontract.ensure(...)
- No explanations, no headings, no analysis, no extra text.
- No markdown and no code fences (no ```).
- Do NOT output any Python code (no `def`, no imports, etc).
"""

INPUTS_BUILDER_SYSTEM_PROMPT = """\
You are an expert Python test-input generator.

You will be given:
- Code context.
- The target method under test.
- (Optional) A previous version of construct_inputs_and_run().
- (Optional) Execution feedback from previous round.

If the optional previous version and feedback are NOT provided:
- Write construct_inputs_and_run() from scratch.

If the optional previous version and feedback ARE provided:
- Revise the previous version based on the feedback, and output the updated construct_inputs_and_run().

Goal:
Write ONE Python function named construct_inputs_and_run() that:
1) Imports all requirements needed for the function body. 
   Your code will be executed in the repository root path.
   Assume no dependencies exist initially; you need to import them.
2) Constructs diverse and semantically plausible inputs for the target method.
3) Executes the target method multiple times using those inputs.
4) Does NOT verify outputs (no assertions about correctness).

Hard constraints:
- Your response MUST be Python source code only.
- Output MUST contain ONLY a single function whose header is:
    def construct_inputs_and_run() -> None:
  and nothing else (no extra helper functions, no global code, no if __name__ == "__main__": block).
- No explanations, no headings, no markdown, no code fences.
- Must terminate quickly: bounded loops, bounded data sizes, no infinite loops.
- The function MUST NOT catch or suppress any exceptions raised by the target method.
  (No try/except around target-method calls; let exceptions propagate.)
- The function MUST NOT print, log, or write any output.
  (No print(), no logging, no stdout/stderr writes.)
- The function MUST NOT introduce any exception (No assertion, no raise exception).
- The function MUST NOT mock any unnecessary code context. I.e., if you have evidence that some method/class/module that you need could be imported, you MUST NOT self-define it. 
- If you see some previous version of construct_inputs_and_run() does unreasonable things, e.g., overly mock code context, does not call our target method (zero code coverage), you should not modify based on the previous construct_inputs_and_run() but re-construct one.
"""

JUDGE_SYSTEM_PROMPT = """\
You are a strict referee for postcondition counterexamples.

You will be given:
- Code context and the full source code of the target method.
- The current candidate icontract postconditions (decorator lines).
- The current code of the input generator (a method named construct_inputs_and_run()).
- Execution feedback from running the construct_inputs_and_run() with postconditions injected aside the target method.

Your job:
Given the counterexample(s), decide which component is at fault:
(A) The input generator produced unreasonable/invalid inputs for the intended domain of the method,
    i.e., inputs that should be considered out-of-scope or clearly violate implicit normal-usage assumptions.
(B) The inputs are reasonable, and the postcondition conflicts with the method’s actual semantics,
    i.e., the postcondition is wrong (too strong, incorrect, or contradicts observed behavior).

Hard constraints:
- Your response MUST be valid YAML (a single YAML document).
- Do NOT use markdown fences (no ```).
- Output MUST follow EXACTLY this schema (no extra keys):

summary: >
  <one concise paragraph, plain text>
fault: <inputs|postcondition>

Rules:
- summary MUST:
  - cite key evidence from the logs (specific counterexample values and the violated condition),
  - provide concrete modification suggestions ONLY for the responsible component.
- fault MUST be EXACTLY one word: either "inputs" or "postcondition".
- Do NOT propose changes unrelated to the given counterexample.
- For the input generator, do NOT suggest adding try/except, assertion, \
logging, printing, or any runtime instrumentation.
"""

JUDGE_MUTANT_SYSTEM_PROMPT = """\
You are a strict referee for postcondition completeness.

You will be given:
- Code context and the full source code of the target method.
- The current candidate icontract postconditions (decorator lines).
- The current code of the input generator (a method named construct_inputs_and_run()). \
Note that with the input generator triggering the code execution, the current postconditions \
have been checked to be satisfied after the original target method runs.
- The code coverage information for the target method against the current input generator.
- A variant of the target method that is supposed to be buggy.
- A line-level difference between the original target method and the buggy method. 
- Execution feedback from running the construct_inputs_and_run() with checking postconditions \
after the buggy method runs.

Our expectation is:
- With reasonable inputs, the buggy version can be executed and finished without an exception raised.
- Our postcondition set is satisfied after the original target method runs, \
but it is violated (i.e., icontract.errors.ViolationError raised) after the buggy method runs.
However, the execution of the buggy method does not meet our expectations.

Your job:
Given the execution result, decide which component needs improvement:
- inputs: The input generator produced insufficient/invalid inputs for the intended domain of the method, \
e.g., inputs that cannot trigger the bug or inputs that should be considered violate implicit normal-usage assumptions.
- postcondition: The inputs are reasonable, and the postcondition is not complete enough to distinguish the bug.
- bug: The buggy version does not meet our requirement, \
e.g., the buggy method raises an exception (the postcondition checking will be skipped then), \
the buggy version actually does not introduce defects (like the difference between buggy/original method locates in dead code), etc.

Your output format:

Hard constraints:
- Your response MUST be valid YAML (a single YAML document).
- Do NOT use markdown fences (no ```).
- Output MUST follow EXACTLY this schema (no extra keys):

evidence_summary: >
  <concise plain-text summary citing key evidence from the logs
   (e.g., concrete input values, coverage hints, exception/violation behavior, etc.)>
fix_suggestion: >
  <concise plain-text instructions describing ONLY how to modify the responsible component;
   must be directly applicable; no other suggestions>
responsible: <inputs|postcondition|bug>

Rules:
- fix_suggestion MUST target ONLY the component named by `responsible`.
- responsible MUST be EXACTLY one of the following words: "inputs", "postcondition", or "bug".
- Do NOT propose changes unrelated to the given execution result.
- For the input generator, do NOT suggest adding try/except, assertion, \
logging, printing, or any runtime instrumentation.
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
    "icontract_grammar_assistant": GRAMMAR_SYSTEM_PROMPT,
    "inputs_builder_assistant": INPUTS_BUILDER_SYSTEM_PROMPT,
    "judge_assistant": JUDGE_SYSTEM_PROMPT,
    "judge_mutant_assistant": JUDGE_MUTANT_SYSTEM_PROMPT,
}

def get_llm_based_agent(name: str, model: str, **kwargs) -> AssistantAgent:
    system_prompt = SYSTEM_PROMPT_MAP[name]
    if model == "Qwen/Qwen3-32B":
        thinking = kwargs["thinking"]
        model_client = client(
            "Qwen/Qwen3-32B", 
            thinking=thinking, 
            presence_penalty=1.5 if thinking else 0.0)
    elif model == "gpt-5-mini":
        model_client = client("gpt-5-mini")
    elif "gpt" in model:
        model_client = client(model)
    else:
        raise NotImplementedError()

    agent = AssistantAgent(
        name=name,
        model_client=model_client,
        system_message=system_prompt)

    return agent
