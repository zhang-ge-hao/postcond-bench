
from src.ds import *
import json
from openai import OpenAI

from src.agent.proto_fix_v2.tools.splitter import split_icontract_postconditions

import os, json
from src.ds import *
from typing import *
import random
from src.curator.eval_postcond import eval_postcond


KFS = ["jml_fail", "icontract_fail"]

def read_benchmark(p, save_mem=False) -> List[Method]:
    print(f"Reading {p}.")
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            if save_mem:
                method.repo.env_config = None
                method.repo.failed_tests = None
                method.cover_tests = None
                method.mutants = None
                method.postconds = None
                method.responses = None
            methods.append(method)
    return methods


if __name__ == "__main__":
    github_url = "https://github.com/roboflow/maestro/blob/f394fce0b2c2fe98b3f457ad5abb61a9c7e88c7b/./maestro/trainer/common/datasets/roboflow.py#L10-L41"

    methods = read_benchmark("data/step/9.Qwen3-32B-agent--v2-all")
    method = [m for m in methods if m.github_url == github_url][0]
    
    method_content = method.content
    postcond_set = method.postconds[0]

    postconds = split_icontract_postconditions(postcond_set)

    postcond = postconds[-1].to_decorator_block()

    # print(method_content)
    # print(postcond)

    prompt_template = open("src/agent/proto_fix_v2/tools/prompt_template.txt").read()

    prompt = prompt_template.format(method_source=method_content, postcondition=postcond)

    print(prompt)

    client = OpenAI(api_key="EMPTY", base_url=f"http://localhost:19990/v1")

    response = client.chat.completions.create(
        model="Qwen/Qwen3-32B",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        top_p=0.95,
        presence_penalty=1.5,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": True},
            "top_k": 20,
            "min_p": 0,
        },
    )

    response: str = [c.message.content for c in response.choices][0]
    print(response)