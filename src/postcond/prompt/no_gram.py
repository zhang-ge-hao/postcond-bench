from src.ds import *
from src.clone import repository_reproduct
from src.util import parse_file, read_code
from src.postcond.prompt.util import remove_method_bodies
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
    "Note that your response should only contain {target_desc}."
)

def prompt_no_gram(method: Method, w_code: bool,
                   context_ratio: float) -> str:
    """cwd need to be the repo path"""

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
        lang=lang,
        dsl_name=dsl_name,
        method_name=method.name,
        target_desc=target_desc,
        grammar_restriction=grammar_restriction
    )

    return prompt
