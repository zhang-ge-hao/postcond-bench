from src.ds import *


def must_fail_inj(method: Method, code_str: str) -> str:
    lang = method.repo.language
    if lang == "python":
        stat = "assert False"
    elif lang == "java":
        stat = "assert false;"
    code_lines = code_str.split("\n")
    body_start_line_0i = method.body_start_line - 1
    while body_start_line_0i < len(code_lines) - 1 and \
            (
                code_lines[body_start_line_0i].strip() == "" or \
                code_lines[body_start_line_0i].strip() == "{" # for java
            ):
        body_start_line_0i += 1
    body_start_line_str = code_lines[body_start_line_0i]
    indent = body_start_line_str[: -len(body_start_line_str.lstrip())]
    stat = indent + stat
    prefix_lines = code_lines[: body_start_line_0i]
    suffix_lines = code_lines[body_start_line_0i: ]
    return "\n".join(prefix_lines + [stat] + suffix_lines)


def check_postcond_exec_inj(method: Method, code_str: str) -> str:
    """
    将 method 的方法体包裹进：
      - Python: try: <body> except BaseException: os._exit(88)
      - Java  : try { <inner body> } catch (Throwable e) { System.exit(88); }
    注意：Java 仅替换方法外层花括号**内部**的语句区间，不动外层 '{' 与 '}'。
    所有行号为 1-based 且闭区间。
    """
    if not (1 <= method.body_start_line <= method.end_line):
        return code_str

    # 维持原有换行符风格（\n 或 \r\n）
    def detect_eol(s: str) -> str:
        # 简单启发：若文件中出现过 \r\n，则采用 \r\n，否则用 \n
        return "\r\n" if "\r\n" in s and "\n" in s else "\n"

    eol = detect_eol(code_str)
    lines = code_str.splitlines(keepends=True)

    body_lo = method.body_start_line - 1
    body_hi = method.end_line - 1
    if body_lo < 0 or body_hi >= len(lines) or body_lo > body_hi:
        return code_str

    lang = (method.repo.language or "").strip().lower()

    def leading_ws(s: str) -> str:
        i = 0
        while i < len(s) and s[i] in (' ', '\t'):
            i += 1
        return s[:i]

    def is_blank(s: str) -> bool:
        return s.strip() == ""

    if lang == "python":
        body_lines = lines[body_lo:body_hi + 1]

        # —— 稳健的缩进探测（跳过空行，取最小前导空白）——
        non_empty_ws = [leading_ws(l) for l in body_lines if not is_blank(l)]
        if not non_empty_ws:
            # 方法体全空白，保守不改
            return code_str

        base_indent = min(non_empty_ws, key=len)
        indent_unit = '\t' if '\t' in base_indent else '    '
        deeper_indent = base_indent + indent_unit

        injected = [f"{base_indent}try:{eol}"]
        injected.extend([f"{indent_unit}{l}" for l in body_lines])  # 原体整体深一层
        injected.append(f"{base_indent}except BaseException as __inj_ex:\n")
        injected.append(f"{deeper_indent}print(\"Exception within current method!\")\n")
        injected.append(f"{deeper_indent}assert False\n")
        injected.append(f"{deeper_indent}raise __inj_ex\n")

        new_lines = lines[:body_lo] + injected + lines[body_hi + 1:]
        return "".join(new_lines)

    elif lang == "java":
        raw = lines[body_lo:body_hi + 1]
        if not raw:
            return code_str

        # 判定首尾是否为单独的大括号行（只包含可选空白 + { / }）
        first_is_open_brace = raw[0].strip() == "{"
        last_is_close_brace = raw[-1].strip() == "}"

        # 仅替换花括号内的“内部语句区间”
        inner_lo = body_lo + (1 if first_is_open_brace else 0)
        inner_hi = body_hi - (1 if last_is_close_brace else 0)

        # 若内部为空（例如空方法体），我们仍然在内部插入 try/catch（空 try 块）
        inner_lines = lines[inner_lo:inner_hi + 1] if inner_lo <= inner_hi else []

        # —— 计算内部语句区间的基缩进（尽量贴近原风格）——
        non_empty_ws = [leading_ws(l) for l in inner_lines if not is_blank(l)]
        if non_empty_ws:
            base_indent = min(non_empty_ws, key=len)
        else:
            # 内部全空：基缩进 = 外层块内的一个层级
            # 优先从开括号行推断，否则从闭括号行推断
            brace_line = lines[body_lo] if first_is_open_brace else lines[inner_lo - 1] if inner_lo - 1 >= 0 else ""
            brace_ws = leading_ws(brace_line)
            indent_unit_guess = '\t' if '\t' in brace_ws else '    '
            base_indent = brace_ws + indent_unit_guess

        # 再次推断缩进单位（高优先从 base_indent 是否含 tab；否则看周边括号行）
        def pick_indent_unit() -> str:
            if '\t' in base_indent:
                return '\t'
            # 看花括号行是否用 tab
            candidates = []
            if body_lo >= 0: candidates.append(lines[body_lo])
            if body_hi < len(lines): candidates.append(lines[body_hi])
            return '\t' if any('\t' in leading_ws(c) for c in candidates) else '    '

        indent_unit = pick_indent_unit()
        deeper_indent = base_indent + indent_unit

        # 组装注入内容：只替换内部语句区间
        injected = [f"{base_indent}try {{\n"]
        injected.extend([f"{indent_unit}{l}" for l in inner_lines])
        injected.append(f"{base_indent}}} catch (Throwable __inj_ex) {{\n")
        injected.append(f"{deeper_indent}System.out.println(\"Exception within current method!\");\n")
        injected.append(f"{deeper_indent}assert false;\n")
        injected.append(f"{deeper_indent}throw __inj_ex;\n")
        injected.append(f"{base_indent}}}\n")

        # 写回：保留外层 '{' 与 '}' 行（若存在）
        new_lines = lines[:inner_lo] + injected + lines[inner_hi + 1:]
        return "".join(new_lines)

    else:
        # 其它语言暂不处理
        raise NotImplementedError()
