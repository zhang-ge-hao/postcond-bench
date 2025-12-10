
import os, json


root_dir = "data/ground_truth/java/filtered"


def classify_note(note: str):
    if "timeout" in note.lower():
        return "timeout"
    if "\niter" in note.lower():
        return "iterator"
    if "hard" in note.lower():
        return "hard"
    if "function object" in note.lower() or "class object" in note.lower():
        return "language_entities"
    if "wrong originally" in note.lower() or "originally wrong" in note.lower():
        return "wrong_originally"
    if "mock" in note.lower():
        return "mock"
    if "random used" in note.lower():
        return "random"
    if "no api" in note.lower():
        return "no_api"
    return None

filter_types = {}

for fn in os.listdir(root_dir):
    with open(f"{root_dir}/{fn}") as file:
        lines = []
        in_block = False
        for line in file:
            if line.startswith("```") and not in_block:
                in_block = True
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                lines.append(line)
        note = "".join(lines)
    cate = classify_note(note)
    if cate == "hard":
        print(f"{root_dir}/{fn}")
        print(note[: 200])
    if cate is None:
        print(f"{root_dir}/{fn}")
        print(note[: 200])
    else:
        if cate not in filter_types:
            filter_types[cate] = 0
        filter_types[cate] += 1

print(json.dumps(filter_types, indent=2))