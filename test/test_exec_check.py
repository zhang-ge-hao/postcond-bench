

from src.method.exec_check import (
    exec_check,
    exec_check_pool
)
from src.ds import *
from src.clone import repository_reproduct

if __name__ == "__main__":
    # # input_dir = "data/step/4.cov/OpenHFT--Chronicle-Wire.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[130]

    # input_dir = "data/step/4.cov/OpenHFT--Chronicle-Wire.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[67]

    # # input_dir = "data/step/4.cov/strimzi--strimzi-kafka-bridge.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[0]

    # exec_check(method)

    exec_check_pool("data/step/4.cov", "data/step/5.exec_check")
