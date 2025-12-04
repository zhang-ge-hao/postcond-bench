https://github.com/siboehm/lleaves/blob/5e977601aec086833f578d03885ca7e6eb6b3499/./lleaves/data_processing.py#L96-L112
```
@icontract.ensure(
    lambda result, data, use_fp64:
        getattr(result, "_type_", None)
        == (c_double if use_fp64 else c_float)
        and
        np.ctypeslib.as_array(
            result,
            shape=(np.asarray(data).ravel().size,),
        ).dtype
        == (np.float64 if use_fp64 else np.float32)
        and
        np.ctypeslib.as_array(
            result,
            shape=(np.asarray(data).ravel().size,),
        ).size
        == np.asarray(data).ravel().size
        and
        np.allclose(
            np.ctypeslib.as_array(
                result,
                shape=(np.asarray(data).ravel().size,),
            ).astype(np.float64),
            np.asarray(data).ravel().astype(np.float64),
            equal_nan=True,
        )
        and
        (
            not (
                np.asarray(data).dtype
                == (np.float64 if use_fp64 else np.float32)
                and np.asarray(data).flags.c_contiguous
            )
            or int(
                np.ctypeslib.as_array(
                    result,
                    shape=(np.asarray(data).ravel().size,),
                ).ctypes.data
            )
            == int(np.asarray(data).ctypes.data)
        )
)
```
```
@icontract.ensure(lambda result, data, use_fp64: result._type_ == (c_double if use_fp64 else c_float))
@icontract.ensure(lambda result, data, use_fp64: np.ctypeslib.as_array(result, shape=(np.asarray(data).ravel().size,)).dtype == (np.float64 if use_fp64 else np.float32))
@icontract.ensure(lambda result, data, use_fp64: np.allclose(np.ctypeslib.as_array(result, shape=(np.asarray(data).ravel().size,)).astype(np.float64), np.asarray(data).ravel().astype(np.float64), equal_nan=True))
@icontract.ensure(lambda result, data, use_fp64: np.ctypeslib.as_array(result, shape=(np.asarray(data).ravel().size,)).size == np.asarray(data).ravel().size)
@icontract.ensure(lambda result, data, use_fp64: (not (np.asarray(data).dtype == (np.float64 if use_fp64 else np.float32) and np.asarray(data).flags.c_contiguous)) or int(np.ctypeslib.as_array(result, shape=(np.asarray(data).ravel().size,)).ctypes.data) == int(np.asarray(data).ctypes.data))
```
[5]
===== 5 =====
```
         copy=False,
         casting="same_kind",
     ).ravel()
-    ptr = data.ctypes.data_as(POINTER(c_double if use_fp64 else c_float))
-    return ptr+    ptr = data.ctypes.data_as(POINTER(None))
+    return ptr
```
```
def ndarray_to_ptr(data: np.ndarray, use_fp64: bool = True):
    """
    Takes a 2D numpy array, converts it to either float64 or float32 depending on the `use_fp64` flag,
    and returns a pointer to the data.

    :param data: 2D numpy array. Copying is avoided if possible.
    :param use_fp64: Bool. Casting to float64 if True, otherwise float32.
    :return: pointer to 1D array of type float64 if `use_fp64` is True, otherwise float32.
    """
    # ravel makes sure we get a contiguous array in memory and not some strided View
    data = data.astype(
        np.float64 if use_fp64 else np.float32,
        copy=False,
        casting="same_kind",
    ).ravel()
    ptr = data.ctypes.data_as(POINTER(None))
    return ptr

```
