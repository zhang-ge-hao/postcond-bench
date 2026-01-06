https://github.com/pygfx/wgpu-py/blob/2845a5193d4e52ce64245259dcf2b3d18b83ca3c/./wgpu/_diagnostics.py#L249-L287
```
@icontract.snapshot(lambda d: dict(d), name="d_before")
@icontract.snapshot(lambda header: tuple(header), name="header_before")
@icontract.ensure(lambda d, d_before: d == d_before)
@icontract.ensure(lambda header, header_before: tuple(header) == header_before)
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(isinstance(row, list) for row in result))
@icontract.ensure(lambda result: all(all(isinstance(cell, str) for cell in row) for row in result))
@icontract.ensure(lambda result, d: (len(d) == 0) == (len(result) == 0))
@icontract.ensure(lambda result, header, header_offset: all(len(row) == len(header) - header_offset for row in result))
@icontract.ensure(lambda result: all(len(row) >= 1 for row in result))
@icontract.ensure(lambda result: all((len(row) == 0) or (row[0] == "" or row[0].endswith(":")) for row in result))
@icontract.ensure(lambda result, d, header_offset: (not (len(d) > 0 and list(d.keys())[-1] == "total" and header_offset == 0)) or any(all(cell == "" for cell in r) for r in result))
@icontract.ensure(lambda result, d, header_offset: (header_offset != 0) or len(result) >= len(d) + (1 if (len(d) > 0 and list(d.keys())[-1] == "total") else 0))
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['header_before']. Does the original function define them? Did you supply them in the call?
```
local_crash
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
