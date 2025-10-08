from src.ds import *
import os

from src.method.cov import (
    cov_filter,
    cov_filter_pool
)

if __name__ == "__main__":
    # # # input_dir = "data/step/3.static/aeturrell--skimpy.jsonl"
    # # # input_dir = "data/step/3.static/alimate--errors-spring-boot-starter.jsonl"

    # # input_dir = "data/step/3.static/sqlalchemy--alembic.jsonl"
    # # methods = Method.load_li(input_dir)
    # # method = methods[7]

    # input_dir = "data/step/3.static/jenkinsci--kubernetes-plugin.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[13]

    # cov_filter(method)

    cov_filter_pool("data/step/3.static", "data/step/4.cov")
