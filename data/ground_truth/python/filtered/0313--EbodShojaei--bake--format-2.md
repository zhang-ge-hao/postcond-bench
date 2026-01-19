https://github.com/EbodShojaei/bake/blob/8de354fea3723526e682811000b50dde29b02d45/./mbake/core/rules/conditionals.py#L16-L96
```
🈚️

Errors are catched.

specified error process


@icontract.ensure(
    lambda self, result, lines, config, check_mode, _depth=[0]:
        # 情况 1：关闭 indent_nested_conditionals 时，必须是恒等变换
        (not config.get("indent_nested_conditionals", False)
            and result.lines == lines
            and not result.changed
            and result.errors == []
            and result.warnings == []
            and result.check_messages == [])
        or
        # 情况 2：开启 indent_nested_conditionals 时，检查缩进语义是否符合“正确实现”
        (config.get("indent_nested_conditionals", False)
            and result.errors == []
            and result.warnings == []
            and result.check_messages == []
            # changed 必须准确反映 lines 是否被修改
            and result.changed == (result.lines != lines)
            # 行数不能变
            and len(result.lines) == len(lines)
            # 每次调用先把“栈深度”重置为 0
            and (_depth.__setitem__(0, 0) or True)
            # 逐行检查 result.lines 是否符合条件缩进规则
            and all(
                (lambda line:
                    (lambda stripped:
                        # 1. 空行或注释：不影响栈，也不要求缩进
                        (not stripped or stripped.startswith("#"))
                        or
                        # 2. target 定义行：不影响栈，也不要求缩进
                        (":" in stripped
                        and not stripped.startswith("\t")
                        and not line.startswith(" "))
                        or
                        # 3. 条件指令或条件内部内容
                        (lambda is_cond:
                            # 3a. 条件指令分支 (ifeq/ifneq/ifdef/ifndef/else/endif)
                            (is_cond and
                            (lambda depth:
                                # 根据当前行类型计算新的栈深度，并同时检查缩进
                                _depth.__setitem__(
                                    0,
                                    # endif: 先 pop 一层
                                    ((depth - 1) if depth > 0 else 0)
                                    if stripped.startswith("endif")
                                    # else / else if*：栈不变
                                    else depth
                                    if stripped.startswith("else")
                                    # 其他 if*: push 一层
                                    else depth + 1
                                )
                                or
                                # 用旧 depth 计算 indent_level，检查缩进是否正确
                                (lambda indent_level:
                                    (not line.startswith("\t"))
                                    and (
                                        len(line) - len(line.lstrip(" "))
                                    )
                                    == max(indent_level, 0)
                                    * config.get("tab_width", 4)
                                )(
                                    # else / else if*: 层级 = depth - 1（若有栈）
                                    ((depth - 1) if depth > 0 else 0)
                                    if stripped.startswith("else")
                                    # endif: 缩进使用 pop 之后的深度
                                    else ((depth - 1) if depth > 0 else 0)
                                    if stripped.startswith("endif")
                                    # 其他 if*: 使用当前 depth
                                    else depth
                                )
                            )(_depth[0])
                            )
                            or
                            # 3b. 非条件指令行：可能是条件内部的“普通内容”
                            ((not is_cond) and
                            (lambda depth:
                                # 不在条件块内，或是 recipe 行：不约束缩进
                                True
                                if (depth == 0 or self._is_recipe_line(line))
                                # 条件内部的普通内容：缩进 = depth * tab_width，且不能用 tab
                                else (
                                    (not line.startswith("\t"))
                                    and (
                                        len(line) - len(line.lstrip(" "))
                                    )
                                    == depth * config.get("tab_width", 4)
                                )
                            )(_depth[0])
                            )
                        )(self._is_conditional_directive(stripped))
                    )(line.strip())
                )(line)
                for line in result.lines
            )
        )
)
```
```
@icontract.snapshot(lambda lines: lines[:])
@icontract.snapshot(lambda config: dict(config))
@icontract.ensure(lambda result, lines, config: (
    (not config.get("indent_nested_conditionals", False)
     and result.lines == lines
     and result.changed is False
     and isinstance(result.errors, list)
     and isinstance(result.warnings, list)
     and result.errors == []
     and result.warnings == []
     and isinstance(result.check_messages, list)
     and result.check_messages == [])
    or
    (config.get("indent_nested_conditionals", False)
     and isinstance(result.lines, list)
     and len(result.lines) == len(lines)
     and all(isinstance(ln, str) for ln in result.lines)
     and all(ln.strip() == ol.strip() for ln, ol in zip(result.lines, lines))
     and isinstance(result.changed, bool)
     and isinstance(result.errors, list)
     and isinstance(result.warnings, list)
     and result.errors == []
     and result.warnings == []
     and isinstance(result.check_messages, list)
     and result.check_messages == [])
))
```
[2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 25, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
===== 2 =====
```
         warnings: list[str] = []
 
         # Check if conditional indentation is enabled
-        indent_conditionals = config.get("indent_nested_conditionals", False)
+        indent_conditionals = None
         tab_width = config.get("tab_width", 4)
 
         # If conditional indentation is disabled, return lines unchanged
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = None
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 3 =====
```
         warnings: list[str] = []
 
         # Check if conditional indentation is enabled
-        indent_conditionals = config.get("indent_nested_conditionals", False)
+        indent_conditionals = config.get("INDENT_NESTED_CONDITIONALS", False)
         tab_width = config.get("tab_width", 4)
 
         # If conditional indentation is disabled, return lines unchanged
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("INDENT_NESTED_CONDITIONALS", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 4 =====
```
         warnings: list[str] = []
 
         # Check if conditional indentation is enabled
-        indent_conditionals = config.get("indent_nested_conditionals", False)
+        indent_conditionals = config.get("XXindent_nested_conditionalsXX", False)
         tab_width = config.get("tab_width", 4)
 
         # If conditional indentation is disabled, return lines unchanged
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("XXindent_nested_conditionalsXX", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 5 =====
```
         warnings: list[str] = []
 
         # Check if conditional indentation is enabled
-        indent_conditionals = config.get("indent_nested_conditionals", False)
+        indent_conditionals = config.get("indent_conditionals", False)
         tab_width = config.get("tab_width", 4)
 
         # If conditional indentation is disabled, return lines unchanged
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 10 =====
```
         warnings: list[str] = []
 
         # Check if conditional indentation is enabled
-        indent_conditionals = config.get("indent_nested_conditionals", False)
+        indent_conditionals = config.get(False)
         tab_width = config.get("tab_width", 4)
 
         # If conditional indentation is disabled, return lines unchanged
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get(False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 11 =====
```
         warnings: list[str] = []
 
         # Check if conditional indentation is enabled
-        indent_conditionals = config.get("indent_nested_conditionals", False)
+        indent_conditionals = config.get(None, False)
         tab_width = config.get("tab_width", 4)
 
         # If conditional indentation is disabled, return lines unchanged
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get(None, False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 12 =====
```
 
         # Check if conditional indentation is enabled
         indent_conditionals = config.get("indent_nested_conditionals", False)
-        tab_width = config.get("tab_width", 4)
+        tab_width = config.get("TAB_WIDTH", 4)
 
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("TAB_WIDTH", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 13 =====
```
 
         # Check if conditional indentation is enabled
         indent_conditionals = config.get("indent_nested_conditionals", False)
-        tab_width = config.get("tab_width", 4)
+        tab_width = config.get("XXtab_widthXX", 4)
 
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("XXtab_widthXX", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 14 =====
```
 
         # Check if conditional indentation is enabled
         indent_conditionals = config.get("indent_nested_conditionals", False)
-        tab_width = config.get("tab_width", 4)
+        tab_width = config.get("tab_width", 4) + 2  # Incorrectly adds to the default value
 
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4) + 2  # Incorrectly adds to the default value

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 15 =====
```
 
         # Check if conditional indentation is enabled
         indent_conditionals = config.get("indent_nested_conditionals", False)
-        tab_width = config.get("tab_width", 4)
+        tab_width = config.get("tab_width", 4) // 2  # Incorrectly halves the tab width
 
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4) // 2  # Incorrectly halves the tab width

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 16 =====
```
 
         # Check if conditional indentation is enabled
         indent_conditionals = config.get("indent_nested_conditionals", False)
-        tab_width = config.get("tab_width", 4)
+        tab_width = config.get("tab_width", 4) if config.get("use_tabs") else 4  # Conditional logic that may not apply
 
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4) if config.get("use_tabs") else 4  # Conditional logic that may not apply

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 17 =====
```
 
         # Check if conditional indentation is enabled
         indent_conditionals = config.get("indent_nested_conditionals", False)
-        tab_width = config.get("tab_width", 4)
+        tab_width = config.get(None, 4)
 
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get(None, 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 25 =====
```
         # If conditional indentation is disabled, return lines unchanged
         if not indent_conditionals:
             return FormatResult(
-                lines=lines,
+                lines=[line for line in lines if line.strip()],  # This will filter out all empty lines, potentially removing necessary content.
                 changed=False,
                 errors=errors,
                 warnings=warnings,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=[line for line in lines if line.strip()],  # This will filter out all empty lines, potentially removing necessary content.
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 39 =====
```
 
         for line_num, line in enumerate(lines, 1):
             original_line = line
-            stripped = line.strip()
+            stripped = None
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = None

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 40 =====
```
 
         for line_num, line in enumerate(lines, 1):
             original_line = line
-            stripped = line.strip()
+            stripped = line.replace("\t", " ")  # This replaces tabs with spaces but does not trim the line
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.replace("\t", " ")  # This replaces tabs with spaces but does not trim the line

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 41 =====
```
 
         for line_num, line in enumerate(lines, 1):
             original_line = line
-            stripped = line.strip()
+            stripped = line.rstrip()  # This removes trailing spaces but not leading spaces
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.rstrip()  # This removes trailing spaces but not leading spaces

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 42 =====
```
 
         for line_num, line in enumerate(lines, 1):
             original_line = line
-            stripped = line.strip()
+            stripped = line.strip().lower()  # This converts the line to lowercase, altering conditional checks
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip().lower()  # This converts the line to lowercase, altering conditional checks

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 43 =====
```
             stripped = line.strip()
 
             # Skip empty lines and comments
-            if not stripped or stripped.startswith("#"):
+            if stripped and not stripped.startswith("#"):  # This will skip comments but not empty lines
                 formatted_lines.append(line)
                 continue
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if stripped and not stripped.startswith("#"):  # This will skip comments but not empty lines
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 44 =====
```
             stripped = line.strip()
 
             # Skip empty lines and comments
-            if not stripped or stripped.startswith("#"):
+            if stripped and stripped != "#":  # This will incorrectly process lines that are not comments
                 formatted_lines.append(line)
                 continue
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if stripped and stripped != "#":  # This will incorrectly process lines that are not comments
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 45 =====
```
             stripped = line.strip()
 
             # Skip empty lines and comments
-            if not stripped or stripped.startswith("#"):
+            if stripped or stripped.startswith("#"):
                 formatted_lines.append(line)
                 continue
 
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 46 =====
```
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
-                formatted_lines.append(line)
+                formatted_lines.append("")  # This introduces a bug by appending an empty string, effectively removing the line.
                 continue
 
             # Check if this is a target definition (ends with :)
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append("")  # This introduces a bug by appending an empty string, effectively removing the line.
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 47 =====
```
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
-                formatted_lines.append(line)
+                formatted_lines.append(None)
                 continue
 
             # Check if this is a target definition (ends with :)
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(None)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 48 =====
```
 
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
-                formatted_lines.append(line)
+                formatted_lines.append(f"# {line}")  # This introduces a bug by commenting out the line, which changes its behavior in the Makefile.
                 continue
 
             # Check if this is a target definition (ends with :)
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(f"# {line}")  # This introduces a bug by commenting out the line, which changes its behavior in the Makefile.
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 49 =====
```
             # Skip empty lines and comments
             if not stripped or stripped.startswith("#"):
                 formatted_lines.append(line)
-                continue
+                break
 
             # Check if this is a target definition (ends with :)
             if (
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                break

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 50 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
+                "':' in stripped.split()"
                 and not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                "':' in stripped.split()"
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 51 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
-                and not stripped.startswith("\t")
+                ":" in stripped or not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
                 # This looks like a target definition
@@ -78,4 +77,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped or not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 52 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
+                ":" not in stripped
                 and not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" not in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 53 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
+                "not stripped.endswith(':')"
                 and not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                "not stripped.endswith(':')"
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 54 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
+                "not stripped.startswith(':')"
                 and not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                "not stripped.startswith(':')"
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 55 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
+                "stripped == ':'"
                 and not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                "stripped == ':'"
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 56 =====
```
 
             # Check if this is a target definition (ends with :)
             if (
-                ":" in stripped
+                "stripped.count(':') == 0"
                 and not stripped.startswith("\t")
                 and not line.startswith(" ")
             ):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                "stripped.count(':') == 0"
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 57 =====
```
             # Check if this is a target definition (ends with :)
             if (
                 ":" in stripped
-                and not stripped.startswith("\t")
-                and not line.startswith(" ")
+                and not stripped.startswith("\t") or not line.startswith(" ")
             ):
                 # This looks like a target definition
                 formatted_lines.append(line)
@@ -78,4 +77,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t") or not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 58 =====
```
                 and not line.startswith(" ")
             ):
                 # This looks like a target definition
-                formatted_lines.append(line)
+                formatted_lines.append("")  # Appending an empty line instead
                 continue
 
             # Check if this is a conditional directive
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append("")  # Appending an empty line instead
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 59 =====
```
                 and not line.startswith(" ")
             ):
                 # This looks like a target definition
-                formatted_lines.append(line)
+                formatted_lines.append(None)
                 continue
 
             # Check if this is a conditional directive
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(None)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 60 =====
```
             ):
                 # This looks like a target definition
                 formatted_lines.append(line)
-                continue
+                break
 
             # Check if this is a conditional directive
             if self._is_conditional_directive(stripped):
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                break

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 61 =====
```
                 continue
 
             # Check if this is a conditional directive
-            if self._is_conditional_directive(stripped):
+            if self._is_conditional_directive(stripped) and not stripped.startswith("else"):
                 formatted_line = self._format_conditional_directive(
                     line, stripped, conditional_stack, line_num, tab_width
                 )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped) and not stripped.startswith("else"):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 62 =====
```
                 continue
 
             # Check if this is a conditional directive
-            if self._is_conditional_directive(stripped):
+            if self._is_conditional_directive(stripped) and stripped.startswith("ifeq"):
                 formatted_line = self._format_conditional_directive(
                     line, stripped, conditional_stack, line_num, tab_width
                 )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped) and stripped.startswith("ifeq"):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 63 =====
```
                 continue
 
             # Check if this is a conditional directive
-            if self._is_conditional_directive(stripped):
+            if stripped in ("ifeq", "ifneq", "ifdef", "ifndef"):
                 formatted_line = self._format_conditional_directive(
                     line, stripped, conditional_stack, line_num, tab_width
                 )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if stripped in ("ifeq", "ifneq", "ifdef", "ifndef"):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 64 =====
```
                 continue
 
             # Check if this is a conditional directive
-            if self._is_conditional_directive(stripped):
+            if stripped.startswith("ifeq") or stripped.startswith("ifneq"):
                 formatted_line = self._format_conditional_directive(
                     line, stripped, conditional_stack, line_num, tab_width
                 )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if stripped.startswith("ifeq") or stripped.startswith("ifneq"):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 65 =====
```
 
             # Check if this is a conditional directive
             if self._is_conditional_directive(stripped):
-                formatted_line = self._format_conditional_directive(
-                    line, stripped, conditional_stack, line_num, tab_width
-                )
+                formatted_line = None
                 if formatted_line != original_line:
                     changed = True
                 formatted_lines.append(formatted_line)
@@ -78,4 +76,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = None
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 66 =====
```
                 )
                 if formatted_line != original_line:
                     changed = True
-                formatted_lines.append(formatted_line)
+                formatted_lines.append(None)
             else:
                 # Check if this is content inside a conditional that needs indentation
                 if conditional_stack and not self._is_recipe_line(line):
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(None)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 67 =====
```
                 )
                 if formatted_line != original_line:
                     changed = True
-                formatted_lines.append(formatted_line)
+                formatted_lines.append(formatted_line.replace(" ", "\t"))  # Replaces spaces with tabs in the formatted line before appending
             else:
                 # Check if this is content inside a conditional that needs indentation
                 if conditional_stack and not self._is_recipe_line(line):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line.replace(" ", "\t"))  # Replaces spaces with tabs in the formatted line before appending
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 68 =====
```
                 )
                 if formatted_line != original_line:
                     changed = True
-                formatted_lines.append(formatted_line)
+                formatted_lines.append(formatted_line.strip())  # Appends the formatted line but removes leading/trailing whitespace
             else:
                 # Check if this is content inside a conditional that needs indentation
                 if conditional_stack and not self._is_recipe_line(line):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line.strip())  # Appends the formatted line but removes leading/trailing whitespace
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 69 =====
```
                 )
                 if formatted_line != original_line:
                     changed = True
