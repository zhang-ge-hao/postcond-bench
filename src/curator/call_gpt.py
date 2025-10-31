
import json
from openai import OpenAI
import os
import time

from src.ds import *
from src.util import create_tempdir

from src.curator.mutant_doc import get_mutant_doc
from src.curator.zip_download import download_github_commit_zip

from src.curator.eval_postcond import eval_postcond

import logging

ICONTRACT_EXAMPLES = """
# icontract Grammar Examples

Here are some examples that use `@icontract.ensure` and `@icontract.snapshot`:

Code with postcondition:
```python
import icontract
from typing import List

@icontract.snapshot(lambda lst: lst[:])
@icontract.ensure(lambda OLD, lst, value: lst == OLD.lst + [value])
def some_func(lst: List[int], value: int) -> None:
    lst.append(value)
    lst.append(1984)  # bug

some_func(lst=[1, 2], value=3)
```

Result:
```
Traceback (most recent call last):
  ...
icontract.errors.ViolationError: File /tmp/tmp.py, line 5 in <module>:
lst == OLD.lst + [value]:
OLD was a bunch of OLD values
OLD.lst was [1, 2]
lst was [1, 2, 3, 1984]
result was None
value was 3
```

Code with postcondition:
```python
@icontract.ensure(lambda result, x: result > x)
def some_func(x: int, y: int = 5) -> int:
    return x - y

some_func(x=10)
```

Result:
```
Traceback (most recent call last):
  ...
icontract.errors.ViolationError: File /tmp/tmp.py, line 4 in <module>:
result > x:
result was 5
x was 10
y was 5
```

Here are some examples that use variable positional and keyword arguments:

Code with postcondition:
```
@icontract.snapshot(lambda _ARGS: _ARGS[0], name="a0")
@icontract.ensure(lambda OLD: OLD.a0 == 0)
def function_a(*args) -> int:
    return 123

function_a(1)
```

Result:
```
Traceback (most recent call last):
  ...
icontract.errors.ViolationError: File /tmp/tmp.py, line 5 in <module>:
OLD.a0 == 0:
OLD was a bunch of OLD values
OLD.a0 was 1
args was 1
result was 123
```

Code with postcondition:
```
@icontract.snapshot(lambda _KWARGS: _KWARGS["x"], name="ax")
@icontract.ensure(lambda OLD: OLD.ax == 0)
def function_a(**kwargs) -> int:
    return 123

function_a(x=1)
```

Result:
```
Traceback (most recent call last):
  ...
icontract.errors.ViolationError: File /tmp/tmp.py, line 5 in <module>:
OLD.ax == 0:
OLD was a bunch of OLD values
OLD.ax was 1
result was 123
x was 1
```
"""

JML_EXAMPLES = """
# JML Grammar

An ensures clause states a postcondition for a method.
That is, the given predicate must be true just at any return statement in the method body (with any returned value substituted for \\result) and may be assumed by the caller after the call. 

The \old expression enables referring to the value of an expression in a previous program state.

Examples:

```
//@ ensures \\result == my_minutes;
public int minutes() {return my_minutes;}
```

```
//@ ensures \old(my_seconds) + 1 < SECS_IN_MIN ==> my_seconds == \old(my_seconds) + 1;
public void tick() {
    my_seconds += 1;
    if (my_seconds >= SECS_IN_MIN) {my_minutes += 1; my_seconds = 0;}
    if (my_minutes >= MINS_IN_HOUR) {my_hours += 1; my_minutes = 0;}
    if (my_hours >= HOURS_IN_DAY) {my_hours = 0;}
}
```

Note that you are only allowed to use the subset of JML grammar:
- `//@ ensures <jml-expression>`
- `\\result`
- `\old(<expression>)`
- `==>`, `<==>` and `<=!=>`

Do NOT use JML quantified expressions, like `\\forall` or `\\exists`. You can use Java native grammars, like Java Streams, to replace them.
"""

ICONTRACT_TARGET_DESC = "`@icontract.ensure` and `@icontract.snapshot` lines"

JML_TARGET_DESC = "JML `ensures` lines with leading `//@ ensures`"

PROMPT_TEMPLATE = (
    "{mutants}\n"
    "{grammar_examples}\n"
    "# Guideline\n"
    "{repo_zip_file_name} includes a {lang} repository. "
    "You can use `code_interpreter` tool to locate the code context. "
    "Now we need to write {dsl_name} postconditions for "
    "method `{method_path}` (line numbers start from 1). "
    "The above includes mutants for the target method.\n"
    "Try to generate correct and complete postconditions. "
    "Our goal is that the postconditions are always satisfied after the original method runs, "
    "but not satisfied after the mutants run, i.e., can kill all the mutants.\n"
    "Note that your response should only contain {target_desc}."
)

