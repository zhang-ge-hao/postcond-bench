from openai import OpenAI
import os
import time
import boto3
from dataclasses import dataclass


@dataclass
class ModelGeneration:
    response: str
    thought: str = None
    input_tokens: int = None
    output_tokens: int = None
    reasoning_tokens: int = None
    cost_usd: float = None


def _safe_getattr(obj, attr: str, default=None):
    if obj is None:
        return default
    return getattr(obj, attr, default)


def model_generate_structured(model_name: str, prompt: str, n: int, port=None):
    if model_name == "deepseek-reasoner":
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
        generations = []
        for _ in range(n):
            response = None
            while response is None:
                try:
                    response = client.chat.completions.create(
                        model="deepseek-reasoner",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=4096,
                        timeout=600,
                    )
                except:
                    time.sleep(20)
            choice = response.choices[0]
            message = choice.message
            usage = _safe_getattr(response, "usage")
            completion_details = _safe_getattr(usage, "completion_tokens_details")
            generations.append(ModelGeneration(
                response=_safe_getattr(message, "content", "") or "",
                thought=_safe_getattr(message, "reasoning_content"),
                input_tokens=_safe_getattr(usage, "prompt_tokens"),
                output_tokens=_safe_getattr(usage, "completion_tokens"),
                reasoning_tokens=_safe_getattr(completion_details, "reasoning_tokens"),
            ))
        return generations

    return [
        ModelGeneration(response=response)
        for response in model_generate(
            model_name=model_name,
            prompt=prompt,
            n=n,
            port=port,
        )
    ]

def model_generate(model_name: str, prompt, n, port=None):
    if model_name == "gpt-5":
        client = OpenAI()
        postconditions = []
        for _ in range(n):
            response = None
            while response is None:
                try:
                    response = client.responses.create(
                        model="gpt-5",
                        input=prompt,
                        reasoning={"effort": "medium"},
                    )
                except:
                    time.sleep(20)
            postconditions.append(response.output_text)
    if "gpt" in model_name:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            n=n,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif "llama" in model_name.lower():
        assert port is not None
        model_name = f"meta-llama/{model_name}-Instruct"
        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt},],
            n=n, 
            max_tokens=2048,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif "deepseek-coder-v2" in model_name.lower():
        assert port is not None
        model_name = f"deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct"
        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt},],
            n=n, 
            max_tokens=2048,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif "Qwen3" in model_name:
        assert port is not None
        model_name = f"Qwen/{model_name}"
        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt},],
            n=n, temperature=0.7, top_p=0.8,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": False},
                "top_k": 20,
                "min_p": 0,
            },
            max_tokens=2048,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif "gemma-3" in model_name:
        assert port is not None
        model_name = f"google/{model_name}-it"
        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt},],
            n=n, 
            max_tokens=2048,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif "phi-4" in model_name.lower():
        assert port is not None
        if "mini" in model_name:
            model_name = "microsoft/Phi-4-mini-instruct"
        else:
            model_name = "microsoft/phi-4"
        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt},],
            n=n, temperature=0.5, # from phi-4 tech report
            max_tokens=2048,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif model_name == "qwen3-coder":
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        postconditions = []
        for _ in range(n):
            response = None
            while response is None:
                try:
                    response = client.chat.completions.create(
                        model="qwen3-coder-480b-a35b-instruct",
                        messages=[{"role": "user", "content": prompt}],
                    )
                except:
                    time.sleep(20)
            postconditions.append(response.choices[0].message.content)
    else:
        raise NotImplementedError()
    return postconditions
