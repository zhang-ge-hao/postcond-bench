

from src.postcond.prompt.infile import (
    prompt_infile
)
from src.ds import *
from src.clone import repository_reproduct

if __name__ == "__main__":
    input_dir = "data/step/6.mutation/evansd--whitenoise.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[0]

    print(prompt_infile(method, w_code=False))
    pass
    print(prompt_infile(method, w_code=True))
    pass

    input_dir = "data/step/6.mutation/xuxueli--xxl-tool.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[0]

    print(prompt_infile(method, w_code=False))
    pass
    print(prompt_infile(method, w_code=True))
    pass
