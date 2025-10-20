# src/mutation/java_mutators.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Iterable

from tree_sitter import Node

# -----------------------------
# 通用文本替换工具（基于 bytes 偏移）
# -----------------------------

@dataclass(frozen=True)
class TextEdit:
    start_byte: int
    end_byte: int
    replacement: str

def apply_single_edit(code_str: str, edit: TextEdit) -> str:
    b = code_str.encode("utf-8")
    before = b[:edit.start_byte]
    after = b[edit.end_byte:]
    rep = edit.replacement.encode("utf-8")
    newb = before + rep + after
    return newb.decode("utf-8")

def node_text(code_str: str, node: Node) -> str:
    b = code_str.encode("utf-8")
    return b[node.start_byte:node.end_byte].decode("utf-8")

def is_identifier_like(node: Node) -> bool:
    return node.type in ("identifier",)

def is_field_access_like(node: Node) -> bool:
    # tree-sitter-java 常见字段/成员访问节点：field_access, scoped_identifier, member_select
    return node.type in ("field_access", "scoped_identifier", "member_select")

def child_of_type(node: Node, t: str) -> Optional[Node]:
    for i in range(node.child_count):
        c = node.child(i)
        if c.type == t:
            return c
    return None

def find_all(node: Node, type_name: str) -> Iterable[Node]:
    # DFS
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.type == type_name:
            yield cur
        for i in range(cur.child_count):
            stack.append(cur.child(i))

def token_is_operator_between_children(code_str: str, node: Node, ops: set[str]) -> Optional[Tuple[int, int, str]]:
    """
    在 binary_expression 的子节点中，直接查找匿名运算符 token。
    返回 (start_byte, end_byte, op_string)；找不到则返回 None。
    """
    if node.type != "binary_expression":
        return None

    # 遍历所有 child，找到“未命名”的且类型就是我们想要的运算符
    # （tree-sitter 把运算符作为匿名 token，c.is_named == False，c.type 为 '<', '<=', '<<', '>>', '>>>', '+', ...）
    for i in range(node.child_count):
        c = node.child(i)
        if not c.is_named and c.type in ops:
            # 直接使用这个 token 的 byte 范围即可替换
            op = c.type
            return (c.start_byte, c.end_byte, op)

    return None

def has_string_literal_child(node: Node, code_str: str) -> bool:
    # 直接判断子树是否包含 string_literal
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.type == "string_literal":
            return True
        for i in range(cur.child_count):
            stack.append(cur.child(i))
    return False

def extract_method_return_type(method_node: Node, code_str: str) -> Optional[str]:
    # method_declaration: modifiers? type declarator (parameters) ...
    # 尝试读取第一个类型节点（type, integral_type, floating_point_type, void_type, etc.）
    # 简化策略：找到第一个类型类节点文本
    type_nodes = ("type", "integral_type", "floating_point_type", "void_type", "boolean_type", "type_identifier", "generic_type")
    for i in range(method_node.child_count):
        c = method_node.child(i)
        if c.type in type_nodes:
            return node_text(code_str, c).strip()
    return None

def method_has_notnull_annotation(method_node: Node, code_str: str) -> bool:
    # 粗略检查：在 method_declaration 的起始前的修饰（modifiers）里含有 @NotNull
    # 也可能写在返回类型注解位置，这里以源码片段文本包含为近似
    head_text = node_text(code_str, method_node)[:200]  # 取签名前一小段
    return "@NotNull" in head_text or "@javax.annotation.Nonnull" in head_text or "@NonNull" in head_text

# -----------------------------
# Mutator 抽象基类
# -----------------------------

class JavaMutator:
    name: str = "base"

    def mutate(self, code_str: str, root: Node) -> List[str]:
        edits = self._collect_edits(code_str, root)
        mutants = []
        for e in edits:
            mutants.append(apply_single_edit(code_str, e))
        return mutants

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        raise NotImplementedError

# -----------------------------
# 具体 Mutators
# -----------------------------

class ConditionalsBoundaryMutator(JavaMutator):
    name = "conditionals_boundary"
    mapping = {
        "<": "<=",
        "<=": "<",
        ">": ">=",
        ">=": ">"
    }
    targets = set(mapping.keys())

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        for be in find_all(root, "binary_expression"):
            tok = token_is_operator_between_children(code_str, be, self.targets)
            if not tok:
                continue
            start, end, op = tok
            edits.append(TextEdit(start, end, self.mapping[op]))
        return edits


class NegateConditionalsMutator(JavaMutator):
    name = "negate_conditionals"
    mapping = {
        "==": "!=",
        "!=": "==",
        "<=": ">",
        ">=": "<",
        "<": ">=",
        ">": "<=",
    }
    targets = set(mapping.keys())

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        for be in find_all(root, "binary_expression"):
            tok = token_is_operator_between_children(code_str, be, self.targets)
            if not tok:
                continue
            start, end, op = tok
            edits.append(TextEdit(start, end, self.mapping[op]))
        return edits


