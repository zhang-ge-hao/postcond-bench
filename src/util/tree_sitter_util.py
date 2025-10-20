import os

from typing import List, Dict
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import tree_sitter_java as tsjava

from dataclasses import dataclass
from typing import *

def get_language_and_parser(lang: str):
    if lang == "python":
        language = Language(tspython.language())
    elif lang == "java":
        language = Language(tsjava.language())
    else:
        raise NotImplementedError()
    parser = Parser(language)
    return language, parser


def read_code(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        code_str = file.read()
        code_bytes = bytes(code_str, encoding="utf-8")
        return code_str, code_bytes


def parse_file(file_path: str, parser):
    code_str, code_bytes = read_code(file_path)
    tree = parser.parse(code_bytes)
    return tree, code_str, code_bytes

def parse_code(code_str: str, parser):
    code_bytes = code_str.encode("utf-8")
    tree = parser.parse(code_bytes)
    return tree, code_str, code_bytes
