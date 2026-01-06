import os, json, sys
import shutil

from src.ds import *

from tqdm import tqdm

PI_WORKDIR = os.environ.get("PI_WORKDIR")

models = [
    # "deepseek-coder-v2",
    # "Qwen3-8B",
    # "phi-4-mini",
    # "phi-4",
    # "gpt-4.1",
    # "gpt-4o-mini",
    # "claude-sonnet-4",
    # "claude-3-5-haiku",
    # "Qwen3-32B",
    "gpt-5",
    "llama-4-maverick",
    # "claude-sonnet-4-5",
]
for model in models:
    for dir in os.listdir("data/step"):
        if not f"9.{model}--" in dir:
            continue
        dir = f"data/step/{dir}"
        count = 0
        for fn in os.listdir(dir):
            path = f"{dir}/{fn}"
            with open(path) as file:
                method = Method.from_dict(json.load(file))
            if method.postcond_corr is not None:
                count += 1
        print(count, 230 * 2 - count, dir)
    print()
exit()


kept_fns = []
human_fns = []

for fn in os.listdir("data/step/8.benchmark"):
    with open(f"data/step/8.benchmark/{fn}") as file:
        method = Method.from_dict(json.load(file))
    if method.ref_source == "auto":
        kept_fns.append(fn)
    else:
        human_fns.append(fn)

rm_paths = []
add_paths = []
re_eval_paths = []

for dir in os.listdir("data/step"):
    if not dir.startswith("9."):
        continue
    current_fns = os.listdir(f"data/step/{dir}")
    print(len(current_fns), dir)
#     for fn in current_fns:
#         if fn not in kept_fns:
#             rm_paths.append(f"data/step/{dir}/{fn}")
#     for fn in kept_fns:
#         if fn not in current_fns:
#             add_paths.append(f"data/step/{dir}/{fn}")
    
#     for fn in human_fns:
#         if fn not in current_fns:
#             re_eval_paths.append(f"data/step/{dir}/{fn}")

# print(len(rm_paths))
# print(len(add_paths))
# print(len(re_eval_paths))

# for rm_path in tqdm(rm_paths):
#     os.remove(rm_path)

# for add_path in tqdm(add_paths):
#     src_path = f"{PI_WORKDIR}/{add_path}"
#     if os.path.exists(src_path):
#         shutil.copy(src_path, add_path)
#     else:
#         # print(add_path)
#         pass

# for re_eval_path in tqdm(re_eval_paths):
#     src_path = f"{PI_WORKDIR}/{re_eval_path}"
#     if os.path.exists(src_path):
#         with open(src_path) as file:
#             method = Method.from_dict(json.load(file))
#         method.postcond_corr = None
#         method.mutant_kill = None
#         with open(re_eval_path, "w") as file:
#             json.dump(method.to_dict(), file, indent=2)
