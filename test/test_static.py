from src.ds import Repo
import os

from src.method.static import (
    method_collection,
    method_collection_pool
)

if __name__ == "__main__":
    # input_dir = "data/step/2.runnable"
    # for file_name in os.listdir(input_dir):
    #     file_path = f"{input_dir}/{file_name}"
    #     repo = Repo.load(file_path)
    #     method_collection(repo)
    
    method_collection_pool("data/step/2.runnable", 
                           "data/step/3.static")
