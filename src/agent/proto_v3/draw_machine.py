import json
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


# -----------------------------
# Pretty-printers for JSON AST
# -----------------------------
def _term_to_str(t: Dict[str, Any]) -> str:
    if "var" in t:
        return str(t["var"])
    if "int" in t:
        return str(t["int"])
    if "bool" in t:
        return "true" if bool(t["bool"]) else "false"
    # fallback
    return json.dumps(t, ensure_ascii=False)


def _expr_to_str(node: Dict[str, Any]) -> str:
    # atom: {"pred": {...}} or {"op": "...", "args": [...]}
    if "pred" in node:
        rel = node["pred"]["rel"]
        args = node["pred"].get("args", [])
        return f"{rel}({', '.join(_term_to_str(a) for a in args)})"
    if "op" not in node:
        return json.dumps(node, ensure_ascii=False)

    op = node["op"]
    args = node.get("args", [])

    # Unary
    if op == "Not":
        return f"not({_expr_to_str(args[0])})"

    # N-ary boolean
    if op in ("And", "Or"):
        sep = " and " if op == "And" else " or "
        return "(" + sep.join(_expr_to_str(a) for a in args) + ")"

    # Binary connectives
    if op == "Implies":
        return f"({_expr_to_str(args[0])} -> {_expr_to_str(args[1])})"

    # Comparisons
    if op in ("Eq", "Ne", "Lt", "Le", "Gt", "Ge"):
        sym = {"Eq": "==", "Ne": "!=", "Lt": "<", "Le": "<=", "Gt": ">", "Ge": ">="}[op]
        return f"({_expr_to_str(args[0])} {sym} {_expr_to_str(args[1])})"

    # Arithmetic
    if op in ("Add", "Sub", "Mul"):
        sym = {"Add": "+", "Sub": "-", "Mul": "*"}[op]
        return "(" + f" {sym} ".join(_expr_to_str(a) for a in args) + ")"

    # Ite (term-like)
    if op == "Ite":
        return f"(if {_expr_to_str(args[0])} then {_expr_to_str(args[1])} else {_expr_to_str(args[2])})"

    # fallback
    return f"{op}(" + ", ".join(_expr_to_str(a) for a in args) + ")"


