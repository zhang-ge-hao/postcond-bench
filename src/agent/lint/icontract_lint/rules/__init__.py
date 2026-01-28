from __future__ import annotations

from typing import Callable, List, Protocol

from ..context import CheckContext
from ..models import Issue

from .ic001_first_arg_lambda import run as ic001
from .ic002_use_old_for_snapshots import run as ic002
from .ic003_lambda_parameters import run as ic003
from .ic004_bracket_matching import run_pre as ic004_pre
from .ic005_varargs_placeholders import run as ic005
from .ic006_bind_referenced_params import run as ic006
from .ic007_special_names_must_be_bound import run as ic007
from .ic008_decorator_must_be_icontract_qualified import run as ic008
from .ic009_snapshot_requires_name_kw import run as ic009
from .ic010_snapshot_name_unique import run as ic010
from .ic011_old_usage_must_be_attr_and_defined import run as ic011


class Rule(Protocol):
    def __call__(self, ctx: CheckContext) -> List[Issue]: ...


RULES: List[Callable[[CheckContext], List[Issue]]] = [
    ic001,
    ic002,
    ic003,
    ic005,
    ic006,
    ic008,  # decorator correctness early
    ic009,  # snapshot must have name=
    ic010,  # snapshot name uniqueness/conflicts
    ic007,  # special variables used must be bound
    ic011,  # OLD usage rules
]


def run_pre_rules(combined: str, lines: List[str]) -> List[Issue]:
    return ic004_pre(combined, lines)


def run_rules(ctx: CheckContext) -> List[Issue]:
    out: List[Issue] = []
    for rule in RULES:
        out.extend(rule(ctx))
    return out
