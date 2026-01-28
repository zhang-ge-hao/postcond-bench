
import asyncio
import re
from typing import Sequence, Optional
from src.ds import *

from autogen_agentchat.agents import AssistantAgent, BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_core.models import ModelFamily

from src.agent.lint.icontract_lint import grammar_verify

FAIL_RESPONSE_TEMPLATE = """We found the icontract API usage or grammar mistake inside the generated postconditions.
Target method:
```
{method_content}
```
The set of icontract postconditions:
```
{attempt_postcond}
```
Error message:
```
{lint_message}
```
"""

PASS_RESPONSE_TEMPLATE = """No issues found from the generated postconditions in icontract API usage or grammar.
Target method:
```
{method_content}
```
The set of icontract postconditions:
```
{attempt_postcond}
```
"""


def extract_latest_postcond(
        messages: Sequence[BaseChatMessage], 
        source_names: List[str]) -> Optional[str]:
    for m in reversed(messages):
        if isinstance(m, TextMessage) and m.source in source_names:
            if isinstance(m.content, str):
                return m.content
    return None


class IcontractLintAgent(BaseChatAgent):
    def __init__(self, name: str, method_src: str, gen_agent_names: List[str]):
        super().__init__(name=name,
                         description=("An icontract lint tool. "
                                      "With method and a postcondition set "
                                      "inputted, this tool outputs a result "
                                      "message of icontract API usgae / grammar "
                                      "checking."))
        self._method_src = method_src
        self._gen_agent_names = gen_agent_names

    @property
    def produced_message_types(self):
        return (TextMessage,)

    async def on_messages(
            self, 
            messages: Sequence[BaseChatMessage],
            cancellation_token,) -> Response:
        postcond = extract_latest_postcond(
            messages, source_names=self._gen_agent_names)

        if not postcond:
            msg = TextMessage(
                source=self.name,
                content=(
                    "I did not receive any postcondition lines from the generator.\n"
                    "Please output ONLY @icontract.snapshot(...) and @icontract.ensure(...) lines."
                ),
            )
            return Response(chat_message=msg)

        lint_message = grammar_verify(self._method_src, postcond)

        if "No issues found" in lint_message:
            message_content = PASS_RESPONSE_TEMPLATE.format(
                method_content=self._method_src,
                attempt_postcond=postcond
            )
        else:
            message_content = FAIL_RESPONSE_TEMPLATE.format(
                method_content=self._method_src,
                attempt_postcond=postcond,
                lint_message=lint_message
            )
        return Response(chat_message=TextMessage(
            source=self.name, content=message_content))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        # 这个 verifier 没有状态；需要的话你也可以清空缓存
        return

