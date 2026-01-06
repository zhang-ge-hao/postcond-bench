
import os
from src.ds import *

from itertools import product
from tqdm import tqdm
import shutil
from src.postcond import response_post_process

from transformers import AutoTokenizer, Llama4ForConditionalGeneration

PI_WORKDIR = os.environ.get("PI_WORKDIR")


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
    b_model_name = "Qwen3-32B"
    if method.w_code is not None:
        b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        b_folder_name = b_model_name
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    if method.w_code is not None:
        folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        folder_name = method.model_name
    if method.prompting is not None:
        folder_name += f"--{method.prompting}"
    folder_path = f"{output_root}/9.{folder_name}"
    
    repo_name = method.repo.github_path.replace("/", "--")
    file_name = f"{repo_name}--{method.rlid}"
    
    custom_id = f"{folder_name}--{file_name}"

    if not os.path.exists(f"{folder_path}"):
        os.makedirs(f"{folder_path}")

    output_path = f"{folder_path}/{file_name}.json"
    cache_path = f"{PI_WORKDIR}/{b_output_root}/9.{folder_name}/{file_name}.json"
    if os.path.exists(cache_path):
        shutil.copy(cache_path, output_path)
        return 0

    with open(f"{b_folder_path}/{file_name}.json") as file:
        b_method = Method.from_dict(json.load(file))

    method.prompt = b_method.prompt

    responses = [None] * method.generate_num
    for generate_idx in range(method.generate_num):
        json_id = f"{custom_id}--{generate_idx}"
        for response_dict in response_dicts:
            if response_dict["recordId"].replace("--wo_code", "") == json_id:
                model_output = response_dict["modelOutput"]["content"]
                model_output = [d for d in model_output if d["type"] == "text"][0]
                model_output = model_output["text"]
                responses[generate_idx] = model_output
    if all(r is not None for r in responses):
        postconds = [response_post_process(r) for r in responses]
        assert all(p is not None for p in postconds)
    else:
        postconds = None

    method.postconds = postconds

    with open(f"{folder_path}/{file_name}.json", "w") as file:
        json.dump(method.to_dict(), file, indent=2)
    
    return 1 if method.postconds is None else 2

def combine_claude_4_5():
    methods = read_benchmark()

    methods = methods

    model_names = ["claude-sonnet-4-5"]

    promptings = ["v2-all", "v2-code", "v2-nl"]
    generate_nums = [5, 5, 5]

    methods_output_root = "data/step_gen/"
    methods_output_root = os.path.abspath(methods_output_root)

    response_dicts = []
    model_output_paths = [
        "data/batch--claude-sonnet-4-5--out--v2",
    ]
    for model_output_path in model_output_paths:
        for file_name in os.listdir(model_output_path):
            file_path = f"{model_output_path}/{file_name}"
            with open(file_path) as file:
                for line in file:
                    response_dicts.append(json.loads(line))

    status_hist = [0, 0, 0]

    for model_name in model_names:
        for method in tqdm(methods):
            for prompting, generate_num in zip(promptings, generate_nums):
                method.model_name = model_name
                method.task_version = "v2"
                method.w_code = None
                method.prompting = prompting
                method.generate_num = generate_num
                status = combine_claude_4_5_item(
                    method, response_dicts=response_dicts,
                    output_root=methods_output_root)
                status_hist[status] += 1
    print(status_hist)


