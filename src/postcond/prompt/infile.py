from src.ds import *
from src.clone import repository_reproduct
from src.util import parse_file, read_code
from src.postcond.prompt.util import remove_method_bodies

ICONTRACT_EXAMPLES = """
## icontract Grammar Examples

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
## JML Grammar

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
    "## Code Context\n"
    "```\n"
    "{code_context}\n"
    "```\n"
    "## Target Method\n"
    "```\n"
    "{target_method}\n"
    "```\n"
    "{grammar_examples}\n"
    "## Guideline\n"
    "Above is the {lang} code context and target method. "
    "You should generate {dsl_name} format postconditions for "
    "this method `{method_name}`.\n"
    "Try to generate correct and complete postconditions.\n"
    "Note that your response should only contain {target_desc}."
)

def cut_context(code_context: str, target_method: str, context_ratio: float):
    if context_ratio >= 1:
        return code_context
    if context_ratio == 0:
        return ""
    lines = code_context.split("\n")
    assert target_method in code_context
    line_count = int(len(lines) * context_ratio)
    if line_count == 0:
        return ""
    # 1. 找到 target_method 在 code_context 中第一次出现的字符位置
    start_pos = code_context.index(target_method)
    end_pos = start_pos + len(target_method)

    # 2. 计算起止行号（0-based）
    #    行号 = 该字符之前出现的 '\n' 的次数
    start_line = code_context[:start_pos].count("\n")
    end_line = code_context[:end_pos].count("\n")

    # 3. 计算中间行
    mid_line = (start_line + end_line) // 2

    n = len(lines)
    included = set()
    included.add(mid_line)

    # 4. 从中间行开始，按 “上、下、上、下…” 的顺序扩展，直到达到 line_count
    up = mid_line - 1
    down = mid_line + 1

    while len(included) < line_count and (up >= 0 or down < n):
        if up >= 0 and len(included) < line_count:
            included.add(up)
            up -= 1
        if down < n and len(included) < line_count:
            included.add(down)
            down += 1

    # 5. 按原始顺序还原成字符串
    chosen_lines = [lines[i] for i in sorted(included)]
    return "\n".join(chosen_lines)

def prompt_infile(method: Method, w_code: bool, context_ratio: float) -> str:
    """cwd need to be the repo path"""

    lang = method.repo.language
    if lang == "python":
        dsl_name = "icontract"
        grammar_examples = ICONTRACT_EXAMPLES
        target_desc = ICONTRACT_TARGET_DESC
    elif lang == "java":
        grammar_examples = JML_EXAMPLES
        dsl_name = "JML"
        target_desc = JML_TARGET_DESC
    else:
        raise NotImplementedError()

    code_str, code_bytes = read_code(method.file)

    if w_code:
        code_context = code_str
        target_method = method.content
    else:
        code_context = remove_method_bodies(
            code_str=code_str,
            code_path=method.file,
            repo=method.repo,
            lang=lang
        )
        target_method = method.header
    
    code_context = cut_context(code_context, target_method, context_ratio)

    prompt = PROMPT_TEMPLATE.format(
        code_context=code_context,
        target_method=target_method,
        grammar_examples=grammar_examples,
        lang=lang,
        dsl_name=dsl_name,
        method_name=method.name,
        target_desc=target_desc
    )

    return prompt
