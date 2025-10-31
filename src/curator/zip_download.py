import os
import requests
from typing import Optional

def download_github_commit_zip(
    github_path: str,
    commit: str,
    dest_zip_path: str,
    token: Optional[str] = None,
) -> str:
    """
    Download a ZIP archive of a GitHub repository at a specific commit.

    Args:
        owner: Repository owner (user or org), e.g. "octocat".
        repo: Repository name, e.g. "Hello-World".
        commit_sha: The commit SHA (full 40 chars recommended).
        dest_zip_path: Local file path to save the ZIP, e.g. "./src.zip".
        token: Optional GitHub token for private repos or higher rate limits.

    Returns:
        The absolute path of the saved ZIP file.

    Raises:
        RuntimeError: If the HTTP request fails.
    """
    # Use codeload endpoint to avoid an extra redirect
    url = f"https://codeload.github.com/{github_path}/zip/{commit}"

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/vnd.github+json"

    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            msg = (
                f"Download failed: HTTP {r.status_code}\n"
                f"URL: {url}\n"
                f"- Is the repository private? If so, provide a token.\n"
                f"- Do you have access to the repo/commit?\n"
                f"- Does the commit SHA exist in this repository?"
            )
            raise RuntimeError(msg) from e

        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(os.path.abspath(dest_zip_path)) or ".", exist_ok=True)

        # Stream to file to avoid large memory usage
        with open(dest_zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)

    return os.path.abspath(dest_zip_path)


if __name__ == "__main__":
    # Example: download a specific commit of octocat/Hello-World
    github_path = "logfellow/logstash-logback-encoder"
    commit = "eecb205fde0598bcfedc557ecc57ccc9e854c303"  # replace with your commit SHA
    dest = "./demo.zip"

    # For private repos, set GITHUB_TOKEN env var or pass it directly
    token = os.getenv("GITHUB_TOKEN")  # or set to a string like "ghp_***"
    path = download_github_commit_zip(github_path, commit, dest, token)
    print(f"Saved to: {path}")
