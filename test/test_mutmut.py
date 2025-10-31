from src.mutation.mutmut import generate_mutants_for_method
from typing import *
import difflib

# ------------------------- Demo：多触发一些 mutators -------------------------
def _print_diffs(title: str, original: str, mutants: List[str], limit: Optional[int] = 40) -> None:
    print(f"\n===== {title} =====")
    print(f"original:\n{original.rstrip()}\n")
    print(f"generated mutants: {len(mutants)}")
    if limit is None:
        limit = len(mutants)
    for i, mcode in enumerate(mutants[:limit], 1):
        print(f"\n--- mutant #{i} ---")
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            mcode.splitlines(keepends=True),
            fromfile="original",
            tofile=f"mutant_{i:04d}",
            n=3,
        )
        print("".join(diff), end="")


def main():
    snippets = [
        # 1) 数字、增强赋值、比较/布尔、字符串方法、对称/非对称 swap、arg 删除
        ("""\
def f(a, b, s: str):
    x = 1
    x += 2
    if a < b and a != 0:
        t = s.lower().ljust(5)
    else:
        t = s.upper().rjust(3)
    return t
"""),
        # 2) “方法片段”（带缩进 self）、dict(...) 关键字名、lambda、运算符 swap
        ("""\
    def method(self, a, b):
        d = dict(alpha=1, beta=2)
        z = (lambda k=None: None)(k=0)
        return (a + b) * 2
"""),
        # 3) not 去除、in/is 的对调、match case 删除、一元运算等
        ("""\
def classify(x):
    if not (x in [1,2] or x is 3):
        y = 1
    else:
        y = 2
    match x:
        case 0 | 1:
            return "small"
        case _:
            return "big"
"""),
        # 4) 纯字符串（大小写/包裹/非转义区间大小写）
        ("""\
def g(s):
    return "AbC\\n\\tXyZ"
"""),
        # 5) async：含 //、+、**，触发算术/比较等
        ("""\
async def h(n: int):
    return (n + 1) // 2 if n >= 0 else (n ** 2)
"""),
        # 6) split/rsplit 非对称（带 maxsplit），rjust/ljust 等
        ("""\
def parse_line(s):
    parts = s.split(",", 1)
    return [p.strip().lower().rjust(3) for p in parts if p]
"""),
    ]

    for idx, src in enumerate(snippets, 1):
        muts = generate_mutants_for_method(src)
        _print_diffs(f"Snippet #{idx}", src, muts, limit=40)


if __name__ == "__main__":
    main()
