from __future__ import annotations

from src.ds import Method
from src.postcond.prompt.infile import ICONTRACT_EXAMPLES
from src.util import read_code


GUIDELINE = (
    "Above is the Python code context and target method. "
    "You should generate icontract format postconditions for "
    "this method `{method_name}`.\n"
    "Try to generate correct and complete postconditions.\n"
    "Note that your response should only contain "
    "`@icontract.ensure` and `@icontract.snapshot` lines."
)

THINK_OPEN_TAG = "<think>"
THINK_CLOSE_TAG = "</think>"

RPG_RESPONSE_FORMAT_SECTION = f"""## Response Format

Return exactly two consecutive parts in this order, with no prose before, between, or after them:

Here is an example:

{THINK_OPEN_TAG}
<grammar>
id: 1
parents: null
edges: null
content: Postconditions must be written as @icontract.ensure decorators that make assertions about the return value. When comparing pre-state and post-state, use @icontract.snapshot to capture the pre-state and then reference it as OLD.* in the ensure clause.
</grammar>
<format>
id: 2
parents: null
edges: null
content: The response must contain only @icontract.snapshot and @icontract.ensure decorator lines, with no other prose. All snapshots must appear before all ensures.
</format>
<context>
id: 3
parents: null
edges: null
content: The target method is PrecertificateSignedCertificateTimestamps.__eq__, which compares two instances. The method signature is `def __eq__(self, other: object) -> bool:`. The method body is incomplete (contains only `...`), but similar __eq__ methods in the file show the pattern: return NotImplemented if other is not of the same type, else compare relevant attributes.
</context>
<context>
id: 4
parents: null
edges: null
content: PrecertificateSignedCertificateTimestamps stores a list of SignedCertificateTimestamp objects in _signed_certificate_timestamps. The method should return True if both instances have equal _signed_certificate_timestamps lists, False otherwise, and NotImplemented if other is not a PrecertificateSignedCertificateTimestamp.
</context>
<context>
id: 5
parents: null
edges: null
content: Looking at the pattern in SignedCertificateTimestamps.__eq__ (defined later in the same file), the canonical implementation checks isinstance and then compares self._signed_certificate_timestamps == other._signed_certificate_timestamps.
</context>
<dividing>
id: 6
parents: 3, 4, 5
edges: The __eq__ method has two branches: (1) if other is not an instance of PrecertificateSignedCertificateTimestamps, return NotImplemented; (2) if other is an instance, return the result of comparing _signed_certificate_timestamps lists.
content:
    1. When other is not a PrecertificateSignedCertificateTimestamps instance, the result should be NotImplemented.
    2. When other is a PrecertificateSignedCertificateTimestamps instance, the result should be True if and only if both instances have equal _signed_certificate_timestamps.
</dividing>
<planning>
id: 7
parents: 6
edges: Expand branch 1 into a concrete postcondition for the NotImplemented case.
content: When isinstance(other, PrecertificateSignedCertificateTimestamps) is False, the return value must be NotImplemented. We can express this as a postcondition that checks: if the condition holds, result == NotImplemented.
</planning>
<attempt>
id: 8
parents: 7
edges: Write the postcondition for branch 1.
content:
    @icontract.ensure(lambda result, other: not isinstance(other, PrecertificateSignedCertificateTimestamps) implies (result is NotImplemented))
</attempt>
<reflection>
id: 9
parents: 8, 1, 2
edges: The attempt uses 'implies' which is not standard Python syntax. Postconditions must use valid Python expressions. The correct form is to use logical implication via conditional: (not condition) or (condition and result_check).
content: Rewrite the postcondition using valid Python conditional logic. The pattern should be: (isinstance check) or (result is NotImplemented). Alternatively, structure it as: if not isinstance, then result is NotImplemented.
</reflection>
<attempt>
id: 10
parents: 9
edges: Rewrite branch 1 postcondition with valid Python syntax.
content:
    @icontract.ensure(lambda result, other: isinstance(other, PrecertificateSignedCertificateTimestamps) or result is NotImplemented)
</attempt>
<planning>
id: 11
parents: 6
edges: Expand branch 2 into a concrete postcondition for the equality comparison case.
content: When isinstance(other, PrecertificateSignedCertificateTimestamps) is True, the result should be a boolean that matches the comparison of _signed_certificate_timestamps. We need to snapshot self._signed_certificate_timestamps and other._signed_certificate_timestamps, then ensure result equals their equality.
</planning>
<attempt>
id: 12
parents: 11
edges: Write the postcondition for branch 2 using snapshots and ensure.
content:
    @icontract.snapshot(lambda self: self._signed_certificate_timestamps, name="self_scts")
    @icontract.snapshot(lambda other: other._signed_certificate_timestamps if isinstance(other, PrecertificateSignedCertificateTimestamps) else None, name="other_scts")
    @icontract.ensure(lambda result, OTHER, self: not isinstance(OTHER.other, PrecertificateSignedCertificateTimestamps) or (result == (OLD.self_scts == OLD.other_scts)))
</attempt>
<reflection>
id: 13
parents: 12, 1, 2
edges: The attempt is overly complex. Snapshots should capture state without conditional logic. The second snapshot is problematic because it conditions on isinstance. A simpler approach is better.
content: Simplify by combining both branches into one ensure that captures the method's complete contract: return NotImplemented if not isinstance, else return the boolean equality result.
</reflection>
<attempt>
id: 14
parents: 13, 10
edges: Merge both branches into a single coherent set of postconditions.
content:
    @icontract.ensure(lambda result, other: isinstance(other, PrecertificateSignedCertificateTimestamps) or result is NotImplemented)
    @icontract.ensure(lambda result, other, self: not isinstance(other, PrecertificateSignedCertificateTimestamps) or isinstance(result, bool))
</attempt>
<reflection>
id: 15
parents: 14, 1, 2
edges: Review whether we need to actually capture the _signed_certificate_timestamps attributes and compare them. The postconditions so far only check type conditions and result type, not the actual equality semantics.
content: We should add a postcondition that verifies when isinstance(other, PrecertificateSignedCertificateTimestamps) is True, result equals the comparison of the _signed_certificate_timestamps attributes.
</reflection>
<planning>
id: 16
parents: 15
edges: Refine the postcondition set to include the actual equality check.
content: Add a postcondition that when other is a PrecertificateSignedCertificateTimestamps, the result should equal the boolean comparison of the two _signed_certificate_timestamps lists. This requires snapshots of the needed values before the method executes.
</planning>
<attempt>
id: 17
parents: 16
edges: Write complete postconditions including snapshots for the equality comparison.
content:
    @icontract.snapshot(lambda self: self._signed_certificate_timestamps, name="self_scts")
    @icontract.ensure(lambda result, other: isinstance(other, PrecertificateSignedCertificateTimestamps) or result is NotImplemented)
    @icontract.ensure(lambda result, other, OLD: not isinstance(other, PrecertificateSignedCertificateTimestamps) or (result == (OLD.self_scts == other._signed_certificate_timestamps)))
</attempt>
{THINK_CLOSE_TAG}
@icontract.snapshot(lambda self: self._signed_certificate_timestamps, name="self_scts")
@icontract.ensure(lambda result, other: isinstance(other, PrecertificateSignedCertificateTimestamps) or result is NotImplemented)
@icontract.ensure(lambda result, other, OLD: not isinstance(other, PrecertificateSignedCertificateTimestamps) or (result == (OLD.self_scts == other._signed_certificate_timestamps)))

RPG node types:
- <grammar>: syntax or contract-writing rules that should be obeyed. Its content must be extracted from the prompt or supplied from stable prior knowledge about writing valid postconditions. Its parents and edges must be null.
- <format>: output-format rules that should be obeyed. Its content must summarize the required response format. Its parents and edges must be null.
- <context>: factual information extracted from the code context. Its parents and edges must be null.
- <dividing>: a divide-and-conquer control node. Its content must be a numbered list in the exact format "1. ..." then "2. ..." then "3. ..." on separate lines.
- <reflection>: a control node that identifies conflicts between a current attempt or plan and known information, and gives a correction.
- <planning>: a worker node that summarizes one or more parent nodes into a natural-language plan for how the final postconditions should be written.
- <attempt>: a worker node that summarizes one or more parent nodes into a concrete set of candidate postconditions.

Rules:
- Wrap the entire reasoning graph in exactly one top-level {THINK_OPEN_TAG}...{THINK_CLOSE_TAG} block.
- Immediately after {THINK_CLOSE_TAG}, write only the final postcondition set using @icontract.snapshot and @icontract.ensure lines, plus any necessary continuation lines for multiline lambdas.
- Use only these node tags: <grammar>, <format>, <context>, <dividing>, <reflection>, <planning>, <attempt>.
- Each tag occurrence represents exactly one node. Repeat the same tag if you need multiple nodes of that type.
- Every node must contain these four fields in this exact order: id, parents, edges, content.
- id must be a unique integer and must increase strictly from 1.
- parents must be either null or a comma-separated list of earlier node ids such as 3 or 5, 8.
- edges must be null only for <grammar>, <format>, and <context>. For every other node, edges must be a non-empty natural-language description of the reasoning move from the parent nodes to the current node.
- content may span multiple indented continuation lines only when needed. This is especially expected for <dividing> and <attempt> nodes.
- For <grammar>, <format>, and <context>, parents must be null and edges must be null.
- For <dividing>, content must be a numbered list using exactly the pattern "1. ...", "2. ...", "3. ..." on separate lines. The out-degree of a dividing node should equal the number of numbered items in its content.
- For <reflection>, parents must include at least one <attempt> or <planning> node. Any additional parents may be <grammar>, <format>, or <context> nodes that expose the conflict.
- For <planning>, parents must contain one or more earlier nodes, and content must be natural language describing how the final postconditions should be written.
- For <attempt>, parents must contain one or more earlier nodes, and content must be a set of postconditions written as @icontract.snapshot and @icontract.ensure lines.
- Keep the graph concise but non-trivial. Use the graph to show how the final postcondition set was designed, not just to restate the code.
- The final node in the DAG must be an <attempt> node.
- The final <attempt> node should match the final postcondition set written after {THINK_CLOSE_TAG}.
"""


