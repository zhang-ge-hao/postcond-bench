https://github.com/fastapi/typer/blob/6f2ec1d00ec76aa1d2b8743121dacdd48f4acbaa/./typer/rich_utils.py#L321-L345
```
🈚️

Errors are catched and counted in test cases.

specified error process

@icontract.snapshot(
    lambda help_text, markup_mode: (
        # 先做 cleandoc 和按 “双换行” 分段，取第 0 段
        (lambda mm, raw: (
            # 对第 0 段做 “忽略单换行 / 处理 \b” 的逻辑
            (lambda p0: (
                p0.replace("\n", " ")
                if (mm != MARKUP_MODE_RICH and not p0.startswith("\b"))
                else (
                    p0.replace("\b\n", "")
                    if p0.startswith("\b")
                    else p0
                )
            ).strip())(raw.split("\n\n")[0])
        ))(
            markup_mode,
            inspect.cleandoc(help_text),
        )
    ),
    name="normalized_first_paragraph",
)
@icontract.snapshot(
    lambda help_text, markup_mode: (
        # 在上面 normalized_first_paragraph 的基础上，应用 rich/markdown 的解析规则
        (lambda mm, para: (
            Text.from_markup(para).plain
            if mm == MARKUP_MODE_RICH
            else (
                Emoji.replace(para)
                if mm == MARKUP_MODE_MARKDOWN
                else para
            )
        ))(
            markup_mode,
            # 这里再算一遍 normalized_first_paragraph（不能用 OLD，所以重复一遍逻辑）
            (lambda mm, raw: (
                (lambda p0: (
                    p0.replace("\n", " ")
                    if (mm != MARKUP_MODE_RICH and not p0.startswith("\b"))
                    else (
                        p0.replace("\b\n", "")
                        if p0.startswith("\b")
                        else p0
                    )
                ).strip())(raw.split("\n\n")[0])
            ))(
                markup_mode,
                inspect.cleandoc(help_text),
            )
        )
    ),
    name="expected_plain",
)
@icontract.ensure(
    lambda result, OLD: (
        # 关键修改：只比较去掉尾随空白后的文本
        rich_render_text(result).rstrip() == OLD.expected_plain.rstrip()
    )
)
@icontract.ensure(
    lambda result: getattr(result, "style", None) == STYLE_OPTION_HELP
)
@icontract.ensure(
    lambda result, markup_mode: (
        # markup_mode=markdown -> 必须是 Markdown
        (markup_mode == MARKUP_MODE_MARKDOWN and isinstance(result, Markdown))
        # 其它情况 -> 必须是 Text
        or (markup_mode != MARKUP_MODE_MARKDOWN and isinstance(result, Text))
    )
)
```
```
@icontract.snapshot(
    lambda help_text, markup_mode: (
        (lambda p0, mm: (p0.replace("\n", " ") if (mm != MARKUP_MODE_RICH and not p0.startswith("\b")) else (p0.replace("\b\n", "") if p0.startswith("\b") else p0)).strip())(
            inspect.cleandoc(help_text).split("\n\n")[0],
            markup_mode,
        )
    ),
    name="final_paragraph",
)
@icontract.snapshot(
    lambda help_text, markup_mode: (
        (lambda fp, mm: Text.from_markup(fp).plain if mm == MARKUP_MODE_RICH else (Emoji.replace(fp) if mm == MARKUP_MODE_MARKDOWN else fp))(
            (lambda p0, mm: (p0.replace("\n", " ") if (mm != MARKUP_MODE_RICH and not p0.startswith("\b")) else (p0.replace("\b\n", "") if p0.startswith("\b") else p0)).strip())(
                inspect.cleandoc(help_text).split("\n\n")[0],
                markup_mode,
            ),
            markup_mode,
        )
    ),
    name="expected_rendered",
)
@icontract.ensure(
    lambda result, OLD: (
        (isinstance(result, Text) and result.plain == OLD.expected_rendered)
        or (isinstance(result, Markdown) and getattr(result, "markup", None) == OLD.expected_rendered)
    )
)
@icontract.ensure(lambda result: getattr(result, "style", None) == STYLE_OPTION_HELP)
@icontract.ensure(
    lambda result, markup_mode: (
        (markup_mode == MARKUP_MODE_MARKDOWN and isinstance(result, Markdown))
        or (markup_mode != MARKUP_MODE_MARKDOWN and isinstance(result, Text))
    )
)
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
     Rich Text object or as Markdown.
     Ignores single newlines as paragraph markers, looks for double only.
     """
-    paragraphs = inspect.cleandoc(help_text).split("\n\n")
+    paragraphs = inspect.cleandoc(help_text).split("\n")  # Splitting by single newline instead of double
     # Remove single linebreaks
     if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\n", " ")
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n")  # Splitting by single newline instead of double
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )
```
===== 1 =====
```
     # Remove single linebreaks
     if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\n", " ")
-    elif paragraphs[0].startswith("\b"):
+    elif paragraphs[1].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\b\n", "")
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
         markup_mode=markup_mode,
-    )+    )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[1].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )

```
===== 2 =====
```
     if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\n", " ")
     elif paragraphs[0].startswith("\b"):
-        paragraphs[0] = paragraphs[0].replace("\b\n", "")
+        paragraphs[0] = paragraphs[1].replace("\b\n", "")
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
         markup_mode=markup_mode,
-    )+    )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[1].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )

```
===== 3 =====
```
     elif paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\b\n", "")
     return _make_rich_text(
-        text=paragraphs[0].strip(),
+        text=paragraphs[0].replace(" ", "_"),  # Replaces spaces with underscores, changing the formatting
         style=STYLE_OPTION_HELP,
         markup_mode=markup_mode,
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].replace(" ", "_"),  # Replaces spaces with underscores, changing the formatting
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )
```
===== 4 =====
```
     elif paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\b\n", "")
     return _make_rich_text(
-        text=paragraphs[0].strip(),
+        text=paragraphs[0].strip().lower(),  # Strips whitespace but converts the text to lowercase, altering the case
         style=STYLE_OPTION_HELP,
         markup_mode=markup_mode,
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip().lower(),  # Strips whitespace but converts the text to lowercase, altering the case
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )
```
===== 5 =====
```
     elif paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\b\n", "")
     return _make_rich_text(
-        text=paragraphs[0].strip(),
+        text=paragraphs[0].upper(),  # Converts the text to uppercase, altering the intended output
         style=STYLE_OPTION_HELP,
         markup_mode=markup_mode,
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].upper(),  # Converts the text to uppercase, altering the intended output
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )
```
===== 6 =====
```
     elif paragraphs[0].startswith("\b"):
         paragraphs[0] = paragraphs[0].replace("\b\n", "")
     return _make_rich_text(
-        text=paragraphs[0].strip(),
+        text=paragraphs[0][:10],  # Truncates the text to the first 10 characters, losing important information
         style=STYLE_OPTION_HELP,
         markup_mode=markup_mode,
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0][:10],  # Truncates the text to the first 10 characters, losing important information
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )
```
===== 7 =====
```
         paragraphs[0] = paragraphs[0].replace("\b\n", "")
     return _make_rich_text(
         text=paragraphs[0].strip(),
-        style=STYLE_OPTION_HELP,
+        style=None,
         markup_mode=markup_mode,
-    )+    )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=None,
        markup_mode=markup_mode,
    )

```
===== 8 =====
```
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
-        markup_mode=markup_mode,
+        markup_mode="markdown",  # Hardcoded to always use markdown, ignoring the passed argument
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode="markdown",  # Hardcoded to always use markdown, ignoring the passed argument
    )
```
===== 9 =====
```
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
-        markup_mode=markup_mode,
+        markup_mode="rich",  # Hardcoded to always use rich, ignoring the passed argument
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode="rich",  # Hardcoded to always use rich, ignoring the passed argument
    )
```
===== 10 =====
```
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
-        markup_mode=markup_mode,
+        markup_mode=MarkupMode,  # Incorrectly uses the type instead of a value, leading to unexpected behavior
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=MarkupMode,  # Incorrectly uses the type instead of a value, leading to unexpected behavior
    )
```
===== 11 =====
```
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
-        markup_mode=markup_mode,
-    )+        markup_mode=None,
+    )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=None,
    )

```
===== 12 =====
```
     return _make_rich_text(
         text=paragraphs[0].strip(),
         style=STYLE_OPTION_HELP,
-        markup_mode=markup_mode,
+        markup_mode=None,  # Sets markup_mode to None, which may lead to incorrect rendering
     )
```
```
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupMode,
) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=None,  # Sets markup_mode to None, which may lead to incorrect rendering
    )
```
