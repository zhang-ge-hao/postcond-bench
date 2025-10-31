import json
from src.util import set_logging, create_tempdir
from src.clone import RepoClone, repository_reproduct
from src.repo.reproduction import (
    PoetryReproduction,
    MavenReproduction
)
from src.runner import testsuite_run
import random
import shutil
import os
from typing import *
from src.pool import run_with_pool_file_monitor

from src.ds import Repo

from src.util import get_uuid7
import logging


def reproduce_pool(input_dir=None, repos: List[Repo]=None, 
                   output_dir=None, task_num=None, task_idx=None):
    assert output_dir is not None
    assert input_dir is not None or repos is not None

    task_name = "reproduce"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    if repos is None:
        repos: List[Repo] = []
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".json"):
                if "python" in file_name:
                    lang = "python"
                elif "java" in file_name:
                    lang = "java"
                else:
                    raise NotImplementedError()
                with open(f"{input_dir}/{file_name}") as file:
                    biglist_dict = json.load(file)
                for github_path in biglist_dict["selected"]:
                    repos.append(Repo(
                        github_path=github_path, 
                        commit=None, language=lang,
                        env_config=None, failed_tests=None, test_time=None))
    
    if task_num is not None and task_idx is not None:
        github_paths = [r.github_path for r in repos]
        github_paths.sort()
        selected_paths = [p for i, p in enumerate(github_paths) 
                          if i % task_num == task_idx]
        repos = [r for r in repos if r.github_path in selected_paths]
        # ban huggingface repos
        repos = [r for r in repos if "huggingface" not in r.github_path]
        # ban swe repos
        repos = [r for r in repos if "swe-" not in r.github_path.lower()]

    print(len(repos))
    # # ===== debug =====
    # import random
    # repos = random.sample(repos, 100)
    # print(len([r for r in repos if r.language == "python"]))
    # print(len([r for r in repos if r.language == "java"]))
    # exit()
    # # ===== debug =====

    summary_path = f"{log_dir}/__summary.md"
    
    params_list = []
    task_names = []
    log_paths = []

    for repo in repos:
        tn = repo.github_path.replace("/", "--")
        lp = f"{log_dir}/{tn}.log"
        output_path = f"{output_dir}/{tn}.json"
        output_path = os.path.abspath(output_path)
        if os.path.exists(output_path):
            continue
        params_list.append((repo, output_path))
        task_names.append(tn)
        log_paths.append(lp)

    _, repos = run_with_pool_file_monitor(
        func=reproduce,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )


def reproduce(repo: Repo, output_path: str) -> Repo:
    """output_path need to be absolute"""
    assert repo.github_path is not None
    # assert repo.commit is not None
    assert repo.language is not None

    py_dir = os.path.dirname(os.path.abspath(__file__))
    init_prompt_path = os.path.join(py_dir, "fmt", f"{repo.language}-init.md")
    follow_prompt_path = os.path.join(py_dir, "fmt", f"{repo.language}-follow.md")

    if repo.language == "python":
        reproduction_cls = PoetryReproduction
    elif repo.language == "java":
        reproduction_cls = MavenReproduction
    else:
        raise NotImplementedError()

    with create_tempdir() as dirname:
        clone = RepoClone(dirname, repo.github_path, repo.commit)
        clone.remove_cache()
        success, repo_dir = clone.clone()
        if repo.commit is None:
            repo.commit = clone.commit
        if success:
            reproduction = reproduction_cls(
                repo_dir, init_prompt_path, follow_prompt_path)
            logging.info(f"Reproduce started.")
            result = reproduction.run()
            if result is not None and result.success:
                with open(reproduction.config_path) as file:
                    repo.env_config = "".join(file.readlines())
                with repository_reproduct(repo, require_clone=True) as (repo_dir, clone):
                    test_res = testsuite_run(
                        lang=repo.language, 
                        timeout=200, 
                        require_not_interrupted=True)
                    repo.failed_tests = test_res.failed_tests
                    repo.test_time = test_res.running_time
                    clone.resnapshot(repo_dir)
                repo.save(output_path)
                return repo
            else:
                raise RuntimeError(f"reproduction run failed: {result.log}")
        else:
            raise RuntimeError("clone failed.")
    return None


def reuse_pool(input_dir=None, output_dir=None):
    task_name = "reuse"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
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
    _, repos = run_with_pool_file_monitor(
        func=reuse,
        task_names=task_names,
        log_paths=log_paths,
        params_list=repos,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
    for tn, repo in zip(task_names, repos):
        if repo:
            repo.save(f"{output_dir}/{tn}.json")


def reuse(repo: Repo) -> Repo:
    with repository_reproduct(repo, require_clone=True) as (repo_dir, clone):
        clone.remove_cache()
        test_res = testsuite_run(
            lang=repo.language,
            timeout=200, require_not_interrupted=True)
        repo.failed_tests = test_res.failed_tests
        repo.test_time = test_res.running_time
        clone.resnapshot(repo_dir)
    
    return repo
