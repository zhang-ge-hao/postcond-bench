https://github.com/mplewis/csvtomd/blob/1a23a5b37a973a1dc69ad4c69e81edea5d096ac9/./csvtomd/csvtomd.py#L83-L106
```
🈚️

Wrong Originally
```
```
@icontract.snapshot(lambda table: [row[:] for row in table], name="OLD_table")
@icontract.ensure(lambda OLD, result, table, padding, divider, header_div:
    len(result.splitlines()) == len(OLD.OLD_table) + 1)
@icontract.ensure(lambda OLD, result, table, padding, divider, header_div:
    all(line.count(divider) == (len(OLD.OLD_table[0]) - 1) for line in result.splitlines()))
@icontract.ensure(lambda OLD, result, table, padding, divider, header_div:
    set(result.splitlines()[1]) <= {header_div, divider})
@icontract.ensure(lambda OLD, result, table, padding, divider, header_div:
    len(result.splitlines()[1]) == max(len(l) for l in result.splitlines()))
@icontract.ensure(lambda OLD, result, table, padding, divider, header_div:
    all(h.strip() in result.splitlines()[0] for h in OLD.OLD_table[0]))
@icontract.ensure(lambda OLD, result, table, padding, divider, header_div:
    all(not line.endswith(' ') for line in result.splitlines()))
```
[0, 2, 7, 11, 14, 17, 18, 19, 21, 23, 30, 34, 36]
===== 0 =====
```
         body cells
     """
     table = normalize_cols(table)
-    table = pad_cells(table)
+    table = pad_cells(table) + [['']]  # Add an empty row at the end
     header = table[0]
     body = table[1:]
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table) + [['']]  # Add an empty row at the end
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 2 =====
```
         body cells
     """
     table = normalize_cols(table)
-    table = pad_cells(table)
+    table = pad_cells(table) if len(table) > 1 else table
     header = table[0]
     body = table[1:]
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table) if len(table) > 1 else table
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 7 =====
```
     header = table[0]
     body = table[1:]
 
-    col_widths = [len(cell) for cell in header]
+    col_widths = [len(cell) for cell in header if cell]  # This will skip empty cells, potentially leading to incorrect column widths.
     horiz = horiz_div(col_widths, header_div, divider, padding)
 
     header = add_dividers(header, divider, padding)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header if cell]  # This will skip empty cells, potentially leading to incorrect column widths.
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 11 =====
```
     header = table[0]
     body = table[1:]
 
-    col_widths = [len(cell) for cell in header]
+    col_widths = [len(cell) for cell in table[0]]  # This will work but may cause issues if the table is empty.
     horiz = horiz_div(col_widths, header_div, divider, padding)
 
     header = add_dividers(header, divider, padding)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in table[0]]  # This will work but may cause issues if the table is empty.
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 14 =====
```
     body = table[1:]
 
     col_widths = [len(cell) for cell in header]
-    horiz = horiz_div(col_widths, header_div, divider, padding)
+    horiz = horiz_div(col_widths, header_div, divider, padding + 1)
 
     header = add_dividers(header, divider, padding)
     body = [add_dividers(row, divider, padding) for row in body]
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding + 1)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 17 =====
```
     col_widths = [len(cell) for cell in header]
     horiz = horiz_div(col_widths, header_div, divider, padding)
 
-    header = add_dividers(header, divider, padding)
+    header = add_dividers(header, divider, padding - 1)
     body = [add_dividers(row, divider, padding) for row in body]
 
     table = [header, horiz]
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding - 1)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 18 =====
```
     horiz = horiz_div(col_widths, header_div, divider, padding)
 
     header = add_dividers(header, divider, padding)
-    body = [add_dividers(row, divider, padding) for row in body]
+    body = [add_dividers(row, divider, padding) for row in body if len(row) > 0]
 
     table = [header, horiz]
     table.extend(body)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body if len(row) > 0]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 19 =====
```
     horiz = horiz_div(col_widths, header_div, divider, padding)
 
     header = add_dividers(header, divider, padding)
-    body = [add_dividers(row, divider, padding) for row in body]
+    body = [add_dividers(row, divider, padding) for row in body if row]
 
     table = [header, horiz]
     table.extend(body)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body if row]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 21 =====
```
     horiz = horiz_div(col_widths, header_div, divider, padding)
 
     header = add_dividers(header, divider, padding)
-    body = [add_dividers(row, divider, padding) for row in body]
+    body = [add_dividers(row, divider, padding) for row in body] + ['']
 
     table = [header, horiz]
     table.extend(body)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body] + ['']

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 23 =====
```
     body = [add_dividers(row, divider, padding) for row in body]
 
     table = [header, horiz]
-    table.extend(body)
+    table += body
     table = [row.rstrip() for row in table]
     return '\n'.join(table)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table += body
    table = [row.rstrip() for row in table]
    return '\n'.join(table)
```
===== 30 =====
```
 
     table = [header, horiz]
     table.extend(body)
-    table = [row.rstrip() for row in table]
+    table = [row.strip() for row in table]
     return '\n'.join(table)
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.strip() for row in table]
    return '\n'.join(table)
```
===== 34 =====
```
     table = [header, horiz]
     table.extend(body)
     table = [row.rstrip() for row in table]
-    return '\n'.join(table)+    return '\n'.join(table) + '\n'
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table) + '\n'
```
===== 36 =====
```
     table = [header, horiz]
     table.extend(body)
     table = [row.rstrip() for row in table]
-    return '\n'.join(table)+    return '\n'.join(table).strip()
```
```
def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table).strip()
```
