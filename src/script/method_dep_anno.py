import numpy as np
import os, json
from src.ds import *
import random
from src.util import get_diff

KFS = ["jml_fail", "icontract_fail"]


def read_benchmark(p="data/step/7.reference") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods

if __name__ == "__main__":
    random.seed(42)

    output_path = "data/step/8.benchmark"

    methods = read_benchmark(output_path)

    headers = [m.header for m in methods]
    header_count = {h: 0 for h in headers}
    for h in headers:
        header_count[h] += 1
    counts = list(header_count.values())
    counts.sort()
    print(counts)
    exit()

    # rn_2_lang = {m.repo.github_path: m.repo.language for m in methods}
    # repo_names = [m.repo.github_path for m in methods]
    # repo_count = {rn: 0 for rn in repo_names}
    # for rn in repo_names:
    #     repo_count[rn] += 1
    # repo_count = list(repo_count.items())
    # repo_count.sort(key=lambda t: -t[1])
    # py_sampled_count = 0
    # java_sampled_count = 0
    # py_ori_count = 0
    # java_ori_count = 0
    # for rn, c in repo_count:
    #     print(f"{c:4d} {rn}")
    #     if rn_2_lang[rn] == "python":
    #         py_ori_count += c
    #         py_sampled_count += min(c, 20)
    #     else:
    #         java_ori_count += c
    #         java_sampled_count += min(c, 20)
        
    # print(py_sampled_count)
    # print(java_sampled_count)
    # print(py_ori_count)
    # print(java_ori_count)
    # exit()

    with open("data/step/0.append/dep_anno_python.json") as file:
        dep_anno_python: Dict[str, int] = json.load(file)
    with open("data/step/0.append/dep_anno_java.json") as file:
        dep_anno_java: Dict[str, int] = json.load(file)

    select_count = 150

    github_urls_py = [m.github_url for m in methods if m.repo.language == "python"]
    github_urls_java = [m.github_url for m in methods if m.repo.language == "java"]

    dep_anno_python = {k: v for k, v in dep_anno_python.items() if k in github_urls_py}
    dep_anno_java = {k: v for k, v in dep_anno_java.items() if k in github_urls_java}

    selected_py = [m for m in methods if m.repo.language == "python" and m.github_url not in dep_anno_python]
    selected_java = [m for m in methods if m.repo.language == "java" and m.github_url not in dep_anno_java]

    selected_py = random.sample(selected_py, select_count - len(dep_anno_python))
    selected_java = random.sample(selected_java, select_count - len(dep_anno_java))

    for github_url, anno in dep_anno_python.items():
        if github_url in github_urls_py:
            print(github_url)
            # print(anno)
    for py_method in selected_py:
        print(py_method.github_url)
        # print()
    

    for github_url, anno in dep_anno_java.items():
        if github_url in github_urls_java:
            print(github_url)
            # print(anno)
    for py_method in selected_java:
        print(py_method.github_url)
        # print()
