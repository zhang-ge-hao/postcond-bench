import os
import json
from multiprocessing import Pool
from functools import partial

from src.postcond import response_post_process
from src.postcond.model import model_generate

from tqdm import tqdm

root_dir = "data/ground_truth/python"

prompt_template = """```
{postcond}
```

这是一组用icontract写成的postcondition。
帮我重写一遍，原本ensure和snapshot装饰器的逻辑保持完全一致，但是去掉所有的注释和日志部分。

注意要去除的部分包括且只包括：
1. ensure装饰器被违反的时候要写出的日志。
2. Python日志。

例如原本的postcondition为：
```
@icontract.snapshot(lambda lst: lst[:], name="old_lst")
# do something
@icontract.ensure(lambda OLD, lst, value: True, "Violation.")
```

重写后的postcondition应为：
```
@icontract.snapshot(lambda lst: lst[:], name="old_lst")
@icontract.ensure(lambda OLD, lst, value: True)
```

返回结果中只包含重写后的postconditions。
"""


def process_file(fn: str):
    """处理单个文件的函数，运行在子进程中。"""
    full_path = os.path.join(root_dir, fn)

    # 子进程-任务开始日志
    print(f"[PID {os.getpid()}] Start processing: {fn}")

    with open(full_path, "r", encoding="utf-8") as file:
        file_lines = file.readlines()

    idxs = []
    lines = []
    in_block = False
    for idx, line in enumerate(file_lines):
        if line.startswith("```") and not in_block:
            in_block = True
        elif line.startswith("```") and in_block:
            break
        elif in_block:
            lines.append(line)
            idxs.append(idx)

    postcond = "".join(lines)

    prompt = prompt_template.format(postcond=postcond)
    response = model_generate("gpt-4o-mini", prompt, 1)[0]
    postcond = response_post_process(response)

    postcond += "\n"

    out_lines = file_lines[: min(idxs)] + [postcond] + file_lines[max(idxs) + 1:]

    with open(full_path, "w", encoding="utf-8") as file:
        for line in out_lines:
            file.write(line)

    # 子进程-任务结束日志
    print(f"[PID {os.getpid()}] Finished processing: {fn}")

    # 让 tqdm 有东西可以计数（返回值无关紧要）
    return fn


if __name__ == "__main__":
    file_names = os.listdir(root_dir)
    file_names = [fn for fn in file_names if fn.endswith(".md")]

    # 进程池大小 = 10
    with Pool(processes=10) as pool:
        # 用 tqdm 包一下 map 以显示整体进度
        for _ in tqdm(pool.imap_unordered(process_file, file_names), total=len(file_names)):
            pass
