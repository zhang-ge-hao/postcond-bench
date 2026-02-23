import os, json, argparse, time
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Any, Optional

import requests
import numpy as np

from src.ds import Method
from pathlib import Path

KFS = ["jml_fail", "icontract_fail"]
GRAPHQL = "https://api.github.com/graphql"


def parse_cutoff(s: str) -> datetime:
    s = s.strip()
    if len(s) == 10 and s[4] == "-" and s[7] == "-":
        return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    if s.endswith("Z"):
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def read_benchmark(p: str, save_mem: bool = False) -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(p, fn), "r", encoding="utf-8") as f:
            data = json.load(f)
        m = Method.from_dict(data) if hasattr(Method, "from_dict") else Method(**data)

        if save_mem:
            m.repo.env_config = None
            m.repo.failed_tests = None
            m.cover_tests = None
            m.mutants = None
            m.postconds = None
            m.responses = None
        methods.append(m)
    return methods


def load_all_methods_for_model(
        step_dir: str, model_name: str, lang: str,
        prompting: str
        ) -> List[Method]:
    all_methods: List[Method] = []
    for folder_name in os.listdir(step_dir):
        if not folder_name.startswith("9."):
            continue
        if folder_name.startswith(f"9.{model_name}--"):
            all_methods.extend(read_benchmark(os.path.join(step_dir, folder_name), save_mem=True))
    return [m for m in all_methods 
            if m.model_name == model_name 
            and m.repo.language==lang
            and m.prompting == prompting]


def _iso_to_dt(ts: str) -> datetime:
    if ts.endswith("Z"):
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fetch_blame_ranges(
    token: str,
    owner: str,
    repo: str,
    commit: str,
    path: str,
    session: requests.Session,
) -> List[Dict[str, Any]]:
    """
    返回 GraphQL blame.ranges（整文件），每段含：
      startingLine, endingLine, commit { oid, committedDate }
    """
    query = """
    query($owner:String!, $repo:String!, $expression:String!, $path:String!){
      repository(owner:$owner, name:$repo){
        object(expression:$expression){
          ... on Commit {
            blame(path:$path){
              ranges{
                startingLine
                endingLine
                commit{
                  oid
                  committedDate
                }
              }
            }
          }
        }
      }
    }
    """
    variables = {"owner": owner, "repo": repo, "expression": commit, "path": path}
    headers = {"Authorization": f"bearer {token}", "Accept": "application/json"}

    r = session.post(GRAPHQL, json={"query": query, "variables": variables}, headers=headers, timeout=60)
    r.raise_for_status()
    payload = r.json()

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    obj = payload.get("data", {}).get("repository", {}).get("object")
    if not obj or not obj.get("blame"):
        raise RuntimeError(f"no blame for {owner}/{repo}@{commit}:{path}")

    return obj["blame"]["ranges"] or []


def compute_create_update_from_ranges(
    ranges: List[Dict[str, Any]],
    start_line: int,
    end_line: int,
) -> Tuple[datetime, datetime]:
    """
    只在本地对 ranges 裁剪到 [start_line, end_line]，取 commit.committedDate 的 min/max
    """
    times: List[datetime] = []
    for rng in ranges:
        s = int(rng["startingLine"])
        e = int(rng["endingLine"])
        lo = max(s, start_line)
        hi = min(e, end_line)
        if lo > hi:
            continue
        dt = _iso_to_dt(rng["commit"]["committedDate"])
        # 段内每行同一次 commit，min/max 只需要加一次也行，但加多次不影响 min/max
        times.append(dt)

    if not times:
        raise RuntimeError(f"no ranges overlap with L{start_line}-L{end_line}")

    return min(times), max(times)


def compute_corr1_comp1(methods: List[Method]) -> Dict[str, float]:
    if len(methods) == 0:
        return {"n_methods": 0, "corr@1": float("nan"), "comp@1": float("nan")}

    corr_pass = 0
    comp_pass = 0
    for m in methods:
        if not m.postcond_corr or not m.mutant_kill:
            continue
        corr_res = m.postcond_corr[0]
        comp_res = m.mutant_kill[0]

        if corr_res == "passed":
            corr_pass += 1
            if m.ref_mutant_kill is None:
                continue
            ok = all(
                (r_f not in KFS) or (f in KFS)
                for f, r_f in zip(comp_res, m.ref_mutant_kill)
            )
            if ok:
                comp_pass += 1

    n = len(methods)
    return {"n_methods": n, "corr@1": corr_pass / n, "comp@1": comp_pass / n}


CACHE_PATH = Path("data/blame_cache.json")

def load_disk_cache() -> Dict[str, Any]:
    if not CACHE_PATH.exists():
        return {}
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        try:
            obj = json.load(f)
            return obj if isinstance(obj, dict) else {}
        except json.JSONDecodeError:
            # 文件坏了就当没缓存，避免直接炸
            return {}

def save_disk_cache(cache: Dict[str, Any]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_PATH.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)
    os.replace(tmp, CACHE_PATH)

def parse_boundary_mmdd(s: str) -> Tuple[int, int]:
    """
    'MM-DD' -> (month, day)
    """
    s = s.strip()
    try:
        mm, dd = s.split("-")
        m = int(mm)
        d = int(dd)
        if not (1 <= m <= 12):
            raise ValueError
        if not (1 <= d <= 31):
            raise ValueError
        return m, d
    except Exception:
        raise ValueError(f"--boundary 需要 MM-DD 格式，例如 09-30；你传的是: {s}")

