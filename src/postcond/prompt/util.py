

from src.ds import *
from src.util import (
    parse_code, 
    get_language_and_parser
)
from src.method.static import (
    iter_method_ts_node,
    get_method
)

def remove_method_bodies(
        code_str: str, 
        code_path: str, 
        repo: Repo, 
        lang: str) -> str:
    omit = "..."
    _, parser = get_language_and_parser(lang)
    tree, code_str, code_bytes = parse_code(code_str, parser)
    body_lines = set()
    for method_ts_node in iter_method_ts_node(tree, lang):
        method = get_method(method_ts_node, code_str, 
                            code_bytes, code_path, repo,
                            apply_restriction=False)
        if method is not None:
            for line in range(method.body_start_line, method.end_line + 1):
                body_lines.add(line - 1)
    ret_lines = []
    for line_idx, line in enumerate(code_str.split("\n")):
        if line_idx not in body_lines:
            if not line.strip() and (ret_lines and ret_lines[-1] == omit):
                continue
            ret_lines.append(line)
        elif ret_lines and ret_lines[-1] == omit:
            continue
        else:
            ret_lines.append(omit)
    return "\n".join(ret_lines)
