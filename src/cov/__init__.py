import os
import xml.etree.ElementTree as ET

from src.ds import *

def _norm_path(p: str) -> str:
    return os.path.normpath(p).replace("\\", "/").lower()

def _match_filename(target_path: str, candidate: str) -> bool:
    """用 endswith 做鲁棒匹配：既能匹配纯文件名，也能匹配相对路径。"""
    t = _norm_path(target_path)
    c = _norm_path(candidate)
    return c.endswith(t) or os.path.basename(c) == os.path.basename(t)

def _ratio(numer: int, denom: int):
    if denom <= 0:
        return None  # 方法区间内没有任何“可执行行”，无法定义行覆盖率
    return numer / denom

def _jacoco_collect_sourcefiles_with_paths(root):
    """
    收集 (候选相对路径列表, <sourcefile>元素)：
    - 优先包含 group（模块名）/ package / sourcefile 的组合
    - 同时回退到 package/sourcefile 与仅文件名
    - package 里常见是 'com/foo/bar'（也可能是 'com.foo.bar'），两种分隔都尝试
    """
    results = []

    def pkg_to_path(pkg_name: str) -> str:
        if not pkg_name:
            return ""
        # 兼容两种分隔
        path_slash = pkg_name.replace(".", "/")
        return path_slash

    def add_from_pkg_container(pkg_container, group_name=""):
        for pkg in pkg_container.findall("package"):
            pkg_name = pkg.attrib.get("name", "") or ""
            pkg_path = pkg_to_path(pkg_name)

            for sf in pkg.findall("sourcefile"):
                sf_name = sf.attrib.get("name", "") or ""
                # 组合多级候选（从最具体到最粗略）
                cands = []
                if group_name and pkg_path:
                    cands.append(f"{group_name}/{pkg_path}/{sf_name}")
                if pkg_path:
                    cands.append(f"{pkg_path}/{sf_name}")
                cands.append(sf_name)  # 兜底：只有文件名
                results.append((cands, sf))

    # 1) group 下的 package
    for grp in root.findall("group"):
        gname = (grp.attrib.get("name", "") or "").strip()
        add_from_pkg_container(grp, group_name=gname)

    # 2) 根层级下的 package
    add_from_pkg_container(root, group_name="")

    return results

def _best_jacoco_sourcefile_for_method(root, method_file: str):
    """
    在所有 (候选相对路径列表, sourcefile) 中，找与 method.file 最匹配的那个：
    - 评分 = 能作为 method_file 的后缀匹配成功时的候选长度
    - 取评分最高者（最长后缀匹配）
    """
    target = _norm_path(method_file)
    best = None
    best_score = -1

    for cand_list, sf in _jacoco_collect_sourcefiles_with_paths(root):
        for cand in cand_list:
            c = _norm_path(cand)
            if target.endswith(c):
                score = len(c)
                if score > best_score:
                    best_score = score
                    best = sf
                # 命中越具体的候选，score 越大，越会覆盖之前较短的匹配

    return best, best_score

def _java_method_line_coverage(method, jacoco_xml_path: str):
    """
    改进版：
      - 先用 group/package/sourcefile 的最长后缀匹配来定位唯一的 <sourcefile>。
      - 再在 [start_line, end_line] 闭区间内统计：可执行行=report中出现的行；被覆盖行=ci>0。
    """
    tree = ET.parse(jacoco_xml_path)
    root = tree.getroot()

    start_ln = int(method.start_line)
    end_ln = int(method.end_line)

    sf_elem, score = _best_jacoco_sourcefile_for_method(root, method.file)
    if sf_elem is None or score < 0:
        return {
            "covered": 0,
            "executable": 0,
            "coverage": None,
            "note": "file not found in JaCoCo report (no path suffix matched)"
        }

    target_file_hits = {}  # nr -> covered(bool)
    for line in sf_elem.findall("line"):
        nr = int(line.attrib.get("nr", "-1"))
        if start_ln <= nr <= end_ln:
            ci = int(line.attrib.get("ci", "0"))
            target_file_hits[nr] = (ci > 0)

    executable_lines = len(target_file_hits)
    covered_lines = sum(1 for v in target_file_hits.values() if v)
    coverage = None if executable_lines == 0 else covered_lines / executable_lines

    return {
        "covered": covered_lines,
        "executable": executable_lines,
        "coverage": coverage,
        "note": None
    }


def _py_method_line_coverage(method: Method, cov_xml_path: str):
    """
    coverage.py (pytest-cov) XML 结构要点：
      - <packages><package>...<class filename="src/pkg/mod.py"><lines><line number="N" hits="H"/></lines>
      - 行被覆盖：hits > 0
    """
    tree = ET.parse(cov_xml_path)
    root = tree.getroot()

    start_ln = int(method.start_line)
    end_ln = int(method.end_line)

    target_file_hits = {}  # line_no -> (covered: bool)
    target_file_found = False

    # 遍历所有 <class> 的 filename；同样用 endswith 做鲁棒匹配
    for cls in root.iter("class"):
        filename = cls.attrib.get("filename") or cls.attrib.get("name") or ""
        if not filename:
            continue
        if not _match_filename(method.file, filename):
            continue

        target_file_found = True
        lines_tag = cls.find("lines")
        if lines_tag is None:
            continue

        for line in lines_tag.findall("line"):
            try:
                nr = int(line.attrib.get("number", "-1"))
            except ValueError:
                continue
            if nr < start_ln or nr > end_ln:
                continue

            hits = int(line.attrib.get("hits", "0"))
            covered = hits > 0
            target_file_hits[nr] = covered

    if not target_file_found:
        return {
            "covered": 0,
            "executable": 0,
            "coverage": None,
            "note": "file not found in coverage.py report"
        }

    executable_lines = len(target_file_hits)
    covered_lines = sum(1 for v in target_file_hits.values() if v)
    return {
        "covered": covered_lines,
        "executable": executable_lines,
        "coverage": _ratio(covered_lines, executable_lines),
        "note": None
    }

def compute_method_line_coverage(method: Method):
    """
    返回字典：
      {
        "covered": 被覆盖的行数（仅统计报告中出现的“可执行行”）,
        "executable": 可执行行数,
        "coverage": 覆盖率 (0~1) 或 None（没有可执行行/文件不在报告中）,
        "note": 额外说明（文件不在报告中等）
      }
    """
    lang = (method.repo.language or "").strip().lower()
    if lang == "java":
        path = "./target/site/jacoco/jacoco.xml"
        if not os.path.exists(path):
            return {"covered": 0, "executable": 0, "coverage": None, "note": f"report not found: {path}"}
        return _java_method_line_coverage(method, path)

    if lang == "python":
        path = "./coverage.xml"
        if not os.path.exists(path):
            return {"covered": 0, "executable": 0, "coverage": None, "note": f"report not found: {path}"}
        return _py_method_line_coverage(method, path)

    return {"covered": 0, "executable": 0, "coverage": None, "note": f"unsupported language: {lang}"}

