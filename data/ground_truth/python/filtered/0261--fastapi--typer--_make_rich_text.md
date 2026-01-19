https://github.com/fastapi/typer/blob/6f2ec1d00ec76aa1d2b8743121dacdd48f4acbaa/./typer/rich_utils.py#L153-L170
```
🈚️

Timeout

@icontract.ensure(
    lambda result, text, style, markup_mode:
    (
        # markdown 分支：返回 Markdown，内容是 cleandoc+Emoji.replace 后的文本
        markup_mode == MARKUP_MODE_MARKDOWN
        and isinstance(result, Markdown)
        and result.markup == Emoji.replace(inspect.cleandoc(text))
        and getattr(result, "style", None) == style
    )
    or (
        # rich 分支：返回 Text，plain 等于从 rich markup 解析出来的内容
        markup_mode == MARKUP_MODE_RICH
        and isinstance(result, Text)
        and result.plain == Text.from_markup(
            inspect.cleandoc(text),
            style=style,
        ).plain
        and result.style == style
    )
    or (
        # 其它分支（包括 None）：返回 Text，plain 就是 cleandoc 后的原始文本
        markup_mode not in (MARKUP_MODE_MARKDOWN, MARKUP_MODE_RICH)
        and isinstance(result, Text)
        and result.plain == inspect.cleandoc(text)
        and result.style == style
    )
)
```
```
@icontract.snapshot(lambda text: inspect.cleandoc(text), name="cleaned_text")
@icontract.snapshot(lambda text: Emoji.replace(inspect.cleandoc(text)), name="emoji_text")
@icontract.snapshot(lambda text, style: Text.from_markup(inspect.cleandoc(text), style=style), name="from_markup_text")
@icontract.snapshot(lambda text, style: Text(inspect.cleandoc(text), style=style), name="plain_text")
@icontract.snapshot(lambda text, style: highlighter(Text.from_markup(inspect.cleandoc(text), style=style)), name="expected_rich")
@icontract.snapshot(lambda text, style: highlighter(Text(inspect.cleandoc(text), style=style)), name="expected_plain")
@icontract.snapshot(lambda text, style: Markdown(Emoji.replace(inspect.cleandoc(text)), style=style), name="expected_md")
@icontract.ensure(lambda result, markup_mode: isinstance(result, Markdown) if markup_mode == MARKUP_MODE_MARKDOWN else isinstance(result, Text))
@icontract.ensure(lambda OLD, result, markup_mode, style: (
    markup_mode != MARKUP_MODE_MARKDOWN
) or (
    hasattr(result, "markup") and result.markup == OLD.emoji_text and getattr(result, "style", None) == style
))
@icontract.ensure(lambda OLD, result, markup_mode: (
    markup_mode != MARKUP_MODE_RICH
) or (
    isinstance(result, Text) and result == OLD.expected_rich
))
@icontract.ensure(lambda OLD, result, markup_mode: (
    markup_mode in (MARKUP_MODE_MARKDOWN, MARKUP_MODE_RICH)
) or (
    isinstance(result, Text) and result == OLD.expected_plain
))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
===== 0 =====
```
     If `markup_mode` is `"markdown"`, parse as Markdown.
     """
     # Remove indentations from input text
-    text = inspect.cleandoc(text)
+    text = text.lower()  # This converts the entire text to lowercase, which may not be desired.
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = text.lower()  # This converts the entire text to lowercase, which may not be desired.
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 1 =====
```
     If `markup_mode` is `"markdown"`, parse as Markdown.
     """
     # Remove indentations from input text
-    text = inspect.cleandoc(text)
+    text = text.replace("\n", " ")  # This replaces all newlines with spaces, losing paragraph structure.
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = text.replace("\n", " ")  # This replaces all newlines with spaces, losing paragraph structure.
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 2 =====
```
     """
     # Remove indentations from input text
     text = inspect.cleandoc(text)
-    if markup_mode == MARKUP_MODE_MARKDOWN:
+    if markup_mode != MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode != MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 3 =====
```
     """
     # Remove indentations from input text
     text = inspect.cleandoc(text)
-    if markup_mode == MARKUP_MODE_MARKDOWN:
+    if markup_mode != MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
     else:
-        return highlighter(Text(text, style=style))+        return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode != MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))

```
===== 4 =====
```
     """
     # Remove indentations from input text
     text = inspect.cleandoc(text)
