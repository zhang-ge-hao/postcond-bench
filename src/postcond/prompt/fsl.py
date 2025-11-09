from src.ds import *
from src.clone import repository_reproduct
from src.util import parse_file, read_code
from src.postcond.prompt.util import remove_method_bodies
from difflib import get_close_matches

from src.postcond.prompt.infile import (
    ICONTRACT_EXAMPLES,
    JML_EXAMPLES,
    ICONTRACT_TARGET_DESC,
    JML_TARGET_DESC,
    cut_context
)

SHOT_PROMPT_TEMPLATE = (
    "## Target Method\n"
    "```\n"
    "{target_method}\n"
    "```\n"
    "## Guideline\n"
    "Above is the {lang} code context and target method. "
    "You should generate {dsl_name} format postconditions for "
    "this method `{method_name}`.\n"
    "Try to generate correct and complete postconditions.\n"
    "Note that your response should only contain {target_desc}.\n\n"
    "```\n"
    "{ref_postcond}\n"
    "```\n"
)

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

def prompt_fsl(method: Method, w_code: bool, methods: List[Method], shot_num, 
               context_ratio: float) -> str:
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
    
    # only exclude itself
    candidate_methods = [
        m for m in methods 
        if m.github_url != method.github_url and \
            m.repo.language == method.repo.language]
    header_2_method: Dict[str, Method] = {m.header: m for m in candidate_methods}

    sim_headers = get_close_matches(
        method.header, 
        [m.header for m in candidate_methods], 
        n=shot_num,
        cutoff=0)
    
    fsl_examples = [header_2_method[h] for h in sim_headers]

    shot_prompts = []
    for fsl_example in fsl_examples:
        target_method = fsl_example.content if w_code else fsl_example.header
        method_name = fsl_example.name
        ref_postcond = fsl_example.ref_postcond
        shot_prompt = SHOT_PROMPT_TEMPLATE.format(
            target_method=target_method,
            lang=lang,
            dsl_name=dsl_name,
            method_name=method_name,
            target_desc=target_desc,
            ref_postcond=ref_postcond
        )
        shot_prompts.append(shot_prompt)


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

    prompt = "\n\n".join(shot_prompts + [prompt])

    return prompt
