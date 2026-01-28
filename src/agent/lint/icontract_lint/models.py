from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Issue:
    code: str                # e.g., IC001
    rule: str                # short rule name
    message: str             # human readable (English)
    line: int                # 1-based
    col: int                 # 0-based
    end_line: Optional[int] = None
    end_col: Optional[int] = None
    snippet: Optional[str] = None
    caret: Optional[str] = None

    def format(self) -> str:
        loc = f"Line {self.line}, Col {self.col}"
        header = f"{self.rule} — {loc}"
        body = self.message
        if self.snippet is not None and self.caret is not None:
            return f"{header}\n{body}\n\n{self.snippet}\n{self.caret}"
        return f"{header}\n{body}"
