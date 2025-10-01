import os
import time
import requests
from collections import Counter
from typing import List, Set, Dict, Tuple, Optional
from tqdm import tqdm
import json
from dataclasses import dataclass, asdict

# ----------------------------
# Data structures
# ----------------------------
@dataclass
class Result:
    # Step 1: top repos by stars within the language search (up to ~1000)
    top_repos: List[Tuple[str, int]]  # [(full_name, stargazers_count)]
    # Step 2: topics per repo and topic frequency, both counted from top_repos
    tag_map: Dict[str, List[str]]     # {repo_full_name: [topic_lower, ...]}
    freq_list: Dict[str, int]         # {topic_lower: count}
    # Step 3: per-tag retrieval results BEFORE de-dup selection
    retrieve: Dict[str, List[Tuple[str, int]]]  # {tag: [(full_name, stars), ...]}
    # Step 4: final selected unique repos across tags (flattened)
    selected: List[str]               # [full_name]

# ----------------------------
# GitHub selector
# ----------------------------
class GitHubTopicRepoSelector:
    def __init__(
        self,
        github_token: str,
        min_stars: int = 100,
        per_page: int = 100,
        max_search_pages: int = 10,
        sleep_between_requests: float = 1.0,
    ):
        """
        :param github_token: GitHub personal access token to raise rate limits.
        :param min_stars: Minimum stars used in tag searches (e.g., stars:>={min_stars}).
        :param per_page: Per-page size for Search API (max 100).
        :param max_search_pages: Max pages for Search API (commonly <= 10 pages ~ 1000 items).
        :param sleep_between_requests: Sleep seconds between API calls to avoid rate limiting.
        """
        self.token = github_token
        self.min_stars = min_stars
        self.per_page = min(per_page, 100)
        self.max_search_pages = max_search_pages
        self.sleep = sleep_between_requests
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            # Topics API historically needed the preview header; keeping for compatibility.
            "Accept": "application/vnd.github.mercy-preview+json"
        })

    # ------------- low-level API helpers -------------

    def _search_repositories(
        self,
        query: str,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        max_pages: Optional[int] = None,
        licenses: List[str] = None
    ) -> List[Dict]:
        """
        Generic Search API wrapper. Returns list of repository items (dicts).
        """
        def is_allowed_licenses(item) -> bool:
            if not "license" in item \
                or item["license"] is None \
                    or not "key" in item["license"]:
                return False
            return item["license"]["key"] in licenses

        repos = []
        per_page = self.per_page
        max_pages = max_pages if max_pages is not None else self.max_search_pages
        for page in range(1, max_pages + 1):
            params = {
                "q": query,
                "per_page": per_page,
                "page": page,
            }
            if sort:
                params["sort"] = sort
            if order:
                params["order"] = order

            resp = self.session.get("https://api.github.com/search/repositories", params=params)
            if resp.status_code != 200:
                print(f"[Warning] Search API returned {resp.status_code}. Message: {resp.text}")
                break

            data = resp.json()
            items = data.get("items", [])
            if not items:
                break
            
            page_size = len(items)

            if licenses is not None:
                items = [item for item in items if is_allowed_licenses(item)]
            repos.extend(items)

            # If fewer than per_page, no more pages left.
            if page_size < per_page:
                break

            # Avoid hammering the API.
            time.sleep(self.sleep)

        return repos

    def _get_topics_of_repo(self, full_name: str) -> List[str]:
        """
        Fetch topics for a repository.
        :param full_name: "owner/repo"
        :return: list of topic names.
        """
        url = f"https://api.github.com/repos/{full_name}/topics"
        resp = self.session.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("names", [])
        else:
            print(f"[Warning] Failed to get topics for {full_name}. status={resp.status_code}")
            return []

    # ------------- high-level operations -------------

    def fetch_top_repos(self, language: str, max_pages_for_count: Optional[int] = None) -> List[Tuple[str, int]]:
        """
        Step 1: Get top repositories by stars for a language (up to ~1000).
        Returns a list of (full_name, stargazers_count).
        """
        target = (max_pages_for_count or self.max_search_pages) * self.per_page
        print(f"[Step 1] Fetching top ~{target} starred repositories for language={language} ...")
        repos = self._search_repositories(
            query=f"language:{language}",
            sort="stars",
            order="desc",
            max_pages=max_pages_for_count
        )
        top_repos = []
        for repo in repos:
            full_name = repo.get("full_name")
            stars = repo.get("stargazers_count", 0)
            if full_name:
                top_repos.append((full_name, stars))
        print(f"[Step 1] Retrieved {len(top_repos)} repositories for {language}.")
        return top_repos

    def build_tag_map_and_freq(self, top_repos: List[Tuple[str, int]]) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
        """
        Step 2: For each repo in top_repos, fetch its topics and build:
          - tag_map: {repo_full_name: [topic_lower, ...]}
          - freq_map: {topic_lower: count}
        """
        print(f"[Step 2] Building tag_map and frequency from {len(top_repos)} repositories ...")
        tag_map: Dict[str, List[str]] = {}
        counter = Counter()

        for full_name, _stars in tqdm(top_repos):
            topics = self._get_topics_of_repo(full_name)
            topics_lower = [t.lower() for t in topics]
            tag_map[full_name] = topics_lower
            for t in topics_lower:
                counter[t] += 1
            time.sleep(self.sleep)

        freq_map = dict(counter.most_common())
        print(f"[Step 2] tag_map size = {len(tag_map)}; unique topics = {len(freq_map)}.")
        return tag_map, freq_map

    def select_repos_per_tag(
        self,
        language: str,
        tag_counts_sorted: List[Tuple[str, int]],
        per_tag_count: int,
        max_pages_per_tag: Optional[int] = None
    ) -> Tuple[Dict[str, List[Tuple[str, int]]], List[str]]:
        """
        Step 3 & 4:
        - For each tag (iterate from low to high frequency), search repos by stars and build:
        (a) retrieve[tag]: ALL repos returned by the search (no de-dup, no truncation;
            bounded only by the Search API pagination limit, typically ~1000).
        (b) selection: choose up to 'per_tag_count' repos per tag, skipping duplicates globally.

        Returns:
        retrieve_map, selected_list
        """
        print(f"[Step 3/4] Searching and selecting per-tag repositories for language={language} ...")
        selected_set: Set[str] = set()
        retrieve_map: Dict[str, List[Tuple[str, int]]] = {}
        result_map: Dict[str, List[Tuple[str, int]]] = {}

        size_query = "size:<20480"

        licenses = [
            "mit",
            "apache-2.0",
            "bsd-2-clause",
            "bsd-3-clause",
            "isc",
            "unlicense",
            "zlib",
        ]

        sorted_tags = sorted(tag_counts_sorted, key=lambda x: x[1])
        for tag, freq in tqdm(sorted_tags):
            print(f"  [Tag] '{tag}' (freq={freq}): retrieving and selecting ...")
            query = f"topic:{tag} language:{language} stars:>={self.min_stars} {size_query}"
            repos = self._search_repositories(
                query,
                sort="stars",
                order="desc",
                max_pages=max_pages_per_tag,
                licenses=licenses
            )

            # (a) retrieve: ALL repos returned by the search (no truncation)
            all_found = []
            for repo in repos:
                full_name = repo.get("full_name")
                if not full_name:
                    continue
                stars = repo.get("stargazers_count", 0)
                all_found.append((full_name, stars))
            retrieve_map[tag] = all_found

            # (b) selected for this tag: de-dup globally, up to per_tag_count
            per_selected: List[Tuple[str, int]] = []
            for repo in repos:
                full_name = repo.get("full_name")
                if not full_name or full_name in selected_set:
                    continue
                stars = repo.get("stargazers_count", 0)
                per_selected.append((full_name, stars))
                selected_set.add(full_name)
                if len(per_selected) >= per_tag_count:
                    break

            if len(per_selected) < per_tag_count:
                print(f"    [Note] Tag '{tag}' selected {len(per_selected)} unique repos "
                    f"(target {per_tag_count}).")
            print(f"    [Info] Tag '{tag}': retrieved={len(all_found)}, selected={len(per_selected)}")

            result_map[tag] = per_selected
            time.sleep(self.sleep)

        total_selected = sum(len(v) for v in result_map.values())
        print(f"[Step 4] Total unique selected repositories: {total_selected} "
            f"(expected up to {len(sorted_tags) * per_tag_count}).")

        # Flatten to a single list of full_name for 'selected'
        flat_selected = []
        for _tag, lst in result_map.items():
            flat_selected.extend([full_name for full_name, _stars in lst])

        return retrieve_map, flat_selected

    def select_from_cached_retrieve(
        self,
        tag_counts_sorted: List[Tuple[str, int]],
        retrieve_map: Dict[str, List[Tuple[str, int]]],
        per_tag_count: int,
    ) -> Tuple[Dict[str, List[Tuple[str, int]]], List[str]]:
        """
        使用已有的 retrieve_map（{tag: [(full_name, stars), ...]}）在本地做 Step 3/4：
        - 不再访问网络；
        - 仍然保持“按低频到高频 tag 优先”的全局去重与挑选逻辑；
        - 返回 (result_map, flat_selected) 与在线逻辑一致。
        """
        print(f"[Step 3/4 - cached] Selecting per-tag repositories from cached retrieve ...")
        selected_set: Set[str] = set()
        result_map: Dict[str, List[Tuple[str, int]]] = {}

        # 与在线流程保持一致：按 tag 频次从低到高挑选，保证全局去重的优先级相同
        sorted_tags = sorted(tag_counts_sorted, key=lambda x: x[1])

        def _coerce_item(item) -> Tuple[Optional[str], int]:
            # 兼容 JSON 反序列化后的 list/tuple 或 dict 形式
            if isinstance(item, (list, tuple)):
                if not item:
                    return None, 0
                full_name = item[0]
                stars = item[1] if len(item) > 1 else 0
                return full_name, int(stars or 0)
            if isinstance(item, dict):
                return item.get("full_name"), int(item.get("stargazers_count", 0) or 0)
            return None, 0

        for tag, freq in tqdm(sorted_tags):
            cached_list = retrieve_map.get(tag, []) or []
            per_selected: List[Tuple[str, int]] = []

            for raw in cached_list:
                full_name, stars = _coerce_item(raw)
                if not full_name or full_name in selected_set:
                    continue
                per_selected.append((full_name, stars))
                selected_set.add(full_name)
                if len(per_selected) >= per_tag_count:
                    break

            result_map[tag] = per_selected
            print(f"    [Info] Tag '{tag}': cached={len(cached_list)}, selected={len(per_selected)}")

        flat_selected = [full_name for _tag, lst in result_map.items() for (full_name, _stars) in lst]
        print(f"[Step 4 - cached] Total unique selected repositories: {len(flat_selected)} "
              f"(expected up to {len(sorted_tags) * per_tag_count}).")
        return result_map, flat_selected