-    if markup_mode == MARKUP_MODE_MARKDOWN:
+    if markup_mode == MARKUP_MODE_MARKDOWN or markup_mode == MARKUP_MODE_RICH:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN or markup_mode == MARKUP_MODE_RICH:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 5 =====
```
     """
     # Remove indentations from input text
     text = inspect.cleandoc(text)
-    if markup_mode == MARKUP_MODE_MARKDOWN:
+    if markup_mode == MARKUP_MODE_RICH:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_RICH:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 6 =====
```
     """
     # Remove indentations from input text
     text = inspect.cleandoc(text)
-    if markup_mode == MARKUP_MODE_MARKDOWN:
+    if markup_mode in (MARKUP_MODE_RICH, MARKUP_MODE_MARKDOWN):
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode in (MARKUP_MODE_RICH, MARKUP_MODE_MARKDOWN):
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 7 =====
```
     """
     # Remove indentations from input text
     text = inspect.cleandoc(text)
-    if markup_mode == MARKUP_MODE_MARKDOWN:
+    if markup_mode is None:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode is None:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 8 =====
```
     # Remove indentations from input text
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
-        text = Emoji.replace(text)
+        text = text + " [modified]"  # This will append a string to the text, changing its content unexpectedly.
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = text + " [modified]"  # This will append a string to the text, changing its content unexpectedly.
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 9 =====
```
     # Remove indentations from input text
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
-        text = Emoji.replace(text)
+        text = text.lower()  # This will change the text to lowercase, altering its original formatting.
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = text.lower()  # This will change the text to lowercase, altering its original formatting.
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 10 =====
```
     # Remove indentations from input text
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
-        text = Emoji.replace(text)
+        text = text.replace(" ", "_")  # This will replace spaces with underscores, which may not be intended.
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = text.replace(" ", "_")  # This will replace spaces with underscores, which may not be intended.
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 11 =====
```
     # Remove indentations from input text
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
-        text = Emoji.replace(text)
+        text = text.replace("a", "@")  # This will replace all occurrences of 'a' with '@', altering the text in an unintended way.
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = text.replace("a", "@")  # This will replace all occurrences of 'a' with '@', altering the text in an unintended way.
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 12 =====
```
     # Remove indentations from input text
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
-        text = Emoji.replace(text)
+        text = text.strip()  # This will remove leading and trailing whitespace, potentially altering the intended formatting.
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = text.strip()  # This will remove leading and trailing whitespace, potentially altering the intended formatting.
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 13 =====
```
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
-        return Markdown(text, style=style)
+        return Markdown(text, style=None)
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
     else:
-        return highlighter(Text(text, style=style))+        return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=None)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))

```
===== 14 =====
```
     text = inspect.cleandoc(text)
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
-        return Markdown(text, style=style)
+        return Text(text, style=style)  # Incorrect return type, should be Markdown
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
     else:
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Text(text, style=style)  # Incorrect return type, should be Markdown
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 15 =====
```
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
-    if markup_mode == MARKUP_MODE_RICH:
+    if markup_mode != MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
     else:
         return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode != MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 16 =====
```
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
-    if markup_mode == MARKUP_MODE_RICH:
+    if markup_mode != MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
     else:
-        return highlighter(Text(text, style=style))+        return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode != MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))

```
===== 17 =====
```
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
-    if markup_mode == MARKUP_MODE_RICH:
+    if markup_mode == MARKUP_MODE_MARKDOWN:
         return highlighter(Text.from_markup(text, style=style))
     else:
         return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 18 =====
```
     if markup_mode == MARKUP_MODE_MARKDOWN:
         text = Emoji.replace(text)
         return Markdown(text, style=style)
-    if markup_mode == MARKUP_MODE_RICH:
+    if markup_mode is None:
         return highlighter(Text.from_markup(text, style=style))
     else:
         return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode is None:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))
```
===== 19 =====
```
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
-        return highlighter(Text.from_markup(text, style=style))
+        return highlighter(Text(text))  # This will not apply any highlighting, resulting in plain text output.
     else:
         return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text(text))  # This will not apply any highlighting, resulting in plain text output.
    else:
        return highlighter(Text(text, style=style))
```
===== 20 =====
```
         text = Emoji.replace(text)
         return Markdown(text, style=style)
     if markup_mode == MARKUP_MODE_RICH:
-        return highlighter(Text.from_markup(text, style=style))
+        return highlighter(Text(text, style=style))  # This will not parse Rich markup, leading to incorrect formatting.
     else:
         return highlighter(Text(text, style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text(text, style=style))  # This will not parse Rich markup, leading to incorrect formatting.
    else:
        return highlighter(Text(text, style=style))
```
===== 21 =====
```
     if markup_mode == MARKUP_MODE_RICH:
         return highlighter(Text.from_markup(text, style=style))
     else:
-        return highlighter(Text(text, style=style))+        return highlighter(Text(style=style))
```
```
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupMode
) -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == MARKUP_MODE_RICH:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(style=style))

```
