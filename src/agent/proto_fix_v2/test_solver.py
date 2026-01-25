
from src.ds import *
import json
from openai import OpenAI

from src.agent.proto_fix_v2.tools.splitter import split_icontract_postconditions

if __name__ == "__main__":
    method_path = "data/step/9.Qwen3-32B-agent--v2-all/z3z1ma--dbt-osmosis--_get_setting_for_node.json"

    with open(method_path) as file:
        method = Method.from_dict(json.load(file))
    
    method_content = method.content
    postcond_set = method.postconds[0]

    postconds = split_icontract_postconditions(postcond_set)

    postcond = postconds[0].to_decorator_block()

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