def _collect_body_preds(rule_body: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    preds = []
    for a in rule_body:
        if isinstance(a, dict) and "pred" in a:
            preds.append(a["pred"])
    return preds


def _collect_body_constraints(rule_body: List[Dict[str, Any]]) -> List[str]:
    cons = []
    for a in rule_body:
        if isinstance(a, dict) and "pred" in a:
            continue
        if isinstance(a, dict):
            cons.append(_expr_to_str(a))
        else:
            cons.append(str(a))
    return cons


# -----------------------------
# Diagram layout + rendering
# -----------------------------
@dataclass
class NodeBox:
    name: str
    x: float
    y: float
    w: float
    h: float


@dataclass
class Edge:
    src: Optional[str]  # None means "entry"/no source relation
    dst: str
    rule_id: str
    rule_desc: str
    cond_text: str


def _wrap_text_lines(
    text: str,
    font_name: str,
    font_size: int,
    max_width: float,
) -> List[str]:
    # simple greedy wrap; keeps existing newlines as hard breaks
    lines_out: List[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines_out.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            test = cur + " " + w
            if stringWidth(test, font_name, font_size) <= max_width:
                cur = test
            else:
                lines_out.append(cur)
                cur = w
        lines_out.append(cur)
    return lines_out


def _draw_rounded_box(c: canvas.Canvas, x: float, y: float, w: float, h: float, r: float = 10):
    # reportlab has roundRect
    c.roundRect(x, y, w, h, r, stroke=1, fill=1)


def _draw_arrow(
    c: canvas.Canvas,
    x1: float, y1: float,
    x2: float, y2: float,
    arrow_len: float = 10,
    arrow_w: float = 5,
):
    # line
    c.line(x1, y1, x2, y2)

    # arrowhead
    ang = math.atan2(y2 - y1, x2 - x1)
    bx = x2 - arrow_len * math.cos(ang)
    by = y2 - arrow_len * math.sin(ang)
    lx = bx + arrow_w * math.cos(ang + math.pi / 2)
    ly = by + arrow_w * math.sin(ang + math.pi / 2)
    rx = bx + arrow_w * math.cos(ang - math.pi / 2)
    ry = by + arrow_w * math.sin(ang - math.pi / 2)

    c.saveState()
    c.setLineWidth(1)
    c.lines([(x2, y2, lx, ly), (x2, y2, rx, ry), (lx, ly, rx, ry)])
    c.restoreState()


def render_state_machine_pdf(
    json_content: Union[str, Dict[str, Any]],
    out_pdf_path: str,
    *,
    page_size=landscape(A4),
    title: str = "Horn-rule State Machine",
) -> None:
    """
    Render the Horn-rule state machine (relations + rules) into a single PDF.

    Layout strategy:
    - Nodes (relations) drawn in a graph area on the left.
    - Edges labeled only with rule IDs to avoid clutter.
    - A legend panel on the right lists each rule ID with its description + constraints.
    - If there are multiple edges between the same (src,dst), they are vertically offset.
    """
    spec = json.loads(json_content) if isinstance(json_content, str) else json_content

    relations = spec.get("relations", [])
    rules = spec.get("rules", [])

    # Determine which relations exist
    rel_names = [r["name"] for r in relations]
    has_loop = "Loop" in rel_names

    # Collect edges from rules (head rel + body pred rels)
    edges: List[Edge] = []
    for i, rule in enumerate(rules, start=1):
        head = rule.get("head", {})
        head_rel = head.get("rel")
        if not head_rel:
            continue

        rule_id = f"R{i}"
        rule_desc = rule.get("description", "").strip() or "(no description)"
        body = rule.get("body", []) or []

        preds = _collect_body_preds(body)
        src_rels = [p.get("rel") for p in preds if isinstance(p, dict) and p.get("rel") in rel_names]

        conds = _collect_body_constraints(body)
        cond_text = ""
        if conds:
            # join constraints compactly
            cond_text = " & ".join(conds)

        # We do NOT add "Bad" as a relation; but we do want to visualize it if rule head is Bad
        # Also allow src rel "Final" etc. if present as predicate atoms.
        if head_rel == "Bad":
            # Extract which relation(s) appear in body preds (often Final)
            srcs = [p.get("rel") for p in preds if isinstance(p, dict) and p.get("rel")]
            if not srcs:
                edges.append(Edge(src=None, dst="Bad", rule_id=rule_id, rule_desc=rule_desc, cond_text=cond_text))
            else:
                for s in srcs:
                    edges.append(Edge(src=s, dst="Bad", rule_id=rule_id, rule_desc=rule_desc, cond_text=cond_text))
            continue

        # Normal relation heads
        if not src_rels:
            edges.append(Edge(src=None, dst=head_rel, rule_id=rule_id, rule_desc=rule_desc, cond_text=cond_text))
        else:
            for s in src_rels:
                edges.append(Edge(src=s, dst=head_rel, rule_id=rule_id, rule_desc=rule_desc, cond_text=cond_text))

    # Prepare canvas
    W, H = page_size
    c = canvas.Canvas(out_pdf_path, pagesize=page_size)

    margin = 0.5 * inch
    gutter = 0.3 * inch

    # Split into graph + legend
    legend_w = W * 0.38
    graph_w = W - 2 * margin - gutter - legend_w
    graph_x0 = margin
    graph_y0 = margin
    graph_h = H - 2 * margin

    legend_x0 = graph_x0 + graph_w + gutter
    legend_y0 = margin
    legend_h = graph_h

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, H - margin + 0.05 * inch, title)

    # Node sizes
    node_w = min(2.2 * inch, graph_w / 3.0)
    node_h = 0.75 * inch
    y_center = graph_y0 + graph_h * 0.62

    # Place nodes
    nodes: Dict[str, NodeBox] = {}

    # Init, Loop (optional), Final on a row; Bad below Final (if referenced)
    x_positions = []
    if has_loop:
        x_positions = [
            graph_x0 + graph_w * 0.12,
            graph_x0 + graph_w * 0.48,
            graph_x0 + graph_w * 0.84,
        ]
        order = ["Init", "Loop", "Final"]
    else:
        x_positions = [
            graph_x0 + graph_w * 0.18,
            graph_x0 + graph_w * 0.80,
        ]
        order = ["Init", "Final"]

    for name, x in zip(order, x_positions):
        nodes[name] = NodeBox(name=name, x=x - node_w / 2, y=y_center - node_h / 2, w=node_w, h=node_h)

    # Decide if we need Bad node (if any edge dst is Bad)
    need_bad = any(e.dst == "Bad" or e.src == "Bad" for e in edges)
    if need_bad:
        final_box = nodes.get("Final")
        bx = (final_box.x + final_box.w / 2) if final_box else (graph_x0 + graph_w * 0.8)
        by = graph_y0 + graph_h * 0.22
        nodes["Bad"] = NodeBox(name="Bad", x=bx - node_w / 2, y=by - node_h / 2, w=node_w, h=node_h)

    # Draw nodes
    for name, box in nodes.items():
        c.saveState()
        if name == "Bad":
            c.setFillColorRGB(1.0, 0.92, 0.92)
            c.setStrokeColorRGB(0.8, 0.2, 0.2)
        else:
            c.setFillColorRGB(0.94, 0.95, 0.97)
            c.setStrokeColorRGB(0.2, 0.2, 0.2)

        _draw_rounded_box(c, box.x, box.y, box.w, box.h, r=12)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(box.x + box.w / 2, box.y + box.h / 2 + 4, name)
        c.restoreState()

    # Entry pseudo-node point
    entry_x = nodes["Init"].x - 0.6 * inch if "Init" in nodes else graph_x0 + 0.2 * inch
    entry_y = nodes["Init"].y + nodes["Init"].h / 2 if "Init" in nodes else y_center
    c.saveState()
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.circle(entry_x, entry_y, 3, stroke=0, fill=1)
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(entry_x - 10, entry_y - 16, "ENTRY")
    c.restoreState()

    # Group parallel edges for offsets
    pair_to_edges: Dict[Tuple[Optional[str], str], List[Edge]] = {}
    for e in edges:
        key = (e.src, e.dst)
        pair_to_edges.setdefault(key, []).append(e)

    # Draw edges (in graph area)
    c.setFont("Helvetica", 10)
    for (src, dst), es in pair_to_edges.items():
        for idx, e in enumerate(es):
            # compute endpoints
            if src is None:
                x1, y1 = entry_x, entry_y
                src_box = None
            else:
                src_box = nodes.get(src)
                if not src_box:
                    continue
                x1 = src_box.x + src_box.w
                y1 = src_box.y + src_box.h / 2

            dst_box = nodes.get(dst)
            if not dst_box:
                continue
            x2 = dst_box.x
            y2 = dst_box.y + dst_box.h / 2

            # offset for parallel edges
            offset = (idx - (len(es) - 1) / 2.0) * 18.0
            y1o = y1 + offset
            y2o = y2 + offset

            # keep within bounds a bit
            y1o = max(graph_y0 + 20, min(graph_y0 + graph_h - 20, y1o))
            y2o = max(graph_y0 + 20, min(graph_y0 + graph_h - 20, y2o))

            # styling
            c.saveState()
            if dst == "Bad" or src == "Bad":
                c.setStrokeColorRGB(0.8, 0.2, 0.2)
            else:
                c.setStrokeColorRGB(0.1, 0.1, 0.1)
            _draw_arrow(c, x1, y1o, x2, y2o)
            c.restoreState()

            # edge label: rule id only (avoid clutter)
            mx = (x1 + x2) / 2
            my = (y1o + y2o) / 2 + 6
            c.saveState()
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(mx - 10, my, e.rule_id)
            c.restoreState()

    # Legend panel
    c.saveState()
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.rect(legend_x0, legend_y0, legend_w, legend_h, stroke=1, fill=0)
    c.restoreState()

    legend_pad = 0.25 * inch
    x = legend_x0 + legend_pad
    y = legend_y0 + legend_h - legend_pad

    c.setFont("Helvetica-Bold", 13)
    c.drawString(x, y, "Rule Legend")
    y -= 0.25 * inch

    # Build rule legend entries in original order (R1..Rn)
    # Even if a rule produces multiple edges, list it once.
    rid_to_rule: Dict[str, Tuple[str, str]] = {}  # rid -> (desc, cond_text)
    for e in edges:
        if e.rule_id not in rid_to_rule:
            rid_to_rule[e.rule_id] = (e.rule_desc, e.cond_text)

    # Use the JSON rules order for legend ordering
    ordered_rids = [f"R{i}" for i in range(1, len(rules) + 1) if f"R{i}" in rid_to_rule]

    c.setFont("Helvetica", 10)
    line_h = 12
    max_text_w = legend_w - 2 * legend_pad

    def new_page():
        nonlocal y
        c.showPage()
        # re-draw title and legend frame on new page
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, H - margin + 0.05 * inch, title + " (cont.)")

        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.rect(legend_x0, legend_y0, legend_w, legend_h, stroke=1, fill=0)

        y = legend_y0 + legend_h - legend_pad
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x, y, "Rule Legend (cont.)")
        y -= 0.25 * inch
        c.setFont("Helvetica", 10)

    for rid in ordered_rids:
        desc, cond = rid_to_rule[rid]
        entry = f"{rid}: {desc}"
        if cond:
            entry += f"\n  if {cond}"

        lines = _wrap_text_lines(entry, "Helvetica", 10, max_text_w)

        # page break if needed
        if y - (len(lines) * line_h) < (legend_y0 + legend_pad):
            new_page()

        # draw
        c.setFont("Helvetica-Bold", 10)
        # first line: make rule id visually pop if possible
        if lines:
            # try to bold only the "Rk:" prefix on first line
            first = lines[0]
            c.drawString(x, y, first)
            y -= line_h

        c.setFont("Helvetica", 10)
        for ln in lines[1:]:
            c.drawString(x, y, ln)
            y -= line_h

        y -= 6  # extra spacing between entries

    c.save()


