
import os
from src.ds import *

from itertools import product
from tqdm import tqdm

from src.postcond import response_post_process


def read_benchmark(p="data/step/8.benchmark") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods


def combine_claude_4_5_item(
        method: Method, response_dicts: List[Dict], output_root: str):
    output_root = os.path.abspath(output_root)

    b_output_root = "data/step"
    b_model_name = "claude-3-5-haiku"
    b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    if method.prompting is not None:
        folder_name += f"--{method.prompting}"
    folder_path = f"{output_root}/9.{folder_name}"
    
    repo_name = method.repo.github_path.replace("/", "--")
    file_name = f"{repo_name}--{method.rlid}"
    
    custom_id = f"{folder_name}--{file_name}"

    with open(f"{b_folder_path}/{file_name}.json") as file:
        b_method = Method.from_dict(json.load(file))

    method.prompt = b_method.prompt

    responses = [None] * method.generate_num
    for generate_idx in range(method.generate_num):
        json_id = f"{custom_id}--{generate_idx}"
        for response_dict in response_dicts:
            if response_dict["recordId"] == json_id:
                model_output = response_dict["modelOutput"]["content"]
                model_output = [d for d in model_output if d["type"] == "text"][0]
                model_output = model_output["text"]
                responses[generate_idx] = model_output
    
    postconds = [response_post_process(r) for r in responses]

    assert all(p is not None for p in postconds)

    method.postconds = postconds

    if not os.path.exists(f"{folder_path}"):
        os.makedirs(f"{folder_path}")
    with open(f"{folder_path}/{file_name}.json", "w") as file:
        json.dump(method.to_dict(), file, indent=2)

def combine_claude_4_5():
    methods = read_benchmark()

    methods = methods

    model_names = ["claude-sonnet-4-5"]

    prompting = [None, "no_gram", "fsl_1", "fsl_3", "fsl_5"]
    generate_nums = [5, 1, 1, 1, 1]

    methods_output_root = "data/step_tmp/"
    methods_output_root = os.path.abspath(methods_output_root)

    response_dicts = []
    model_output_path = "data/batch--claude-sonnet-4-5--out"
    for file_name in os.listdir(model_output_path):
        file_path = f"{model_output_path}/{file_name}"
        with open(file_path) as file:
            for line in file:
                response_dicts.append(json.loads(line))

    __iter = list(product([True, False], zip(prompting, generate_nums)))
    for model_name in model_names:
        for method in tqdm(methods):
            for w_code, (prompting, generate_num) in __iter:
                method.model_name = model_name
                method.w_code = w_code
                method.prompting = prompting
                method.generate_num = generate_num
                combine_claude_4_5_item(
                    method, response_dicts=response_dicts,
                    output_root=methods_output_root)


def combine_gpt_5_item(
        method: Method, response_dicts: List[Dict], output_root: str,
        gen_root: str):
    output_root = os.path.abspath(output_root)

    b_output_root = "data/step"
    b_model_name = "claude-3-5-haiku"
    b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    if method.prompting is not None:
        folder_name += f"--{method.prompting}"
    folder_path = f"{output_root}/9.{folder_name}"

    gen_folder_path = f"{gen_root}/9.{folder_name}"
    
    repo_name = method.repo.github_path.replace("/", "--")
    file_name = f"{repo_name}--{method.rlid}"
    
    custom_id = f"{folder_name}--{file_name}"

    with open(f"{b_folder_path}/{file_name}.json") as file:
        b_method = Method.from_dict(json.load(file))

    method.prompt = b_method.prompt

    responses = [None] * method.generate_num
    for generate_idx in range(method.generate_num):
        json_id = f"{custom_id}--{generate_idx}"
        for response_dict in response_dicts:
            if response_dict["custom_id"] == json_id:
                model_output = response_dict["response"]["body"]["output"]
                model_output = [d for d in model_output if d["type"] == "message"][0]
                assert len(model_output["content"]) == 1
                model_output = model_output["content"][0]["text"]
                responses[generate_idx] = model_output

    if all(r is not None for r in responses):
        postconds = [response_post_process(r) for r in responses]

        assert all(p is not None for p in postconds)

        method.postconds = postconds

        if not os.path.exists(f"{gen_folder_path}"):
            os.makedirs(f"{gen_folder_path}")
        with open(f"{gen_folder_path}/{file_name}.json", "w") as file:
            json.dump(method.to_dict(), file, indent=2)

