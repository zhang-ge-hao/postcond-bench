
from typing import *
from openai import OpenAI

class LLM:
    def generate(self, prompt, n) -> List[str]:
        raise NotImplementedError()

class GPT_4_1(LLM):
    def __init__(self):
        self.client = OpenAI()
    
    def generate(self, prompt, n) -> List[str]:
        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt},
            ],
            n=n
        )
        ret = [choice.message.content for choice in response.choices]
        return ret


LLM_MAP: Dict[str, type[LLM]] = {
    "gpt-4.1": GPT_4_1,
}