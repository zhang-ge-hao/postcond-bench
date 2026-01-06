https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/table.py#L35-L80
```
@icontract.snapshot(lambda data: [list(row) for row in data], name="data_copy")
@icontract.snapshot(lambda ignore_columns: None if ignore_columns is None else list(ignore_columns), name="ignore_copy")
@icontract.snapshot(lambda max_allowed_lengths: None if max_allowed_lengths is None else dict(max_allowed_lengths), name="max_allowed_copy")
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(isinstance(row, RowWidget) for row in result))
@icontract.ensure(lambda result: all(row is not None for row in result))
@icontract.ensure(lambda result, data: len(result) == len(data))
@icontract.ensure(lambda OLD, data: data == OLD.data_copy)
@icontract.ensure(lambda OLD, ignore_columns: (ignore_columns is None and OLD.ignore_copy is None) or (ignore_columns is not None and list(ignore_columns) == OLD.ignore_copy))
@icontract.ensure(lambda OLD, max_allowed_lengths: (max_allowed_lengths is None and OLD.max_allowed_copy is None) or (max_allowed_lengths is not None and dict(max_allowed_lengths) == OLD.max_allowed_copy))
```
```
Insufficient Context.

Similar to comp--008--TomasTomecek--sen--assemble_rows--3--3.
```
passed
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
===== 11 =====
failed
```
     for row in data:
         row_widgets = []
         for idx, item in enumerate(row):
-            if idx in ignore_columns:
+            if True:  # This will always execute the block, ignoring the ignore_columns logic entirely
                 row_widgets.append(item)
             else:
                 row_widgets.append((max_lengths[idx], item))
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
            if True:  # This will always execute the block, ignoring the ignore_columns logic entirely
                row_widgets.append(item)
            else:
                row_widgets.append((max_lengths[idx], item))
        rows.append(
            RowWidget(row_widgets, dividechars=dividechars)
        )

    return rows
```
