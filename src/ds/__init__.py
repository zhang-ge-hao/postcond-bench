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

    def save(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, file_path: str) -> 'Repo':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)


@dataclass
class StaticMethod:
    rlid: str # repo-level id

    github_url: str

    name: str
    content: str
    header: str
    
    file: str
    start_line: int
    end_line: int
    body_start_line: int
    
    lines: int
    stats: int
    cc: int

    comment: str

    repo: Repo

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Repo':
        data["repo"] = Repo(**data["repo"])
        return cls(**data)


# @dataclass
class DynamicMethod(StaticMethod):
    cover_tests: List[str]

    line_cov: float
