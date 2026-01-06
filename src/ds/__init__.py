from dataclasses import dataclass, asdict
import json
from typing import *

@dataclass
class Repo:
    github_path: str
    commit: str
    language: str

    env_config: str

    failed_tests: List[str]
    test_time: float

    def save(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, file_path: str) -> 'Repo':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)


@dataclass
class Method:
    rlid: str # repo-level id

    github_url: str

    name: str

    line_cov: float
    lines: int
    stats: int
    cc: int

    content: str
    header: str
    
    file: str
    start_line: int
    end_line: int
    body_start_line: int

    comment: str

    test_time: float

    cover_tests: List[str]

    repo: Repo

    mutants: List[str] = None
    mutant_tags: List[List[str]] = None

    ref_source: str = None
    ref_postcond: str = None
    ref_mutant_kill: List[str] = None

    model_name: str = None
    port: str = None
    generate_num: int = None

    task_version: int = None

    w_code: bool = None

    prompt: str = None
    prompting: str = None

    postconds: List[str] = None
    responses: List[str] = None

    postcond_corr: List[str] = None
    mutant_kill: List[List[str]] = None

    traversal_rank: int = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        data["repo"] = Repo(**data["repo"])
        return cls(**data)
    
    @classmethod
    def save_li(cls, method_list, file_path):
        with open(file_path, "w") as file:
            for m in method_list:
                file.write(json.dumps(m.to_dict()) + "\n")
    
    @classmethod
    def load_li(cls, file_path) -> List["Method"]:
        methods = []
        with open(file_path) as file:
            for line in file:
                methods.append(cls.from_dict(json.loads(line)))
        return methods
