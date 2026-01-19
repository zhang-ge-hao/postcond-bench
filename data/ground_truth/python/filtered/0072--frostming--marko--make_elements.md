https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/inline_parser.py#L85-L112
```
🈚️

Timeout

@icontract.ensure(
    lambda result, tokens, text, start, end, fallback:
        (lambda end_:
            (lambda holes, fallback_children:
                # 1. 所有元素都是 InlineElement
                all(isinstance(el, InlineElement) for el in result)
                # 2. 元素总数 = token 数 + 洞数（洞 => fallback 元素）
                and len(result) == len(tokens) + len(holes)
                # 3. 每个 fallback.children == 对应洞的子串
                and fallback_children == [text[s:e] for (s, e) in holes]
            )(
                # holes: 所有 [s, e) 洞区间
                [
                    (s, e)
                    for (s, e) in zip(
                        [start] + [tok.end for tok in tokens],
                        [tok.start for tok in tokens] + [end_],
                    )
                    if s < e
                ],
                # fallback_children: result 中所有 fallback 的 children
                [el.children for el in result if isinstance(el, fallback)]
            )
        )(
            len(text) if end is None else end
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
===== 0 =====
```
     :returns: a list of inline elements.
     """
     result: list[InlineElement] = []
-    end = end or len(text)
+    end = end if end is not None else 0
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end if end is not None else 0
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 1 =====
```
     :returns: a list of inline elements.
     """
     result: list[InlineElement] = []
-    end = end or len(text)
+    end = end or 0
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or 0
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 2 =====
```
     result: list[InlineElement] = []
     end = end or len(text)
     prev_end = start
-    for token in tokens:
+    for token in reversed(tokens):  # This will process tokens in reverse order, which may lead to incorrect element creation.
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in reversed(tokens):  # This will process tokens in reverse order, which may lead to incorrect element creation.
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 3 =====
```
     result: list[InlineElement] = []
     end = end or len(text)
     prev_end = start
-    for token in tokens:
+    for token in tokens[1:]:  # This will skip the first token, potentially missing elements.
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens[1:]:  # This will skip the first token, potentially missing elements.
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 4 =====
```
     result: list[InlineElement] = []
     end = end or len(text)
     prev_end = start
-    for token in tokens:
+    for token in tokens[:-1]:  # This will skip the last token, potentially missing elements.
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens[:-1]:  # This will skip the last token, potentially missing elements.
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 5 =====
```
     end = end or len(text)
     prev_end = start
     for token in tokens:
-        if prev_end < token.start:
+        if prev_end == token.start:  # This will only add fallback elements when there is no gap.
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end == token.start:  # This will only add fallback elements when there is no gap.
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 6 =====
```
     end = end or len(text)
     prev_end = start
     for token in tokens:
-        if prev_end < token.start:
+        if prev_end > token.start:  # This will skip adding the fallback for valid gaps.
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end > token.start:  # This will skip adding the fallback for valid gaps.
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 7 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(None)  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
         result.append(fallback(text[prev_end:end]))  # type: ignore
-    return result+    return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(None)  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result

```
===== 8 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(fallback(None))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
         result.append(fallback(text[prev_end:end]))  # type: ignore
-    return result+    return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(None))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result

```
===== 9 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(fallback(text[prev_end : token.start + 1]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start + 1]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 10 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(fallback(text[prev_end : token.start].replace(" ", "_")))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start].replace(" ", "_")))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 11 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(fallback(text[prev_end : token.start].strip()))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start].strip()))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 12 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(fallback(text[prev_end : token.start].upper()))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start].upper()))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 13 =====
```
     prev_end = start
     for token in tokens:
         if prev_end < token.start:
