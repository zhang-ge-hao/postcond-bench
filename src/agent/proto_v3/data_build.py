import os, sys
import random
from src.ds import *
from src.clone import repository_reproduct
from openpyxl import Workbook
import csv
from tqdm import tqdm
from dataclasses import dataclass, asdict
from multiprocessing import Pool

from src.agent.proto_v3.splitter import split_icontract_postconditions
from src.curator.eval_postcond import eval_postcond

KFS = ["jml_fail", "icontract_fail"]

def read_benchmark(p, save_mem=False) -> List[Method]:
    print(f"Reading {p}.")
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            if save_mem:
                method.repo.env_config = None
                method.repo.failed_tests = None
                method.cover_tests = None
                method.mutants = None
                method.postconds = None
                method.responses = None
            methods.append(method)
    return methods


def build_wo_res():
    root_dir = "data/step/9.Qwen3-32B-reason--v2-all"
    out_dir = "src/agent/proto_v3/data"
    methods = read_benchmark(root_dir)

    repos = set([m.repo.github_path for m in methods])
    __methods = {r: [] for r in repos}
    for m in methods:
        __methods[m.repo.github_path].append(m)
    methods: Dict[str, List[Method]] = __methods

    data_wo_res = []
    for rn, ms in tqdm(methods.items()):
        assert len(ms) > 0
        repo = ms[0].repo
        with repository_reproduct(repo) as repo_dir:
            for m in ms:
                with open(m.file) as file:
                    file_content = file.read()
                method_content = m.content
                fn = rn.replace("/", "--") + "--" + m.rlid
                benchmark_path = os.path.join(root_dir, f"{fn}.json")
                github_url = m.github_url
                assert len(m.postconds) == 1
                postcond_set = m.postconds[0]
                corr_flag = m.postcond_corr[0]
                lang = m.repo.language
                if corr_flag not in ["passed"] + KFS:
                    continue
                if lang == "python":
                    postconds = split_icontract_postconditions(postcond_set)
                    postconds = [p.to_decorator_block() for p in postconds]
                elif lang == "java":
                    lines = postcond_set.split("\n")
                    lines = [li for li in lines if li.strip()]
                    assert all(li.strip().startswith("//@ ensures") for li in lines), postcond_set
                    postconds = lines
                else:
                    raise NotImplementedError()
                
                for p in postconds:
                    data_wo_res.append([fn, lang, github_url, p, method_content, file_content, benchmark_path])
    
    data_wo_res.insert(0, ["id", "lang", "github_path", "postcond", "method_content", "file_content", "benchmark_path"])
    with open(f"{out_dir}/out.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data_wo_res)

@dataclass
class _data:
    id: str
    lang: str
    github_path: str
    postcond: str
    method_content: str
    file_content: str
    benchmark_path: str
    corr_flag: str = None

    @classmethod
    def from_args(cls, args):
        # 排除掉 corr_flag 后的前 7 个字段进行映射
        return cls(*args[:7])

def process_item(item):
    """
    具体的单个任务处理函数，将被多个进程调用
    """
    try:
        with open(item.benchmark_path) as file:
            # 假设 Method 在你的全局作用域中已定义
            method = Method.from_dict(json.load(file))
        
        # 调用评估逻辑
        corr_flag = eval_postcond(method, item.postcond, eval_corr_only=True)
        item.corr_flag = corr_flag
        return item
    except Exception as e:
        print(f"Error processing {item.id}: {e}")
        return item

def build_res():
    out_dir = "src/agent/proto_v3/data"
    wo_res_path = f"{out_dir}/out.csv"
    
    # 动态调整 CSV 限制
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int //= 2

    # 1. 读取并封装数据
    with open(wo_res_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        # 跳过空行或错误数据，只取有效行
        raw_data = [row for row in reader if row]

    # 转换成对象列表
    data_objects = [_data.from_args(row) for row in raw_data]

    # 2. 准备并行任务：打乱顺序
    # 我们创建一个带索引的元组列表 [(index, item), ...]
    indexed_data = list(enumerate(data_objects))
    random.shuffle(indexed_data)

    # 3. 使用进程池处理
    processed_indexed_data = []
    # 使用 pool.imap 可以在处理完成后获取结果
    with Pool(processes=30) as pool:
        # 这里的 map 接收的是带索引的任务
        # 为了保持 process_item 简洁，我们稍微包装一下
        with tqdm(total=len(indexed_data), desc="Processing") as pbar:
            # 使用 starmap 的变体或简单处理
            for idx, processed_item in pool.imap_unordered(wrap_process, indexed_data):
                processed_indexed_data.append((idx, processed_item))
                pbar.update()

    # 4. 恢复原始顺序
    # 按照之前记录的 index 进行排序
    processed_indexed_data.sort(key=lambda x: x[0])
    final_data = [item for idx, item in processed_indexed_data]

    # 5. 写入 CSV
    headers_to_write = ["id", "lang", "github_path", "corr_flag", "postcond", "method_content", "file_content", "benchmark_path"]
    data_w_res = [headers_to_write]
    
    for item in final_data:
        data_w_res.append([getattr(item, k) for k in headers_to_write])

    with open(f"{out_dir}/out2.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data_w_res)

def wrap_process(indexed_item):
    """辅助函数：拆解索引并调用核心处理逻辑"""
    idx, item = indexed_item
    res_item = process_item(item)
    return idx, res_item


def to_xlsx():
    out_dir = "src/agent/proto_v3/data"
    w_res_path = f"{out_dir}/out2.csv"
    # 动态调整 CSV 限制
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int //= 2

    # 1. 读取并封装数据
    with open(w_res_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        for row in reader:
            ws.append(row)
        wb.save(f"{out_dir}/out2.xlsx")


if __name__ == "__main__":
    build_wo_res()
    build_res()
    to_xlsx()