
from src.ds import *
from src.util import read_code
import asyncio

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import BaseChatMessage, TextMessage, StopMessage
from autogen_core import CancellationToken

from src.agent.proto_v2.agents import (
    get_llm_based_agent, 
    IcontractLintAgent
)

from autogen_agentchat.conditions._terminations import TerminationCondition


class MaxGrammarRetriesWithoutLintSuccessTermination(TerminationCondition):

    component_provider_override = "custom.MaxGrammarRetriesWithoutLintSuccessTermination"

    def __init__(
        self,
        grammar_source: str = "grammar_assistant",
        lint_source: str = "icontract_lint",
        lint_ok_phrase: str = "No issues found",
        max_retries: int = 10,
        stop_reason: str = "Reached grammar fix limit.",
    ):
        self.grammar_source = grammar_source
        self.lint_source = lint_source
        self.lint_ok_phrase = lint_ok_phrase
        self.max_retries = max_retries
        self.stop_reason = stop_reason

        self._terminated = False
        self._lint_ok_last = None   # None/True/False
        self._grammar_retries = 0
        self._last_seen_source = None

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def reset(self) -> None:
        self._terminated = False
        self._lint_ok_last = None
        self._grammar_retries = 0
        self._last_seen_source = None

    async def __call__(self, messages) -> StopMessage | None:
        if self._terminated:
            raise RuntimeError("Termination condition has already been reached.")

        # Process delta messages in order
        for m in messages:
            if not isinstance(m, BaseChatMessage):
                continue

            src = getattr(m, "source", None)
            text = getattr(m, "content", None) if isinstance(getattr(m, "content", None), str) else ""

            self._last_seen_source = src

            # Update lint status
            if src == self.lint_source:
                ok = (self.lint_ok_phrase in text)
                self._lint_ok_last = ok
                if ok:
                    # Lint passed -> reset retry counter
                    self._grammar_retries = 0

            # Count grammar retries only when we're in the "lint failing" loop
            if src == self.grammar_source:
                # Only count when the most recent lint result is explicitly failing
                if self._lint_ok_last is False:
                    self._grammar_retries += 1
                else:
                    # Grammar used not as part of lint-fail loop (rare in your selector),
                    # don't treat it as retry; reset to be safe.
                    self._grammar_retries = 0

        # Trigger: after the Nth grammar attempt, if lint still fails, you'll see a LINT fail.
        # So stop when we are at end-of-delta and last message is a failing lint.
        if (
            self._grammar_retries >= self.max_retries
            and self._last_seen_source == self.lint_source
            and self._lint_ok_last is False
        ):
            self._terminated = True
            return StopMessage(content=self.stop_reason, source="termination")

        return None


class MaxDiagnosisAboutToBeCalledTermination(TerminationCondition):
    """
    Allow diagnosis_assistant to respond at most `max_calls` times.
    Stop *before* the (max_calls+1)-th diagnosis would be selected.

    Important: TerminationCondition in AgentChat receives ONLY the delta messages
    since the last call, not the full history. So we keep internal counters.
    """

    component_provider_override = "custom.MaxDiagnosisAboutToBeCalledTermination"

    def __init__(
        self,
        diagnosis_source: str = "diagnosis_assistant",
        max_calls: int = 4,  # allow 4; stop before 5th
        gate_source: str = "icontract_lint",
        gate_phrase: str = "No issues found",
        stop_reason: str = "Reached diagnosis limit.",
    ):
        self.diagnosis_source = diagnosis_source
        self.max_calls = max_calls
        self.gate_source = gate_source
        self.gate_phrase = gate_phrase
        self.stop_reason = stop_reason

        self._terminated = False
        self._diag_calls = 0

    @property
    def terminated(self) -> bool:
        return self._terminated

    async def reset(self) -> None:
        self._terminated = False
        self._diag_calls = 0

    async def __call__(self, messages) -> StopMessage | None:
        if self._terminated:
            # Match the framework expectation: once terminated, don't evaluate again.
            raise RuntimeError("Termination condition has already been reached.")

        # 1) Count any diagnosis messages in this delta
        for m in messages:
            if isinstance(m, BaseChatMessage) and getattr(m, "source", None) == self.diagnosis_source:
                self._diag_calls += 1

        # 2) If we've already had 4 diagnosis outputs, and this delta includes a lint "No issues found",
        #    then selector would pick diagnosis next -> stop NOW.
        if self._diag_calls >= self.max_calls:
            for m in messages:
                if (
                    isinstance(m, BaseChatMessage)
                    and getattr(m, "source", None) == self.gate_source
                    and isinstance(getattr(m, "content", None), str)
                    and (self.gate_phrase in m.content)
                ):
                    self._terminated = True
                    return StopMessage(content=self.stop_reason, source="termination")

        return None


