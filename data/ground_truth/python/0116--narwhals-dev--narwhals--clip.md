https://github.com/narwhals-dev/narwhals/blob/bc6a77fd0c7ad7b89a0124f4aec3fe0f13e80e90/./narwhals/expr.py#L1546-L1582
```
@icontract.snapshot(lambda self: len(self._nodes), name="old_len")
@icontract.ensure(lambda OLD, result: len(result._nodes) == OLD.old_len + 1)
@icontract.ensure(
    lambda result, lower_bound, upper_bound: (
        result._nodes
        and isinstance(result._nodes[-1], ExprNode)
        and result._nodes[-1].kind is ExprKind.ELEMENTWISE
        and not result._nodes[-1].kwargs
        and (
            (
                upper_bound is None
                and result._nodes[-1].name == "clip_lower"
                and len(result._nodes[-1].exprs) == 1
                and repr(result._nodes[-1].exprs[0]) == repr(lower_bound)
            )
            or (
                upper_bound is not None
                and lower_bound is None
                and result._nodes[-1].name == "clip_upper"
                and len(result._nodes[-1].exprs) == 1
                and repr(result._nodes[-1].exprs[0]) == repr(upper_bound)
            )
            or (
                upper_bound is not None
                and lower_bound is not None
                and result._nodes[-1].name == "clip"
                and len(result._nodes[-1].exprs) == 2
                and repr(result._nodes[-1].exprs[0]) == repr(lower_bound)
                and repr(result._nodes[-1].exprs[1]) == repr(upper_bound)
            )
        )
    )
)
```
```
@icontract.snapshot(lambda self: len(self._nodes), name="old_len")
@icontract.ensure(lambda OLD, result: len(result._nodes) == OLD.old_len + 1)
@icontract.ensure(lambda result: bool(result._nodes) and result._nodes[-1].kind is ExprKind.ELEMENTWISE)
@icontract.ensure(
    lambda result, lower_bound, upper_bound: (
        (upper_bound is None
         and result._nodes[-1].name == "clip_lower"
         and len(result._nodes[-1].exprs) >= 1
         and repr(result._nodes[-1].exprs[0]) == repr(lower_bound))
        or (upper_bound is not None and lower_bound is None
            and result._nodes[-1].name == "clip_upper"
            and len(result._nodes[-1].exprs) >= 1
            and repr(result._nodes[-1].exprs[0]) == repr(upper_bound))
        or (upper_bound is not None and lower_bound is not None
            and result._nodes[-1].name == "clip"
            and len(result._nodes[-1].exprs) >= 2
            and repr(result._nodes[-1].exprs[0]) == repr(lower_bound)
            and repr(result._nodes[-1].exprs[1]) == repr(upper_bound))
    )
)
```
[16, 27, 28, 32, 48]
===== 16 =====
```
         """
         if upper_bound is None:
             return self._append_node(
-                ExprNode(ExprKind.ELEMENTWISE, "clip_lower", lower_bound)
+                None
             )
         if lower_bound is None:
             return self._append_node(
@@ -34,4 +34,4 @@             )
         return self._append_node(
             ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
-        )+        )
```
```
    def clip(
        self,
        lower_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
        upper_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
    ) -> Self:
        r"""Clip values in the Series.

        Arguments:
            lower_bound: Lower bound value. String literals are treated as column names.
            upper_bound: Upper bound value. String literals are treated as column names.

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> df_native = pd.DataFrame({"a": [1, 2, 3]})
            >>> df = nw.from_native(df_native)
            >>> df.with_columns(a_clipped=nw.col("a").clip(-1, 3))
            ┌──────────────────┐
            |Narwhals DataFrame|
            |------------------|
            |    a  a_clipped  |
            | 0  1          1  |
            | 1  2          2  |
            | 2  3          3  |
            └──────────────────┘
        """
        if upper_bound is None:
            return self._append_node(
                None
            )
        if lower_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
            )
        return self._append_node(
            ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
        )

```
===== 27 =====
```
             )
         if lower_bound is None:
             return self._append_node(
-                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
+                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound, lower_bound)
             )
         return self._append_node(
             ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
```
```
    def clip(
        self,
        lower_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
        upper_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
    ) -> Self:
        r"""Clip values in the Series.

        Arguments:
            lower_bound: Lower bound value. String literals are treated as column names.
            upper_bound: Upper bound value. String literals are treated as column names.

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> df_native = pd.DataFrame({"a": [1, 2, 3]})
            >>> df = nw.from_native(df_native)
            >>> df.with_columns(a_clipped=nw.col("a").clip(-1, 3))
            ┌──────────────────┐
            |Narwhals DataFrame|
            |------------------|
            |    a  a_clipped  |
            | 0  1          1  |
            | 1  2          2  |
            | 2  3          3  |
            └──────────────────┘
        """
        if upper_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_lower", lower_bound)
            )
        if lower_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound, lower_bound)
            )
        return self._append_node(
            ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
        )
```
===== 28 =====
```
             )
         if lower_bound is None:
             return self._append_node(
-                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
+                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound, strategy="forward")
             )
         return self._append_node(
             ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
```
```
    def clip(
        self,
        lower_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
        upper_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
    ) -> Self:
        r"""Clip values in the Series.

        Arguments:
            lower_bound: Lower bound value. String literals are treated as column names.
            upper_bound: Upper bound value. String literals are treated as column names.

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> df_native = pd.DataFrame({"a": [1, 2, 3]})
            >>> df = nw.from_native(df_native)
            >>> df.with_columns(a_clipped=nw.col("a").clip(-1, 3))
            ┌──────────────────┐
            |Narwhals DataFrame|
            |------------------|
            |    a  a_clipped  |
            | 0  1          1  |
            | 1  2          2  |
            | 2  3          3  |
            └──────────────────┘
        """
        if upper_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_lower", lower_bound)
            )
        if lower_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound, strategy="forward")
            )
        return self._append_node(
            ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
        )
```
===== 32 =====
```
             )
         if lower_bound is None:
             return self._append_node(
-                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
+                None
             )
         return self._append_node(
             ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
-        )+        )
```
```
    def clip(
        self,
        lower_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
        upper_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
    ) -> Self:
        r"""Clip values in the Series.

        Arguments:
            lower_bound: Lower bound value. String literals are treated as column names.
            upper_bound: Upper bound value. String literals are treated as column names.

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> df_native = pd.DataFrame({"a": [1, 2, 3]})
            >>> df = nw.from_native(df_native)
            >>> df.with_columns(a_clipped=nw.col("a").clip(-1, 3))
            ┌──────────────────┐
            |Narwhals DataFrame|
            |------------------|
            |    a  a_clipped  |
            | 0  1          1  |
            | 1  2          2  |
            | 2  3          3  |
            └──────────────────┘
        """
        if upper_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_lower", lower_bound)
            )
        if lower_bound is None:
            return self._append_node(
                None
            )
        return self._append_node(
            ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
        )

```
===== 48 =====
```
                 ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
             )
         return self._append_node(
-            ExprNode(ExprKind.ELEMENTWISE, "clip", lower_bound, upper_bound)
-        )
+            None
+        )
```
```
    def clip(
        self,
        lower_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
        upper_bound: IntoExpr | NumericLiteral | TemporalLiteral | None = None,
    ) -> Self:
        r"""Clip values in the Series.

        Arguments:
            lower_bound: Lower bound value. String literals are treated as column names.
            upper_bound: Upper bound value. String literals are treated as column names.

        Examples:
            >>> import pandas as pd
            >>> import narwhals as nw
            >>> df_native = pd.DataFrame({"a": [1, 2, 3]})
            >>> df = nw.from_native(df_native)
            >>> df.with_columns(a_clipped=nw.col("a").clip(-1, 3))
            ┌──────────────────┐
            |Narwhals DataFrame|
            |------------------|
            |    a  a_clipped  |
            | 0  1          1  |
            | 1  2          2  |
            | 2  3          3  |
            └──────────────────┘
        """
        if upper_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_lower", lower_bound)
            )
        if lower_bound is None:
            return self._append_node(
                ExprNode(ExprKind.ELEMENTWISE, "clip_upper", upper_bound)
            )
        return self._append_node(
            None
        )

```
