

from .vllm_chat_completion_client import VLLMChatCompletionClient
from autogen_core.models import ModelFamily, ChatCompletionClient


def qwen3_client(
        function_calling=True, 
        port=19990, 
        thinking=False,
        tool_choice=None,
        presence_penalty=0.0) -> VLLMChatCompletionClient:

    if thinking:
        enable_thinking, temperature, top_p = True, 0.6, 0.95
    else:
        enable_thinking, temperature, top_p = False, 0.7, 0.8
    return VLLMChatCompletionClient(
        model="Qwen/Qwen3-32B",
        base_url=f"http://localhost:{port}/v1",
        api_key="EMPTY",
        model_info={
            "vision": False,
            "function_calling": function_calling,
            "json_output": False,
            "structured_output": False,
            "family": ModelFamily.UNKNOWN,
        },
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": enable_thinking},
            "top_k": 20,
            "min_p": 0
        },
        # 如果你希望模型“自动决定要不要调用工具”，通常需要 tool_choice=auto
        tool_choice=tool_choice,
    )


def client(model_name, **kwargs) -> ChatCompletionClient:
    if model_name == "Qwen/Qwen3-32B":
        return qwen3_client(**kwargs)
    else:
        raise NotImplementedError()
