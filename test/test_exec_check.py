

from src.method.exec_check import exec_check
from src.ds import *

if __name__ == "__main__":
    # input_dir = "data/step/4.cov/python-cmd2--cmd2.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[50]

    input_dir = "data/step/4.cov/addthis--stream-lib.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[0]

    exec_check(method)