def combine_gpt_5():
    methods = read_benchmark()

    methods = methods

    model_names = ["gpt-5"]

    prompting = [None, "no_gram", "fsl_1", "fsl_3", "fsl_5"]
    generate_nums = [5, 1, 1, 1, 1]

    methods_output_root = "data/step_tmp/"
    methods_output_root = os.path.abspath(methods_output_root)

    gen_root = "data/step_gen/"
    gen_root = os.path.abspath(gen_root)

    response_dicts = []
    model_output_path = "data/batch--gpt-5--out--1st-run"
    for file_name in os.listdir(model_output_path):
        file_path = f"{model_output_path}/{file_name}"
        with open(file_path) as file:
            for line in file:
                response_dicts.append(json.loads(line))

    __iter = list(product([True, False], zip(prompting, generate_nums)))
    for model_name in model_names:
        for method in tqdm(methods):
            for w_code, (prompting, generate_num) in __iter:
                method.model_name = model_name
                method.w_code = w_code
                method.prompting = prompting
                method.generate_num = generate_num
                combine_gpt_5_item(
                    method, response_dicts=response_dicts,
                    output_root=methods_output_root,
                    gen_root=gen_root)

def get_jsons(
        method: Method, 
        methods: List[Method],
        output_root: str) -> List[Dict]:
    output_root = os.path.abspath(output_root)

    b_output_root = "data/step"
    b_model_name = "claude-3-5-haiku"
    b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    if method.prompting is not None:
        folder_name += f"--{method.prompting}"
    folder_path = f"{output_root}/9.{folder_name}"
    
    repo_name = method.repo.github_path.replace("/", "--")
    file_name = f"{repo_name}--{method.rlid}"
    
    custom_id = f"{folder_name}--{file_name}"

    with open(f"{b_folder_path}/{file_name}.json") as file:
        b_method = Method.from_dict(json.load(file))

    method.prompt = b_method.prompt

    ret = []

    for generate_idx in range(method.generate_num):
        json_id = f"{custom_id}--{generate_idx}"
        if method.model_name == "gpt-5":
            json_post = {
                "custom_id": json_id,
                "method": "POST", 
                "url": "/v1/responses", 
                "body": {
                    "model": "gpt-5",
                    "input": method.prompt,
                    "reasoning": {
                        "effort": "medium"
                    }
                }
            }
            ret.append(json_post)
        elif method.model_name == "claude-sonnet-4-5":
            json_post = {
                "recordId": json_id,
                "modelInput": {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "thinking": {
                        "type": "enabled",
                        "budget_tokens": 2048
                    },
                    "messages": [
                        {
                            "role": "user", 
                            "content": [
                                {
                                    "type": "text", 
                                    "text": method.prompt
                                } 
                            ]
                        }
                    ]
                }
            }
            ret.append(json_post)

    if not os.path.exists(f"{folder_path}"):
        os.makedirs(f"{folder_path}")
    with open(f"{folder_path}/{file_name}.json", "w") as file:
        json.dump(method.to_dict(), file, indent=2)

    return ret


def get_prompts():
    methods = read_benchmark()

    methods = methods

    model_names = ["gpt-5", "claude-sonnet-4-5"]

    prompting = [None, "no_gram", "fsl_1", "fsl_3", "fsl_5"]
    generate_nums = [5, 1, 1, 1, 1]

    methods_output_root = "data/step_tmp/"
    methods_output_root = os.path.abspath(methods_output_root)
    
    __iter = list(product([True, False], zip(prompting, generate_nums)))
    for model_name in model_names:

        json_list = []
        for method in tqdm(methods):
            for w_code, (prompting, generate_num) in __iter:
                method.model_name = model_name
                method.w_code = w_code
                method.prompting = prompting
                method.generate_num = generate_num
                json_list.extend(get_jsons(
                    method, methods, 
                    output_root=methods_output_root))

        split_num = 7
        for split_idx in range(split_num):
            jsonl_output_path = f"data/batch--{model_name}/batch--{model_name}--{split_idx}.jsonl"
            with open(jsonl_output_path, "w") as file:
                for json_idx, json_post in enumerate(json_list):
                    if json_idx % split_num == split_idx:
                        file.write(json.dumps(json_post) + "\n")

if __name__ == "__main__":
    # get_prompts()
    # combine_claude_4_5()
    combine_gpt_5()