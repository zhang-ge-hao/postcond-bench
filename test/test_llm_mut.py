

from src.mutation.llm import generate_mutants_for_method
from src.ds import *
from src.clone import repository_reproduct

if __name__ == "__main__":
    input_dir = "data/step/5.exec_check/xuxueli--xxl-tool.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[0]

    input_dir = "data/step/5.exec_check/aeturrell--skimpy.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[0]

    generate_mutants_for_method(method)
    pass
