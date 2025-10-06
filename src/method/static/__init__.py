import os
from src.ds import Repo, StaticMethod
from typing import *
from src.util import get_language_and_parser
from src.clone import repository_reproduct
from uuid6 import uuid7
import json
from src.pool import run_with_pool_file_monitor
from src.method.static.analysis import (
    iter_tree_and_code_bytes,
    iter_method_ts_node,
    get_method_body,
    get_comment,
    is_good_comment,
    has_return,
    get_stat_number,
    get_cc,
    get_line_position_1i,
    get_method_name,
)

class METHOD_RESTRICTION:
    stat = 10
    cc = 3
    comment = 15


def get_method(method_ts_node, code_str, 
               code_bytes, code_path, 
               repo: Repo) -> StaticMethod:
    github_path = repo.github_path
    commit = repo.commit
    lang = repo.language

    # has body
    body_ts_node = get_method_body(method_ts_node, lang)
    if body_ts_node is None:
        return None

    # comment
    comment = get_comment(method_ts_node, body_ts_node, code_bytes, lang)
    if comment is None:
        return None
    if not is_good_comment(comment, lang, METHOD_RESTRICTION.comment):
        return None

    # has return
    if not has_return(method_ts_node, lang):
        return None

    # stat number and cc
    stat_number = get_stat_number(body_ts_node, lang)
    cc_dict = get_cc(body_ts_node, code_bytes, lang)
    cc = cc_dict["total"]
    if cc < METHOD_RESTRICTION.cc and stat_number < METHOD_RESTRICTION.stat:
        return None

    # parse line-wise positions
    start_line, end_line, body_start_line = get_line_position_1i(
        method_ts_node, body_ts_node, lang)
    
    # content and header
    code_lines = code_str.split("\n")
    content = "\n".join(code_lines[start_line - 1: end_line])
    header = "\n".join(code_lines[start_line - 1: body_start_line - 1])

    github_url = (f"https://github.com/{github_path}/blob/"
                  f"{commit}/{code_path}"
                  f"#L{start_line}-L{end_line}")
    
    # method name
    name = get_method_name(method_ts_node, code_bytes, lang)

    ret = StaticMethod(
        rlid=None, # NOTE: will be assigned afterward
        github_url=github_url,
        name=name,
        content=content,
        header=header,
        file=code_path,
        start_line=start_line,
        end_line=end_line,
        body_start_line=body_start_line,
        lines=end_line - start_line + 1,
        stats=stat_number,
        cc=cc,
        comment=comment,
        repo=repo)
    return ret


def method_collection(repo: Repo) -> List[StaticMethod]:
    language = repo.language

    _, parser = get_language_and_parser(language)

    ret: List[StaticMethod] = []
    with repository_reproduct(repo) as repo_dir:
        __generator = iter_tree_and_code_bytes(language, parser)
        for tree, code_str, code_bytes, code_path in __generator:
            for method_ts_node in iter_method_ts_node(tree, language):
                method = get_method(method_ts_node, code_str, 
                                    code_bytes, code_path, repo)
                if method is not None:
                    ret.append(method)

    # get repo-level id
    ret.sort(key=lambda m: (m.file, m.start_line))
    method_name_map = {}
    for method in ret:
        if method.name in method_name_map:
            method_name_map[method.name] += 1
            rlid = f"{method.name}-{method_name_map[method.name]}"
        else:
            method_name_map[method.name] = 1
            rlid = method.name
        method.rlid = rlid

    return ret


def method_collection_pool(input_dir=None, output_dir=None):
    task_name = "static"
    log_dir = f"data/__log/{task_name}--{uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    repos: List[Repo] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            with open(f"{input_dir}/{file_name}") as file:
                repo_dict = json.load(file)
            repos.append(Repo(**repo_dict))

    summary_path = f"{log_dir}/__summary.md"
    task_names = [r.github_path.replace("/", "--") for r in repos]
    log_paths = [f"{log_dir}/{tn}.log" for tn in task_names]
    _, method_lists = run_with_pool_file_monitor(
        func=method_collection,
        task_names=task_names,
        log_paths=log_paths,
        params_list=repos,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
    for tn, method_list in zip(task_names, method_lists):
        if method_list:
            with open(f"{output_dir}/{tn}.jsonl", "w") as file:
                for m in method_list:
                    file.write(json.dumps(m.to_dict()) + "\n")
