

from src.method.exec_check import (
    exec_check,
    exec_check_pool
)
from src.ds import *

if __name__ == "__main__":
    # # input_dir = "data/step/4.cov/python-cmd2--cmd2.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[50]

    # # input_dir = "data/step/4.cov/addthis--stream-lib.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[0]

    # # input_dir = "data/step/4.cov/falconry--falcon.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[103]

    # # input_dir = "data/step/4.cov/Password4j--password4j.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[11]

    # input_dir = "data/step/4.cov/networknt--json-schema-validator.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[31]

    # exec_check(method)

    exec_check_pool("data/step/4.cov", "data/step/5.exec_check")
