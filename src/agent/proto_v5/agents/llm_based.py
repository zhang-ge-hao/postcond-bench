from __future__ import annotations

from autogen_agentchat.agents import AssistantAgent

from src.agent.proto_v4.models import client


POSTCONDITION_SYSTEM_PROMPT = """\
You are an expert formal specification writer for Python.

You will be given:
- Code context.
- The target method.
- The current accepted inputs program.
- Optional current postconditions.
- Optional execution or lint feedback.

Goal:
Write postconditions that satisfy all of the following:
1) They pass icontract lint.
2) They do not raise an exception after the original target method runs on the given inputs.
3) They raise icontract.errors.ViolationError after buggy mutants run on the given inputs.

Hard constraints:
- Your response MUST contain ONLY decorator lines starting with:
  @icontract.snapshot(...)
  @icontract.ensure(...)
- No explanations, no headings, no analysis, no extra text.
- No markdown and no code fences.
- Do NOT output any Python code such as def or import.
"""


INPUTS_BUILDER_SYSTEM_PROMPT = """\
You are an expert Python input generator.

You will be given:
- Code context.
- The target method under test.
- Optional accepted inputs program that already works.
- Optional latest candidate inputs function.
- Optional feedback from execution.

Goal:
Write ONE Python function named construct_inputs_and_run() that:
1) Calls the target method multiple times with strong and diverse inputs.
2) Helps cover more statements in the target method.
3) Does not verify outputs.

Important notes:
- If an accepted inputs program is provided, your new function will run together with it.
- In that case, focus on NEW and STRONGER cases.
- If a latest candidate inputs function is provided, it is the most recent trial that was not accepted yet.
- Use it with the execution feedback to understand what failed and how to improve the next version.
- Do not depend on print output.

Hard constraints:
- Your response MUST be Python source code only.
- Output MUST contain ONLY a single function whose header is:
    def construct_inputs_and_run() -> None:
- No extra helper functions, no global code, no if __name__ == "__main__": block.
- No explanations, no headings, no markdown, no code fences.
- Must terminate quickly: bounded loops, bounded data sizes, no infinite loops.
- The function MUST NOT catch or suppress exceptions raised by the target method.
- The function MUST NOT print, log, or write any output.
- The function MUST NOT use assert or raise.
- If code from the repository can be imported, import it instead of mocking it.
"""


SYSTEM_PROMPT_MAP = {
    "postcondition_assistant": POSTCONDITION_SYSTEM_PROMPT,
    "inputs_builder_assistant": INPUTS_BUILDER_SYSTEM_PROMPT,
}


def get_llm_based_agent(name: str, model: str, **kwargs) -> AssistantAgent:
    system_prompt = SYSTEM_PROMPT_MAP[name]
    if model == "Qwen/Qwen3-32B":
        thinking = kwargs.get("thinking", False)
        model_client = client(
            "Qwen/Qwen3-32B",
            thinking=thinking,
            presence_penalty=1.5 if thinking else 0.0,
        )
    elif model == "gpt-5-mini":
        model_client = client("gpt-5-mini")
    elif "gpt" in model:
        model_client = client(model)
    else:
        raise NotImplementedError()

    return AssistantAgent(
        name=name,
        model_client=model_client,
        system_message=system_prompt,
    )