def _indent_of(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" \t"))]


def _detect_body_indent(lines: list[str], method: Method) -> str:
    for line_number in range(method.body_start_line, method.end_line + 1):
        content = lines[line_number - 1]
        if content.strip():
            return _indent_of(content)

    header_line = lines[method.start_line - 1]
    return _indent_of(header_line) + "    "


def _build_code_context(lines: list[str], method: Method) -> str:
    body_start_index = method.body_start_line - 1
    body_end_index = method.end_line - 1

    if body_start_index > body_end_index:
        return "\n".join(lines)

    body_indent = _detect_body_indent(lines, method)
    elided_lines = lines[:body_start_index] + [f"{body_indent}..."] + lines[body_end_index + 1 :]
    return "\n".join(elided_lines)


def _build_target_method(lines: list[str], method: Method) -> str:
    header_end_line = max(method.start_line, method.body_start_line - 1)
    return "\n".join(lines[method.start_line - 1 : header_end_line])


def _render_baseline_prompt(code_context: str, target_method: str, method_name: str) -> str:
    return (
        "## Code context\n"
        "```python\n"
        f"{code_context}\n"
        "```\n\n"
        "## Target method\n"
        "```python\n"
        f"{target_method}\n"
        "```\n\n"
        f"{ICONTRACT_EXAMPLES.strip()}\n\n"
        "## Guideline\n"
        f"{GUIDELINE.format(method_name=method_name)}\n"
    )


def _render_rpg_prompt(code_context: str, target_method: str, method_name: str) -> str:
    baseline_prompt = _render_baseline_prompt(code_context, target_method, method_name)
    return baseline_prompt.rstrip() + "\n\n" + RPG_RESPONSE_FORMAT_SECTION + "\n"


def build_method_prompt(method: Method, prompt_mode: str) -> str:
    if method.repo.language != "python":
        raise NotImplementedError("The eval prompt builder currently supports only python methods.")

    code_str, _ = read_code(method.file)
    lines = code_str.splitlines()
    code_context = _build_code_context(lines, method)
    target_method = _build_target_method(lines, method)

    if prompt_mode == "baseline":
        return _render_baseline_prompt(code_context, target_method, method.name)
    if prompt_mode == "rpg":
        return _render_rpg_prompt(code_context, target_method, method.name)
    raise ValueError(f"Unsupported prompt mode: {prompt_mode}")