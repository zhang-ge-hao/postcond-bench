#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用 CodeBERT 为字符串生成向量 embedding，
基于余弦距离实现 distance 函数，
再用最远点优先（farthest-first traversal）对字符串做“多样性优先”排序。

依赖：
    pip install transformers torch numpy
"""

from typing import List
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from src.ds import *
import os


# =========================
# 1. 加载 CodeBERT 模型
# =========================

MODEL_NAME = "microsoft/codebert-base"  # CodeBERT 基础版（RoBERTa 架构）

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.to(device)
model.eval()


# =========================
# 2. 文本 -> CodeBERT 向量
# =========================

@torch.no_grad()
def encode_texts_with_codebert(
    texts: List[str],
    batch_size: int = 16,
    max_length: int = 256,
) -> np.ndarray:
    """
    使用 CodeBERT 将一批字符串编码为向量，并做 L2 归一化（方便用余弦距离）。

    返回：
        embeddings: np.ndarray, 形状 [n_texts, hidden_size]，每一行已 L2 归一化。
    """
    all_embeddings = []

    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start : start + batch_size]

        # Tokenize
        inputs = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Forward
        outputs = model(**inputs)  # BaseModelOutputWithPoolingAndCrossAttentions
        last_hidden_state = outputs.last_hidden_state  # [B, L, H]
        attention_mask = inputs["attention_mask"]      # [B, L]

        # 做一个简单的 mean pooling（只对非 padding token 求平均）
        mask = attention_mask.unsqueeze(-1)            # [B, L, 1]
        masked_hidden = last_hidden_state * mask       # padding 的位置变 0
        sum_hidden = masked_hidden.sum(dim=1)          # [B, H]
        lengths = mask.sum(dim=1)                      # [B, 1]
        lengths = torch.clamp(lengths, min=1)          # 避免除 0
        mean_pooled = sum_hidden / lengths             # [B, H]

        # 转成 numpy
        batch_embeddings = mean_pooled.cpu().numpy()
        all_embeddings.append(batch_embeddings)

    embeddings = np.concatenate(all_embeddings, axis=0)

    # L2 归一化，使得余弦相似度可以直接用点积表示
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.clip(norms, a_min=1e-12, a_max=None)
    embeddings = embeddings / norms

    return embeddings


# =========================
# 3. 距离函数：基于 embedding 的余弦距离
# =========================

def cosine_distance(embeddings: np.ndarray, i: int, j: int) -> float:
    """
    计算第 i, j 个向量之间的余弦距离（1 - cosine_similarity）。

    假设 embeddings[i], embeddings[j] 已经是 L2 归一化的。
    """
    sim = float(np.dot(embeddings[i], embeddings[j]))  # cos similarity in [-1, 1]
    # 根据需求，distance 越大表示越不相似：
    return 1.0 - sim


# =========================
# 4. 最远点优先排序（farthest-first traversal）
# =========================

def farthest_first_order(embeddings: np.ndarray) -> List[int]:
    """
    给定所有字符串的 embedding（每行一个），
    返回一个下标排列 indices，使得：
        不论取前 k 个，都是“互相尽量不相似”的一组代表点。
    """
    n = embeddings.shape[0]
    if n == 0:
        return []

    first_idx = 0

    selected: List[int] = [first_idx]
    in_selected = np.zeros(n, dtype=bool)
    in_selected[first_idx] = True

    # 维护每个点到“当前已选集合”的最近距离
    min_dist_to_selected = np.full(n, np.inf, dtype=float)
    min_dist_to_selected[first_idx] = 0.0

    # 初始化：用 first_idx 更新一次
    for i in range(n):
        if not in_selected[i]:
            min_dist_to_selected[i] = cosine_distance(embeddings, i, first_idx)

    for _ in range(1, n):
        # 关键：只在「未选中的点」里找 argmax
        # 已选中的位置强制设为 -inf，这样不会被选到
        candidate_scores = np.where(in_selected, -np.inf, min_dist_to_selected)
        next_idx = int(np.argmax(candidate_scores))

        # 理论上这里一定还有未选点；保险起见做个防御性判断
        if not np.isfinite(candidate_scores[next_idx]):
            break  # 所有点都已选中

        selected.append(next_idx)
        in_selected[next_idx] = True
        min_dist_to_selected[next_idx] = 0.0

        # 更新其它未选点的最近距离
        for i in range(n):
            if not in_selected[i]:
                d = cosine_distance(embeddings, i, next_idx)
                if d < min_dist_to_selected[i]:
                    min_dist_to_selected[i] = d

    # 可选：检查一下有没有遗漏
    # assert len(set(selected)) == n, f"only {len(set(selected))} unique indices for n={n}"

    return selected

# =========================
# 5. 示例：完整流程
# =========================

def main(methods: List[Method]) -> List[Method]:

    texts = [m.header for m in methods]

    print("Encoding texts with CodeBERT...")
    embeddings = encode_texts_with_codebert(texts, batch_size=4)
    print("Embeddings shape:", embeddings.shape)

    print("Computing farthest-first order...")
    order = farthest_first_order(embeddings)

    print(f"len(order) = {len(order)}")
    print(f"len(methods) = {len(methods)}")

    for rank, idx in enumerate(order, start=1):
        methods[idx].traversal_rank = rank

    return methods


def read_benchmark(p="data/step/7.reference") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods


if __name__ == "__main__":
    methods = read_benchmark()
    python_methods = [m for m in methods if m.repo.language == "python"]
    java_methods = [m for m in methods if m.repo.language == "java"]

    python_methods.sort(key=lambda m: (m.repo.github_path, m.rlid))
    java_methods.sort(key=lambda m: (m.repo.github_path, m.rlid))

    python_methods = main(python_methods)
    java_methods = main(java_methods)

    output_dir = "data/step/8.benchmark_m"

    for method in python_methods + java_methods:
        rn = method.repo.github_path.replace("/", "--")
        fn = f"{rn}--{method.rlid}"
        with open(f"{output_dir}/{fn}.json", "w") as file:
            file.write(json.dumps(method.to_dict(), indent=2))

    # methods = read_benchmark("data/step/8.benchmark_m")
    # process_methods = [m for m in methods if m.repo.github_path == "kellyjonbrazil/jc" and m.name == "_process"]
    # ranks = [m.traversal_rank for m in process_methods]
    # ranks.sort()
    # print(ranks)