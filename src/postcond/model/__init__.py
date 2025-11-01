
from typing import *
from openai import OpenAI

class LLM:
    def generate(self, prompt, n) -> List[str]:
        raise NotImplementedError()

class OpenAIModel(LLM):
    def __init__(self, model_name):
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
    def __init__(self):
        super().__init__("gpt-4.1")


class GPT_4o_mini(OpenAIModel):
    def __init__(self):
        super().__init__("gpt-4o-mini")


LLM_MAP: Dict[str, type[LLM]] = {
    "gpt-4.1": GPT_4_1,
    "gpt-4o-mini": GPT_4o_mini,
}