def combine_gpt_5_item(
        method: Method, response_dicts: List[Dict], output_root: str):
    output_root = os.path.abspath(output_root)

    b_output_root = "data/step"
    b_model_name = "Qwen3-32B"
    if method.w_code is not None:
        b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        b_folder_name = b_model_name
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    if method.w_code is not None:
        folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        folder_name = method.model_name
    if method.prompting is not None:
        folder_name += f"--{method.prompting}"
    folder_path = f"{output_root}/9.{folder_name}"
    
    repo_name = method.repo.github_path.replace("/", "--")
    file_name = f"{repo_name}--{method.rlid}"
    
    custom_id = f"{folder_name}--{file_name}"

    if not os.path.exists(f"{folder_path}"):
        os.makedirs(f"{folder_path}")

    output_path = f"{folder_path}/{file_name}.json"
    cache_path = f"{PI_WORKDIR}/{b_output_root}/9.{folder_name}/{file_name}.json"
    if os.path.exists(cache_path):
        shutil.copy(cache_path, output_path)
        return 0

    with open(f"{b_folder_path}/{file_name}.json") as file:
        b_method = Method.from_dict(json.load(file))

    method.prompt = b_method.prompt

    responses = [None] * method.generate_num
    for generate_idx in range(method.generate_num):
        json_id = f"{custom_id}--{generate_idx}"
        for response_dict in response_dicts:
            if response_dict["custom_id"].replace("--wo_code", "") == json_id:
                model_output = response_dict["response"]["body"]["output"]
                model_output = [d for d in model_output if d["type"] == "message"][0]
                assert len(model_output["content"]) == 1
                model_output = model_output["content"][0]["text"]
                responses[generate_idx] = model_output

    if all(r is not None for r in responses):
        postconds = [response_post_process(r) for r in responses]
        assert all(p is not None for p in postconds)
    else:
        postconds = None

    method.postconds = postconds

    with open(f"{folder_path}/{file_name}.json", "w") as file:
        json.dump(method.to_dict(), file, indent=2)
    
    return 1 if method.postconds is None else 2

def combine_gpt_5():
    methods = read_benchmark()

    methods = methods

    model_names = ["gpt-5"]

    promptings = ["v2-all", "v2-code", "v2-nl"]
    generate_nums = [5, 5, 5]

    methods_output_root = "data/step_gen/"
    methods_output_root = os.path.abspath(methods_output_root)

    response_dicts = []
    model_output_paths = [
        "data/batch--gpt-5--out--3rd-run",
    ]
    for model_output_path in model_output_paths:
        for file_name in os.listdir(model_output_path):
            file_path = f"{model_output_path}/{file_name}"
            with open(file_path) as file:
                for line in file:
                    response_dicts.append(json.loads(line))

    status_hist = [0, 0, 0]

    for model_name in model_names:
        for method in tqdm(methods):
            for prompting, generate_num in zip(promptings, generate_nums):
                method.model_name = model_name
                method.task_version = "v2"
                method.w_code = None
                method.prompting = prompting
                method.generate_num = generate_num
                status = combine_gpt_5_item(
                    method, response_dicts=response_dicts,
                    output_root=methods_output_root)
                status_hist[status] += 1
    print(status_hist)



def combine_llama_4_item(
        method: Method, response_dicts: List[Dict], output_root: str):
    output_root = os.path.abspath(output_root)

    b_output_root = "data/step"
    b_model_name = "Qwen3-32B"
    if method.w_code is not None:
        b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        b_folder_name = b_model_name
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    if method.w_code is not None:
        folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        folder_name = method.model_name
    if method.prompting is not None:
        folder_name += f"--{method.prompting}"
    folder_path = f"{output_root}/9.{folder_name}"
    
    repo_name = method.repo.github_path.replace("/", "--")
    file_name = f"{repo_name}--{method.rlid}"
    
    custom_id = f"{folder_name}--{file_name}"

    if not os.path.exists(f"{folder_path}"):
        os.makedirs(f"{folder_path}")

    output_path = f"{folder_path}/{file_name}.json"
    cache_path = f"{PI_WORKDIR}/{b_output_root}/9.{folder_name}/{file_name}.json"
    if os.path.exists(cache_path):
        shutil.copy(cache_path, output_path)
        return 0

    with open(f"{b_folder_path}/{file_name}.json") as file:
        b_method = Method.from_dict(json.load(file))

    method.prompt = b_method.prompt

    responses = [None] * method.generate_num
    for generate_idx in range(method.generate_num):
        json_id = f"{custom_id}--{generate_idx}"
        for response_dict in response_dicts:
            if response_dict["recordId"].replace("--wo_code", "") == json_id:
                model_output = response_dict["modelOutput"]["generation"]
                responses[generate_idx] = model_output
    if all(r is not None for r in responses):
        postconds = [response_post_process(r) for r in responses]
        assert all(p is not None for p in postconds)
    else:
        postconds = None

    method.postconds = postconds

    with open(f"{folder_path}/{file_name}.json", "w") as file:
        json.dump(method.to_dict(), file, indent=2)
    
    return 1 if method.postconds is None else 2