def _msg_text(m: Any) -> str:
    c = getattr(m, "content", None)
    return c if isinstance(c, str) else ""


def _contains_no_issues(messages: List[BaseChatMessage], source: str) -> bool:
    # find latest message from `source`
    for m in reversed(messages):
        if getattr(m, "source", None) == source and isinstance(getattr(m, "content", None), str):
            return "No issues found" in m.content
    return False


def _latest_from_sources(messages: List[BaseChatMessage], sources: List[str]) -> Optional[str]:
    for m in reversed(messages):
        if getattr(m, "source", None) in sources and isinstance(getattr(m, "content", None), str):
            return m.content
    return None


async def _run_one_agent(
    agent,
    messages: List[BaseChatMessage],
    *,
    stream_to_console: bool=False,
    stream_to_file: str=None,
) -> List[BaseChatMessage]:
    """
    Run one agent with the full shared messages as input.
    Append only the messages produced by this agent (to avoid duplicating input).
    Return the newly produced messages.
    """
    new_msgs: List[BaseChatMessage] = []
    cancel = CancellationToken()

    async for msg in agent.run_stream(task=messages, cancellation_token=cancel):
        # streaming print
        if stream_to_console:
            print(pretty_stream_message(msg))
        if stream_to_file:
            with open(stream_to_file, "a") as file:
                file.write(pretty_stream_message(msg) + "\n")

        # Only keep messages that are produced by this agent itself
        # (ignore echoed user/input messages if the runtime yields them)
        if getattr(msg, "source", None) == agent.name:
            new_msgs.append(msg)

    # extend shared history
    messages.extend(new_msgs)
    return new_msgs


TASK_PROMPT_TEMPLATE = (
    "Code Context:\n"
    "```\n"
    "{code_context}\n"
    "```\n"
    "Target Method:\n"
    "```\n"
    "{target_method}\n"
    "```\n"
    "Guideline:\n"
    "Above is the python code context and target method. "
    "You should generate icontract format postconditions for "
    "this method `{method_name}`.\n"
    "Try to generate correct and complete postconditions.\n"
)


def build_task_prompt(method: Method) -> str:

    lang = getattr(method.repo, "language", None)
    prompting = getattr(method, "prompting", None)
    if lang and lang != "python":
        raise ValueError(f"This agent only supports python, got: {lang!r}")
    if prompting and prompting != "v2-all":
        raise ValueError(f"This agent only supports prompting='v2-all', got: {prompting!r}")

    code_str, _ = read_code(method.file)
    code_context = code_str
    target_method = method.content

    return TASK_PROMPT_TEMPLATE.format(
        code_context=code_context,
        target_method=target_method,
        method_name=method.name,
    )


def pretty_stream_message(msg: Any) -> str:
    """
    Minimal console printing (so we don't rely on autogen_agentchat.ui.Console).
    """
    # Many AgentChat messages have fields: source, content
    source = getattr(msg, "source", None)
    content = getattr(msg, "content", None)

    result = []

    # Try to make it look similar to Console's essential output
    if isinstance(content, str) and content.strip():
        label = source or msg.__class__.__name__
        result.append(f"---------- {label} ----------")
        result.append(content)
    
    return "\n".join(result)


def _latest_text_from(history: list[BaseChatMessage], source: str) -> str | None:
    for m in reversed(history):
        if getattr(m, "source", None) == source and isinstance(getattr(m, "content", None), str):
            return m.content
    return None

def _contains_no_issues_from(history: list[BaseChatMessage], source: str) -> bool:
    text = _latest_text_from(history, source)
    return bool(text) and ("No issues found" in text)

