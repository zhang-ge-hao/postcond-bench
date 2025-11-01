from .temp_dir import change_dir, create_tempdir
from .logger import set_logging, setup_child_io_logging
from .tree_sitter_util import (
    get_language_and_parser, 
    read_code, 
    parse_file,
    parse_code
)
import difflib

def get_uuid7():
    from uuid6 import uuid7
    return uuid7()

def get_diff(src: str, tgt: str) -> str:
    diff_lines = difflib.unified_diff(
        src.splitlines(keepends=True),
        tgt.splitlines(keepends=True),
        lineterm=""
    )
    diff_str = "".join(list(diff_lines)[3: ])
    diff_str = diff_str.rstrip()
    return diff_str