class IncrementsMutator(JavaMutator):
    name = "increments"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []

        # update_expression: ++i, i++, --i, i--
        for ue in find_all(root, "update_expression"):
            txt = node_text(code_str, ue)
            if "++" in txt or "--" in txt:
                # 判断是否为局部变量：其子节点若为 identifier 认为是局部
                # update_expression 结构多样，保守检查任意子节点是否 identifier
                is_local = any(is_identifier_like(ue.child(i)) for i in range(ue.child_count))
                is_member = any(is_field_access_like(ue.child(i)) for i in range(ue.child_count))
                if is_local and not is_member:
                    if "++" in txt:
                        edits.append(TextEdit(ue.start_byte + txt.index("++"), ue.start_byte + txt.index("++") + 2, "--"))
                    else:
                        edits.append(TextEdit(ue.start_byte + txt.index("--"), ue.start_byte + txt.index("--") + 2, "++"))

        # assignment_expression: i += 1 / i -= 1
        for ae in find_all(root, "assignment_expression"):
            txt = node_text(code_str, ae)
            # 左孩子为 identifier 才认为是局部
            lhs = ae.child(0) if ae.child_count >= 1 else None
            if lhs and is_identifier_like(lhs) and not is_field_access_like(lhs):
                # 在 lhs 与 rhs 之间找操作符
                if "+=" in txt or "-=" in txt:
                    if "+=" in txt:
                        off = txt.index("+=")
                        edits.append(TextEdit(ae.start_byte + off, ae.start_byte + off + 2, "-="))
                    else:
                        off = txt.index("-=")
                        edits.append(TextEdit(ae.start_byte + off, ae.start_byte + off + 2, "+="))
        return edits


class InvertNegativesMutator(JavaMutator):
    name = "invert_negatives"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        for ue in find_all(root, "unary_expression"):
            txt = node_text(code_str, ue).strip()
            # 仅处理以 '-' 开头的一元表达式
            if not txt.startswith("-"):
                continue
            # 获取操作数节点
            # 常见结构： ('-' token) + operand
            # 这里通过子节点跳过符号，定位操作数
            if ue.child_count == 0:
                continue
            # 寻找第一个非符号子节点
            operand: Optional[Node] = None
            for i in range(ue.child_count):
                c = ue.child(i)
                if c.type not in ("-",):
                    operand = c
                    break
            if operand is None:
                continue

            # 过滤常量负号（不对 -1/-2.0 等）
            if operand.type in ("decimal_integer_literal", "hex_integer_literal", "octal_integer_literal",
                                "binary_integer_literal", "decimal_floating_point_literal",
                                "hex_floating_point_literal"):
                continue

            # 简化支持：identifier / field_access / (identifier)
            is_ok = operand.type in ("identifier", "field_access", "parenthesized_expression")
            if not is_ok:
                continue

            # 替换：删除前导 '-'
            # 通过定位 ue 源码中第一个 '-' 的位置实现
            dash_pos = node_text(code_str, ue).find("-")
            edits.append(TextEdit(ue.start_byte + dash_pos, ue.start_byte + dash_pos + 1, ""))
        return edits


class MathMutator(JavaMutator):
    name = "math"
    mapping = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*",
        "%": "*",
        "&": "|",
        "|": "&",
        "^": "&",
        "<<": ">>",
        ">>": "<<",
        ">>>": "<<",
    }
    targets = set(mapping.keys())

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        for be in find_all(root, "binary_expression"):
            tok = token_is_operator_between_children(code_str, be, self.targets)
            if not tok:
                continue
            start, end, op = tok

            # 避免字符串拼接："foo" + x 或 x + "bar"
            if op == "+":
                left = be.child(0)
                right = be.child(be.child_count - 1)
                if has_string_literal_child(left, code_str) or has_string_literal_child(right, code_str):
                    continue

            edits.append(TextEdit(start, end, self.mapping[op]))
        return edits


class VoidMethodCallMutator(JavaMutator):
    name = "void_method_call"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        # 工程化近似：删除由 method_invocation 构成的整条 expression_statement
        for st in find_all(root, "expression_statement"):
            if st.child_count == 0:
                continue
            # 语句内部若含有 method_invocation 且不是赋值/使用结果，近似视作 void 调用
            inner = node_text(code_str, st)
            # 简单过滤：含 '=' 的可能是赋值调用结果，保留
            if "=" in inner:
                continue
            # 结构性检查：直接包含 method_invocation
            has_invocation = any(
                st.child(i).type in ("method_invocation",) for i in range(st.child_count)
            )
            if not has_invocation:
                continue
            # 删除整条语句（含分号与换行）
            edits.append(TextEdit(st.start_byte, st.end_byte, ""))  # 空替换
        return edits


# ---- Return 替换基元 ----

def _collect_return_sites(root: Node) -> List[Node]:
    return list(find_all(root, "return_statement"))

def _method_node(root: Node) -> Optional[Node]:
    # content 是单个方法，root 可能就是 method_declaration 或者包含它
    # 保险起见遍历找第一个
    for n in find_all(root, "method_declaration"):
        return n
    return None

def _normalize_type_name(t: Optional[str]) -> str:
    if not t:
        return ""
    return " ".join(t.replace("\n", " ").replace("\t", " ").split())

