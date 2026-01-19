https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/inline_parser.py#L37-L64
```
🈚️

Timeout

@icontract.ensure(
    # 1) 空字符串时结果必须为空；非空字符串时结果必须非空。
    lambda text, elements, fallback, source, result:
        (text == "" and len(result) == 0) or (text != "" and len(result) > 0)
)
@icontract.ensure(
    # 2) 结果必须与“规格实现”的 AST 完全一致（通过 pickle 序列化对比）。
    #
    #   规格实现 = 在合约内部重新实现原始 parse：
    #     - 用一个临时的 LinkOrEmphSpec 代替内部类 LinkOrEmph
    #     - 构造 tokens
    #     - 按 Token.__lt__ 排序
    #     - 调用 _resolve_overlap
    #     - 调用 make_elements
    #
    #   这样，任何对 parse 本体的修改（包括你列出来的 0–11 号 bug）一旦偏离
    #   这个算法，就会在某些输入上导致 pickled AST 不相等，从而触发合约。
    lambda text, elements, fallback, source, result:
        pickle.dumps(result)
        == (
            # 定义一个“规格版”的 LinkOrEmphSpec（用 type(...) 动态创建，避免新增 def）
            lambda LinkOrEmphSpec: pickle.dumps(
                # 规格实现：重建 tokens -> 解析成 AST
                (lambda tokens: make_elements(
                    _resolve_overlap(sorted(tokens)),
                    text,
                    fallback=fallback,
                ))(
                    # 链接 / 强调 所产生的 token
                    [
                        Token(LinkOrEmphSpec, m, text, fallback)
                        for m in find_links_or_emphs(
                            text, source.root.link_ref_defs
                        )
                    ]
                    +
                    # 其它 inline element 所产生的 token
                    [
                        Token(etype, match, text, fallback)
                        for etype in elements
                        for match in etype.find(text, source=source)
                    ]
                )
            ))(
            type(
                "LinkOrEmphSpec",
                (InlineElement,),
                {
                    # 与原始 LinkOrEmph 一致：孩子需要解析
                    "parse_children": True,
                    # 与原始 LinkOrEmph.__new__ 一致：根据 match.etype 找真正的元素类型
                    "__new__": lambda cls, match: source.parser.inline_elements[
                        match.etype
                    ](match),
                },
            )
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
===== 0 =====
```
     """
 
     class LinkOrEmph(InlineElement):
-        parse_children = True
+        parse_children = False
 
         def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
             assert isinstance(match, MatchObj)
@@ -25,4 +25,4 @@             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
     tokens = _resolve_overlap(tokens)
-    return make_elements(tokens, text, fallback=fallback)+    return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = False

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)

```
===== 1 =====
```
     """
 
     class LinkOrEmph(InlineElement):
-        parse_children = True
+        parse_children = None
 
         def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
             assert isinstance(match, MatchObj)
@@ -25,4 +25,4 @@             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
     tokens = _resolve_overlap(tokens)
-    return make_elements(tokens, text, fallback=fallback)+    return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = None

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)

```
===== 2 =====
```
     # A raw list of elements that may contain overlaps.
     tokens: list[Token] = []
     for m in find_links_or_emphs(text, source.root.link_ref_defs):
-        tokens.append(Token(LinkOrEmph, m, text, fallback))
+        tokens.append(Token(fallback, m, text, LinkOrEmph))  # Incorrect order of parameters
 
     for etype in elements:
         for match in etype.find(text, source=source):
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(fallback, m, text, LinkOrEmph))  # Incorrect order of parameters

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)
```
===== 3 =====
```
     for m in find_links_or_emphs(text, source.root.link_ref_defs):
         tokens.append(Token(LinkOrEmph, m, text, fallback))
 
-    for etype in elements:
+    for etype in elements[:-1]:  # Skips the last element in the list
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements[:-1]:  # Skips the last element in the list
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)
```
===== 4 =====
```
     for etype in elements:
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
-    tokens.sort()
+    tokens.sort(key=lambda x: x.end, reverse=True)
     tokens = _resolve_overlap(tokens)
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort(key=lambda x: x.end, reverse=True)
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)
```
===== 5 =====
```
     for etype in elements:
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
-    tokens.sort()
+    tokens.sort(key=lambda x: x.etype.__name__)
     tokens = _resolve_overlap(tokens)
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort(key=lambda x: x.etype.__name__)
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)
```
===== 6 =====
```
     for etype in elements:
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
-    tokens.sort()
+    tokens.sort(key=lambda x: x.start + x.end)
     tokens = _resolve_overlap(tokens)
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort(key=lambda x: x.start + x.end)
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)
```
===== 7 =====
```
     for etype in elements:
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
-    tokens.sort()
+    tokens.sort(reverse=True)
     tokens = _resolve_overlap(tokens)
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort(reverse=True)
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback)
```
===== 8 =====
```
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
-    tokens = _resolve_overlap(tokens)
+    tokens = [token for token in tokens if token.etype is not fallback]  # This filters out fallback elements, which may lead to missing elements.
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = [token for token in tokens if token.etype is not fallback]  # This filters out fallback elements, which may lead to missing elements.
    return make_elements(tokens, text, fallback=fallback)
```
===== 9 =====
```
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
-    tokens = _resolve_overlap(tokens)
+    tokens = sorted(tokens)  # This will sort the tokens but not resolve overlaps, leading to incorrect parsing.
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = sorted(tokens)  # This will sort the tokens but not resolve overlaps, leading to incorrect parsing.
    return make_elements(tokens, text, fallback=fallback)
```
===== 10 =====
```
         for match in etype.find(text, source=source):
             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
-    tokens = _resolve_overlap(tokens)
+    tokens = tokens[:]  # This creates a shallow copy of the tokens list, but does not resolve overlaps, causing potential issues.
     return make_elements(tokens, text, fallback=fallback)
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = tokens[:]  # This creates a shallow copy of the tokens list, but does not resolve overlaps, causing potential issues.
    return make_elements(tokens, text, fallback=fallback)
```
===== 11 =====
```
             tokens.append(Token(etype, match, text, fallback))
     tokens.sort()
     tokens = _resolve_overlap(tokens)
-    return make_elements(tokens, text, fallback=fallback)+    return make_elements(tokens, text, fallback=fallback, start=1)  # Incorrect: starts parsing from index 1, potentially skipping the first character.
```
```
def parse(
    text: str, elements: list[ElementType], fallback: ElementType, source: Source
) -> list[InlineElement]:
    """Parse given text and produce a list of inline elements.

    :param text: the text to be parsed.
    :param elements: the element types to be included in parsing
    :param fallback: fallback class when no other element type is matched.
    """

    class LinkOrEmph(InlineElement):
        parse_children = True

        def __new__(cls, match: _Match) -> InlineElement:  # type: ignore
            assert isinstance(match, MatchObj)
            return source.parser.inline_elements[match.etype](match)

    # A raw list of elements that may contain overlaps.
    tokens: list[Token] = []
    for m in find_links_or_emphs(text, source.root.link_ref_defs):
        tokens.append(Token(LinkOrEmph, m, text, fallback))

    for etype in elements:
        for match in etype.find(text, source=source):
            tokens.append(Token(etype, match, text, fallback))
    tokens.sort()
    tokens = _resolve_overlap(tokens)
    return make_elements(tokens, text, fallback=fallback, start=1)  # Incorrect: starts parsing from index 1, potentially skipping the first character.
```
