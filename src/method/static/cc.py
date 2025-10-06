# 依赖：tree_sitter（已存在于你的环境）、源码 bytes
# 说明：
#   - 复杂度 = 1 + 决策点数
#   - Python: if/elif、for/while、三目(if-exp)、except、推导式(for/if)、match/case、
#             and/or（每个布尔运算符 +1）、可选 assert
#   - Java: if、for/while/do、switch 的 case/default、catch、三目(?:)、
#           逻辑 && / ||（每个运算符 +1）

from typing import Dict, Iterable

# ------- 小助手 -------
def _walk(node) -> Iterable:
    stack = [node]
    while stack:
        n = stack.pop()
        yield n
        # 反向压栈保证子节点自然顺序
        stack.extend(reversed(list(n.children)))

def _slice_between(src_bytes: bytes, left_node, right_node) -> bytes:
    """tree-sitter-java 的 binary_expression 运算符文本在左右子树之间"""
    return src_bytes[left_node.end_byte:right_node.start_byte]

# ========== Python 复杂度 ==========
def cyclomatic_complexity_python(fn_node, src_bytes: bytes, *, count_assert: bool = False) -> Dict[str, int]:
    """
    参数：
      fn_node   : Python 的 function_definition / async_function_definition 节点（或更高层想要统计的子树）
      src_bytes : 整个源码的 bytes（UTF-8），用于读取布尔运算符等原文
      count_assert : 是否把 assert 计入决策点
    返回：
      breakdown 字典，含各项计数与 total
    """
    b = {
        "base": 1, "ifs": 0, "elifs": 0, "loops": 0, "bool_ops": 0,
        "ternary": 0, "catches": 0, "cases": 0, "comp_for": 0, "comp_if": 0,
        "asserts": 0, "total": 0,
    }

    for n in _walk(fn_node):
        t = n.type
        if t == "if_statement":
            b["ifs"] += 1
            # 统计 elif 子句
            for ch in n.children:
                if ch.type == "elif_clause":
                    b["elifs"] += 1
        elif t in {"for_statement", "while_statement"}:
            b["loops"] += 1
        elif t == "conditional_expression":  # x if cond else y
            b["ternary"] += 1
        elif t == "except_clause":
            b["catches"] += 1
        elif t in {"list_comprehension", "set_comprehension", "dictionary_comprehension", "generator_expression"}:
            # 推导式中的 for_in_clause 与 if_clause
            for d in _walk(n):
                if d.type == "for_in_clause":
                    b["comp_for"] += 1
                elif d.type == "if_clause":
                    b["comp_if"] += 1
        elif t == "match_statement":  # Python 3.10+
            for ch in n.children:
                if ch.type == "case_clause":
                    b["cases"] += 1
        elif t == "boolean_operator":
            # 文本为 b"and"/b"or"
            op = src_bytes[n.start_byte:n.end_byte]
            if op in (b"and", b"or"):
                b["bool_ops"] += 1
        elif t == "assert_statement" and count_assert:
            b["asserts"] += 1

    b["total"] = sum(v for k, v in b.items() if k not in ("total"))
    return b

# ========== Java 复杂度 ==========
def cyclomatic_complexity_java(method_node, src_bytes: bytes, *, count_assert: bool = False) -> Dict[str, int]:
    """
    参数：
      method_node : Java 的 method_declaration / constructor_declaration 节点（或更高层想要统计的子树）
      src_bytes   : 整个源码的 bytes（UTF-8），用于读取运算符与 switch label 文本
      count_assert: Java 一般不把 assert 计入，这里可选
    返回：
      breakdown 字典，含各项计数与 total
    """
    b = {
        "base": 1, "ifs": 0, "loops": 0, "bool_ops": 0,
        "ternary": 0, "catches": 0, "cases": 0, "asserts": 0, "total": 0,
    }

    for n in _walk(method_node):
        t = n.type
        if t == "if_statement":
            b["ifs"] += 1
        elif t in {"for_statement", "enhanced_for_statement", "while_statement", "do_statement"}:
            b["loops"] += 1
        elif t in {"switch_statement", "switch_expression"}:
            # 统计每个 switch_label（case/default）
            for d in _walk(n):
                if d.type == "switch_label":
                    lbl = src_bytes[d.start_byte:d.end_byte].strip()
                    if lbl.startswith((b"case", b"default")):
                        b["cases"] += 1
        elif t == "catch_clause":
            b["catches"] += 1
        elif t == "conditional_expression":  # ?: 三目
            b["ternary"] += 1
        elif t == "binary_expression":
            # 识别 && 和 ||（每个算 1）
            left = n.child_by_field_name("left")
            right = n.child_by_field_name("right")
            if left and right:
                op_bytes = _slice_between(src_bytes, left, right)
                # 一条表达式里可能同时含有两个不同逻辑运算（极少见），分别计数
                if b"&&" in op_bytes:
                    b["bool_ops"] += op_bytes.count(b"&&")
                if b"||" in op_bytes:
                    b["bool_ops"] += op_bytes.count(b"||")
        elif t == "assert_statement" and count_assert:
            b["asserts"] += 1

    b["total"] = sum(v for k, v in b.items() if k not in ("total"))
    return b
