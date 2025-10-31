from src.ds import *
from copy import deepcopy


def must_fail_inj(method: Method, code_str: str) -> str:
    lang = method.repo.language
    if lang == "python":
        stat = "assert False"
    elif lang == "java":
        stat = "assert false;"
    code_lines = code_str.split("\n")
    body_start_line_0i = method.body_start_line - 1
    while body_start_line_0i < len(code_lines) - 1 and \
            (
                code_lines[body_start_line_0i].strip() == "" or \
                code_lines[body_start_line_0i].strip() == "{" # for java
            ):
        body_start_line_0i += 1
    body_start_line_str = code_lines[body_start_line_0i]
    indent = body_start_line_str[: -len(body_start_line_str.lstrip())]
    stat = indent + stat
    prefix_lines = code_lines[: body_start_line_0i]
    suffix_lines = code_lines[body_start_line_0i: ]
    return "\n".join(prefix_lines + [stat] + suffix_lines)