# ----------------------------
# I/O utilities
# ----------------------------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def save_result_json(path: str, result: Result):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(result), f, ensure_ascii=False, indent=2)
    print(f"[IO] Result saved to: {path}")

def load_result_json(path: str) -> Optional[Result]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Backward compatibility with older caches (no tag_map/freq_list)
        return Result(
            top_repos=data.get("top_repos", []),
            tag_map=data.get("tag_map", {}),
            freq_list=data.get("freq_list", {}),
            retrieve=data.get("retrieve", {}),
            selected=data.get("selected", []),
        )
    except Exception as e:
        print(f"[Warning] Failed to load cache from {path}: {e}")
        return None

# ----------------------------
# Main flow
# ----------------------------
def main():
    # Read GitHub token
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "YOUR_GITHUB_TOKEN"
    if not GITHUB_TOKEN or GITHUB_TOKEN == "YOUR_GITHUB_TOKEN":
        print("Please set env var GITHUB_TOKEN or hardcode a valid GitHub token.")
        return

    # Parameters
    min_stars = 200          # threshold for tag searches
    num_tags = 200           # how many most frequent tags to use in Step 3/4
    per_tag_count = 25       # how many repos per tag to retrieve/select
    # # for Java
    # num_tags = 400           # how many most frequent tags to use in Step 3/4
    # per_tag_count = 100      # how many repos per tag to retrieve/select
    max_pages_for_count = 10 # pages for step 1
    max_pages_per_tag = 10   # pages for step 3
    sleep_between_requests = 3.0

    selector = GitHubTopicRepoSelector(
        github_token=GITHUB_TOKEN,
        min_stars=min_stars,
        per_page=100,
        max_search_pages=10,
        sleep_between_requests=sleep_between_requests
    )

    languages = ["Python", "Java"]
    out_dir = "data"
    final_results: Dict[str, Result] = {}

    for lang in languages:
        cache_path = os.path.join(out_dir, f"result_{lang.lower()}.json")
        print(f"\n===== Language: {lang} =====")
        # Try to load cached top_repos + tag_map (+ freq_list if any)
        cached = load_result_json(cache_path)

        if cached and cached.top_repos and cached.tag_map:
            # If freq_list missing in an older cache, rebuild from tag_map
            if not cached.freq_list:
                print("[Cache] Found top_repos and tag_map, rebuilding freq_list from tag_map ...")
                counter = Counter()
                for topics in cached.tag_map.values():
                    for t in topics:
                        counter[t] += 1
                cached.freq_list = dict(counter.most_common())
                save_result_json(cache_path, cached)
            else:
                print("[Cache] Found existing top_repos, tag_map and freq_list. Skipping Steps 1 & 2.")
            result_obj = cached
        else:
            # Fresh or partial cache
            result_obj = cached or Result(top_repos=[], tag_map={}, freq_list={}, retrieve={}, selected=[])

            # Step 1: get top repos if missing
            if not result_obj.top_repos:
                result_obj.top_repos = selector.fetch_top_repos(
                    language=lang, max_pages_for_count=max_pages_for_count
                )

            # Step 2: tag_map + freq_list if missing
            if not result_obj.tag_map or not result_obj.freq_list:
                tag_map, freq_map = selector.build_tag_map_and_freq(result_obj.top_repos)
                result_obj.tag_map = tag_map
                result_obj.freq_list = freq_map

            # Persist after Step 1 & 2
            save_result_json(cache_path, result_obj)
            print("[Checkpoint] Saved after Steps 1 & 2.")

        # Prepare tag list for Steps 3/4 using the current freq_list
        tag_counts_sorted = sorted(result_obj.freq_list.items(), key=lambda x: x[1], reverse=True)
        tag_counts_sorted = tag_counts_sorted[:num_tags]

        # Step 3 & 4:
        # 如果已有完整的 retrieve（之前完整跑通过），则直接用缓存按新的 per_tag_count 重选；
        # 否则，才调用线上检索。
        tags_needed = {t for t, _ in tag_counts_sorted}
        have_retrieve = bool(result_obj.retrieve)
        has_all_needed = have_retrieve and tags_needed.issubset(set(result_obj.retrieve.keys()))

        if has_all_needed:
            print("[Cache] Found full retrieve map for required tags. Recomputing selection with "
                  f"per_tag_count={per_tag_count} without hitting the API.")
            result_map, selected_list = selector.select_from_cached_retrieve(
                tag_counts_sorted=tag_counts_sorted,
                retrieve_map=result_obj.retrieve,
                per_tag_count=per_tag_count
            )
            # 只更新 selected；retrieve 已有且复用
            result_obj.selected = selected_list
            save_result_json(cache_path, result_obj)
            print("[Final] Saved after re-selection from cache (no API calls).")
        else:
            # 仍然可能存在部分 retrieve，但不完整；为保证结果完整性，这里走一次完整检索
            retrieve_map, selected_list = selector.select_repos_per_tag(
                language=lang,
                tag_counts_sorted=tag_counts_sorted,
                per_tag_count=per_tag_count,
                max_pages_per_tag=max_pages_per_tag
            )
            result_obj.retrieve = retrieve_map
            result_obj.selected = selected_list
            save_result_json(cache_path, result_obj)
            print("[Final] Saved after Steps 3 & 4.")
        final_results[lang] = result_obj

    # Optional: simple summary to stdout
    for lang, res in final_results.items():
        print(f"\n=== Language: {lang} ===")
        print(f"Top repos: {len(res.top_repos)}")
        print(f"Repos with topics (tag_map): {len(res.tag_map)}")
        print(f"Unique topics in freq_list: {len(res.freq_list)}")
        print(f"Tags retrieved: {len(res.retrieve)}")
        print(f"Total selected unique repos: {len(res.selected)}")

if __name__ == "__main__":
    main()