def bucket_year_by_boundary(dt: datetime, boundary_mmdd: str) -> int:
    """
    每年用 boundary (MM-DD) 作为分界：
    - 若 dt > 当年 boundary 的 23:59:59（UTC），归到 next_year
    - 否则归到当年
    """
    dt = dt.astimezone(timezone.utc)
    m, d = parse_boundary_mmdd(boundary_mmdd)
    boundary = datetime(dt.year, m, d, 23, 59, 59, tzinfo=timezone.utc)
    return dt.year + 1 if dt > boundary else dt.year

def main():
    from tqdm import tqdm

    ap = argparse.ArgumentParser()
    ap.add_argument("--step-dir", default="data/step")
    ap.add_argument("--model", default="gpt-5")
    ap.add_argument("--lang", default="python")
    ap.add_argument("--prompting", default="v2-nl")
    ap.add_argument("--from-year", type=int, default=0, help="起始年份（含），0 表示自动")
    ap.add_argument("--to-year", type=int, default=0, help="结束年份（含），0 表示自动")
    ap.add_argument("--token", default=None, help="GitHub token；不传则读取环境变量 GITHUB_TOKEN")
    ap.add_argument("--split-by", choices=["create", "update"], default="create")
    ap.add_argument("--boundary", default="09-30",
                help="按这个 MM-DD 作为每年分界，例如 09-30（默认），06-30")
    ap.add_argument("--limit", type=int, default=0, help="调试用：只处理前 N 个 methods（0=不限制）")
    ap.add_argument("--sleep", type=float, default=0.0, help="每次 API 调用后 sleep 秒数，避免触发限流")
    args = ap.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("需要 GitHub token：传 --token 或设置环境变量 GITHUB_TOKEN")

    methods = load_all_methods_for_model(
        args.step_dir, args.model, args.lang, args.prompting)
    if args.limit and args.limit > 0:
        methods = methods[: args.limit]

    # 缓存：同一文件只查一次 ranges
    disk_cache = load_disk_cache()
    # 内存里仍然用 dict，但 key 改成 str，value 存 ranges
    cache: Dict[str, List[Dict[str, Any]]] = disk_cache

    from collections import defaultdict
    buckets: Dict[int, List[Method]] = defaultdict(list)
    bucket_years: List[int] = []
    failed = 0

    session = requests.Session()

    wrote_since_last = 0
    FLUSH_EVERY = 50  # 每新增 50 个文件缓存就落盘一次，防崩

    pbar = tqdm(methods, total=len(methods), dynamic_ncols=True, desc="Blame+Split")
    for m in pbar:
        try:
            gh = m.repo.github_path.strip("/")
            owner, repo = gh.split("/", 1)

            # 文件级别 key（整文件 ranges）
            file_key = f"{gh}@{m.repo.commit}:{m.file}"

            cache_hit = file_key in cache
            if not cache_hit:
                ranges = fetch_blame_ranges(
                    token=token,
                    owner=owner,
                    repo=repo,
                    commit=m.repo.commit,
                    path=m.file,
                    session=session,
                )
                cache[file_key] = ranges
                wrote_since_last += 1

                if args.sleep > 0:
                    time.sleep(args.sleep)

                if wrote_since_last >= FLUSH_EVERY:
                    save_disk_cache(cache)
                    wrote_since_last = 0

            ct, ut = compute_create_update_from_ranges(
                cache[file_key],
                m.start_line,
                m.end_line,
            )

            t = ct if args.split_by == "create" else ut
            by = bucket_year_by_boundary(t, args.boundary)
            buckets[by].append(m)
            bucket_years.append(by)

            pbar.set_postfix({
                "uniq_files": len(cache),
                "hit": int(cache_hit),
                "fail": failed,
            })

        except Exception:
            failed += 1
            pbar.set_postfix({
                "uniq_files": len(cache),
                "hit": 0,
                "fail": failed,
            })
            continue

    # 循环结束再落盘一次，确保最新缓存写入
    save_disk_cache(cache)

    print(f"Model: {args.model}")
    print(f"Split_by: {args.split_by} | boundary: {args.boundary} (UTC)")
    print(f"Methods loaded: {len(methods)} | failed(blame): {failed}")
    print(f"Unique files cached: {len(cache)}")
    print()

    if not bucket_years:
        print("No methods bucketed (all blame failed or empty input).")
        return

    # 年份范围：可选参数 from/to-year（如果你没加这俩参数，就直接用 min/max）
    y0 = min(bucket_years)
    y1 = max(bucket_years)

    bm, bd = parse_boundary_mmdd(args.boundary)

    def window_str(year: int) -> str:
        # year 表示 “(year-1)-boundary+1天 .. year-boundary” 这个区间
        # 为了简单显示成两端日期（不精确到+1天也没关系，但我给你精确版）
        start = datetime(year - 1, bm, bd, tzinfo=timezone.utc) + timedelta(days=1)
        end = datetime(year, bm, bd, tzinfo=timezone.utc)
        return f"[{start.date()}, {end.date()}]"

    from datetime import timedelta

    for year in range(y0, y1 + 1):
        ms = buckets.get(year, [])
        res = compute_corr1_comp1(ms)
        print(f"{year} {window_str(year)}  n={res['n_methods']}, corr@1={res['corr@1']:.4f}, comp@1={res['comp@1']:.4f}")

if __name__ == "__main__":
    main()
