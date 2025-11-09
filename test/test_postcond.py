from src.postcond import (
    postcond_generation,
    postcond_generation_pool
)

from src.ds import *
from src.clone import repository_reproduct
import json
import os

if __name__ == "__main__":
    methods = []
    input_dir = "data/step/8.benchmark/"
    for fn in os.listdir(input_dir):
        file_path = f"{input_dir}/{fn}"
        with open(file_path) as file:
            methods.append(Method.from_dict(json.load(file)))

    input_path = "data/step/8.benchmark/americanexpress--unify-jdocs--getDifferences.json"
    with open(input_path) as file:
        method = Method.from_dict(json.load(file))

    method.model_name = "phi-4"
    method.generate_num = 1
    method.w_code = True
    method.prompting = None
    method.port = "19990"

    method = postcond_generation(method, methods=methods)

    pass

    # postcond_generation_pool("data/step/6.mutation", "data/step/7.postcond")