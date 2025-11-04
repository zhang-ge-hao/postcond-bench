
from typing import *
from openai import OpenAI

class LLM:
    def generate(self, prompt, n) -> List[str]:
        raise NotImplementedError()

class OpenAIModel(LLM):
    def __init__(self, model_name, **kwargs):
        self.client = OpenAI()
        self.model_name = model_name
    
    def generate(self, prompt, n) -> List[str]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            n=n
        )
        ret = [choice.message.content for choice in response.choices]
        return ret

class GPT_4_1(OpenAIModel):
    def __init__(self, **kwargs):
        super().__init__("gpt-4.1")


class GPT_4o_mini(OpenAIModel):
    def __init__(self, **kwargs):
        super().__init__("gpt-4o-mini")


class VllmModel(LLM):
    def __init__(self, model_name, port, **kwargs):
        self.model_name = model_name

        openai_api_key = "EMPTY"
        openai_api_base = f"http://localhost:{port}/v1"
        self.client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
    
    def generate(self, prompt, n) -> List[str]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            n=n
        )
        ret = [choice.message.content for choice in response.choices]
        return ret


class Qwen3(VllmModel):
    def generate(self, prompt, n) -> List[str]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            n=n,
            temperature=0.7, top_p=0.8,
            extra_body={
                # 关键就在这里
                "chat_template_kwargs": {"enable_thinking": False},
            },
        )
        ret = [choice.message.content for choice in response.choices]
        return ret


class Qwen3_8B(Qwen3):
    def __init__(self, port, **kwargs):
        super().__init__("Qwen/Qwen3-8B", port, **kwargs)


LLM_MAP: Dict[str, type[LLM]] = {
    "gpt-4.1": GPT_4_1,
    "gpt-4o-mini": GPT_4o_mini,
    "Qwen3-8B": Qwen3_8B,
}