def combine_llama_4():
    methods = read_benchmark()

    methods = methods

    model_names = ["llama-4-maverick"]

    promptings = ["v2-all", "v2-code", "v2-nl"]
    generate_nums = [5, 5, 5]

    methods_output_root = "data/step_gen/"
    methods_output_root = os.path.abspath(methods_output_root)

    response_dicts = []
    model_output_paths = [
        "data/batch--llama-4-maverick--out",
    ]
    for model_output_path in model_output_paths:
        for file_name in os.listdir(model_output_path):
            file_path = f"{model_output_path}/{file_name}"
            with open(file_path) as file:
                for line in file:
                    response_dicts.append(json.loads(line))

    status_hist = [0, 0, 0]

    for model_name in model_names:
        for method in tqdm(methods):
            for prompting, generate_num in zip(promptings, generate_nums):
                method.model_name = model_name
                method.task_version = "v2"
                method.w_code = None
                method.prompting = prompting
                method.generate_num = generate_num
                status = combine_llama_4_item(
                    method, response_dicts=response_dicts,
                    output_root=methods_output_root)
                status_hist[status] += 1
    print(status_hist)


def get_jsons(
        method: Method, 
        methods: List[Method],
        output_root: str,
        tokenizer=None) -> List[Dict]:
    output_root = os.path.abspath(output_root)

    b_output_root = "data/step"
    b_model_name = "Qwen3-32B"
    if method.w_code is not None:
        b_folder_name = b_model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        b_folder_name = b_model_name
    if method.prompting is not None:
        b_folder_name += f"--{method.prompting}"
    b_folder_path = f"{b_output_root}/9.{b_folder_name}"

    if method.w_code is not None:
        folder_name = method.model_name + "--" + ("w_code" if method.w_code else "wo_code")
    else:
        folder_name = method.model_name
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
        elif method.model_name == "llama-4-maverick":
            messages = [{"role": "user", "content": method.prompt}]
            formatted_prompt = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True)

            # Format the request payload using the model's native structure.
            native_request = {
                "prompt": formatted_prompt
            }
            json_post = {
                "recordId": json_id,
                "modelInput": native_request
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

    # model_names = ["gpt-5", "claude-sonnet-4-5", "llama-4-maverick"]
    model_names = ["llama-4-maverick"]

    promptings = ["v2-all", "v2-code", "v2-nl"]
    generate_nums = [5, 5, 5]

    methods_output_root = "data/step_tmp/"
    methods_output_root = os.path.abspath(methods_output_root)
    
    claude_out_dir = "data/batch--claude-sonnet-4-5--out--1st-run"
    claude_exist_ids = []
    for fn in os.listdir(claude_out_dir):
        with open(f"{claude_out_dir}/{fn}") as file:
            for line in file:
                claude_exist_ids.append(json.loads(line)["recordId"])
    gpt5_out_dir = "data/batch--gpt-5--out--1st-run"
    gpt5_exist_ids = []
    for fn in os.listdir(gpt5_out_dir):
        with open(f"{gpt5_out_dir}/{fn}") as file:
            for line in file:
                gpt5_exist_ids.append(json.loads(line)["custom_id"])

    model_id = "meta-llama/Llama-4-Maverick-17B-128E-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    for model_name in model_names:

        json_list = []
        for method in tqdm(methods):
            for prompting, generate_num in zip(promptings, generate_nums):
                method.model_name = model_name
                method.w_code = None
                method.prompting = prompting
                method.generate_num = generate_num
                json_list.extend(get_jsons(
                    method, methods, 
                    output_root=methods_output_root, tokenizer=tokenizer))        

        split_num = 1
        for split_idx in range(split_num):
            jsonl_output_path = f"data/batch--{model_name}/batch--{model_name}--{split_idx}.jsonl"
            with open(jsonl_output_path, "w") as file:
                for json_idx, json_post in enumerate(json_list):
                    
                    if "gpt" in model_name and json_post["custom_id"] in gpt5_exist_ids:
                        continue
                    elif "claude" in model_name and json_post["recordId"] in claude_exist_ids:
                        continue

                    if json_idx % split_num == split_idx:
                        file.write(json.dumps(json_post) + "\n")

if __name__ == "__main__":
    # get_prompts()
    # combine_claude_4_5()
    # combine_gpt_5()
    combine_llama_4()