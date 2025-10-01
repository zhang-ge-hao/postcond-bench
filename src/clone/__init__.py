import os
from src.util.temp_dir import change_dir, create_tempdir
import contextlib
from src.ds import Repo
import toml
import fcntl
import tempfile
import shutil
import pygit2
import tarfile
from typing import *


class RepoClone:
    def __init__(self, base_dir: str, github_path: str, commit: Optional[str] = None,
                 cache_base: str = None):
        self.github_path = github_path
        self.base_dir = base_dir
        self.commit = commit
        self.cache_base = cache_base

        if cache_base is None:
            pi_workdir = os.getenv("PI_WORKDIR")
            self.cache_base = os.path.join(pi_workdir, "sb_tmp__repos")
            os.makedirs(self.cache_base, exist_ok=True)

    # ---------- 工具 ----------
    def _folder_name(self) -> str:
        return self.github_path.replace("/", "--")

    def _repo_url(self) -> str:
        return f"https://github.com/{self.github_path}.git"

    def _ensure_dir(self, p: str):
        os.makedirs(p, exist_ok=True)

    @contextlib.contextmanager
    def _exclusive_file_lock(self, lock_path: str):
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            with os.fdopen(fd, "w") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                yield
        finally:
            # 关闭文件自动释放锁
            pass

    def _clone_and_checkout_to(self, url: str, workdir: str, commit: Optional[str]) -> str:
        """
        用 pygit2 克隆到 workdir（非 bare），检出指定 commit（或默认分支最新）。
        返回最终检出的 commit oid（str）。
        """
        # pygit2.clone_repository 支持设置 checkout_branch；深度（shallow）在较新版本可通过 kw 传递 depth=1
        # 若你的环境 pygit2 不支持 depth 参数，可以先 clone（深度默认完整或受服务器限制），再 fetch/checkout。
        repo = pygit2.clone_repository(url, workdir, checkout_branch=None)

        if commit:
            # 允许传入短/长哈希或分支/标签名
            try:
                # 先当 OID 解析
                target = repo.revparse_single(commit)
            except KeyError:
                # 当名字解析（可能是refs/heads/... 或 refs/tags/...）
                ref = repo.lookup_reference(f"refs/heads/{commit}") if f"refs/heads/{commit}" in repo.references \
                      else repo.lookup_reference(f"refs/tags/{commit}")
                target = repo[ref.target]
        else:
            # 未指定：使用 HEAD 所指向的 commit
            head_ref = repo.lookup_reference("HEAD").resolve()
            target = repo[head_ref.target]

        # 将目标树检出到工作区
        repo.checkout_tree(target, strategy=pygit2.GIT_CHECKOUT_FORCE)
        # 将 HEAD 置为游离指针到目标 commit（非必须，但有助于一致性）
        repo.set_head(target.id)

        return str(target.id)

    def _make_uncompressed_tar_from_dir(self, src_dir: str, tar_path: str):
        # 删除 .git
        git_dir = os.path.join(src_dir, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir)

        # 写入到临时 .partial，成功后原子替换
        tmp_tar = tar_path + ".partial"
        # 确保父目录存在
        self._ensure_dir(os.path.dirname(tar_path))

        # 用标准库 tarfile，无压缩：mode='w'
        with tarfile.open(tmp_tar, mode="w", dereference=False, format=tarfile.PAX_FORMAT) as tf:
            # 将 src_dir 下的所有内容打包到 tar 根目录
            for root, dirs, files in os.walk(src_dir):
                # 保留相对路径
                rel_root = os.path.relpath(root, src_dir)
                # 目录本身（除了 "."）也可以加入以保留空目录
                if rel_root != ".":
                    tf.add(root, arcname=rel_root, recursive=False)
                for name in files:
                    abs_path = os.path.join(root, name)
                    arcname = os.path.normpath(os.path.join(rel_root, name))
                    tf.add(abs_path, arcname=arcname, recursive=False)

        os.replace(tmp_tar, tar_path)

    def _extract_tar_to_dir(self, tar_path: str, dest_dir: str):
        with tarfile.open(tar_path, mode="r") as tf:
            tf.extractall(path=dest_dir)

    # ---------- 主流程 ----------
    def clone(self):
        folder_name = self._folder_name()
        dest_path = os.path.join(self.base_dir, folder_name)
        repo_url = self._repo_url()
        cache_dir = os.path.join(self.cache_base, folder_name)

        def load_catch_commit():
            if not os.path.exists(cache_dir):
                return None
            commits = [n[:-4] for n in os.listdir(cache_dir) if n.endswith(".tar")]
            if len(commits) == 0:
                return None
            return commits[0]
        # 1) 如果未提供 commit，需要先做一次轻量克隆解析 HEAD 的 OID
        #    我们直接克隆到 /tmp/sb_tmp__* 临时目录，随后即删除
        if self.commit is None:
            loaded_commit = load_catch_commit()
            if loaded_commit is None:
                with tempfile.TemporaryDirectory(prefix="sb_tmp__resolve_head_") as tmp_root:
                    workdir = os.path.join(tmp_root, "repo")
                    resolved_oid = self._clone_and_checkout_to(repo_url, workdir, None)
                    self.commit = resolved_oid  # 用具体 OID 做缓存 key
            else:
                self.commit = loaded_commit

        # 2) 缓存路径与锁
        self._ensure_dir(cache_dir)
        cache_tar = os.path.join(cache_dir, f"{self.commit}.tar")
        lock_path = os.path.join(cache_dir, f"{self.commit}.lock")

        # 3) 构建缓存 tar（不存在时；并发安全）
        if not os.path.exists(cache_tar):
            with self._exclusive_file_lock(lock_path):
                if not os.path.exists(cache_tar):
                    # 克隆到 /tmp/sb_tmp__*，检出指定 commit
                    with tempfile.TemporaryDirectory(prefix="sb_tmp__repo_cache_build_") as tmp_root:
                        workdir = os.path.join(tmp_root, "repo")
                        _oid = self._clone_and_checkout_to(repo_url, workdir, self.commit)
                        # 理论上 _oid == self.commit（可能大小写格式不同），用 _oid 更稳妥
                        # 但缓存 key 已由 self.commit 决定，这里只负责打包
                        self._make_uncompressed_tar_from_dir(workdir, cache_tar)

        # 4) 将缓存解包到目标路径
        if os.path.exists(dest_path):
            if os.listdir(dest_path):
                # 为了安全起见，避免覆盖已有内容（与原实现一致）
                return False, dest_path
        else:
            self._ensure_dir(dest_path)

        self._extract_tar_to_dir(cache_tar, dest_path)
        return True, dest_path
    
    def remove_cache(self):
        folder_name = self._folder_name()
        cache_dir = os.path.join(self.cache_base, folder_name)
        self._ensure_dir(cache_dir)
        cache_tar = os.path.join(cache_dir, f"{self.commit}.tar")
        lock_path = os.path.join(cache_dir, f"{self.commit}.lock")
        if os.path.exists(cache_tar):
            os.remove(cache_tar)
        if os.path.exists(lock_path):
            os.remove(lock_path)

    def resnapshot(self, repo_dir: Optional[str] = None) -> Tuple[bool, str]:
        """
        在你对工作目录做了修改后调用：重新打包当前 repo 内容为 tar，
        并覆盖当前 commit 对应的缓存 tar 包（不包含 .git）。
        返回 (success, cache_tar)。
        约定：请先调用 clone()，以确保 self.commit 已解析。
        """
        if not self.commit:
            raise RuntimeError("resnapshot(): commit 未知。请先调用 clone() 以解析/设置 commit。")

        folder_name = self._folder_name()
        # 若未显式传入，默认使用 clone() 解包到的标准目标路径
        dest_path = os.path.join(self.base_dir, folder_name)
        if repo_dir is None:
            repo_dir = dest_path

        if not os.path.exists(repo_dir):
            raise FileNotFoundError(f"resnapshot(): repo 目录不存在：{repo_dir}")

        cache_dir = os.path.join(self.cache_base, folder_name)
        self._ensure_dir(cache_dir)
        cache_tar = os.path.join(cache_dir, f"{self.commit}.tar")
        lock_path = os.path.join(cache_dir, f"{self.commit}.lock")

        # 并发安全 & 原子覆盖
        with self._exclusive_file_lock(lock_path):
            self._make_uncompressed_tar_from_dir(repo_dir, cache_tar)

        return True, cache_tar


@contextlib.contextmanager
def repository_reproduct(repo: Repo, require_clone: bool=False):
    with create_tempdir() as dirname:
        clone = RepoClone(dirname, repo.github_path, repo.commit)
        success, repo_dir = clone.clone()
        if not success:
            raise RuntimeError("clone failed.")
        if repo.env_config is not None:
            if repo.language == "python":
                config_file_name = "pyproject.toml" 
            elif repo.language == "java":
                config_file_name = "pom.xml"
            else:
                raise NotImplementedError()
            config_path = os.path.join(repo_dir, config_file_name)
            with open(config_path, "w") as file:
                file.write(repo.env_config)
        with change_dir(repo_dir):
            if not require_clone:
                yield repo_dir
            else:
                yield repo_dir, clone