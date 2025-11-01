# single_def_mutator_demo_compat.py
import textwrap
from typing import List, Optional
import re

import libcst as cst

# 改成你的实际导入路径
from src.mutation.mutmut.node_mutation import mutation_operators


# ---------- 兼容补丁：operator_* 崩了时，数字/字符串做兜底突变 ----------
def _fallback_mutations(node: cst.CSTNode):
    # 数字：+1
    if isinstance(node, cst.Integer):
        try:
            yield node.with_changes(value=str(int(node.value) + 1))
        except Exception:
            return
    elif isinstance(node, cst.Float):
        try:
            yield node.with_changes(value=repr(float(node.value) + 1.0))
        except Exception:
            return
    # 纯字符串：包裹 / 大小写
    elif isinstance(node, cst.SimpleString):
        v = node.value
        if len(v) >= 2 and (v[0] == v[-1] in ('"', "'")):
            q = v[0]
            inner = v[1:-1]
            for nv in (f"{q}XX{inner}XX{q}", f"{q}{inner.lower()}{q}", f"{q}{inner.upper()}{q}"):
                if nv != v:
                    yield node.with_changes(value=nv)


# ---------- 单点替换 & 收集 ----------
class _OneChange(cst.CSTTransformer):
    def __init__(self, target: cst.CSTNode, new: cst.CSTNode):
        self._target = target
        self._new = new
        self._done = False

    def on_leave(self, original_node: cst.CSTNode, updated_node: cst.CSTNode) -> cst.CSTNode:
        if not self._done and original_node is self._target:
            self._done = True
            return self._new
        return updated_node


class _CollectAll(cst.CSTVisitor):
    def __init__(self):
        self.mutations: list[tuple[cst.CSTNode, cst.CSTNode]] = []

    def on_visit(self, node: cst.CSTNode):
        any_success = False
        for node_type, op in mutation_operators:
            if isinstance(node, node_type):
                try:
                    for new_node in op(node):
                        self.mutations.append((node, new_node))
                        any_success = True
                except Exception:
                    # 老版本差异导致的异常：继续尝试其他 operator
                    continue
        # 全部 operator 都没成功，则尝试兜底
        if not any_success:
            try:
                for new_node in _fallback_mutations(node):
                    self.mutations.append((node, new_node))
            except Exception:
                pass
        return True


def _func_to_code(func_node: cst.FunctionDef) -> str:
    """
    兼容老版本 LibCST：节点上没有 .code，就把函数装进一个 Module 再取 Module.code。
    """
    try:
        # 新版可能有 .code（留个快速通道）
        return getattr(func_node, "code")  # type: ignore[attr-defined]
    except Exception:
        pass
    # 老版本：把函数放到 module 里再序列化
    mod = cst.Module(body=[func_node])
    return mod.code


def generate_mutants_for_method(source: str) -> List[str]:
    """
    输入：只包含一个函数/方法定义（可带缩进/装饰器/async）的源码字符串。
    输出：List[str]，每个元素是一份只改一处的突变体源码；会保留原始缩进前缀。
    """
    # 1) 记录原始前导缩进（第一行非空行的前导空白）
    orig = source.rstrip("\n") + "\n"
    indent_prefix = ""
    for line in orig.splitlines(True):  # 保留换行
        if line.strip():  # 非空行
            indent_prefix = re.match(r"[ \t]*", line).group(0)  # 支持空格或Tab
            break

    # 2) 为了能被解析，把公共缩进去掉（兼容“方法片段”）
    dedented = textwrap.dedent(orig)

    # 3) 解析并收集突变
    mod = cst.parse_module(dedented)
    collector = _CollectAll()
    mod.visit(collector)

    mutants: List[str] = []
    for orig_node, new_node in collector.mutations:
        try:
            mutated_mod: cst.Module = mod.visit(_OneChange(orig_node, new_node))
            # 取突变后的第一个函数定义
            func_node: Optional[cst.FunctionDef] = None
            for stmt in mutated_mod.body:
                if isinstance(stmt, cst.FunctionDef):
                    func_node = stmt
                    break
            if func_node is None:
                continue

            # 4) 将函数定义序列化为代码（老/新版 LibCST 都兼容）
            base_code = _func_to_code(func_node)
            # 确保末尾换行
            if not base_code.endswith("\n"):
                base_code += "\n"

            # 5) 补回原始缩进前缀
            indented_code = textwrap.indent(base_code, indent_prefix)

            mutants.append(indented_code)
        except Exception:
            # 个别突变可能导致不合法代码，直接跳过
            continue

    # 可选：去重，防止不同 operator 产生相同源码
    # mutants = list(dict.fromkeys(mutants))
    return mutants
