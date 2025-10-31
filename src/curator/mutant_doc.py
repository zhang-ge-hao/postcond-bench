import json
import difflib

from src.ds import *

def get_mutant_doc(
        method: Method,
        survived_mutant_idxs = None) -> str:

    mutants = method.mutants
    if not survived_mutant_idxs:
        survived_mutant_idxs = list(range(len(mutants)))
    else:
        mutants = [m for i, m in enumerate(mutants) 
                   if i in survived_mutant_idxs]

    original_method = method.content

    doc = (
        "# Original Method\n"
        "```\n"
        f"{original_method}\n"
        "```\n"
    )

    for m_idx, mutant in zip(survived_mutant_idxs, mutants):
        lines = []
        
        diff_lines = difflib.unified_diff(
            original_method.splitlines(keepends=True),
            mutant.splitlines(keepends=True),
            lineterm=""
        )
        diff_str = "".join(list(diff_lines)[3: ])
        diff_str = diff_str.rstrip()

        lines.append(f"# Mutant {m_idx}")
        lines.append("## Mutant Code")
        lines.append("```")
        lines.append(mutant)
        lines.append("```")
        lines.append("## Diff")
        lines.append("```")
        lines.append(diff_str)
        lines.append("```")

        doc += "\n".join(lines) + "\n"

    return doc