def _is_primitive_numeric(t: str) -> bool:
    return any(t.startswith(x) for x in ("int", "short", "long", "char", "float", "double"))

def _is_boolean_type(t: str) -> bool:
    return t.strip().startswith("boolean") or "Boolean" in t

def _is_void(t: str) -> bool:
    return t.strip().startswith("void")

def _is_object_type(t: str) -> bool:
    return not _is_void(t) and not _is_primitive_numeric(t) and not _is_boolean_type(t)

def _ret_expr_for_empty(t: str) -> Optional[str]:
    # 按题述映射
    tN = t.replace("java.lang.", "").replace("java.util.", "")
    if tN.startswith("String"):
        return '""'
    if tN.startswith("Optional"):
        return "Optional.empty()"
    if any(tN.startswith(x) for x in ("List", "Collection")):
        return "java.util.Collections.emptyList()"
    if tN.startswith("Set"):
        return "java.util.Collections.emptySet()"
    if any(tN.startswith(x) for x in ("Integer", "Short", "Long", "Character", "Float", "Double")):
        return "0"
    return None

# ---- 具体 Return 类 ----

class EmptyReturnsMutator(JavaMutator):
    name = "empty_returns"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        m = _method_node(root)
        if m is None:
            return edits
        if method_has_notnull_annotation(m, code_str):
            # 仅 Null returns 需要受 NotNull 限制；Empty 不受限
            pass
        ret_type = _normalize_type_name(extract_method_return_type(m, code_str))
        if not ret_type or _is_void(ret_type):
            return edits

        replacement = _ret_expr_for_empty(ret_type)
        if replacement is None:
            return edits

        for r in _collect_return_sites(root):
            # 仅替换有返回值的 return
            if r.child_count == 0:
                continue
            txt = node_text(code_str, r)
            if "return" in txt and ";" in txt:
                # 把 return 与 ';' 之间内容替换掉
                start = r.start_byte + txt.index("return") + len("return")
                end = r.start_byte + txt.rfind(";")
                edits.append(TextEdit(start, end, " " + replacement))
        return edits


class FalseReturnsMutator(JavaMutator):
    name = "false_returns"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        m = _method_node(root)
        if m is None:
            return edits
        ret_type = _normalize_type_name(extract_method_return_type(m, code_str))
        if not ret_type or not _is_boolean_type(ret_type):
            return edits

        for r in _collect_return_sites(root):
            txt = node_text(code_str, r)
            if "return" in txt and ";" in txt:
                start = r.start_byte + txt.index("return") + len("return")
                end = r.start_byte + txt.rfind(";")
                edits.append(TextEdit(start, end, " false"))
        return edits


class TrueReturnsMutator(JavaMutator):
    name = "true_returns"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        m = _method_node(root)
        if m is None:
            return edits
        ret_type = _normalize_type_name(extract_method_return_type(m, code_str))
        if not ret_type or not _is_boolean_type(ret_type):
            return edits

        for r in _collect_return_sites(root):
            txt = node_text(code_str, r)
            if "return" in txt and ";" in txt:
                start = r.start_byte + txt.index("return") + len("return")
                end = r.start_byte + txt.rfind(";")
                edits.append(TextEdit(start, end, " true"))
        return edits


class NullReturnsMutator(JavaMutator):
    name = "null_returns"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        m = _method_node(root)
        if m is None:
            return edits
        if method_has_notnull_annotation(m, code_str):
            return edits
        ret_type = _normalize_type_name(extract_method_return_type(m, code_str))
        if not ret_type or not _is_object_type(ret_type):
            return edits

        for r in _collect_return_sites(root):
            txt = node_text(code_str, r)
            if "return" in txt and ";" in txt:
                start = r.start_byte + txt.index("return") + len("return")
                end = r.start_byte + txt.rfind(";")
                edits.append(TextEdit(start, end, " null"))
        return edits


class PrimitiveReturnsMutator(JavaMutator):
    name = "primitive_returns"

    def _collect_edits(self, code_str: str, root: Node) -> List[TextEdit]:
        edits: List[TextEdit] = []
        m = _method_node(root)
        if m is None:
            return edits
        ret_type = _normalize_type_name(extract_method_return_type(m, code_str))
        if not ret_type or not _is_primitive_numeric(ret_type):
            return edits

        for r in _collect_return_sites(root):
            txt = node_text(code_str, r)
            if "return" in txt and ";" in txt:
                start = r.start_byte + txt.index("return") + len("return")
                end = r.start_byte + txt.rfind(";")
                edits.append(TextEdit(start, end, " 0"))
        return edits


# 组合：全部 Java Mutators
ALL_JAVA_MUTATORS: List[JavaMutator] = [
    ConditionalsBoundaryMutator(),
    IncrementsMutator(),
    InvertNegativesMutator(),
    MathMutator(),
    NegateConditionalsMutator(),
    VoidMethodCallMutator(),
    EmptyReturnsMutator(),
    FalseReturnsMutator(),
    TrueReturnsMutator(),
    NullReturnsMutator(),
    PrimitiveReturnsMutator(),
]
