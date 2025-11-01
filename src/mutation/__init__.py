
import os
from src.ds import *
from src.util import get_diff

from src.runner import testsuite_run
from src.mutation.mutmut import (
    generate_mutants_for_method as python_mut_gen
)
from src.mutation.pit import (
    generate_mutants_for_method as java_mut_gen
)
from src.mutation.llm import (
    generate_mutants_for_method as llm_mut_gen
)

from src.util import get_uuid7, read_code
from src.inject import check_postcond_exec_mutant_inj
from src.clone import repository_reproduct
from src.pool import run_with_pool_file_monitor

def mutant_candidate_generation(method: Method) -> Method:
    lang = method.repo.language
    if lang == "python":
        rule_muts = python_mut_gen(method.content)
    elif lang == "java":
        rule_muts = java_mut_gen(method.content)
    else:
        raise NotImplementedError()
    llm_muts = llm_mut_gen(method)

    # mutant -> [tags]（保序去重）
    tags_map: dict[str, list[str]] = {}

    def add_tags(m_list, tag: str):
        for m in m_list:
            if m not in tags_map:
                tags_map[m] = []
            if tag not in tags_map[m]:
                tags_map[m].append(tag)

    add_tags(rule_muts, "rule")
    add_tags(llm_muts, "llm")

    # 计算与原始内容的第一个 diff 的绝对行号
    def first_diff_line(mutant: str, content: str, start_line: int) -> int:
        n = min(len(mutant), len(content))
        i = 0
        while i < n and mutant[i] == content[i]:
            i += 1
        # 将第一个差异字符在 content 中的索引 i 映射为绝对行号
        # 行号 = start_line + content[:i] 中的换行数
        return start_line + content[:i].count('\n')

    # 组装为列表并排序
    content = method.content
    start_line = method.start_line
    triples = [(m, tags_map[m], first_diff_line(m, content, start_line)) 
               for m in tags_map.keys()]
    triples = [(m, ts, l) for m, ts, l in triples if method.body_start_line <= l]
    triples.sort(key=lambda t: (t[2], t[0]))  # 先按绝对行号，再按 mutant 字典序稳定排序

    # 回填
    method.mutants = [m for m, _, _ in triples]
    method.mutant_tags = [tags for _, tags, _ in triples]

    return method


def mutant_generation(method: Method, output_path: str=None) -> Method:
    if method.mutants is None and method.mutant_tags is None:
        method = mutant_candidate_generation(method)

    import logging

    logging.info(f"for {method.rlid}, {len(method.mutants)} mutants generated.")

    lang = method.repo.language
    excluded_tests = method.repo.failed_tests
    with repository_reproduct(method.repo) as repo_dir:
        mutants = []
        mutant_tags = []
        __generator = enumerate(zip(method.mutants, method.mutant_tags))
        for mut_idx, (mutant, tags) in __generator:
            logging.info(f"eval started: {method.rlid}--{mut_idx}")
            code_str, code_bytes = read_code(method.file)
            check_pc_exec_code_src = check_postcond_exec_mutant_inj(
                method, mutant, code_str)
            run_result = testsuite_run(
                lang=lang,
                included_tests=method.cover_tests,
                excluded_tests=excluded_tests,
                replace_file_path=method.file,
                replace_file_content=check_pc_exec_code_src,
                need_coverage=False,
                timeout=20)

            if run_result.to_flag() != "failed" \
                    or "Exception within current method!" in run_result.stdout:
                flag = run_result.to_flag()
                continue
            mutants.append(mutant)
            mutant_tags.append(tags)
        method.mutants = mutants
        method.mutant_tags = mutant_tags
    assert len(method.mutants) == len(method.mutant_tags)
    if output_path is not None:
        with open(output_path, "w") as file:
            json.dump(method.to_dict(), file, indent=2)
    return method


def mutant_generation_pool(input_dir=None, output_dir=None,
                           task_num=None, task_idx=None, methods=None):
    task_name = "mut_gen"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    output_dir = os.path.abspath(output_dir)
    os.makedirs(log_dir, exist_ok=True)

    if methods is None:
        methods: List[Method] = []
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".jsonl"):
                for m in Method.load_li(f"{input_dir}/{file_name}"):
                    methods.append(m)
        
        methods.sort(key=lambda m: (-m.lines, m.repo.github_path, m.rlid))
        
    if task_num is not None and task_idx is not None:
        methods = [m for i, m in enumerate(methods) 
                   if i % task_num == task_idx]

    params_list = []
    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"
        out_path = f"{output_dir}/{tn}.json"
        if os.path.exists(out_path):
            continue
        params_list.append((m, out_path))
        task_names.append(tn)
        log_paths.append(f"{log_dir}/{rn}.log")
    
    print(len(params_list))

    summary_path = f"{log_dir}/__summary.md"
    _, ret = run_with_pool_file_monitor(
        func=mutant_generation,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
