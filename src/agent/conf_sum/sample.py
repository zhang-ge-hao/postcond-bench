from __future__ import annotations

from typing import Callable, TypeVar


T = TypeVar("T")


def stable_head_sample(items: list[T], sample_size: int | None, key: Callable[[T], str]) -> list[T]:
    ordered = sorted(items, key=key)
    if sample_size is None:
        return ordered
    if sample_size <= 0:
        return []
    return ordered[:sample_size]