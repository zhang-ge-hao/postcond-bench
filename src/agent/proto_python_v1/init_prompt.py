from src.ds import *
from src.clone import repository_reproduct
from src.util import parse_file, read_code
from src.postcond.prompt.util import (
    remove_method_bodies,
    remove_all_comments
)
from src.postcond.prompt.infile import cut_context


ICONTRACT_TARGET_DESC = "`@icontract.ensure` and `@icontract.snapshot` lines"

JML_TARGET_DESC = "JML `ensures` lines with leading `//@ ensures`"

JML_GARMMAR_RESTRICTION = """Note that you are only allowed to use the subset of JML grammar:
- `//@ ensures <jml-expression>`
- `\\result`
- `\old(<expression>)`
- `==>`, `<==>` and `<=!=>`

Do NOT use JML quantified expressions, like `\\forall` or `\\exists`. You can use Java native grammars, like Java Streams, to replace them.
"""

PROMPT_TEMPLATE = (
    "## Code Context\n"
    "```\n"
    "{code_context}\n"
    "```\n"
    "## Target Method\n"
    "```\n"
    "{target_method}\n"
    "```\n"
    "## Guideline\n"
    "Above is the {lang} code context and target method. "
    "You should generate {dsl_name} format postconditions for "
    "this method `{method_name}`.\n"
    "{grammar_restriction}"
    "Try to generate correct and complete postconditions.\n"
    "## Response Format\n"
    "Considering you are an agent, "
    "you can take some actions and receive a response from the environment. "
    "For each round, "
    "your response should follow one of the following formats:\n"
    "### Making an attempt\n"
    "```\n"
    "ATTEMPT\n"
    "{{POSTCONDITIONS}}\n"
    "```\n"
    "Note that the {{POSTCONDITIONS}} should only contain {target_desc}. "
    "The environment will save the postconditions as the latest attempt.\n"
    "### Grammar Verification\n"
    "```\n"
    "GRAMMAR_VERIFY\n"
    "```\n"
    "The environment will respond with the "
    "verification result of the latest attempt.\n"
    "### Yield\n"
    "```\n"
    "YIELD\n"
    "```\n"
    "Session will end "
    "with the latest attempt as the final result postconditions.\n"
)

def prompt_v2(method: Method) -> str:
    """cwd need to be the repo path"""

    assert method.prompting.startswith("v2")

    lang = method.repo.language
    if lang == "python":
        dsl_name = "icontract"
        target_desc = ICONTRACT_TARGET_DESC
        grammar_restriction = ""
    elif lang == "java":
        dsl_name = "JML"
        target_desc = JML_TARGET_DESC
        grammar_restriction = JML_GARMMAR_RESTRICTION
    else:
        raise NotImplementedError()

    code_str, code_bytes = read_code(method.file)

    assert method.prompting == "v2-all"
    code_context = code_str
    target_method = method.content

    prompt = PROMPT_TEMPLATE.format(
        code_context=code_context,
        target_method=target_method,
        lang=lang,
        dsl_name=dsl_name,
        method_name=method.name,
        target_desc=target_desc,
        grammar_restriction=grammar_restriction
    )

    return prompt


if __name__ == "__main__":
    method_path = "data/step/8.benchmark/a2aproject--a2a-python--append_artifact_to_task.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))
    method.prompting = "v2-all"
    with repository_reproduct(method.repo) as repo_dir:
        print(prompt_v2(method))
