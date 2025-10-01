import json
from src.util import set_logging, create_tempdir
from src.clone import RepoClone, repository_reproduct
from src.repo.reproduction import (
    PoetryReproduction,
    MavenReproduction
)
from src.runner import (
    python_testsuite_run,
    fatjar_testsuite_run
)
import random
import shutil
import os
from typing import *
from src.pool import run_with_pool_file_monitor

from src.ds import Repo

from uuid6 import uuid7
import logging


def reproduce_pool(input_dir=None, repos: List[Repo]=None, 
                   output_dir=None):
    assert output_dir is not None
    assert input_dir is not None or repos is not None

    task_name = "reproduce"
    log_dir = f"data/__log/{task_name}--{uuid7()}"
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
                        env_config=None, failed_tests=None))
    summary_path = f"{log_dir}/__summary.md"
    task_names = [r.github_path.replace("/", "--") for r in repos]
    log_paths = [f"{log_dir}/{tn}.log" for tn in task_names]
    _, repos = run_with_pool_file_monitor(
        func=reproduce,
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


def reproduce(repo: Repo) -> Repo:
    assert repo.github_path is not None
    # assert repo.commit is not None
    assert repo.language is not None

    py_dir = os.path.dirname(os.path.abspath(__file__))
    init_prompt_path = os.path.join(py_dir, "fmt", f"{repo.language}-init.md")
    follow_prompt_path = os.path.join(py_dir, "fmt", f"{repo.language}-follow.md")

    if repo.language == "python":
        reproduction_cls = PoetryReproduction
        testsuite_run = python_testsuite_run
    elif repo.language == "java":
        reproduction_cls = MavenReproduction
        testsuite_run = fatjar_testsuite_run
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
                    test_res = testsuite_run(timeout=200, require_not_interrupted=True)
                    repo.failed_tests = test_res.failed_tests
                    clone.resnapshot(repo_dir)
                return repo
            else:
                raise RuntimeError(f"reproduction run failed: {result.log}")
        else:
            raise RuntimeError("clone failed.")
    return None


def reuse_pool(input_dir=None, output_dir=None):
    task_name = "reuse"
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
    if repo.language == "python":
        testsuite_run = python_testsuite_run
    elif repo.language == "java":
        testsuite_run = fatjar_testsuite_run
    else:
        raise NotImplementedError()

    with repository_reproduct(repo, require_clone=True) as (repo_dir, clone):
        clone.remove_cache()
        test_res = testsuite_run(timeout=200, require_not_interrupted=True)
        repo.failed_tests = test_res.failed_tests
        clone.resnapshot(repo_dir)
    
    return repo
