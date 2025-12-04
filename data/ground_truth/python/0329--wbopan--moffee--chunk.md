https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/compositor.py#L115-L150
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
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74]
===== 0 =====
```
         """
 
         def split_by_div(text, type) -> List[Chunk]:
-            strs = [""]
+            strs = ["XXXX"]
             current_escaped = False
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
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
            strs = ["XXXX"]
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 1 =====
```
 
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
-            current_escaped = False
+            current_escaped = True
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
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
            current_escaped = True
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 2 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.split(" "):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.split(" "):
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 3 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.split("XX\nXX"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.split("XX\nXX"):
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 4 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.split("\n\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.split("\n\n"):
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 5 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.split("\r\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.split("\r\n"):
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 6 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.split(None):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.split(None):
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 7 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.splitlines()[1:]:
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.splitlines()[1:]:
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 8 =====
```
         def split_by_div(text, type) -> List[Chunk]:
             strs = [""]
             current_escaped = False
-            for line in text.split("\n"):
+            for line in text.splitlines(keepends=True):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
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
            for line in text.splitlines(keepends=True):
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 9 =====
```
             strs = [""]
             current_escaped = False
             for line in text.split("\n"):
-                if line.strip().startswith("```"):
+                if line.strip() == "":  # This checks for empty lines, which is irrelevant for code block detection
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
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
                if line.strip() == "":  # This checks for empty lines, which is irrelevant for code block detection
                    current_escaped = not current_escaped
                if is_divider(line, type) and not current_escaped:
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
===== 10 =====
```
             strs = [""]
             current_escaped = False
             for line in text.split("\n"):
-                if line.strip().startswith("```"):
+                if line.strip().endswith("```"):  # This incorrectly checks for closing code blocks only
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
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
                if line.strip().endswith("```"):  # This incorrectly checks for closing code blocks only
                    current_escaped = not current_escaped
                if is_divider(line, type) and not current_escaped:
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
===== 11 =====
```
             strs = [""]
             current_escaped = False
             for line in text.split("\n"):
-                if line.strip().startswith("```"):
+                if line.strip().startswith("#"):  # This checks for header lines instead of code blocks
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
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
                if line.strip().startswith("#"):  # This checks for header lines instead of code blocks
                    current_escaped = not current_escaped
                if is_divider(line, type) and not current_escaped:
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
===== 12 =====
```
             strs = [""]
             current_escaped = False
             for line in text.split("\n"):
-                if line.strip().startswith("```"):
+                if line.strip().startswith("<!--"):  # This checks for HTML comments instead of code blocks
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
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
                if line.strip().startswith("<!--"):  # This checks for HTML comments instead of code blocks
                    current_escaped = not current_escaped
                if is_divider(line, type) and not current_escaped:
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
===== 13 =====
```
             strs = [""]
             current_escaped = False
             for line in text.split("\n"):
-                if line.strip().startswith("```"):
+                if line.strip().startswith("XX```XX"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
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
                if line.strip().startswith("XX```XX"):
                    current_escaped = not current_escaped
                if is_divider(line, type) and not current_escaped:
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
===== 14 =====
```
             current_escaped = False
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
-                    current_escaped = not current_escaped
+                    current_escaped = None
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
                 else:
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
                    current_escaped = None
                if is_divider(line, type) and not current_escaped:
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
===== 15 =====
```
             current_escaped = False
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
-                    current_escaped = not current_escaped
+                    current_escaped = current_escaped
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
                 else:
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
                    current_escaped = current_escaped
                if is_divider(line, type) and not current_escaped:
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
===== 16 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(line, ) and not current_escaped:
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
                if is_divider(line, ) and not current_escaped:
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
===== 17 =====
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
===== 18 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(line, type) and current_escaped:
                     strs.append("\n")
                 else:
                     strs[-1] += line + "\n"
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
                if is_divider(line, type) and current_escaped:
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
===== 19 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(line, type) and current_escaped:
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
                if is_divider(line, type) and current_escaped:
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
===== 20 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(line, type) or current_escaped:
                     strs.append("\n")
                 else:
                     strs[-1] += line + "\n"
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
                if is_divider(line, type) or current_escaped:
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
===== 21 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(line, type) or not current_escaped:
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
                if is_divider(line, type) or not current_escaped:
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
===== 22 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if is_divider(type) and not current_escaped:
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
                if is_divider(type) and not current_escaped:
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
===== 23 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if not is_divider(line, type) and not current_escaped:
                     strs.append("\n")
                 else:
                     strs[-1] += line + "\n"
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
                if not is_divider(line, type) and not current_escaped:
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
===== 24 =====
```
             for line in text.split("\n"):
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
-                if is_divider(line, type) and not current_escaped:
+                if not is_divider(line, type) or current_escaped:
                     strs.append("\n")
                 else:
                     strs[-1] += line + "\n"
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
                if not is_divider(line, type) or current_escaped:
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
===== 25 =====
```
                 if line.strip().startswith("```"):
                     current_escaped = not current_escaped
                 if is_divider(line, type) and not current_escaped:
-                    strs.append("\n")
+                    strs[-1] += "\n"  # Appends a newline to the last string, which may lead to incorrect chunking.
                 else:
                     strs[-1] += line + "\n"
             return [Chunk(paragraph=s) for s in strs]
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
                    strs[-1] += "\n"  # Appends a newline to the last string, which may lead to incorrect chunking.
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
===== 26 =====
```
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
                 else:
-                    strs[-1] += line + "\n"
+                    strs[-1] += line + "XX\nXX"
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "XX\nXX"
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
===== 27 =====
```
                 if is_divider(line, type) and not current_escaped:
                     strs.append("\n")
                 else:
-                    strs[-1] += line + "\n"
+                    strs[-1] = line + "\n"
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] = line + "\n"
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
===== 28 =====
```
                     strs.append("\n")
                 else:
                     strs[-1] += line + "\n"
-            return [Chunk(paragraph=s) for s in strs]
+            return [Chunk(paragraph=s, type=Type.NODE) for s in strs]  # Sets all chunks to type NODE, which may not be appropriate.
 
         # collect "==="
         vchunks = split_by_div(self.raw_md, "=")
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
            return [Chunk(paragraph=s, type=Type.NODE) for s in strs]  # Sets all chunks to type NODE, which may not be appropriate.

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
===== 29 =====
```
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
-        vchunks = split_by_div(self.raw_md, "=")
+        vchunks = split_by_div(self.raw_md, " ")  # Using a space as a divider, which will not split correctly
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
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
        vchunks = split_by_div(self.raw_md, " ")  # Using a space as a divider, which will not split correctly
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 30 =====
```
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
-        vchunks = split_by_div(self.raw_md, "=")
+        vchunks = split_by_div(self.raw_md, "+++")  # Using an invalid divider type
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
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
        vchunks = split_by_div(self.raw_md, "+++")  # Using an invalid divider type
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 31 =====
```
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
-        vchunks = split_by_div(self.raw_md, "=")
+        vchunks = split_by_div(self.raw_md, "<->")
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
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
        vchunks = split_by_div(self.raw_md, "<->")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 32 =====
```
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
-        vchunks = split_by_div(self.raw_md, "=")
+        vchunks = split_by_div(self.raw_md, "===")
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
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
        vchunks = split_by_div(self.raw_md, "===")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 33 =====
```
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
-        vchunks = split_by_div(self.raw_md, "=")
+        vchunks = split_by_div(self.raw_md, "XX=XX")
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, "XX=XX")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 34 =====
```
             return [Chunk(paragraph=s) for s in strs]
 
         # collect "==="
-        vchunks = split_by_div(self.raw_md, "=")
+        vchunks = split_by_div(self.raw_md, None)
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, None)
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 35 =====
```
         # collect "==="
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
-        for i in range(len(vchunks)):
+        for i in range(0, len(vchunks), 2):  # Skips every other chunk, leading to incomplete processing
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
        for i in range(0, len(vchunks), 2):  # Skips every other chunk, leading to incomplete processing
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 36 =====
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
===== 37 =====
```
         # collect "==="
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
-        for i in range(len(vchunks)):
+        for i in range(len(vchunks) - 1):  # Off-by-one error, skips the last chunk
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
        for i in range(len(vchunks) - 1):  # Off-by-one error, skips the last chunk
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 38 =====
```
         # collect "==="
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
-        for i in range(len(vchunks)):
+        for i in range(len(vchunks) // 2):  # Only iterates over half of the chunks
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
        for i in range(len(vchunks) // 2):  # Only iterates over half of the chunks
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 39 =====
```
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
         for i in range(len(vchunks)):
-            hchunks = split_by_div(vchunks[i].paragraph, "<")
+            hchunks = split_by_div(vchunks[i].paragraph, " ")
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, " ")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 40 =====
```
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
         for i in range(len(vchunks)):
-            hchunks = split_by_div(vchunks[i].paragraph, "<")
+            hchunks = split_by_div(vchunks[i].paragraph, "+++")
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "+++")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 41 =====
```
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
         for i in range(len(vchunks)):
-            hchunks = split_by_div(vchunks[i].paragraph, "<")
+            hchunks = split_by_div(vchunks[i].paragraph, "<->")
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<->")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 42 =====
```
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
         for i in range(len(vchunks)):
-            hchunks = split_by_div(vchunks[i].paragraph, "<")
+            hchunks = split_by_div(vchunks[i].paragraph, "=")
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "=")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 43 =====
```
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
         for i in range(len(vchunks)):
-            hchunks = split_by_div(vchunks[i].paragraph, "<")
+            hchunks = split_by_div(vchunks[i].paragraph, "===")
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "===")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 44 =====
```
         vchunks = split_by_div(self.raw_md, "=")
         # split by "<->" if possible
         for i in range(len(vchunks)):
-            hchunks = split_by_div(vchunks[i].paragraph, "<")
+            hchunks = split_by_div(vchunks[i].paragraph, "XX<XX")
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, "=")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "XX<XX")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 45 =====
```
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
-            if len(hchunks) > 1:  # found <->
+            if len(hchunks) < 1:  # checks for no chunks, which is always false
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) < 1:  # checks for no chunks, which is always false
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 46 =====
```
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
-            if len(hchunks) > 1:  # found <->
+            if len(hchunks) == 1:  # incorrectly checks for a single chunk
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) == 1:  # incorrectly checks for a single chunk
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 47 =====
```
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
-            if len(hchunks) > 1:  # found <->
+            if len(hchunks) == 2:  # only processes when exactly two chunks are found
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) == 2:  # only processes when exactly two chunks are found
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 48 =====
```
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
-            if len(hchunks) > 1:  # found <->
+            if len(hchunks) > 0:  # processes even when there's only one chunk
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 0:  # processes even when there's only one chunk
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 49 =====
```
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
-            if len(hchunks) > 1:  # found <->
+            if len(hchunks) >= 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
                    strs.append("\n")
                else:
                    strs[-1] += line + "\n"
            return [Chunk(paragraph=s) for s in strs]

        # collect "==="
        vchunks = split_by_div(self.raw_md, "=")
        # split by "<->" if possible
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) >= 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 50 =====
```
         # split by "<->" if possible
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
-            if len(hchunks) > 1:  # found <->
+            if len(hchunks) >= 1:  # incorrectly allows any number of chunks
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
         if len(vchunks) == 1:
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) >= 1:  # incorrectly allows any number of chunks
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 51 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = Chunk(children=None, type=Type.NODE)
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
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
                vchunks[i] = Chunk(children=None, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 52 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = Chunk(children=hchunks, )
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
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
                vchunks[i] = Chunk(children=hchunks, )

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 53 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = Chunk(children=hchunks, direction=Direction.HORIZONTAL, type=Type.PARAGRAPH)
 
         if len(vchunks) == 1:
             return vchunks[0]
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, direction=Direction.HORIZONTAL, type=Type.PARAGRAPH)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 54 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = Chunk(children=hchunks, direction=Direction.VERTICAL, type=Type.NODE)
 
         if len(vchunks) == 1:
             return vchunks[0]
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, direction=Direction.VERTICAL, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 55 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = Chunk(children=hchunks, type=None)
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
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
                vchunks[i] = Chunk(children=hchunks, type=None)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 56 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = Chunk(type=Type.NODE)
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
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
                vchunks[i] = Chunk(type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 57 =====
```
         for i in range(len(vchunks)):
             hchunks = split_by_div(vchunks[i].paragraph, "<")
             if len(hchunks) > 1:  # found <->
-                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
+                vchunks[i] = None
 
         if len(vchunks) == 1:
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
                if is_divider(line, type) and not current_escaped:
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
                vchunks[i] = None

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 58 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) != 1:
             return vchunks[0]
 
         return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) != 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 59 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) != 1:
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
                if is_divider(line, type) and not current_escaped:
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

        if len(vchunks) != 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 60 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) < 1:
             return vchunks[0]
 
         return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) < 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 61 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) == 0:
             return vchunks[0]
 
         return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 0:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 62 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) == 2:
             return vchunks[0]
 
         return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 2:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 63 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) == 2:
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
                if is_divider(line, type) and not current_escaped:
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

        if len(vchunks) == 2:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 64 =====
```
             if len(hchunks) > 1:  # found <->
                 vchunks[i] = Chunk(children=hchunks, type=Type.NODE)
 
-        if len(vchunks) == 1:
+        if len(vchunks) > 1:
             return vchunks[0]
 
         return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) > 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)
