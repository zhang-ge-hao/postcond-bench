from src.ds import *


def must_fail_inj(method: StaticMethod, code_str: str) -> str:
    lang = method.repo.language
    if lang == "python":
        stat = "assert False"
    elif lang == "java":
        stat = "assert false;"
    code_lines = code_str.split("\n")
    body_start_line = code_lines[method.body_start_line - 1]
    indent = body_start_line[: -len(body_start_line.lstrip())]
    stat = indent + stat
    prefix_lines = code_lines[: method.body_start_line - 1]
    suffix_lines = code_lines[method.body_start_line - 1: ]
    return "\n".join(prefix_lines + [stat] + suffix_lines)
