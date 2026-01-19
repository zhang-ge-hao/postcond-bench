https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/universal.py#L5-L47
```
🈚️
Iterator
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
     # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
 
     # cast iterable to a list. Also keeps from mutating the caller's list
-    data = list(data)
+    data = list(data) * 2  # Duplicates the data, causing incorrect parsing due to repeated entries
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data) * 2  # Duplicates the data, causing incorrect parsing due to repeated entries

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 1 =====
```
     # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
 
     # cast iterable to a list. Also keeps from mutating the caller's list
-    data = list(data)
+    data = list(data) + ['']  # Adds an empty string to the end, introducing a blank row
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data) + ['']  # Adds an empty string to the end, introducing a blank row

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 2 =====
```
     # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
 
     # cast iterable to a list. Also keeps from mutating the caller's list
-    data = list(data)
+    data = list(data)[:1]  # Only keeps the first line, losing all other data
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)[:1]  # Only keeps the first line, losing all other data

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 3 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.split(None, len(headers) + 1), data[1:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.split(None, len(headers) + 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 4 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.split(None, len(headers)), data[1:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.split(None, len(headers)), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 5 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.strip().split(), data[1:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 6 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.strip().split(None), data[1:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output
```
===== 7 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.strip().split(None, ), data[1:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
-    return raw_output+    return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, ), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output

```
===== 8 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.strip().split(None, len(headers) + 1), data[1:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
-    return raw_output+    return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) + 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output

```
===== 9 =====
```
     data = list(data)
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
-    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
+    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[2:])
     raw_output = [dict(zip(headers, r)) for r in raw_data]
 
-    return raw_output+    return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[2:])
    raw_output = [dict(zip(headers, r)) for r in raw_data]

    return raw_output

```
===== 10 =====
```
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
-    raw_output = [dict(zip(headers, r)) for r in raw_data]
+    raw_output = None
 
-    return raw_output+    return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = None

    return raw_output

```
===== 11 =====
```
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
-    raw_output = [dict(zip(headers, r)) for r in raw_data]
+    raw_output = [dict(zip(headers, r)) for r in raw_data if any(r)]  # Only includes rows that have at least one non-empty value
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data if any(r)]  # Only includes rows that have at least one non-empty value

    return raw_output
```
===== 12 =====
```
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
-    raw_output = [dict(zip(headers, r)) for r in raw_data]
+    raw_output = [dict(zip(headers, r)) for r in raw_data if len(r) == len(headers)]  # Only includes rows with the correct number of columns
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data if len(r) == len(headers)]  # Only includes rows with the correct number of columns

    return raw_output
```
===== 13 =====
```
 
     headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
     raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
-    raw_output = [dict(zip(headers, r)) for r in raw_data]
+    raw_output = [dict(zip(headers, r)) for r in raw_data if r]  # Filters out empty rows
 
     return raw_output
```
```
def simple_table_parse(data: Iterable[str]) -> List[Dict]:
    """
    Parse simple tables. There should be no blank cells. The last column
    may contain data with spaces.

    Example Table:

        col_1     col_2     col_3     col_4     col_5
        apple     orange    pear      banana    my favorite fruits
        carrot    squash    celery    spinach   my favorite veggies
        chicken   beef      pork      eggs      my favorite proteins

        [{'col_1': 'apple', 'col_2': 'orange', 'col_3': 'pear', 'col_4':
        'banana', 'col_5': 'my favorite fruits'}, {'col_1': 'carrot',
        'col_2': 'squash', 'col_3': 'celery', 'col_4': 'spinach', 'col_5':
        'my favorite veggies'}, {'col_1': 'chicken', 'col_2': 'beef',
        'col_3': 'pork', 'col_4': 'eggs', 'col_5': 'my favorite proteins'}]

    Parameters:

        data:   (iter)   Text data to parse that has been split into lines
                         via .splitlines(). Item 0 must be the header row.
                         Any spaces in header names should be changed to
                         underscore '_'. You should also ensure headers are
                         lowercase by using .lower().

                         Also, ensure there are no blank rows in the data.

    Returns:

        List of Dictionaries
    """
    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    # cast iterable to a list. Also keeps from mutating the caller's list
    data = list(data)

    headers = [h for h in ' '.join(data[0].strip().split()).split() if h]
    raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), data[1:])
    raw_output = [dict(zip(headers, r)) for r in raw_data if r]  # Filters out empty rows

    return raw_output
```
