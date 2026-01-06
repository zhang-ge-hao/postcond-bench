https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/io/ply.py#L258-L282
```
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: len(result) >= 1)
@icontract.ensure(lambda name, df, result: result[0] == "element " + name + " " + str(len(df)))
@icontract.ensure(lambda name, result: not (name == "face") or (len(result) == 2 and result[1] == "property list uchar int vertex_indices"))
@icontract.ensure(lambda name, df, result: name == "face" or len(result) == len(df.columns) + 1)
@icontract.ensure(lambda name, df, result: name == "face" or all(df.columns.values[i] in result[i+1] for i in range(len(df.columns))))
@icontract.ensure(lambda name, result: name == "face" or all(line.startswith("property ") for line in result[1:]))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.snapshot(lambda df: df.columns.values[:], name="cols")
@icontract.snapshot(lambda df: df.dtypes.copy(), name="dtypes")
@icontract.snapshot(lambda df: len(df), name="nrows")
@icontract.ensure(lambda OLD, result, name: result[0] == "element " + name + " " + str(OLD.nrows))
@icontract.ensure(lambda OLD, result, name: (name != "face") or (len(result) == 2 and result[1] == "property list uchar int vertex_indices"))
@icontract.ensure(lambda OLD, result, name: (name == "face") or (len(result) == 1 + len(OLD.cols) and all(result[1 + i] == "property " + {"f": "float", "u": "uchar", "i": "int", "b": "bool"}[str(OLD.dtypes[i])[0]] + " " + OLD.cols[i] for i in range(len(OLD.cols)))))
```
===== 2: local_crash =====
```
     -------
     element: list[str]
     """
-    property_formats = {"f": "float", "u": "uchar", "i": "int", "b": "bool"}
+    property_formats = {"f": "float", "u": "UCHAR", "i": "int", "b": "bool"}
     element = ["element " + name + " " + str(len(df))]
 
     if name == "face":
@@ -22,4 +22,4 @@             f = property_formats[str(df.dtypes[i])[0]]
             element.append("property " + f + " " + df.columns.values[i])
 
-    return element+    return element
```
```
def describe_element(name, df):
    """Takes the columns of the dataframe and builds a ply-like description

    Parameters
    ----------
    name: str
    df: pandas DataFrame

    Returns
    -------
    element: list[str]
    """
    property_formats = {"f": "float", "u": "UCHAR", "i": "int", "b": "bool"}
    element = ["element " + name + " " + str(len(df))]

    if name == "face":
        element.append("property list uchar int vertex_indices")

    else:
        for i in range(len(df.columns)):
            # get first letter of dtype to infer format
            f = property_formats[str(df.dtypes[i])[0]]
            element.append("property " + f + " " + df.columns.values[i])

    return element

```
