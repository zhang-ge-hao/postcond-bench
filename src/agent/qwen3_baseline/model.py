from openai import OpenAI

def model_generate(model_name: str, prompt, n, port=None):
    if "Qwen3" in model_name and model_name.endswith("-reason"):
        model_name = model_name[: -len("-reason")]
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
            n=n, temperature=0.6, top_p=0.95,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "top_k": 20,
                "min_p": 0,
            },
        )
        responses = [
            f"<think>{c.message.reasoning_content}</think>{c.message.content}" 
            for c in response.choices
        ]
    else:
        raise NotImplementedError()
    return responses
