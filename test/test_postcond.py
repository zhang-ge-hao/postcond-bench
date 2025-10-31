from src.postcond import (
    postcond_generation,
    postcond_generation_pool
)

from src.ds import *
from src.clone import repository_reproduct

if __name__ == "__main__":
    input_dir = "data/step/7.postcond/dpguthrie--yahooquery.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[0]

    method = postcond_generation(method)

    # postcond_generation_pool("data/step/6.mutation", "data/step/7.postcond")