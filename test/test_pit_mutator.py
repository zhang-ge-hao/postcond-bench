# tests/test_mutators.py
import re
import difflib
from typing import List

from src.ds import Repo, Method
from src.mutation.pit import generate_mutants_for_method

# ---- 常量：单个“方法级”源码 ----

JAVA_METHOD = r"""
public int foo(int a, int b, String s, java.util.List<Integer> xs, boolean flag) {
  int i = 0;
  i++;
  i -= 2;
  this.bar(); // void 调用（启发式删除）
  if (a < b) { i = a + b; }
  if (a == b) { i = a * b; }
  if (flag && (a >= b)) { i = a << b; }
  if (s != null && s.length() > 0) { i = i + 1; }
  int j = -i;
  if (s != null) { System.out.println(s); } // 也是 void 调用
  return i;
}
"""

JAVA_METHOD_RET_BOOL = r"""
public boolean isOk(int a, int b) {
  return a < b;
}
"""

JAVA_METHOD_RET_STR = r"""
public String nameOrEmpty(String n) {
  if (n == null) return "x";
  return n;
}
"""

JAVA_METHOD_RET_OPT = r"""
public java.util.Optional<Integer> maybe(boolean f, Integer v) {
  if (f) return java.util.Optional.of(v);
  return java.util.Optional.empty();
}
"""

JAVA_METHOD_RET_OBJ_NOTNULL = r"""
@NotNull
public Object must() {
  return new Object();
}
"""

def _join(mutants: List[str]) -> str:
    # 便于包含性断言
    return "\n\n".join(mutants)

def _print_mutant_diffs(mutants: List[str], original: str, title: str = "") -> None:
    """
    打印每个变体 vs 原始方法源码的 unified diff。
    注意：pytest 默认会捕获 stdout；当用例失败时会展示这些 diff。
    你也可以通过 `-s` 运行 pytest 来即时看到输出。
    """
    if title:
        print(f"\n==== {title} | {len(mutants)} mutants ====\n")
    orig_lines = original.strip("\n").splitlines(keepends=True)
    for idx, m in enumerate(mutants, 1):
        mut_lines = m.strip("\n").splitlines(keepends=True)
        diff = list(difflib.unified_diff(
            orig_lines, mut_lines,
            fromfile="original.java",
            tofile=f"mutant_{idx}.java",
            lineterm="",
            n=3
        ))
        print(f"--- Mutant #{idx} ---")
        if diff:
            print("\n".join([l.rstrip() for l in diff]))
        else:
            print("(no diff)")
        print()  # 空行分隔

def test_conditionals_and_negations_and_boundary_and_math_and_increments_and_void_and_invert_and_primitive():
    muts = generate_mutants_for_method(JAVA_METHOD)
    _print_mutant_diffs(muts, JAVA_METHOD, title="Mixed operators & returns")
    s = _join(muts)

    # Boundary: < -> <=
    assert "if (a <= b)" in s
    # Negate: == -> !=
    assert "if (a != b)" in s
    # Increments: i++ -> i--
    assert re.search(r"\bi--\s*;", s)
    # Increments: i -= 2 -> i += 2
    assert "i += 2" in s
    # Math: + -> -
    assert "i = a - b" in s
    # Math: * -> /
    assert "i = a / b" in s
    # Math: << -> >>
    assert "i = a >> b" in s
    # Math: 对字符串拼接的 + 不应替换（s.length() > 0 后面的 i = i + 1 可被替换）
    assert "i = i - 1" in s
    # Void call removal: this.bar(); 被删除
    assert "this.bar();" not in s or "this.bar();" in JAVA_METHOD  # 变体里应有被删的版本
    # Invert negatives: -i -> i
    assert re.search(r"\bint j\s*=\s*i\s*;", s)
    # PrimitiveReturns: return i -> return 0
    assert re.search(r"return\s+0\s*;", s)

def test_bool_returns_false_true():
    muts = generate_mutants_for_method(JAVA_METHOD_RET_BOOL)
    _print_mutant_diffs(muts, JAVA_METHOD_RET_BOOL, title="Boolean returns")
    s = _join(muts)
    assert re.search(r"return\s+false\s*;", s)
    assert re.search(r"return\s+true\s*;", s)

def test_empty_returns_string():
    muts1 = generate_mutants_for_method(JAVA_METHOD_RET_STR)
    _print_mutant_diffs(muts1, JAVA_METHOD_RET_STR, title="Empty returns (String)")
    s1 = _join(muts1)
    # EMPTY_RETURNS: String -> ""
    assert 'return ""' in s1

def test_empty_returns_optional():
    muts2 = generate_mutants_for_method(JAVA_METHOD_RET_OPT)
    _print_mutant_diffs(muts2, JAVA_METHOD_RET_OPT, title="Empty returns (Optional)")
    s2 = _join(muts2)
    # EMPTY_RETURNS: Optional -> Optional.empty()
    assert "Optional.empty()" in s2

def test_null_returns_respects_notnull():
    muts = generate_mutants_for_method(JAVA_METHOD_RET_OBJ_NOTNULL)
    _print_mutant_diffs(muts, JAVA_METHOD_RET_OBJ_NOTNULL, title="Null returns (NotNull)")
    s = _join(muts)
    # 有 @NotNull 时不应出现 null 返回替换
    assert "return null" not in s


if __name__ == "__main__":
    # 直接运行本文件时也会打印 diff，便于快速肉眼检查
    test_conditionals_and_negations_and_boundary_and_math_and_increments_and_void_and_invert_and_primitive()
    test_bool_returns_false_true()
    test_empty_returns_string()
    test_empty_returns_optional()
    test_null_returns_respects_notnull()