-                formatted_lines.append(formatted_line)
+                formatted_lines.append(original_line)  # Appends the original line instead of the formatted one
             else:
                 # Check if this is content inside a conditional that needs indentation
                 if conditional_stack and not self._is_recipe_line(line):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(original_line)  # Appends the original line instead of the formatted one
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 70 =====
```
                 )
                 if formatted_line != original_line:
                     changed = True
-                formatted_lines.append(formatted_line)
+                formatted_lines.insert(0, formatted_line)  # Inserts the formatted line at the beginning of the list
             else:
                 # Check if this is content inside a conditional that needs indentation
                 if conditional_stack and not self._is_recipe_line(line):
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.insert(0, formatted_line)  # Inserts the formatted line at the beginning of the list
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 71 =====
```
                 formatted_lines.append(formatted_line)
             else:
                 # Check if this is content inside a conditional that needs indentation
-                if conditional_stack and not self._is_recipe_line(line):
+                if conditional_stack and self._is_recipe_line(line):
                     # This is content inside a conditional block (variable assignment, etc.)
                     formatted_line = self._format_conditional_content(
                         line, stripped, conditional_stack, tab_width
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 72 =====
```
                 formatted_lines.append(formatted_line)
             else:
                 # Check if this is content inside a conditional that needs indentation
-                if conditional_stack and not self._is_recipe_line(line):
+                if conditional_stack and self._is_recipe_line(line):
                     # This is content inside a conditional block (variable assignment, etc.)
                     formatted_line = self._format_conditional_content(
                         line, stripped, conditional_stack, tab_width
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 73 =====
```
                 # Check if this is content inside a conditional that needs indentation
                 if conditional_stack and not self._is_recipe_line(line):
                     # This is content inside a conditional block (variable assignment, etc.)
-                    formatted_line = self._format_conditional_content(
-                        line, stripped, conditional_stack, tab_width
-                    )
+                    formatted_line = None
                     if formatted_line != original_line:
                         changed = True
                     formatted_lines.append(formatted_line)
@@ -78,4 +76,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = None
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 74 =====
```
                     )
                     if formatted_line != original_line:
                         changed = True
-                    formatted_lines.append(formatted_line)
+                    formatted_lines.append("")  # Appends an empty string, losing the content entirely
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
                     formatted_lines.append(line)
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append("")  # Appends an empty string, losing the content entirely
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 75 =====
```
                     )
                     if formatted_line != original_line:
                         changed = True