def build_selector_func():
    """
    Deterministic state machine encoded as selector_func(history)-> next_speaker_name.
    history is Sequence[BaseAgentEvent | BaseChatMessage], we only care BaseChatMessage.
    """
    GEN = "generation_assistant"
    LINT = "icontract_lint"
    GRAM = "grammar_assistant"
    DIAG = "diagnosis_assistant"
    COMP = "completion_assistant"

    def selector(history):
        # Filter only chat messages
        msgs = [m for m in history if isinstance(m, BaseChatMessage)]

        # find last speaker
        last = None
        for m in reversed(msgs):
            s = getattr(m, "source", None)
            if s:
                last = s
                break

        # If nothing yet (only initial user task), start with generation
        if last is None or last == "user":
            return GEN

        # After generation/grammar/completion => lint
        if last in (GEN, GRAM, COMP):
            return LINT

        # After lint => if ok then diagnosis else grammar
        if last == LINT:
            if _contains_no_issues_from(msgs, LINT):
                return DIAG
            return GRAM

        # After diagnosis => if ok then (let termination end), else completion
        if last == DIAG:
            if _contains_no_issues_from(msgs, DIAG):
                # return value here doesn't matter if termination triggers;
                # but to be safe, keep returning DIAG or GEN is pointless.
                return DIAG
            return COMP

        # Fallback: go to lint
        return LINT

    return selector


def history_to_role_content_dicts(history: list[BaseChatMessage]) -> list[dict]:
    out: list[dict] = []
    for m in history:
        content = getattr(m, "content", None)
        if not isinstance(content, str) or not content.strip():
            continue
        src = getattr(m, "source", None)
        out.append({"role": src, "content": content})
    return out


async def run_agent(
    method: Method,
    stream_to_console: bool = False,
    stream_to_file: str | None = None):
    model = "Qwen/Qwen3-32B"

    generation = get_llm_based_agent("generation_assistant", model=model, thinking=True)
    diagnosis = get_llm_based_agent("diagnosis_assistant", model=model, thinking=False)
    completion = get_llm_based_agent("completion_assistant", model=model, thinking=False)
    grammar = get_llm_based_agent("grammar_assistant", model=model, thinking=False)

    lint = IcontractLintAgent(
        "icontract_lint",
        method_src=method.content,
        gen_agent_names=["generation_assistant", "completion_assistant", "grammar_assistant"],
    )

    # ---- termination: diagnosis says "No issues found" OR safety cap ----
    termination = (
        TextMentionTermination("No issues found", sources=["diagnosis_assistant"])
        | MaxDiagnosisAboutToBeCalledTermination(max_calls=2,)
        | MaxGrammarRetriesWithoutLintSuccessTermination(max_retries=10,)
        | MaxMessageTermination(max_messages=200)
    )

    # ---- SelectorGroupChat requires a model_client for speaker selection even if selector_func is provided. ----
    # Best effort: reuse an existing model_client from one of your LLM agents.
    selector_model_client = getattr(generation, "_model_client", None)
    if selector_model_client is None:
        raise RuntimeError(
            "Cannot find model_client on generation agent. "
            "Create a ChatCompletionClient (e.g., OpenAIChatCompletionClient) and pass it to SelectorGroupChat."
        )

    team = SelectorGroupChat(
        participants=[generation, lint, grammar, diagnosis, completion],
        model_client=selector_model_client,
        selector_func=build_selector_func(),
        allow_repeated_speaker=True,     # your workflow may bounce lint/grammar a lot
        termination_condition=termination,
        max_turns=200,
    )  # :contentReference[oaicite:4]{index=4}

    task_prompt = build_task_prompt(method)
    task_msg = TextMessage(source="user", content=task_prompt)

    final_result = None
    async for item in team.run_stream(task=task_msg):
        # item can be BaseChatMessage / BaseAgentEvent / TaskResult :contentReference[oaicite:5]{index=5}
        if stream_to_console and isinstance(item, BaseChatMessage):
            print(pretty_stream_message(item))
        if stream_to_file and isinstance(item, BaseChatMessage):
            with open(stream_to_file, "a") as f:
                f.write(pretty_stream_message(item) + "\n")

        # TaskResult is yielded as the last item
        if item.__class__.__name__ == "TaskResult":
            final_result = item

    if final_result is None:
        raise RuntimeError("Team did not yield TaskResult; unexpected termination.")

    # Extract latest postconditions from generation/completion/grammar
    history = getattr(final_result, "messages", None) or []
    for src in ["grammar_assistant", "completion_assistant", "generation_assistant"]:
        text = _latest_text_from(history, src)
        if text:
            return text, history_to_role_content_dicts(history)

    raise RuntimeError("Terminated but cannot find any generated postconditions in final history.")


if __name__ == "__main__":
    import json
    from src.clone import repository_reproduct
    import os

    method_path = "data/step/8.benchmark/a2aproject--a2a-python--append_artifact_to_task.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))

    stream_to_file = os.path.join(os.getcwd(), "data", "anno", "agent.log")

    with repository_reproduct(method.repo) as repo_dir:
        asyncio.run(run_agent(method, 
                              stream_to_console=True,
                              stream_to_file=stream_to_file))
