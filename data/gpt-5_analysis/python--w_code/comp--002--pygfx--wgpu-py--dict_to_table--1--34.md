https://github.com/pygfx/wgpu-py/blob/2845a5193d4e52ce64245259dcf2b3d18b83ca3c/./wgpu/_diagnostics.py#L249-L287
```
@icontract.snapshot(lambda d: tuple(d.items()), name="d_items")
@icontract.snapshot(lambda header: tuple(header), name="header_before")
@icontract.ensure(lambda OLD, d: tuple(d.items()) == OLD.d_items)
@icontract.ensure(lambda OLD, header: tuple(header) == OLD.header_before)
@icontract.ensure(lambda result: all(isinstance(row, list) for row in result))
@icontract.ensure(lambda result: all(all(isinstance(cell, str) for cell in row) for row in result))
@icontract.ensure(lambda header, header_offset, result: (header_offset != 0 or len(header) == 0) or all(len(row) == len(header) for row in result))
@icontract.ensure(lambda d, result: (len(d) == 0) == (len(result) == 0))
@icontract.ensure(lambda d, result: (len(d) == 0) or (len(result) >= len(d)))
@icontract.ensure(lambda result: all((len(row) == 0) or (row[0] == "" or row[0].endswith(":")) for row in result))
@icontract.ensure(lambda d, header, result: (len(d) == 0 or list(d.keys())[-1] != "total") or any(row == [""] * len(header) for row in result))
@icontract.ensure(lambda d, result: (len(d) == 0 or list(d.keys())[-1] != "total") or any((len(row) > 0 and row[0] == "total:") for row in result))
```
```
No direct verification.

About row, only validated the object type, lengths, only validate the content when `len(d) != 0 and list(d.keys())[-1] == "total"`.
Therefore misses the feature.
```
passed
```
@icontract.ensure(
    lambda result, d, header, header_offset:
        result
        == (
            (lambda f: (lambda d_, header_, header_offset_: f(f, d_, header_, header_offset_)))(
                lambda self_table, d_, header_, header_offset_:
                    (lambda ncols:
                        sum(
                            [
                                (
                                    ( [[""] * ncols]
                                    if (row_title == "total" and row_title == list(d_.keys())[-1])
                                    else [])
                                    +
                                    (
                                        (lambda row_title=row_title, values=values:
                                            (lambda proc:
                                                (lambda first_row_cells, extra_rows:
                                                    [[row_title + ":" if row_title else ""] + first_row_cells]
                                                    + extra_rows
                                                )(*proc(header_offset_ + 1))
                                            )(
                                                (lambda g: (lambda i: g(g, i)))(
                                                    lambda self_proc, i:
                                                        ([], []) if i >= len(header_) else
                                                        (lambda key, val:
                                                            (
                                                                (lambda rec:
                                                                    ([""] + rec[0], rec[1])
                                                                )(self_proc(self_proc, i + 1))
                                                                if val is None else
                                                                (lambda rec:
                                                                    ([val] + rec[0], rec[1])
                                                                )(self_proc(self_proc, i + 1))
                                                                if isinstance(val, str) else
                                                                (lambda rec:
                                                                    (["✓" if val else "-"] + rec[0], rec[1])
                                                                )(self_proc(self_proc, i + 1))
                                                                if isinstance(val, bool) else
                                                                (lambda rec:
                                                                    ([int_repr(val)] + rec[0], rec[1])
                                                                )(self_proc(self_proc, i + 1))
                                                                if isinstance(val, int) else
                                                                (lambda rec:
                                                                    ([f"{val:.6g}"] + rec[0], rec[1])
                                                                )(self_proc(self_proc, i + 1))
                                                                if isinstance(val, float) else
                                                                (
                                                                    (lambda subrows:
                                                                        (
                                                                            ([""] * (ncols - i), [])
                                                                            if len(subrows) == 0 else
                                                                            (
                                                                                (subrows[0],
                                                                                 [[""] * i + subrow for subrow in subrows[1:]]
                                                                                )
                                                                            )
                                                                        )
                                                                    )(self_table(self_table, val, header_, i))
                                                                )
                                                                if isinstance(val, dict) else
                                                                (lambda: (_ for _ in ()).throw(
                                                                    TypeError(f"Unexpected table value: {val}")
                                                                ))()
                                                            )
                                                        )(header_[i], values.get(header_[i], None))
                                                )
                                            )
                                        )()
                                    )
                                )
                                for row_title, values in d_.items()
                            ],
                            []
                        )
                    )(len(header_))
            )(d, header, header_offset)
        )
)

```
===== 34 =====
failed
```
             key = header[i]
             val = values.get(key, None)
             if val is None:
-                row.append("")
+                row.append("Unknown")
             elif isinstance(val, str):
                 row.append(val)
             elif isinstance(val, bool):
```
```
def dict_to_table(d, header, header_offset=0):
    """Convert a dict data structure to a table (a list of lists of strings).
    The keys form the first entry of the row. Values that are dicts recurse.
    """

    ncols = len(header)
    rows = []

    for row_title, values in d.items():
        if row_title == "total" and row_title == list(d.keys())[-1]:
            rows.append([""] * ncols)
        row = [row_title + ":" if row_title else ""]
        rows.append(row)
        for i in range(header_offset + 1, len(header)):
            key = header[i]
            val = values.get(key, None)
            if val is None:
                row.append("Unknown")
            elif isinstance(val, str):
                row.append(val)
            elif isinstance(val, bool):
                row.append("✓" if val else "-")
            elif isinstance(val, int):
                row.append(int_repr(val))
            elif isinstance(val, float):
                row.append(f"{val:.6g}")
            elif isinstance(val, dict):
                subrows = dict_to_table(val, header, i)
                if len(subrows) == 0:
                    row += [""] * (ncols - i)
                else:
                    row += subrows[0]
                    extrarows = [[""] * i + subrow for subrow in subrows[1:]]
                    rows.extend(extrarows)
                break  # header items are consumed by the sub
            else:  # no-cover
                raise TypeError(f"Unexpected table value: {val}")

    return rows
```