-            result.append(fallback(text[prev_end : token.start]))  # type: ignore
+            result.append(fallback(text[prev_end : token.start][::-1]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start][::-1]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 14 =====
```
     for token in tokens:
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
-        result.append(token.as_element())
+        result.append(None)
         prev_end = token.end
     if prev_end < end:
         result.append(fallback(text[prev_end:end]))  # type: ignore
-    return result+    return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(None)
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result

```
===== 15 =====
```
     for token in tokens:
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
-        result.append(token.as_element())
+        result.append(fallback(text[prev_end : token.end]))  # Incorrectly appending fallback instead of the element
         prev_end = token.end
     if prev_end < end:
         result.append(fallback(text[prev_end:end]))  # type: ignore
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(fallback(text[prev_end : token.end]))  # Incorrectly appending fallback instead of the element
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 16 =====
```
     for token in tokens:
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
-        result.append(token.as_element())
+        result.append(token)  # Incorrectly appending the token itself instead of the element
         prev_end = token.end
     if prev_end < end:
         result.append(fallback(text[prev_end:end]))  # type: ignore
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token)  # Incorrectly appending the token itself instead of the element
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 17 =====
```
     for token in tokens:
         if prev_end < token.start:
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
-        result.append(token.as_element())
+        result.append(token.as_element()) if token.start % 2 == 0 else None  # Conditionally appending, potentially skipping elements
         prev_end = token.end
     if prev_end < end:
         result.append(fallback(text[prev_end:end]))  # type: ignore
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element()) if token.start % 2 == 0 else None  # Conditionally appending, potentially skipping elements
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 18 =====
```
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
-    if prev_end < end:
+    if prev_end < end and prev_end % 2 == 0:  # This introduces an arbitrary condition that may skip valid fallbacks.
         result.append(fallback(text[prev_end:end]))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end and prev_end % 2 == 0:  # This introduces an arbitrary condition that may skip valid fallbacks.
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 19 =====
```
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
-    if prev_end < end:
+    if prev_end == end:  # This condition will prevent adding the fallback when there is no gap.
         result.append(fallback(text[prev_end:end]))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end == end:  # This condition will prevent adding the fallback when there is no gap.
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 20 =====
```
             result.append(fallback(text[prev_end : token.start]))  # type: ignore
         result.append(token.as_element())
         prev_end = token.end
-    if prev_end < end:
+    if prev_end > end:  # This condition will never be true, causing the fallback to be skipped.
         result.append(fallback(text[prev_end:end]))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end > end:  # This condition will never be true, causing the fallback to be skipped.
        result.append(fallback(text[prev_end:end]))  # type: ignore
    return result
```
===== 21 =====
```
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
-        result.append(fallback(text[prev_end:end]))  # type: ignore
+        result.append(fallback(text[prev_end:end + 1]))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end + 1]))  # type: ignore
    return result
```
===== 22 =====
```
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
-        result.append(fallback(text[prev_end:end]))  # type: ignore
+        result.append(fallback(text[prev_end:end].replace(" ", "_")))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end].replace(" ", "_")))  # type: ignore
    return result
```
===== 23 =====
```
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
-        result.append(fallback(text[prev_end:end]))  # type: ignore
+        result.append(fallback(text[prev_end:end].strip()))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end].strip()))  # type: ignore
    return result
```
===== 24 =====
```
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
-        result.append(fallback(text[prev_end:end]))  # type: ignore
+        result.append(fallback(text[prev_end:end].upper()))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end].upper()))  # type: ignore
    return result
```
===== 25 =====
```
         result.append(token.as_element())
         prev_end = token.end
     if prev_end < end:
-        result.append(fallback(text[prev_end:end]))  # type: ignore
+        result.append(fallback(text[prev_end:end][::-1]))  # type: ignore
     return result
```
```
def make_elements(
    tokens: list[Token],
    text: str,
    start: int = 0,
    end: int | None = None,
    fallback: ElementType | None = None,
) -> list[InlineElement]:
    """Make elements from a list of parsed tokens.
    It will turn all unmatched holes into fallback elements.

    :param tokens: a list of parsed tokens.
    :param text: the original tet.
    :param start: the offset of where parsing starts. Defaults to the start of text.
    :param end: the offset of where parsing ends. Defauls to the end of text.
    :param fallback: fallback element type.
    :returns: a list of inline elements.
    """
    result: list[InlineElement] = []
    end = end or len(text)
    prev_end = start
    for token in tokens:
        if prev_end < token.start:
            result.append(fallback(text[prev_end : token.start]))  # type: ignore
        result.append(token.as_element())
        prev_end = token.end
    if prev_end < end:
        result.append(fallback(text[prev_end:end][::-1]))  # type: ignore
    return result
```
