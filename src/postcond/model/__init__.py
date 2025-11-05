from openai import OpenAI
import anthropic
import os
import time

def model_generate(model_name, prompt, n, port=None):
    if "gpt" in model_name:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            n=n,
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
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
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
    elif model_name == "claude-sonnet-4":
        client = anthropic.Anthropic()
        postconditions = []
        for _ in range(n):
            message = None
            while message is None:
                try:
                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2048
                    )
                except:
                    time.sleep(20)
            postconditions.append(message.content[0].text)
    elif model_name == "claude-3-5-haiku":
        client = anthropic.Anthropic()
        postconditions = []
        for _ in range(n):
            message = None
            while message is None:
                try:
                    message = client.messages.create(
                        model="claude-3-5-haiku-20241022",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2048
                    )
                except:
                    time.sleep(20)
            postconditions.append(message.content[0].text)
    else:
        raise NotImplementedError()
    return postconditions