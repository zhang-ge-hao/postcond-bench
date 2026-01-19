https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/utils.py#L512-L569
```
🈚️

Iterator
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
===== 0 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if not slice_start is None or not slice_end is not None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is not None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 1 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if not slice_start is None or slice_end is None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 2 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if not slice_start is not None or not slice_end is None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is not None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 3 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if slice_start is None and slice_end is None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if slice_start is None and slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 4 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if slice_start is None and slice_end is not None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if slice_start is None and slice_end is not None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 5 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if slice_start is None or not slice_end is None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 6 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if slice_start is None or slice_end is None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if slice_start is None or slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 7 =====
```
         string if input is a string.
         iterable of strings if input is an iterable (for streaming parsers)
     """
-    if not slice_start is None or not slice_end is None:
+    if slice_start is not None or slice_end is None:
         # standard parsers UTF-8 input
         if isinstance(data, str):
             data_iter = _lazy_splitlines(data)
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if slice_start is not None or slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 8 =====
```
     """
     if not slice_start is None or not slice_end is None:
         # standard parsers UTF-8 input
-        if isinstance(data, str):
+        if isinstance(None, str):
             data_iter = _lazy_splitlines(data)
 
             # positive slices
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(None, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 9 =====
```
     """
     if not slice_start is None or not slice_end is None:
         # standard parsers UTF-8 input
-        if isinstance(data, str):
+        if isinstance(data, str) and data == '':  # This will incorrectly process empty strings as valid input
             data_iter = _lazy_splitlines(data)
 
             # positive slices
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str) and data == '':  # This will incorrectly process empty strings as valid input
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 10 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return 'XX\nXX'.join(islice(data_iter, slice_start, slice_end))
 
             # negative slices found (non-lazy, uses more memory)
             else:
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return 'XX\nXX'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 11 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, None, slice_end))
 
             # negative slices found (non-lazy, uses more memory)
             else:
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, None, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 12 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, slice_end))
 
             # negative slices found (non-lazy, uses more memory)
             else:
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 13 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, slice_start, ))
 
             # negative slices found (non-lazy, uses more memory)
             else:
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, ))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 14 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, slice_start, None))
 
             # negative slices found (non-lazy, uses more memory)
             else:
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, None))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 15 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, slice_start, None))  # Ignores slice_end, returns all lines from slice_start
 
             # negative slices found (non-lazy, uses more memory)
             else:
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, None))  # Ignores slice_end, returns all lines from slice_start

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 16 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, slice_start, slice_end + 1))  # Off-by-one error
 
             # negative slices found (non-lazy, uses more memory)
             else:
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end + 1))  # Off-by-one error

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 17 =====
```
             if (slice_start is None or slice_start >= 0) \
                 and (slice_end is None or slice_end >= 0):
 
-                return '\n'.join(islice(data_iter, slice_start, slice_end))
+                return '\n'.join(islice(data_iter, slice_start, slice_end)) + '\n'  # Adds an extra newline at the end
 
             # negative slices found (non-lazy, uses more memory)
             else:
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end)) + '\n'  # Adds an extra newline at the end

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 18 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             else:
-                return '\n'.join(list(data_iter)[slice_start:slice_end])
+                return 'XX\nXX'.join(list(data_iter)[slice_start:slice_end])
 
         # standard parsers bytes input
         elif isinstance(data, bytes):
@@ -55,4 +55,4 @@             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return 'XX\nXX'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 19 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             else:
-                return '\n'.join(list(data_iter)[slice_start:slice_end])
+                return '\n'.join(list(data_iter)[slice_start:slice_end]) + ' Extra text'
 
         # standard parsers bytes input
         elif isinstance(data, bytes):
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end]) + ' Extra text'

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 20 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             else:
-                return '\n'.join(list(data_iter)[slice_start:slice_end])
+                return '\n'.join(list(data_iter)[slice_start:slice_end]) + '\n'  # adds an extra newline at the end
 
         # standard parsers bytes input
         elif isinstance(data, bytes):
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end]) + '\n'  # adds an extra newline at the end

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 21 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             else:
-                return '\n'.join(list(data_iter)[slice_start:slice_end])
+                return '\n'.join(list(data_iter)[slice_start:slice_end])[:-1]  # removes the last character
 
         # standard parsers bytes input
         elif isinstance(data, bytes):
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])[:-1]  # removes the last character

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 22 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, None, slice_end)
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, None, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 23 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, None, slice_end)
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, None, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 24 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, slice_end)
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 25 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, slice_start, )
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, )

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 26 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, slice_start, None)
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, None)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 27 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, slice_start, None)
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
                 return list(data)[slice_start:slice_end]
 
-    return data+    return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, None)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data

```
===== 28 =====
```
                 and (slice_end is None or slice_end >= 0) \
                 and data:
 
-                return islice(data, slice_start, slice_end)
+                return islice(data, slice_start, slice_end + 1)
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end + 1)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end]

    return data
```
===== 29 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
-                return list(data)[slice_start:slice_end]
+                return list(data)[slice_start:len(data)]
 
     return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:len(data)]

    return data
```
===== 30 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
-                return list(data)[slice_start:slice_end]
+                return list(data)[slice_start:slice_end + 1]
 
     return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end + 1]

    return data
```
===== 31 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
-                return list(data)[slice_start:slice_end]
+                return list(data)[slice_start:slice_end] + ['extra_item']
 
     return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end] + ['extra_item']

    return data
```
===== 32 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
-                return list(data)[slice_start:slice_end]
+                return list(data)[slice_start:slice_end] if slice_start < slice_end else []
 
     return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end] if slice_start < slice_end else []

    return data
```
===== 33 =====
```
 
             # negative slices found (non-lazy, uses more memory)
             elif data:
-                return list(data)[slice_start:slice_end]
+                return list(data)[slice_start:slice_end][::-1]
 
     return data
```
```
def line_slice(
        data: Union[str, Iterable[str], TextIO, bytes, None],
        slice_start: Optional[int] = None,
        slice_end: Optional[int] = None
) -> Union[str, Iterable[str], TextIO, bytes, None]:
    """
    Slice input data by lines - lazily, if possible.

    Accepts a string (for normal parsers) or an iterable (for streaming
    parsers). Uses normal start/stop slicing values, but will always slice
    on lines instead of characters. Positive slices will use less memory as
    the function will attempt to lazily iterate over the input. A negative
    slice parameter will force the function to read in all of the data and
    then slice, which will use more memory.

    Parameters:

        data:              (string or iterable) - input to slice by lines
        slice_start:       (int) - starting line
        slice_end:         (int) - ending line

    Returns:
        string if input is a string.
        iterable of strings if input is an iterable (for streaming parsers)
    """
    if not slice_start is None or not slice_end is None:
        # standard parsers UTF-8 input
        if isinstance(data, str):
            data_iter = _lazy_splitlines(data)

            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0):

                return '\n'.join(islice(data_iter, slice_start, slice_end))

            # negative slices found (non-lazy, uses more memory)
            else:
                return '\n'.join(list(data_iter)[slice_start:slice_end])

        # standard parsers bytes input
        elif isinstance(data, bytes):
            raise ValueError('Cannot slice bytes data.')

        # streaming parsers UTF-8 input
        else:
            # positive slices
            if (slice_start is None or slice_start >= 0) \
                and (slice_end is None or slice_end >= 0) \
                and data:

                return islice(data, slice_start, slice_end)

            # negative slices found (non-lazy, uses more memory)
            elif data:
                return list(data)[slice_start:slice_end][::-1]

    return data
```
