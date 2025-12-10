
from src.ds import *
import os
from src.util import get_diff
from multiprocessing import Pool

KFS = ["jml_fail", "icontract_fail"]

def read_benchmark(p="data/step/7.reference") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods


def prompt_helper():
    method_fn = "coderamp-labs--gitingest--_parse_ignore_file"
    code_file = True
    full_trans = False
    w_ref = True
    mutants_list = [2, 5, 6, 7, 9, 25, 30]

    prompt_format = """```

```
{leading}我想给这个方法写一组icontract的postcondition。
{header}我们的预期是希望写出的postcondition随正确版本代码运行的时候可以被满足，和bug版本的代码运行的时候不满足。
要求不能引入额外的辅助方法，纯用icontract的装饰器实现。
{full_trans_inst}帮我实现一下。
"""
    ref_format = """这是我目前版本的postconditions：
{ref_postcond}
这组postcondition已经可以随正确的方法代码并被满足，但仍然无法鉴别一些bug：
{bugs}
以上列举的是bug版本代码和原本正确代码之间的diff。
帮我分析修改一下。"""

    method_dir = "data/step/8.benchmark_m"
    with open(f"{method_dir}/{method_fn}.json") as file:
        method = Method.from_dict(json.load(file))
    
    leading_str = "这是python源码。\n" if code_file else ""
    header_str = f"```\n{method.header}\n```\n" if code_file else ""
    if full_trans:
        full_trans_inst_str = "对这个方法而言，可以将原本正确方法的逻辑转换到postcondition中，在postcondition中计算出正确的返回值，然后将方法的返回值和正确的返回值进行比对。\n"
    else:
        full_trans_inst_str = ""
    prompt = prompt_format.format(
        leading=leading_str,
        header=header_str,
        full_trans_inst=full_trans_inst_str
    )
    if w_ref:
        ref_postcond_str = f"```\n{method.ref_postcond}\n```"
        bugs_str = []
        for mutant_idx in mutants_list:
            diff = get_diff(method.content.rstrip(), method.mutants[mutant_idx].rstrip())
            bugs_str.append(f"```\n{diff}\n```")
        bugs_str = "\n".join(bugs_str)
        ref_prompt = ref_format.format(
            ref_postcond=ref_postcond_str,
            bugs=bugs_str
        )
        prompt += ref_prompt
    print(prompt)


if __name__ == "__main__":
    prompt_helper()