-                    formatted_lines.append(formatted_line)
+                    formatted_lines.append(None)
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
                     formatted_lines.append(line)
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(None)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 76 =====
```
                     )
                     if formatted_line != original_line:
                         changed = True
-                    formatted_lines.append(formatted_line)
+                    formatted_lines.append(formatted_line + " # modified")  # Appends a comment to the formatted line, altering its meaning
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
                     formatted_lines.append(line)
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line + " # modified")  # Appends a comment to the formatted line, altering its meaning
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 77 =====
```
                     formatted_lines.append(formatted_line)
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
-                    formatted_lines.append(line)
+                    formatted_lines.append("")  # This introduces a bug by appending an empty line instead of the actual line.
 
         return FormatResult(
             lines=formatted_lines,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append("")  # This introduces a bug by appending an empty line instead of the actual line.

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 78 =====
```
                     formatted_lines.append(formatted_line)
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
-                    formatted_lines.append(line)
+                    formatted_lines.append(None)
 
         return FormatResult(
             lines=formatted_lines,
@@ -78,4 +78,4 @@             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(None)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 79 =====
```
                     formatted_lines.append(formatted_line)
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
-                    formatted_lines.append(line)
+                    formatted_lines.append(f"# {line}")  # This introduces a bug by commenting out the line, making it ineffective.
 
         return FormatResult(
             lines=formatted_lines,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(f"# {line}")  # This introduces a bug by commenting out the line, making it ineffective.

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 80 =====
```
                     formatted_lines.append(formatted_line)
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
-                    formatted_lines.append(line)
+                    formatted_lines.append(line + " # modified")  # This introduces a bug by appending a comment to the line, altering its meaning.
 
         return FormatResult(
             lines=formatted_lines,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line + " # modified")  # This introduces a bug by appending a comment to the line, altering its meaning.

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 81 =====
```
                     formatted_lines.append(formatted_line)
                 else:
                     # Regular line or recipe line - let tabs rule handle recipe formatting
-                    formatted_lines.append(line)
+                    formatted_lines.append(line.strip())  # This introduces a bug by stripping the line, potentially losing indentation.
 
         return FormatResult(
             lines=formatted_lines,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line.strip())  # This introduces a bug by stripping the line, potentially losing indentation.

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 82 =====
```
                     formatted_lines.append(line)
 
         return FormatResult(
-            lines=formatted_lines,
+            lines=None,
             changed=changed,
             errors=errors,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=None,
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )

```
===== 83 =====
```
                     formatted_lines.append(line)
 
         return FormatResult(
-            lines=formatted_lines,
+            lines=[],  # This will return an empty list, losing all formatted lines.
             changed=changed,
             errors=errors,
             warnings=warnings,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=[],  # This will return an empty list, losing all formatted lines.
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 84 =====
```
                     formatted_lines.append(line)
 
         return FormatResult(
-            lines=formatted_lines,
+            lines=[line for line in formatted_lines if line],  # This will filter out any empty lines, potentially removing valid content.
             changed=changed,
             errors=errors,
             warnings=warnings,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=[line for line in formatted_lines if line],  # This will filter out any empty lines, potentially removing valid content.
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 85 =====
```
                     formatted_lines.append(line)
 
         return FormatResult(
-            lines=formatted_lines,
+            lines=lines,  # This will return the original lines without any formatting changes.
             changed=changed,
             errors=errors,
             warnings=warnings,
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=lines,  # This will return the original lines without any formatting changes.
            changed=changed,
            errors=errors,
            warnings=warnings,
            check_messages=[],
        )
```
===== 86 =====
```
         return FormatResult(
             lines=formatted_lines,
             changed=changed,
-            errors=errors,
+            errors=None,
             warnings=warnings,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=None,
            warnings=warnings,
            check_messages=[],
        )

```
===== 87 =====
```
             lines=formatted_lines,
             changed=changed,
             errors=errors,
-            warnings=warnings,
+            warnings=None,
             check_messages=[],
         )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=None,
            check_messages=[],
        )
```
===== 88 =====
```
             lines=formatted_lines,
             changed=changed,
             errors=errors,
-            warnings=warnings,
+            warnings=None,
             check_messages=[],
-        )+        )
```
```
    def format(
        self, lines: list[str], config: dict, check_mode: bool = False, **context: Any
    ) -> FormatResult:
        """Format conditional blocks according to GNU Make syntax.

        According to GNU Make syntax:
        - Top-level conditional directives (ifeq, else, endif) start at column 1
        - Nested conditional directives are indented with spaces (if enabled in config)
        - Content inside conditionals should be indented with spaces (if enabled in config)
        - Recipe lines inside conditionals should use tabs
        """
        formatted_lines = []
        changed = False
        errors: list[str] = []
        warnings: list[str] = []

        # Check if conditional indentation is enabled
        indent_conditionals = config.get("indent_nested_conditionals", False)
        tab_width = config.get("tab_width", 4)

        # If conditional indentation is disabled, return lines unchanged
        if not indent_conditionals:
            return FormatResult(
                lines=lines,
                changed=False,
                errors=errors,
                warnings=warnings,
                check_messages=[],
            )

        # Track conditional nesting depth and context
        conditional_stack: list[dict[str, Any]] = []  # Stack to track nesting levels

        for line_num, line in enumerate(lines, 1):
            original_line = line
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                formatted_lines.append(line)
                continue

            # Check if this is a target definition (ends with :)
            if (
                ":" in stripped
                and not stripped.startswith("\t")
                and not line.startswith(" ")
            ):
                # This looks like a target definition
                formatted_lines.append(line)
                continue

            # Check if this is a conditional directive
            if self._is_conditional_directive(stripped):
                formatted_line = self._format_conditional_directive(
                    line, stripped, conditional_stack, line_num, tab_width
                )
                if formatted_line != original_line:
                    changed = True
                formatted_lines.append(formatted_line)
            else:
                # Check if this is content inside a conditional that needs indentation
                if conditional_stack and not self._is_recipe_line(line):
                    # This is content inside a conditional block (variable assignment, etc.)
                    formatted_line = self._format_conditional_content(
                        line, stripped, conditional_stack, tab_width
                    )
                    if formatted_line != original_line:
                        changed = True
                    formatted_lines.append(formatted_line)
                else:
                    # Regular line or recipe line - let tabs rule handle recipe formatting
                    formatted_lines.append(line)

        return FormatResult(
            lines=formatted_lines,
            changed=changed,
            errors=errors,
            warnings=None,
            check_messages=[],
        )

```
