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
