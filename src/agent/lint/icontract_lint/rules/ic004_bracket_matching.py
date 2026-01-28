from __future__ import annotations

from typing import List

from ..bracket_match import check_bracket_matching
from ..models import Issue
from ..snippet import make_snippet


def run_pre(combined: str, lines: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    for (line, col, msg) in check_bracket_matching(combined):
        snippet, caret = make_snippet(lines, line, col)
        issues.append(Issue(
            code="IC004",
            rule="Bracket matching",
            message=msg + " (Brackets inside strings/comments are ignored.)",
            line=line,
            col=col,
            snippet=snippet,
            caret=caret
        ))
    return issues
