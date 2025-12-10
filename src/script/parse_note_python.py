
import os, json


root_dir = "data/ground_truth/python/filtered"


def classify_note(note: str):
    if "timeout" in note.lower():
        return "timeout"
    if any(k in note.lower() for k in ["iterator", "iterable", "yield", "generator"]):
        return "iterator"
    if "hard" in note.lower():
        return "hard"
    if "async" in note.lower() or "thread safety" in note.lower() or "subprocess" in note.lower():
        return "concurrency"
    if "function object" in note.lower() or "class object" in note.lower():
        return "language_entities"
    if "mock" in note.lower():
        return "mock"
    if "wrong originally" in note.lower():
        return "wrong_originally"
    if "no icontract" in note.lower() or "no module named 'icontract'" in note.lower():
        return "no_icontract"
    if "specified error process" in note.lower():
        return "specified_error_process"
    return None

filter_types = {
    "no_icontract": 0,
    "timeout": 0,
    "iterator": 0,
    "hard": 0,
    "concurrency": 0,
    "language_entities": 0,
    "mock": 0,
    "wrong_originally": 0,
    "specified_error_process": 0,
}

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
        filter_types[cate] += 1

print(json.dumps(filter_types, indent=2))