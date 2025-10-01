from src.repo import reproduce_pool, reproduce
from src.ds import Repo

repo_dicts = [
    {
        "github_path": "addthis/stream-lib",
        "commit": "5a3bc87c5314f7771ea3968e9015a3d25536343e",
        "language": "java",
    }, {
        "github_path": "adyliu/jafka",
        "commit": "a8500130130ae22087fbcb5c9e605ee1dfd824c1",
        "language": "java",
    }, {
        "github_path": "AppsFlyer/donkey",
        "commit": "e36889e3b18da17d151c6a70673653ea4d24c045",
        "language": "java",
    }, {
        "github_path": "BastiaanJansen/otp-java",
        "commit": "b6fd6e49f6f83d853fd03d5a97d4ae545b1cdc94",
        "language": "java",
    }, {
        "github_path": "byronka/minum",
        "commit": "53878e6165b13f88480330386c60c879ac634a9b",
        "language": "java",
    }, {
        "github_path": "arrow-py/arrow",
        "commit": "86f7520f15b2dd46f9c49f71ce5c15bbc537ed67",
        "language": "python",
    }, {
        "github_path": "authlib/authlib",
        "commit": "0d03ee9dd758f95853356fa1eea3fbce37109eb0",
        "language": "python",
    }, {
        "github_path": "cookiecutter/cookiecutter",
        "commit": "dc494685fc98670db52cc67c317f154ca930a688",
        "language": "python",
    }, {
        "github_path": "duo-labs/py_webauthn",
        "commit": "67cacb6038c7fbc18ba532e14c0f8d18015bf7b4",
        "language": "python",
    }, {
        "github_path": "ekzhang/inline-sql",
        "commit": "bfc05cd991b559dc6b8ea01170d804c2aab534be",
        "language": "python",
    }
]

if __name__ == "__main__":
    repo_dicts = [{**rd, "env_config": None, "failed_tests": None} 
                for rd in repo_dicts]

    repos = [Repo(**rd) for rd in repo_dicts]

    reproduce_pool(repos=repos, output_dir="data/step/2.runnable")

    # from src.util import set_logging
    # set_logging()
    # repo = Repo(
    #     github_path="ekzhang/inline-sql",
    #     commit="bfc05cd991b559dc6b8ea01170d804c2aab534be",
    #     language="python",
    #     env_config=None,
    #     failed_tests=None
    # )
    # # repo = Repo(
    # #     github_path="authlib/authlib",
    # #     commit="0d03ee9dd758f95853356fa1eea3fbce37109eb0",
    # #     language="python",
    # #     env_config=None,
    # #     failed_tests=None
    # # )
    # # repo = Repo(
    # #     github_path="duo-labs/py_webauthn",
    # #     commit="67cacb6038c7fbc18ba532e14c0f8d18015bf7b4",
    # #     language="python",
    # #     env_config=None,
    # #     failed_tests=None
    # # )
    # reproduce(repo)