PROMPT_TEMPLATE_FOLLOWING_ERROR = (
    "```\n{stdout}\n```\n"
    "Run test suite with postcondition injected, failed. "
    "The running message is above. "
    "Please analyze and regenerate the postconditions following "
    "the same requirement."
)

PROMPT_TEMPLATE_FOLLOWING_MUT_SUV = (
    "Run test suite on correct code with postcondition injected, passed. "
    "However, the postcondition you generated cannot kill (distinguish) all mutants. "
    "The mutants that cannot be killed: {mutants}."
)


def _post_process(resp_str: str) -> str:
    lines = []
    inner = False
    for l in resp_str.split("\n"):
        if "```".startswith(l):
            inner = not inner
        elif inner:
            lines.append(l)
    if lines:
        return "\n".join(lines)
    else:
        return resp_str


def call_gpt(method: Method, output_path: str=None) -> Method:

    def _save_m(method: Method, output_path: str):
        if output_path is not None:
            with open(output_path, "w") as file:
                json.dump(method.to_dict(), file, indent=2)

    client = OpenAI()

    github_path = method.repo.github_path
    commit = method.repo.commit
    lang = method.repo.language
    method_file_path = method.file
    method_start_line = method.start_line
    method_end_line = method.end_line
    method_path = f"{method_file_path}#L{method_start_line}-L{method_end_line}"

    if lang == "python":
        grammar_examples = ICONTRACT_EXAMPLES
        target_desc = ICONTRACT_TARGET_DESC
        dsl_name = "icontract"
    elif lang == "java":
        grammar_examples = JML_EXAMPLES
        target_desc = JML_TARGET_DESC
        dsl_name = "JML"

    with create_tempdir() as tmp_dir:
        repo_zip_file_name = f"{github_path.replace('/', '--')}.zip"

        mutant_doc = get_mutant_doc(method)

        download_github_commit_zip(github_path, commit, repo_zip_file_name)

        prompt = PROMPT_TEMPLATE.format(
            mutants = mutant_doc,
            lang=lang,
            grammar_examples=grammar_examples,
            target_desc=target_desc,
            dsl_name=dsl_name,
            repo_zip_file_name=repo_zip_file_name,
            method_path=method_path,
        )

        logging.info(prompt)

        conv = client.conversations.create()

        zip_file = client.files.create(file=open(repo_zip_file_name, "rb"), purpose="assistants")
        resp = client.responses.create(
            model="gpt-5-mini",
            conversation=conv.id,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt}
                ]
            }],
            tools=[
                {
                    "type": "code_interpreter",
                    "container": {
                        "type": "auto",
                        "file_ids": [zip_file.id]
                    }
                }
            ]
        )

        logging.info(resp.output_text)

        max_round = 3
        min_suv = len(method.mutants)

        for round in range(1, max_round + 1):
            postcond = _post_process(resp.output_text)
            eval_ret = eval_postcond(method, postcond)
            if isinstance(eval_ret, str):
                following_prompt = PROMPT_TEMPLATE_FOLLOWING_ERROR.format(
                    stdout=eval_ret)
            elif isinstance(eval_ret, list):
                survived_mutant_idxs = [i for i, f in enumerate(eval_ret) 
                        if f not in ["icontract_fail", "jml_fail"]]
                if len(survived_mutant_idxs) == 0:
                    method.ref_postcond = postcond
                    method.ref_mutant_kill = eval_ret
                    _save_m(method, output_path)
                    return method
                else:
                    mutants_str = ", ".join([f"Mutant {i}" for i in eval_ret])
                    following_prompt = PROMPT_TEMPLATE_FOLLOWING_MUT_SUV.format(
                        mutants=mutants_str
                    )
            else:
                _save_m(method, output_path)
                return method

            if isinstance(eval_ret, list) and \
                    len(survived_mutant_idxs) <= min_suv:
                min_suv = len(survived_mutant_idxs)
                method.ref_postcond = postcond
                method.ref_mutant_kill = eval_ret
            
            if round == max_round:
                _save_m(method, output_path)
                return method

            logging.info(following_prompt)

            resp = client.responses.create(
                model="gpt-5-mini",
                conversation=conv.id,
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": following_prompt}
                    ]
                }],
                tools=[
                    {
                        "type": "code_interpreter",
                        "container": {
                            "type": "auto",
                            "file_ids": [zip_file.id]
                        }
                    }
                ]
            )

            logging.info(str(resp))

        _save_m(method, output_path)
        return method



if __name__ == "__main__":
    doc = call_gpt("adyliu/jafka", "append")
