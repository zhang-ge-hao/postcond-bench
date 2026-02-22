from openai import OpenAI
import anthropic
import os
import time

RETRY_ATTEMPTS = 6
RETRY_SLEEP_BASE_SECONDS = 5


def _retry_call(fn, *, model_name: str, attempts: int = RETRY_ATTEMPTS):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt == attempts:
                break
            time.sleep(min(RETRY_SLEEP_BASE_SECONDS * attempt, 30))
    raise RuntimeError(
        f"Model call failed for {model_name} after {attempts} attempts: {last_error}"
    )


def _generate_n_with_retry(create_call, *, n: int, model_name: str, text_selector):
    postconditions = []
    for _ in range(n):
        response = _retry_call(create_call, model_name=model_name)
        postconditions.append(text_selector(response))
    return postconditions

def model_generate(model_name: str, prompt, n, port=None):
    if model_name == "gpt-5":
        client = OpenAI()
        postconditions = _generate_n_with_retry(
            lambda: client.responses.create(
                model="gpt-5",
                input=prompt,
                reasoning={"effort": "medium"},
            ),
            n=n,
            model_name=model_name,
            text_selector=lambda r: r.output_text,
        )
    elif "gpt" in model_name:
        client = OpenAI()
        response = _retry_call(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                n=n,
            ),
            model_name=model_name,
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
        response = _retry_call(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt},],
                n=n,
                max_tokens=2048,
            ),
            model_name=model_name,
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
        response = _retry_call(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt},],
                n=n,
                max_tokens=2048,
            ),
            model_name=model_name,
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
        response = _retry_call(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt},],
                n=n, temperature=0.7, top_p=0.8,
                extra_body={
                    "chat_template_kwargs": {"enable_thinking": False},
                    "top_k": 20,
                    "min_p": 0,
                },
                max_tokens=2048,
            ),
            model_name=model_name,
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
        response = _retry_call(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt},],
                n=n,
                max_tokens=2048,
            ),
            model_name=model_name,
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
        response = _retry_call(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt},],
                n=n, temperature=0.5, # from phi-4 tech report
                max_tokens=2048,
            ),
            model_name=model_name,
        )
        postconditions = [choice.message.content for choice in response.choices]
    elif model_name == "qwen3-coder":
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        postconditions = _generate_n_with_retry(
            lambda: client.chat.completions.create(
                model="qwen3-coder-480b-a35b-instruct",
                messages=[{"role": "user", "content": prompt}],
            ),
            n=n,
            model_name=model_name,
            text_selector=lambda r: r.choices[0].message.content,
        )
    elif model_name == "claude-sonnet-4":
        client = anthropic.Anthropic()
        postconditions = _generate_n_with_retry(
            lambda: client.messages.create(
                model="claude-sonnet-4-20250514",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048
            ),
            n=n,
            model_name=model_name,
            text_selector=lambda m: m.content[0].text,
        )
        # # 1. 选择你开通 Bedrock 的 region
        # REGION = "us-east-1"  # 按你的实际 region 改
        # # 2. 选择 Claude 模型 ID（按你在 Bedrock 里开的模型改）
        # MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"
        # # 3. 创建 Bedrock Runtime 客户端
        # client = boto3.client(service_name="bedrock-runtime", region_name=REGION,)
        # postconditions = []
        # for _ in range(n):
        #     message_text = None
        #     while message_text is None:
        #         try:
        #             response = client.converse(
        #                 modelId=MODEL_ID,
        #                 messages=[{"role": "user","content": [{"text": prompt}],}],
        #                 inferenceConfig={"maxTokens": 2048},
        #             )
        #             # 从 Bedrock 返回结构里拿出文本
        #             out_msg = response["output"]["message"]
        #             # Claude 返回的 content 是一个 list，每个元素可能包含 text / 其它类型
        #             for item in out_msg["content"]:
        #                 if "text" in item:
        #                     message_text = item["text"]
        #                     break
        #         except Exception as e:
        #             # 你原来的代码是直接 except: 然后 sleep
        #             import logging, random
        #             error_str = str(e)
        #             if "ThrottlingException" in error_str and "Too many requests" in error_str:
        #                 logging.error("Too many requests.")
        #             else:
        #                 logging.error(error_str)
        #             time.sleep(20)
        #     postconditions.append(message_text)
    elif model_name == "claude-3-5-haiku":
        client = anthropic.Anthropic()
        postconditions = _generate_n_with_retry(
            lambda: client.messages.create(
                model="claude-3-5-haiku-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048
            ),
            n=n,
            model_name=model_name,
            text_selector=lambda m: m.content[0].text,
        )
    else:
        raise NotImplementedError()
    return postconditions
