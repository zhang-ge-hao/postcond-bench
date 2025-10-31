from src.repo import reproduce_pool, reproduce
from src.ds import Repo

repo_dicts = [
    {
        "github_path": "100/Solid",
        "commit": "f38ca4906b7a253bfbb74f271229625d0f1df175",
        "language": "java",
        "test_time": None
    }
]

if __name__ == "__main__":
    repo_dicts = [{**rd, "env_config": None, "failed_tests": None} 
                for rd in repo_dicts]

    repos = [Repo(**rd) for rd in repo_dicts]

    reproduce_pool(repos=repos, output_dir="data/step/2.runnable")

    # reproduce_pool(input_dir="data/step/1.biglist", 
    #             output_dir="data/step/2.runnable")