```
===== 65 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=None, direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=None, direction=Direction.VERTICAL, type=Type.NODE)

```
===== 66 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=[], direction=Direction.VERTICAL, type=Type.NODE)  # Returns an empty chunk, losing all content
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=[], direction=Direction.VERTICAL, type=Type.NODE)  # Returns an empty chunk, losing all content
```
===== 67 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, direction=Direction.HORIZONTAL, type=Type.NODE)  # Incorrect direction
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.HORIZONTAL, type=Type.NODE)  # Incorrect direction
```
===== 68 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, direction=Direction.VERTICAL, )
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, )

```
===== 69 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=None)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=None)

```
===== 70 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.PARAGRAPH)  # Incorrect type
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.PARAGRAPH)  # Incorrect type
```
===== 71 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, direction=None, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, direction=None, type=Type.NODE)

```
===== 72 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks, type=Type.NODE)

```
===== 73 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(children=vchunks[:1], direction=Direction.VERTICAL, type=Type.NODE)  # Only returns the first chunk, losing data
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(children=vchunks[:1], direction=Direction.VERTICAL, type=Type.NODE)  # Only returns the first chunk, losing data
```
===== 74 =====
```
         if len(vchunks) == 1:
             return vchunks[0]
 
-        return Chunk(children=vchunks, direction=Direction.VERTICAL, type=Type.NODE)+        return Chunk(direction=Direction.VERTICAL, type=Type.NODE)
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
        for i in range(len(vchunks)):
            hchunks = split_by_div(vchunks[i].paragraph, "<")
            if len(hchunks) > 1:  # found <->
                vchunks[i] = Chunk(children=hchunks, type=Type.NODE)

        if len(vchunks) == 1:
            return vchunks[0]

        return Chunk(direction=Direction.VERTICAL, type=Type.NODE)

```
