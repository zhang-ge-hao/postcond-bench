from __future__ import annotations

import re


_WHITESPACE_RE = re.compile(r"\s+")
_TITLE_PUNCT_RE = re.compile(r"[^a-z0-9]+")


def normalize_whitespace(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value).strip()


def normalize_title(value: str) -> str:
    compact = normalize_whitespace(value).casefold()
    return _TITLE_PUNCT_RE.sub("", compact)