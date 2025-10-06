import os
from src.ds import Repo, StaticMethod
from typing import *
from src.util import parse_file, get_language_and_parser
from src.clone import repository_reproduct
from src.method.static.cc import (
    cyclomatic_complexity_python,
    cyclomatic_complexity_java
)
import json
import unicodedata
import string
import re




def is_code(file_path: str, lang):
    suffix_map = {"python": ".py", "java": ".java"}
    assert lang in suffix_map
    suffix = suffix_map[lang]
    return file_path.endswith(suffix)


def code_paths(lang):
    # cwd in current repo required
    # NOTE: ordered!
    paths = []
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            rel_path = os.path.join(root, name)
            # NOTE: ".venv" not in rel_path
            if ".venv" not in rel_path and is_code(rel_path, lang):
                paths.append(rel_path)
    paths.sort()
    return paths


def iter_tree_and_code_bytes(lang, parser):
    # cwd in current repo required
    for code_path in code_paths(lang):
        tree, code_str, code_bytes = parse_file(code_path, parser)
        yield tree, code_str, code_bytes, code_path


def is_method(ts_node, lang):
    method_type_map = {"python": "function_definition", 
                       "java": "method_declaration"}
    assert lang in method_type_map
    method_type = method_type_map[lang]
    return ts_node.type == method_type


def iter_method_ts_node(tree, lang):
    queue = [tree.root_node]
    while len(queue) > 0:
        cur_node = queue.pop(0)
        if is_method(cur_node, lang):
            yield cur_node
        else:
            for child in cur_node.children:
                queue.append(child)


def get_method_body(method_ts_node, lang):
    if lang == "python":
        if method_ts_node.children[-1].type == "block":
            return method_ts_node.children[-1]
        else:
            return None
    elif lang == "java":
        body = method_ts_node.child_by_field_name("body")
        if body is not None:
            return body
        else:
            return None
    else:
        raise NotImplementedError()


def get_stat_number(body_ts_node, lang):
    number = 0
    queue = [body_ts_node]
    while len(queue) > 0:
        cur_node = queue.pop(0)
        if lang == "python":
            if cur_node.type.endswith("statement"):
                is_str = len(cur_node.children) == 1 and \
                    cur_node.children[0].type == "string"
                if not is_str:
                    number += 1
        elif lang == "java":
            if cur_node.type == "local_variable_declaration":
                number += 1
            elif cur_node.type.endswith("statement"):
                number += 1
        else:
            raise NotImplementedError()
        for child in cur_node.children:
            queue.append(child)
    return number


def get_cc(body_ts_node, code_bytes, lang):
    if lang == "python":
        return cyclomatic_complexity_python(body_ts_node, code_bytes)
    elif lang == "java":
        return cyclomatic_complexity_java(body_ts_node, code_bytes)
    else:
        raise NotImplementedError()


def has_return(method_ts_node, lang):
    if lang == "python":
        stop_types = {"function_definition", 
                      "async_function_definition", 
                      "class_definition", 
                      "lambda"}
        queue = [c for c in method_ts_node.children]
        while len(queue) > 0:
            cur_node = queue.pop(0)
            if cur_node.type in stop_types:
                # 不要进入别的作用域
                continue
            if cur_node.type == "return_statement":
                if len(cur_node.children) > 1:
                    return True
            for child in cur_node.children:
                queue.append(child)
        return False
    elif lang == "java":
        t = method_ts_node.child_by_field_name("type")
        if t is None:
            # 没有 type 基本只会出现在构造器，这里兜底当作“无返回值”
            return False
        # 在 tree-sitter-java 里，void 的节点类型是 'void_type'
        return t.type != "void_type"


def get_comment(method_ts_node, body_ts_node, code_bytes: bytes, lang):
    if lang == "python":
        expression = body_ts_node.children[0]
        if expression.type == "expression_statement" and len(expression.children) == 1:
            string_node = expression.children[0]
            if string_node.type == "string":
                return code_bytes[string_node.start_byte: 
                                  string_node.end_byte].decode("utf-8")
        return None
    elif lang == "java":
        modifier_types = ["modifiers", "marker_annotation", "annotation"]
        comment_types = ["block_comment", "comment"]
        prev = method_ts_node.prev_sibling
        while prev and prev.type in modifier_types + comment_types:
            if prev.type in comment_types:
                prev_str = code_bytes[prev.start_byte: prev.end_byte].decode("utf-8")
                if prev_str.startswith("/*"):
                    return prev_str
            prev = prev.prev_sibling
        return None


def is_good_comment(comment: str, lang, word_restriction) -> bool:
    # 不包含中日韩文
    CJK_RE = re.compile(
        r'[\u2E80-\u2FFF\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]'
        r'|[\uFF01-\uFF60\uFFE0-\uFFE6]'  # 全角标点/符号
    )
    if bool(CJK_RE.search(comment)):
        return False

    # 获取字母和空格
    letters_and_spaces = [
        ch for ch in comment 
        if unicodedata.category(ch).startswith('L') 
        or ch == " "]

    # 获取单词数
    words = [w for w in "".join(letters_and_spaces).split(" ") 
             if len(w) > 0]
    if len(words) < word_restriction:
        return False

    # ascii字母占总字母的95%以上
    letters = [ch for ch in letters_and_spaces if ch != " "]
    if not letters:
        return False
    ascii_letters = sum(ch in string.ascii_letters for ch in letters)
    return ascii_letters / len(letters) >= 0.95


def get_line_position_1i(method_ts_node, body_ts_node, lang):
    end_line = method_ts_node.end_point.row
    
    if lang == "python":
        included_prev_types = ["decorator"]
    elif lang == "java":
        modifier_types = ["modifiers", "marker_annotation", "annotation"]
        comment_types = ["block_comment", "comment"]
        included_prev_types = modifier_types + comment_types
    else:
        raise NotImplementedError()
    stn = method_ts_node # start node
    while stn.prev_sibling and stn.prev_sibling.type in included_prev_types:
        stn = stn.prev_sibling
    start_line = stn.start_point.row

    if lang == "python":
        first_expression = body_ts_node.children[0]
        is_str = len(first_expression.children) == 1 and \
            first_expression.children[0].type == "string"
        if not is_str:
            body_start_line = body_ts_node.start_point.row
        else:
            body_start_line = first_expression.end_point.row + 1
    if lang == "java":
        body_start_line = body_ts_node.start_point.row
    # in case `int main() {`
    if body_start_line == body_ts_node.prev_sibling.end_point.row:
        body_start_line += 1

    start_line += 1
    end_line += 1
    body_start_line += 1

    return start_line, end_line, body_start_line


def get_method_name(method_ts_node, code_bytes, lang):
    name_node = method_ts_node.child_by_field_name('name')
    if name_node is None:
        return "None"
    name = code_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8")
    return name
