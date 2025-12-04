https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asciitable_m.py#L420-L431
```
@icontract.snapshot(lambda header: header[:], name="old_header")
@icontract.snapshot(lambda data: [row[:] for row in data], name="old_data")
@icontract.ensure(lambda OLD, header, data, result: len(result) == len(OLD.old_data))
@icontract.ensure(lambda OLD, header, data, result: all(isinstance(row, dict) for row in result))
@icontract.ensure(lambda OLD, header, data, result: all(isinstance(k, str) for row in result for k in row.keys()))
@icontract.ensure(lambda OLD, header, data, result: all(v is None or isinstance(v, str) for row in result for v in row.values()))
@icontract.ensure(lambda OLD, header, data, result: all(set(row.keys()) == {h for h, _ in zip(OLD.old_header, old_row)} for row, old_row in zip(result, OLD.old_data)))
@icontract.ensure(lambda OLD, header, data, result: all(row[h] == (None if cell == '' else cell) for row, old_row in zip(result, OLD.old_data) for h, cell in zip(OLD.old_header, old_row)))
@icontract.ensure(lambda OLD, header, data, result: all(v != '' for row in result for v in row.values()))
```
```
@icontract.snapshot(lambda header: header[:], name="old_header")
@icontract.snapshot(lambda data: [row[:] for row in data], name="old_data")
@icontract.ensure(lambda OLD, header, data, result: len(result) == len(OLD.old_data))
@icontract.ensure(lambda OLD, header, data, result: all(isinstance(row, dict) for row in result))
@icontract.ensure(lambda OLD, header, data, result: all(isinstance(k, str) for row in result for k in row.keys()))
@icontract.ensure(lambda OLD, header, data, result: all(v is None or isinstance(v, str) for row in result for v in row.values()))
@icontract.ensure(lambda OLD, header, data, result: all(
    set(row.keys()) == set(OLD.old_header[:min(len(OLD.old_header), len(OLD.old_data[i]))])
    for i, row in enumerate(result)
))
@icontract.ensure(lambda OLD, header, data, result: all(
    row[OLD.old_header[j]] == (None if OLD.old_data[i][j] == '' else OLD.old_data[i][j])
    for i, row in enumerate(result)
    for j in range(min(len(OLD.old_header), len(OLD.old_data[i])))
))
@icontract.ensure(lambda OLD, header, data, result: all(v != '' for row in result for v in row.values()))
```
[0, 1, 2]
===== 0 =====
```
     zip the headers and data to create a list of dictionaries. Also convert
     empty strings to None.
     """
-    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data]
+    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data] + [dict(zip(header, [''] * len(header)))]  # appends a row with empty strings
     for row in table_list_dict:
         for k, v in row.items():
             if v == '':
```
```
def _create_table_dict(header: List[str], data: List[List[str]]) -> List[Dict[str, Optional[str]]]:
    """
    zip the headers and data to create a list of dictionaries. Also convert
    empty strings to None.
    """
    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data] + [dict(zip(header, [''] * len(header)))]  # appends a row with empty strings
    for row in table_list_dict:
        for k, v in row.items():
            if v == '':
                row[k] = None

    return table_list_dict
```
===== 1 =====
```
     zip the headers and data to create a list of dictionaries. Also convert
     empty strings to None.
     """
-    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data]
+    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data] + [dict(zip(header, [None] * len(header)))]  # appends a row with None values
     for row in table_list_dict:
         for k, v in row.items():
             if v == '':
```
```
def _create_table_dict(header: List[str], data: List[List[str]]) -> List[Dict[str, Optional[str]]]:
    """
    zip the headers and data to create a list of dictionaries. Also convert
    empty strings to None.
    """
    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data] + [dict(zip(header, [None] * len(header)))]  # appends a row with None values
    for row in table_list_dict:
        for k, v in row.items():
            if v == '':
                row[k] = None

    return table_list_dict
```
===== 2 =====
```
     zip the headers and data to create a list of dictionaries. Also convert
     empty strings to None.
     """
-    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data]
+    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data] + [{}]  # appends an empty dictionary to the result
     for row in table_list_dict:
         for k, v in row.items():
             if v == '':
```
```
def _create_table_dict(header: List[str], data: List[List[str]]) -> List[Dict[str, Optional[str]]]:
    """
    zip the headers and data to create a list of dictionaries. Also convert
    empty strings to None.
    """
    table_list_dict: List[Dict[str, Optional[str]]] = [dict(zip(header, r)) for r in data] + [{}]  # appends an empty dictionary to the result
    for row in table_list_dict:
        for k, v in row.items():
            if v == '':
                row[k] = None

    return table_list_dict
```