if __name__ == "__main__":
    sample = {
  "relations": [
    { "name": "Init", "args": [ { "name": "tokens_length", "sort": "Int" } ] },
    { "name": "Final", "args": [ 
      { "name": "tokens_length", "sort": "Int" }, 
      { "name": "result_is_none", "sort": "Bool" }, 
      { "name": "version_valid", "sort": "Bool" } 
    ] }
  ],
  "vars": [
    { "name": "tokens_length", "sort": "Int", "description": "length of tokens list after removing domain and protocol" },
    { "name": "result_is_none", "sort": "Bool", "description": "flag indicating if the return value is None" },
    { "name": "version_valid", "sort": "Bool", "description": "whether the third token is a valid integer (dataset version)" }
  ],
  "rules": [
    {
      "description": "entry assumptions: snapshot of tokens list after processing identifier",
      "head": { "rel": "Init", "args": [ { "var": "tokens_length" } ] },
      "body": []
    },
    {
      "description": "return None if tokens_length < 2",
      "head": { "rel": "Final", "args": [ { "var": "tokens_length" }, { "bool": True }, { "bool": False } ] },
      "body": [
        { "pred": { "rel": "Init", "args": [ { "var": "tokens_length" } ] } },
        { "op": "Le", "args": [ { "var": "tokens_length" }, { "int": 2 } ] }
      ]
    },
    {
      "description": "return None if tokens_length > 3",
      "head": { "rel": "Final", "args": [ { "var": "tokens_length" }, { "bool": True }, { "bool": False } ] },
      "body": [
        { "pred": { "rel": "Init", "args": [ { "var": "tokens_length" } ] } },
        { "op": "Gt", "args": [ { "var": "tokens_length" }, { "int": 3 } ] }
      ]
    },
    {
      "description": "return (workspace, project, None) if tokens_length == 2",
      "head": { "rel": "Final", "args": [ { "int": 2 }, { "bool": False }, { "bool": False } ] },
      "body": [
        { "pred": { "rel": "Init", "args": [ { "int": 2 } ] } }
      ]
    },
    {
      "description": "return (workspace, project, version) if tokens_length == 3 and version is valid",
      "head": { "rel": "Final", "args": [ { "int": 3 }, { "bool": False }, { "bool": True } ] },
      "body": [
        { "pred": { "rel": "Init", "args": [ { "int": 3 } ] } }
      ]
    },
    {
      "description": "return None if tokens_length == 3 and version is invalid",
      "head": { "rel": "Final", "args": [ { "int": 3 }, { "bool": True }, { "bool": False } ] },
      "body": [
        { "pred": { "rel": "Init", "args": [ { "int": 3 } ] } },
        { "op": "Not", "args": [ { "var": "version_valid" } ] }
      ]
    },
    {
      "description": "derive Bad when Final holds but postcondition is violated",
      "head": { "rel": "Bad", "args": [] },
      "body": [
        { "pred": { "rel": "Final", "args": [ { "var": "tokens_length" }, { "bool": False }, { "var": "version_valid" } ] }},
        {
          "op": "Or",
          "args": [
            {
              "op": "And",
              "args": [
                { "op": "Eq", "args": [ { "var": "tokens_length" }, { "int": 2 } ] },
                { "op": "Eq", "args": [ { "var": "version_valid" }, { "bool": True } ] }
              ]
            },
            {
              "op": "And",
              "args": [
                { "op": "Eq", "args": [ { "var": "tokens_length" }, { "int": 3 } ] },
                { "op": "Eq", "args": [ { "var": "version_valid" }, { "bool": False } ] }
              ]
            }
          ]
        }
      ]
    }
  ]
}
    render_state_machine_pdf(sample, "src/agent/proto_fix_v2/tools/demo.pdf", 
                             title="Example State Machine")
    print("Wrote")
