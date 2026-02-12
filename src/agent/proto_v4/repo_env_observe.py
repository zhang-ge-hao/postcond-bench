
from src.ds import *
import json
import time
from src.clone import repository_reproduct

if __name__ == "__main__":
    method_path = "data/step/8.benchmark/keon--algorithms--_load_byte.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))
    with repository_reproduct(method.repo) as repo_dir:
        print(repo_dir)
        time.sleep(1000000000)
