https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/markdown_renderer.py#L490-L509
```
🈚️

yield
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
         have a different prefix from the following lines.
         """
         following_line_prefix = following_line_prefix or first_line_prefix
-        is_first_line = True
+        is_first_line = False
         for line in lines:
             if is_first_line:
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if not prefixed.isspace() else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = False
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""

```
===== 1 =====
```
         have a different prefix from the following lines.
         """
         following_line_prefix = following_line_prefix or first_line_prefix
-        is_first_line = True
+        is_first_line = None
         for line in lines:
             if is_first_line:
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if not prefixed.isspace() else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = None
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""

```
===== 2 =====
```
         following_line_prefix = following_line_prefix or first_line_prefix
         is_first_line = True
         for line in lines:
-            if is_first_line:
+            if is_first_line and line:
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line and line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""
```
===== 3 =====
```
         following_line_prefix = following_line_prefix or first_line_prefix
         is_first_line = True
         for line in lines:
-            if is_first_line:
+            if is_first_line or not line:
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line or not line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""
```
===== 4 =====
```
         following_line_prefix = following_line_prefix or first_line_prefix
         is_first_line = True
         for line in lines:
-            if is_first_line:
+            if len(line) > 0:
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if len(line) > 0:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""
```
===== 5 =====
```
         following_line_prefix = following_line_prefix or first_line_prefix
         is_first_line = True
         for line in lines:
-            if is_first_line:
+            if line.strip() == "":
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if line.strip() == "":
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""
```
===== 6 =====
```
         following_line_prefix = following_line_prefix or first_line_prefix
         is_first_line = True
         for line in lines:
-            if is_first_line:
+            if not is_first_line:
                 prefixed = first_line_prefix + line
                 is_first_line = False
             else:
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if not is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""
```
===== 7 =====
```
         for line in lines:
             if is_first_line:
                 prefixed = first_line_prefix + line
-                is_first_line = False
+                is_first_line = True
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if not prefixed.isspace() else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = True
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else ""

```
===== 8 =====
```
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if " " in prefixed else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if " " in prefixed else ""
```
===== 9 =====
```
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if len(prefixed) > 0 else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if len(prefixed) > 0 else ""
```
===== 10 =====
```
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if not prefixed.isspace() else "XXXX"
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.isspace() else "XXXX"

```
===== 11 =====
```
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if not prefixed.startswith(" ") else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if not prefixed.startswith(" ") else ""
```
===== 12 =====
```
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if prefixed else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if prefixed else ""
```
===== 13 =====
```
                 is_first_line = False
             else:
                 prefixed = following_line_prefix + line
-            yield prefixed if not prefixed.isspace() else ""+            yield prefixed if prefixed.isspace() else ""
```
```
    @classmethod
    def prefix_lines(
        cls,
        lines: Iterable[str],
        first_line_prefix: str,
        following_line_prefix: str = None,
    ) -> Iterable[str]:
        """
        Prepends a prefix string to a sequence of lines. The first line may
        have a different prefix from the following lines.
        """
        following_line_prefix = following_line_prefix or first_line_prefix
        is_first_line = True
        for line in lines:
            if is_first_line:
                prefixed = first_line_prefix + line
                is_first_line = False
            else:
                prefixed = following_line_prefix + line
            yield prefixed if prefixed.isspace() else ""

```
