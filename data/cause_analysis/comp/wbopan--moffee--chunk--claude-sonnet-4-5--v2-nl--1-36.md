https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/compositor.py#L115-L150
```
@icontract.ensure(lambda self, result: result is not None, "Result must not be None")
@icontract.ensure(lambda self, result: isinstance(result, Chunk), "Result must be a Chunk instance")
@icontract.ensure(lambda self, result: result.direction in [Direction.HORIZONTAL, Direction.VERTICAL], "Direction must be valid")
@icontract.ensure(lambda self, result: result.type in [Type.PARAGRAPH, Type.NODE], "Type must be valid")
@icontract.ensure(lambda self, result: result.alignment in [Alignment.LEFT, Alignment.CENTER, Alignment.RIGHT, Alignment.JUSTIFY], "Alignment must be valid")
@icontract.ensure(lambda self, result: isinstance(result.children, list), "Children must be a list")
@icontract.ensure(lambda self, result: all(isinstance(child, Chunk) for child in result.children), "All children must be Chunk instances")
@icontract.ensure(lambda self, result: not result.children or result.type == Type.NODE, "If chunk has children, it must be of type NODE")
@icontract.ensure(lambda self, result: result.children or result.paragraph is not None or result.type == Type.NODE, "Leaf chunks should have paragraph content or be NODE type")
```
```
return value - inner repository type


return value content

repository defined type
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
===== 36: failed =====
```
         # collect "==="
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
-        for i in range(len(vchunks)):
+        for i in range(1, len(vchunks)):  # Starts from 1, missing the first chunk
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, "=")
        # split by "<->" if possible
        for i in range(1, len(vchunks)):  # Starts from 1, missing the first chunk
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
