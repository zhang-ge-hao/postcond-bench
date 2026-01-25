import re
from typing import List, Dict, Tuple, Optional
from openai import OpenAI

from src.agent.proto_python_v1.tools.icontract_grammar import grammar_verify


def model_generate(model_name: str, messages: List[Dict[str, str]], n: int, port: Optional[int] = None) -> List[str]:
    """
    Chat-style generation. Returns a list of assistant message contents (length n).
    """
    if "Qwen3" in model_name and model_name.endswith("-agent"):
        model_name = model_name[: -len("-agent")]
        assert port is not None
        model_name = f"Qwen/{model_name}"
        client = OpenAI(api_key="EMPTY", base_url=f"http://localhost:{port}/v1")

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            n=n,
            temperature=0.6,
            top_p=0.95,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "top_k": 20,
                "min_p": 0,
            },
        )
        return [c.message.content for c in response.choices]

    raise NotImplementedError()


def _unwrap_code_fence(text: str) -> str:
    """
    Compatible with:
      - ```...``` fenced blocks (optionally with language tag)
      - bare text
    If multiple fenced blocks exist, uses the first one.
    """
    if text is None:
        return ""
    s = text.strip()
    lines = s.split("\n")
    if len(lines) <= 1:
        return s
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return "\n".join(lines[1: -1])
    return s


def _parse_agent_action(raw: str) -> Tuple[str, str]:
    """
    Parse model output into (action, payload).
    Expected (fenced or bare):
      ATTEMPT\n{POSTCONDITIONS}
      GRAMMAR_VERIFY
      COMPLETENESS_VERIFY
      YIELD
    """
    content = _unwrap_code_fence(raw)
    if not content.strip():
        return "UNKNOWN", ""

    lines = content.splitlines()

    action = lines[0].strip().split()[0]
    payload = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
    payload = _unwrap_code_fence(payload)

    return action, payload


def agent_generate(model_name: str, 
                   init_prompt: str, 
                   method_content: str, 
                   port: Optional[int] = None,
                   max_rounds=20):
    """
    Conversation-style loop with an external environment:
      - Each model call uses `messages`.
      - Each environment result is appended as a NEW message before the next model call.
    Conventions:
      - model outputs are appended as role="assistant"
      - environment outputs are appended as role="user"
        (so the assistant "sees" the environment feedback as next-turn user input)

    Returns: (latest_attempt, messages)
    """

    latest_attempt: str = ""

    messages: List[Dict[str, str]] = [
        {"role": "user", "content": init_prompt}
    ]

    for _ in range(max_rounds):
        assistant_raw = model_generate(model_name, messages=messages, n=1, port=port)[0]
        messages.append({"role": "assistant", "content": assistant_raw})

        action, payload = _parse_agent_action(assistant_raw)

        if action == "YIELD":
            break

        if action == "ATTEMPT":
            latest_attempt = payload.strip()
            # env feedback becomes the next user message
            message_content = "Attempt saved successfully!"
        elif action == "GRAMMAR_VERIFY":
            result = grammar_verify(method_content, latest_attempt)
            message_content = str(result)
        else:
            message_content = (
                "Invalid action format. Please reply with exactly one of:\n"
                "ATTEMPT\n{POSTCONDITIONS}\n\n"
                "GRAMMAR_VERIFY\n\n"
                "YIELD"
            )
        messages.append({"role": "user", "content": message_content})
    
    print("=" * 30)
    for mess_idx, message in enumerate(messages):
        if mess_idx:
            print("-" * 30)
        print(message["role"])
        print("-" * 30)
        print(message["content"])
    print("=" * 30)

    return latest_attempt, messages


if __name__ == "__main__":
    from src.agent.proto_python_v1.init_prompt import prompt_v2
    from src.ds import *
    from src.clone import repository_reproduct

    method_path = "data/step/8.benchmark/a2aproject--a2a-python--append_artifact_to_task.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))
    method.prompting = "v2-all"
    method.model_name = "Qwen3-32B-agent"
    method.port = 19990
    with repository_reproduct(method.repo) as repo_dir:
        init_prompt = prompt_v2(method)

    latest_attempt, messages = agent_generate(
        model_name=method.model_name,
        init_prompt=init_prompt, 
        method_content=method.content,
        port=method.port)

    print(latest_attempt)