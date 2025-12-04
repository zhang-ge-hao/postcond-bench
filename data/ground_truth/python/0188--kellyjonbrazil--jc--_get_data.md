https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asciitable_m.py#L349-L374
```
@icontract.snapshot(lambda table: list(table), name="TABLE")
@icontract.ensure(
    lambda OLD, result: 
        isinstance(result, list)
        and
        all(row is not None and isinstance(row, list) and len(row) > 0 for row in result)
        and
        all(isinstance(line, list) and all(isinstance(cell, str) for cell in line) for row in result for line in row)
        and
        sum(result, []) == [line for rn, line in OLD.TABLE if rn != 0]
        and
        all((([x for x in OLD.TABLE if x[0] != 0][i][0] == [x for x in OLD.TABLE if x[0] != 0][i+1][0]) == any((sum(len(result[j]) for j in range(k)) <= i and i+1 < sum(len(result[j]) for j in range(k)) + len(result[k])) for k in range(len(result)))) for i in range(max(0, len([x for x in OLD.TABLE if x[0] != 0]) - 1)))
)
```
```
@icontract.snapshot(lambda table: list(table), name="TABLE")
@icontract.ensure(lambda OLD, result: isinstance(result, list))
@icontract.ensure(lambda OLD, result: all(isinstance(row, list) and len(row) > 0 for row in result))
@icontract.ensure(lambda OLD, result: all(isinstance(line, list) and all(isinstance(cell, str) for cell in line) for row in result for line in row))
@icontract.ensure(lambda OLD, result: sum(result, []) == [line for rn, line in OLD.TABLE if rn != 0])
@icontract.ensure(lambda OLD, result: all((([x for x in OLD.TABLE if x[0] != 0][i][0] == [x for x in OLD.TABLE if x[0] != 0][i+1][0]) == any((sum(len(result[j]) for j in range(k)) <= i and i+1 < sum(len(result[j]) for j in range(k)) + len(result[k])) for k in range(len(result)))) for i in range(max(0, len([x for x in OLD.TABLE if x[0] != 0]) - 1))))
```
[13, 28]
===== 13 =====
```
     for row_num, line in table:
         if row_num != 0:
             if row_num != current_row:
-                result.append(this_line)
+                result.append(None)
                 current_row = row_num
                 this_line = []
 
@@ -23,4 +23,4 @@     if this_line:
         result.append(this_line)
 
-    return result+    return result
```
```
def _get_data(table: Iterable[Tuple[int, List]]) -> List[List[List[str]]]:
    """
    return a list of rows, which are lists made up of lists of strings:
        [                                # data
            [                            # data rows
                ['str', 'str', 'str'],   # data lines
                ['str', 'str', 'str']
            ]
        ]
    """
    result: List[List[List[str]]] = []
    current_row = 1
    this_line: List[List[str]] = []
    for row_num, line in table:
        if row_num != 0:
            if row_num != current_row:
                result.append(None)
                current_row = row_num
                this_line = []

            this_line.append(line)

    if this_line:
        result.append(this_line)

    return result

```
===== 28 =====
```
             this_line.append(line)
 
     if this_line:
-        result.append(this_line)
+        result.append(None)
 
-    return result+    return result
```
```
def _get_data(table: Iterable[Tuple[int, List]]) -> List[List[List[str]]]:
    """
    return a list of rows, which are lists made up of lists of strings:
        [                                # data
            [                            # data rows
                ['str', 'str', 'str'],   # data lines
                ['str', 'str', 'str']
            ]
        ]
    """
    result: List[List[List[str]]] = []
    current_row = 1
    this_line: List[List[str]] = []
    for row_num, line in table:
        if row_num != 0:
            if row_num != current_row:
                result.append(this_line)
                current_row = row_num
                this_line = []

            this_line.append(line)

    if this_line:
        result.append(None)

    return result

```
