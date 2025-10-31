from src.ds import *

from src.jml import rewrite_java_source


def postcond_inj(
        method: Method, 
        code_str: str, 
        postcond: str,
        mutant: str = None):
    lang = method.repo.language

    code_lines = code_str.split("\n")

    method_lines = code_lines[method.start_line - 1: method.end_line]
    if mutant:
        method_lines = mutant.split("\n")
    
    # 计算方法的缩进
    __line = method_lines[0]
    init_indent = __line[: -len(__line.lstrip())]

    # 去除postcond前后的空行
    postcond_lines = postcond.split("\n")
    while postcond_lines and len(postcond_lines[0].strip()) == 0:
        postcond_lines = postcond_lines[1: ]
    while postcond_lines and len(postcond_lines[-1].strip()) == 0:
        postcond_lines = postcond_lines[: -1]
    
    # 将postcond行的缩进和方法默认缩进进行统一
    __line = postcond_lines[0]
    postcond_indent = __line[: -len(__line.lstrip())]
    for l_idx, l in enumerate(postcond_lines):
        postcond_lines[l_idx] = init_indent + l[len(postcond_indent): ]

    # 获取插入postcond后的方法行
    # 注意python的所有postcondition行一定要出现在所有其他装饰器之后
    # 正确顺序：
    # @classmethod
    # @icontract.snapshot(...
    # def push(...
    if lang == "python":
        inj_method_lines = []
        for l in method_lines:
            if l.strip().startswith("def "):
                inj_method_lines.extend(postcond_lines)
            inj_method_lines.append(l)
    elif lang == "java":
        inj_method_lines = postcond_lines + method_lines
    else:
        raise NotImplementedError()

    prefix_lines = code_lines[:method.start_line - 1]
    suffix_lines = code_lines[method.end_line: ]

    # 插入python的import icontract
    # 希望它能成为文件中的第二个import 如果文件中本身没找到import行
    # 就插入到文件第一行
    if lang == "python":
        __prefix_lines = []
        added = False
        for line in prefix_lines:
            __prefix_lines.append(line)
            if not added and \
                (line.startswith("from") or line.startswith("import")):
                __prefix_lines.append("import icontract")
                added = True
        if not added:
            __prefix_lines.insert(0, "import icontract")
        prefix_lines = __prefix_lines
    
    # 组合为插入后的文件
    inj_code_lines = prefix_lines + inj_method_lines + suffix_lines

    # 对于python来说 需要获取插入后的方法的起止行作为local crash的判断依据
    if lang == "python":
        inj_code = "\n".join(inj_code_lines)
        hot_line_start = len(prefix_lines) + 1
        hot_line_end = len(prefix_lines) + len(inj_method_lines)
        local_crash_line_range = (hot_line_start, hot_line_end)

        # ===== Debug =====
        print("===== Debug =====")
        print(inj_code)
        print(local_crash_line_range)
        pass
        # ===== Debug End =====

        return inj_code, local_crash_line_range
    # 对于python来说 不需要起止行 但需要进行JML翻译
    elif lang == "java":
        inj_code = "\n".join(inj_code_lines)
        try:
            inj_code = rewrite_java_source(inj_code)
        except:
            return None, None
        return inj_code, None
