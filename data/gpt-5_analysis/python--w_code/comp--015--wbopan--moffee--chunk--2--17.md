https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/compositor.py#L115-L150
```
@icontract.ensure(lambda result: isinstance(result, Chunk))
@icontract.ensure(lambda result: (result.type == Type.NODE) == (result.paragraph is None))
@icontract.ensure(lambda result: (result.type == Type.PARAGRAPH) == (len(result.children) == 0))
@icontract.ensure(lambda result: result.type != Type.NODE or len(result.children) >= 2)
@icontract.ensure(lambda result: all(isinstance(c, Chunk) for c in result.children))
@icontract.ensure(lambda result: result.type != Type.PARAGRAPH or isinstance(result.paragraph, str))
@icontract.ensure(lambda result: result.type != Type.PARAGRAPH or result.direction == Direction.HORIZONTAL)
@icontract.ensure(lambda result: result.direction != Direction.VERTICAL or result.type == Type.NODE)
@icontract.ensure(lambda result: result.direction != Direction.VERTICAL or all(c.direction == Direction.HORIZONTAL for c in result.children))
@icontract.ensure(lambda result: not (result.type == Type.NODE and result.direction == Direction.HORIZONTAL) or all(c.type == Type.PARAGRAPH and c.paragraph is not None and len(c.children) == 0 for c in result.children))
@icontract.ensure(lambda result: result.direction != Direction.VERTICAL or all((c.type == Type.PARAGRAPH and c.paragraph is not None and len(c.children) == 0) or (c.type == Type.NODE and c.direction == Direction.HORIZONTAL and all(gc.type == Type.PARAGRAPH and gc.paragraph is not None and len(gc.children) == 0 for gc in c.children)) for c in result.children))
```
```
No direct verification.
```
passed
```
@icontract.ensure(lambda self, result: isinstance(result, Chunk))
@icontract.ensure(
    lambda self, result: all(
        (
            (node and node.type == Type.PARAGRAPH and (not node.children))
            or (
                node.type == Type.NODE
                and node.children is not None
                and len(node.children) > 0
                and all(isinstance(ch, Chunk) for ch in node.children)
            )
        )
        for node in (
            [result]
            + (result.children or [])
            + [
                gc
                for child in (result.children or [])
                if child and child.children is not None and len(child.children) > 0
                for gc in ((child and child.children) or [])
            ]
        )
    )
)
@icontract.ensure(
    lambda self, result: (
        sum(
            1
            for i, line in enumerate(self.raw_md.splitlines())
            if is_divider(line, "=")
            and (
                sum(
                    1
                    for j, l in enumerate(self.raw_md.splitlines())
                    if j <= i and l.strip().startswith("```")
                )
                % 2
                == 0
            )
        )
        > 0
        or
        sum(
            1
            for i, line in enumerate(self.raw_md.splitlines())
            if is_divider(line, "<")
            and (
                sum(
                    1
                    for j, l in enumerate(self.raw_md.splitlines())
                    if j <= i and l.strip().startswith("```")
                )
                % 2
                == 0
            )
        )
        > 0
    )
    or (
        result.type == Type.PARAGRAPH
        and (result.children is None or len(result.children) == 0)
        and (result.paragraph is not None)
        and self.raw_md.strip() == result.paragraph.strip()
    )
)
@icontract.ensure(
    lambda self, result: (
        sum(
            1
            for i, line in enumerate(self.raw_md.splitlines())
            if is_divider(line, "=")
            and (
                sum(
                    1
                    for j, l in enumerate(self.raw_md.splitlines())
                    if j <= i and l.strip().startswith("```")
                )
                % 2
                == 0
            )
        )
        == 0
    )
    or (
        result.type == Type.NODE
        and result.direction == Direction.VERTICAL
        and result.children is not None
        and len(result.children)
        == (
            sum(
                1
                for i, line in enumerate(self.raw_md.splitlines())
                if is_divider(line, "=")
                and (
                    sum(
                        1
                        for j, l in enumerate(self.raw_md.splitlines())
                        if j <= i and l.strip().startswith("```")
                    )
                    % 2
                    == 0
                )
            )
            + 1
        )
    )
)
@icontract.ensure(
    lambda self, result: (
        not (
            result.type == Type.NODE
            and
            sum(
                1
                for i, line in enumerate(self.raw_md.splitlines())
                if is_divider(line, "=")
                and (
                    sum(
                        1
                        for j, l in enumerate(self.raw_md.splitlines())
                        if j <= i and l.strip().startswith("```")
                    )
                    % 2
                    == 0
                )
            )
            == 0
            and
            sum(
                1
                for i, line in enumerate(self.raw_md.splitlines())
                if is_divider(line, "<")
                and (
                    sum(
                        1
                        for j, l in enumerate(self.raw_md.splitlines())
                        if j <= i and l.strip().startswith("```")
                    )
                    % 2
                    == 0
                )
            )
            > 0
        )
    )
    or (
        result.direction == Direction.HORIZONTAL
        and result.children is not None
        and len(result.children)
        == (
            sum(
                1
                for i, line in enumerate(self.raw_md.splitlines())
                if is_divider(line, "<")
                and (
                    sum(
                        1
                        for j, l in enumerate(self.raw_md.splitlines())
                        if j <= i and l.strip().startswith("```")
                    )
                    % 2
                    == 0
                )
            )
            + 1
        )
        and all(child.type == Type.PARAGRAPH for child in result.children)
    )
)
@icontract.ensure(
    lambda self, result: all(
        sum(
            1
            for i, line in enumerate((leaf.paragraph or "").splitlines())
            if is_divider(line, "<")
            and (
                sum(
                    1
                    for j, l in enumerate((leaf.paragraph or "").splitlines())
                    if j <= i and l.strip().startswith("```")
                )
                % 2
                == 0
            )
        )
        == 0
        for leaf in [
            node
            for node in (
                [result]
                + (result.children or [])
                + [
                    gc
                    for child in (result.children or [])
                    if child and child.children is not None and len(child.children) > 0
                    for gc in ((child and child.children) or [])
                ]
            )
            if node and node.type == Type.PARAGRAPH
            and (node.children is None or len(node.children) == 0)
        ]
    )
)

```
===== 17 =====
failed
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(line, None) and not current_escaped:
                     strs.append("\n")
                 else:
                     strs[-1] += line + "\n"
@@ -33,4 +33,4 @@         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
```
    @property
    def chunk(self) -> Chunk:
        """
        Split raw_md into chunk tree
        Chunk tree branches when in-page divider is met.
        - adjacent "<->"s create chunk with horizontal direction
        - adjacent "===" create chunk with vertical direction
        "===" possesses higher priority than "<->"

        :return: Root of the chunk tree
        """

        def split_by_div(text, type) -> List[Chunk]:
            strs = [""]
            current_escaped = False
            for line in text.split("\n"):
                if line.strip().startswith("```"):
                    current_escaped = not current_escaped
                if is_divider(line, None) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, "=")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
