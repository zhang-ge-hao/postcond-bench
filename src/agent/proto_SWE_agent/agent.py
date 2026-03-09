from src.ds import *
from src.clone import repository_reproduct

import time, random
import re, subprocess
import asyncio, os
import yaml
from tqdm import tqdm

from typing import Tuple, Optional, Dict

from autogen_core import CancellationToken

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import SelectorGroupChat

from src.agent.lint.icontract_lint import grammar_verify

from src.util import get_diff

prompt_template = """\
Write a set of postconditions with icontract for method `{method_name}` in line {line} of `{file_path}`.

Your response MUST contain ONLY decorator lines starting with: `@icontract.snapshot(...)` and `@icontract.ensure(...)`. The generated postcondition should be correct and complete.

You should apply a minimal modification that only includes postcondition injection.
"""

command_template = """\
sweagent run \
  --agent.model.name=gpt-5-mini \
  --agent.model.completion_kwargs='{"reasoning_effort":"low","drop_params":true}' \
  --env.repo.path=. \
  --problem_statement.path=postcond.md \
  --env.deployment.image=python:3.12 \
  --env.deployment.type=modal
"""

async def run_agent(
    method: Method,
    model: str = "gpt-5-mini",
    max_rounds: int = 20,
    print_stdout: bool = False,
    mutant_sample_num: int = 5,
    collect_logs: bool = False,
) -> Tuple[str, List[dict], Optional[str]]:
    with open("postcond.md", "w") as file:
        file.write(prompt_template.format(method_name=method.name, 
                                          line=method.start_line, 
                                          file_path=method.file))
    time.sleep(1000000)


if __name__ == "__main__":
    method_path = "data/step/8.benchmark/keon--algorithms--hailstone.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))

    with repository_reproduct(method.repo) as repo_dir:
        model = "gpt-5-mini"

        print(repo_dir)

        postconditions, history = asyncio.run(
            run_agent(method, model, print_stdout=True))

        print(json.dumps(history, indent=2))
