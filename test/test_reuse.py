from src.repo import reuse_pool, reuse
from src.ds import Repo


if __name__ == "__main__":
    reuse_pool(input_dir="data/step/0.runnable", output_dir="data/step/2.runnable")
    
    # from src.util import set_logging
    # set_logging()
    # repo = Repo.load("data/step/0.runnable/nnngu--nguSeckill.json")
    # reuse(repo)
