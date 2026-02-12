

import sys, csv, os
from openai import OpenAI
from dataclasses import dataclass
from tqdm import tqdm

@dataclass
class _data:
    id: str
    lang: str
    github_path: str
    postcond: str
    method_content: str
    file_content: str
    benchmark_path: str
    corr_flag: str = None
    response: str = None
    solver_code: str = None


def generate(method_content, postcond):
    prompt_template = open(
        "src/agent/proto_v3/tools/prompt_template.txt").read()

    prompt = prompt_template.format(
        method_source=method_content, 
        postcondition=postcond)

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

    return response


if __name__ == "__main__":
    out_dir = "src/agent/proto_v3/data"
    w_res_path = f"{out_dir}/out2.csv"
    # 动态调整 CSV 限制
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int //= 2

    data = []
    # 1. 读取并封装数据
    with open(w_res_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            data.append(_data(**{k: v for k, v in zip(header, row)}))
    
    for item in tqdm(data):
        generate()