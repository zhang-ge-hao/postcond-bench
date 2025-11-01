from src.postcond import (
    postcond_generation,
    postcond_generation_pool
)

from src.ds import *
from src.clone import repository_reproduct
import json

if __name__ == "__main__":
    input_path = "data/step/8.benchmark/bottlepy--bottle--remote_route.json"
    with open(input_path) as file:
        method = Method.from_dict(json.load(file))

    method.model_name = "gpt-4o-mini"
    method.generate_num = 5
    method.w_code = False

    method = postcond_generation(method)

    pass

    # postcond_generation_pool("data/step/6.mutation", "data/step/7.postcond")