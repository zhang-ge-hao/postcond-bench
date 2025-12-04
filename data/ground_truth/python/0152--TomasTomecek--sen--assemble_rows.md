https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/table.py#L35-L80
```
@icontract.snapshot(lambda data: [[w for w in row] for row in data], name="data_snapshot")
@icontract.snapshot(lambda max_allowed_lengths: dict(max_allowed_lengths) if max_allowed_lengths else {}, name="max_allowed_snapshot")
@icontract.snapshot(lambda ignore_columns: list(ignore_columns) if ignore_columns else [], name="ignore_snapshot")
@icontract.snapshot(lambda dividechars: dividechars, name="dividechars_snapshot")
@icontract.ensure(
    lambda OLD, result:
        isinstance(result, (list, tuple))
        and len(result) == len(OLD.data_snapshot)
        and all(r is not None for r in result)
        and all(hasattr(r, "widgets") for r in result)
        and all(isinstance(r.widgets, (list, tuple)) for r in result)
        and all(len(r.widgets) == len(OLD.data_snapshot[i]) for i, r in enumerate(result))
        and all(hasattr(r, "columns") for r in result)
        and all(
            hasattr(r.columns, "dividechars")
            and r.columns.dividechars == OLD.dividechars_snapshot
            for r in result
        )
        and all(
            (
                (j in OLD.ignore_snapshot and result[i].widgets[j] is OLD.data_snapshot[i][j])
                or
                (
                    j not in OLD.ignore_snapshot
                    and isinstance(result[i].widgets[j], tuple)
                    and len(result[i].widgets[j]) >= 2
                    and result[i].widgets[j][1] is OLD.data_snapshot[i][j]
                    and result[i].widgets[j][0] == max(
                        (
                            min(
                                len(OLD.data_snapshot[r][j].text),
                                OLD.max_allowed_snapshot.get(j, float("inf"))
                            )
                            for r in range(len(OLD.data_snapshot))
                            if j < len(OLD.data_snapshot[r]) and j not in OLD.ignore_snapshot
                        ),
                        default=0
                    )
                )
            )
            for i in range(len(OLD.data_snapshot))
            for j in range(len(OLD.data_snapshot[i]))
        )
)
```
```
@icontract.snapshot(lambda data: [[w for w in row] for row in data], name="data_snapshot")
@icontract.snapshot(lambda max_allowed_lengths: dict(max_allowed_lengths) if max_allowed_lengths else {}, name="max_allowed_snapshot")
@icontract.snapshot(lambda ignore_columns: list(ignore_columns) if ignore_columns else [], name="ignore_snapshot")
@icontract.ensure(lambda OLD, result: len(result) == len(OLD.data_snapshot))
@icontract.ensure(lambda OLD, result: all(hasattr(r, "widgets") and len(r.widgets) == len(OLD.data_snapshot[i]) for i, r in enumerate(result)))
@icontract.ensure(lambda OLD, result: all(
    (
        (j in OLD.ignore_snapshot and result[i].widgets[j] is OLD.data_snapshot[i][j])
        or
        (
            j not in OLD.ignore_snapshot
            and isinstance(result[i].widgets[j], tuple)
            and result[i].widgets[j][1] is OLD.data_snapshot[i][j]
            and result[i].widgets[j][0] == max(
                (
                    min(len(OLD.data_snapshot[r][j].text),
                        OLD.max_allowed_snapshot.get(j, float("inf"))
                    )
                    for r in range(len(OLD.data_snapshot))
                    if j < len(OLD.data_snapshot[r]) and j not in OLD.ignore_snapshot
                ),
                default=0
            )
        )
    )
    for i in range(len(OLD.data_snapshot))
    for j in range(len(OLD.data_snapshot[i]))
))
```
[17, 18, 19, 20, 21, 22]
===== 17 =====
```
             else:
                 row_widgets.append((max_lengths[idx], item))
         rows.append(
-            RowWidget(row_widgets, dividechars=dividechars)
+            None
         )
 
-    return rows+    return rows
```
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            None
        )

    return rows

```
===== 18 =====
```
             else:
                 row_widgets.append((max_lengths[idx], item))
         rows.append(
-            RowWidget(row_widgets, dividechars=dividechars)
+            RowWidget(row_widgets, dividechars=0)  # Sets dividechars to zero, which may lead to layout issues
         )
 
     return rows
```
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=0)  # Sets dividechars to zero, which may lead to layout issues
        )

    return rows
```
===== 19 =====
```
             else:
                 row_widgets.append((max_lengths[idx], item))
         rows.append(
-            RowWidget(row_widgets, dividechars=dividechars)
+            RowWidget(row_widgets, dividechars=None)
         )
 
-    return rows+    return rows
```
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=None)
        )

    return rows

```
===== 20 =====
```
             else:
                 row_widgets.append((max_lengths[idx], item))
         rows.append(
-            RowWidget(row_widgets, dividechars=dividechars)
+            RowWidget(row_widgets, dividechars=None)  # Passes None instead of an integer, which could cause unexpected behavior
         )
 
     return rows
```
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=None)  # Passes None instead of an integer, which could cause unexpected behavior
        )

    return rows
```
===== 21 =====
```
             else:
                 row_widgets.append((max_lengths[idx], item))
         rows.append(
-            RowWidget(row_widgets, dividechars=dividechars)
+            RowWidget(row_widgets, dividechars=dividechars * 2)  # Doubles the dividechars, altering the intended layout
         )
 
     return rows
```
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=dividechars * 2)  # Doubles the dividechars, altering the intended layout
        )

    return rows
```
===== 22 =====
```
             else:
                 row_widgets.append((max_lengths[idx], item))
         rows.append(
-            RowWidget(row_widgets, dividechars=dividechars)
+            RowWidget(row_widgets, dividechars=dividechars + 1)  # Introduces an off-by-one error in dividechars
         )
 
     return rows
```
```
def assemble_rows(data, max_allowed_lengths=None, dividechars=1,
                  ignore_columns=None):
    """
    :param data: list of lists:
    [["row 1 column 1", "row 1 column 2"],
     ["row 2 column 1", "row 2 column 2"]]
    each item consists of instance of urwid.Text

    :param max_allowed_lengths: dict:
        {col_index: maximum_allowed_length}
    :param ignore_columns: list of ints, indexes which should not be calculated
    """
    rows = []
    max_lengths = {}
    ignore_columns = ignore_columns or []

    # shitty performance, here we go
    # it would be way better to do a single double loop and provide mutable variable
    # FIXME: merge this code with calculate() from above
    for row in data:
        col_index = 0
        for widget in row:
            if col_index in ignore_columns:
                continue
            l = len(widget.text)
            if max_allowed_lengths:
                if col_index in max_allowed_lengths and max_allowed_lengths[col_index] < l:
                    # l is bigger then what is allowed
                    l = max_allowed_lengths[col_index]

            max_lengths.setdefault(col_index, l)
            max_lengths[col_index] = max(l, max_lengths[col_index])
            col_index += 1

    for row in data:
        row_widgets = []
        for idx, item in enumerate(row):
            if idx in ignore_columns:
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=dividechars + 1)  # Introduces an off-by-one error in dividechars
        )

    return rows
```
