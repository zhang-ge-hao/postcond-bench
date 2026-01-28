# vllm_chat_completion_client.py
from __future__ import annotations

import asyncio
from typing import Any, AsyncGenerator, Dict, List, Mapping, Optional, Sequence, Union, cast

from pydantic import BaseModel

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import FunctionCall
from autogen_core._cancellation_token import CancellationToken
from autogen_core.logging import LLMCallEvent
from autogen_core.models import CreateResult, LLMMessage, ModelFamily, RequestUsage, UserMessage
from autogen_core.tools import Tool, ToolSchema
import uuid

# ⚠️ 依赖 AutoGen 的内部实现（为了复用其 message/tool 转换与解析逻辑）
from autogen_ext.models.openai._openai_client import (  # type: ignore
    NOT_GIVEN,
    ChatCompletion,
    ChatCompletionChunk,
    Choice,
    ParsedChatCompletion,
    ParsedChoice,
    _add_usage,
    convert_tools,
    create_kwargs,
    logger,
    normalize_stop_reason,
    parse_r1_content,
    to_oai_type,
)


class VLLMChatCompletionClient(OpenAIChatCompletionClient):
    """
    OpenAIChatCompletionClient + vLLM extra_body 透传。

    用法：
        client = VLLMChatCompletionClient(
            model="Qwen/Qwen3-32B",
            base_url="http://localhost:19990/v1",
            api_key="EMPTY",
            model_info={...},
            extra_body={
                "chat_template_kwargs": {"enable_thinking": False},
                "top_k": 20,
                "min_p": 0,
            },
        )
    """

    def __init__(self, *, extra_body: Optional[Mapping[str, Any]] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self._vllm_extra_body: Dict[str, Any] = dict(extra_body or {})

    # -----------------------
    # Non-streaming
    # -----------------------
    async def create(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
    ) -> CreateResult:
        # 与 BaseOpenAIChatCompletionClient.create 基本一致，只改两处：
        # 1) 额外把 extra_body 传给 openai-python SDK
        # 2) 如 use_beta_client(parse) 时，默认不支持 extra_body（可按需扩展）

        # Validate extra_create_args
        extra_create_args_keys = set(extra_create_args.keys())
        if not create_kwargs.issuperset(extra_create_args_keys):
            raise ValueError(f"Extra create args are invalid: {extra_create_args_keys - create_kwargs}")

        # Merge create args
        create_args = self._create_args.copy()
        create_args.update(extra_create_args)

        # Detect beta parse mode (pydantic response_format)
        use_beta_client: bool = False
        response_format_value: Optional[type[BaseModel]] = None
        if "response_format" in create_args:
            value = create_args["response_format"]
            if isinstance(value, type) and issubclass(value, BaseModel):
                response_format_value = value
                use_beta_client = True
            else:
                use_beta_client = False
                response_format_value = None

        # Remove response_format to avoid passing twice
        create_args_no_response_format = {k: v for k, v in create_args.items() if k != "response_format"}

        # Vision check
        if self.model_info["vision"] is False:
            for m in messages:
                if isinstance(m, UserMessage):
                    if isinstance(m.content, list):
                        # 保持与原实现一致：遇到 image part 会在内部判断
                        # 这里不额外做事，交给原实现的 to_oai_type / Image 类型判断逻辑
                        pass

        # json_output override -> response_format
        if json_output is not None:
            if self.model_info["json_output"] is False and json_output is True:
                raise ValueError("Model does not support JSON output.")
            if json_output is True:
                create_args["response_format"] = {"type": "json_object"}
            else:
                create_args["response_format"] = {"type": "text"}

        if self.model_info["json_output"] is False and json_output is True:
            raise ValueError("Model does not support JSON output.")

        # Convert messages
        oai_messages_nested = [to_oai_type(m, prepend_name=self._add_name_prefixes) for m in messages]
        oai_messages = [item for sublist in oai_messages_nested for item in sublist]

        # Tools capability check
        if self.model_info["function_calling"] is False and len(tools) > 0:
            raise ValueError("Model does not support function calling")

        # ---- The only functional change (non-stream): pass extra_body ----
        extra_body_kw = {"extra_body": self._vllm_extra_body} if self._vllm_extra_body else {}

        # Dispatch
        future: Union[asyncio.Task[ParsedChatCompletion[BaseModel]], asyncio.Task[ChatCompletion]]

        if use_beta_client:
            # openai-python 的 beta.parse 是否支持 extra_body 取决于版本；
            # vLLM 通常也不需要这个分支。这里直接显式报错更安全。
            if self._vllm_extra_body:
                raise ValueError(
                    "extra_body is not supported in beta parse mode (Pydantic response_format). "
                    "Use response_format={'type':'json_object'} or disable Pydantic response_format."
                )

        if len(tools) > 0:
            converted_tools = convert_tools(tools)
            if use_beta_client:
                if response_format_value is not None:
                    future = asyncio.ensure_future(
                        self._client.beta.chat.completions.parse(
                            messages=oai_messages,
                            tools=converted_tools,
                            response_format=response_format_value,
                            **create_args_no_response_format,
                        )
                    )
                else:
                    future = asyncio.ensure_future(
                        self._client.beta.chat.completions.parse(
                            messages=oai_messages,
                            tools=converted_tools,
                            **create_args_no_response_format,
                        )
                    )
            else:
                future = asyncio.ensure_future(
                    self._client.chat.completions.create(
                        messages=oai_messages,
                        stream=False,
                        tools=converted_tools,
                        **extra_body_kw,
                        **create_args,
                    )
                )
        else:
            if use_beta_client:
                if response_format_value is not None:
                    future = asyncio.ensure_future(
                        self._client.beta.chat.completions.parse(
                            messages=oai_messages,
                            response_format=response_format_value,
                            **create_args_no_response_format,
                        )
                    )
                else:
                    future = asyncio.ensure_future(
                        self._client.beta.chat.completions.parse(
                            messages=oai_messages,
                            **create_args_no_response_format,
                        )
                    )
            else:
                future = asyncio.ensure_future(
                    self._client.chat.completions.create(
                        messages=oai_messages,
                        stream=False,
                        **extra_body_kw,
                        **create_args,
                    )
                )

        if cancellation_token is not None:
            cancellation_token.link_future(future)

        result: Union[ParsedChatCompletion[BaseModel], ChatCompletion] = await future

        # Usage
        usage = RequestUsage(
            prompt_tokens=result.usage.prompt_tokens if result.usage is not None else 0,
            completion_tokens=(result.usage.completion_tokens if result.usage is not None else 0),
        )

        logger.info(
            LLMCallEvent(
                messages=cast(List[Dict[str, Any]], oai_messages),
                response=result.model_dump(),
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
            )
        )

        # Parse first choice
        choice: Union[ParsedChoice[Any], ParsedChoice[BaseModel], Choice] = result.choices[0]

        content: Union[str, List[FunctionCall]]
        thought: Optional[str] = None

        if choice.message.function_call is not None:
            raise ValueError("function_call is deprecated and is not supported by this model client.")
        elif choice.message.tool_calls is not None and len(choice.message.tool_calls) > 0:
            # tool_calls -> List[FunctionCall]
            calls: List[FunctionCall] = []
            for tool_call in choice.message.tool_calls:
                args = tool_call.function.arguments
                if not isinstance(args, str):
                    raise ValueError("Tool call arguments must be a JSON string.")
                elif choice.message.tool_calls is not None and len(choice.message.tool_calls) > 0:
                    calls: List[FunctionCall] = []
                    for tool_call in choice.message.tool_calls:
                        args = tool_call.function.arguments
                        if not isinstance(args, str):
                            raise ValueError("Tool call arguments must be a JSON string.")

                        # ✅ AutoGen 新版需要 id
                        call_id = getattr(tool_call, "id", None) or f"call_{uuid.uuid4().hex}"

                        calls.append(
                            FunctionCall(
                                id=call_id,
                                name=tool_call.function.name,
                                arguments=args,
                            )
                        )
                    content = calls
            content = calls
        else:
            # Normal content
            content_str = choice.message.content or ""
            # Some families may put "thought" into content; keep original behavior for R1
            if isinstance(content_str, str) and self._model_info["family"] == ModelFamily.R1:
                thought, content_str = parse_r1_content(content_str)
            content = content_str

        response = CreateResult(
            finish_reason=normalize_stop_reason(choice.finish_reason),
            content=content,
            usage=usage,
            cached=False,
            logprobs=None,
            thought=thought,
        )

        # Update usage counters
        self._total_usage = _add_usage(self._total_usage, usage)
        self._actual_usage = _add_usage(self._actual_usage, usage)

        return response

    # -----------------------
    # Streaming: only override the chunk-creator
    # -----------------------
    async def _create_stream_chunks(
        self,
        tool_params: List[Any],  # ChatCompletionToolParam
        oai_messages: List[Any],  # ChatCompletionMessageParam
        create_args: Dict[str, Any],
        cancellation_token: Optional[CancellationToken],
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        extra_body_kw = {"extra_body": self._vllm_extra_body} if self._vllm_extra_body else {}

        stream_future = asyncio.ensure_future(
            self._client.chat.completions.create(
                messages=oai_messages,
                stream=True,
                tools=tool_params if len(tool_params) > 0 else NOT_GIVEN,
                **extra_body_kw,
                **create_args,
            )
        )
        if cancellation_token is not None:
            cancellation_token.link_future(stream_future)

        stream = await stream_future
        while True:
            try:
                chunk_future = asyncio.ensure_future(anext(stream))
                if cancellation_token is not None:
                    cancellation_token.link_future(chunk_future)
                chunk = await chunk_future
                yield chunk
            except StopAsyncIteration:
                break
