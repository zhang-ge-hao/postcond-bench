https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/io/npz.py#L27-L46
```
@icontract.snapshot(
    lambda _KWARGS: {k: v for k, v in _KWARGS.items() if k != "filename"},
    name="old_kwargs",
)
@icontract.ensure(
    lambda filename, OLD, result: result is True,
)
@icontract.ensure(
    lambda filename, OLD, result:
        set(
            np.load(
                filename if filename.endswith(".npz") else filename + ".npz",
                allow_pickle=True,
            ).files
        )
        == set(OLD.old_kwargs.keys()),
)
@icontract.ensure(
    lambda filename, OLD, result:
        all(
            np.array_equal(
                np.load(
                    filename if filename.endswith(".npz") else filename + ".npz",
                    allow_pickle=True,
                )[name],
                (
                    value.to_records(index=False)
                    if isinstance(value, pd.DataFrame)
                    else np.asarray(value)
                ),
            )
            for name, value in OLD.old_kwargs.items()
        ),
)
@icontract.ensure(
    lambda filename, OLD, result:
        all(
            not isinstance(OLD.old_kwargs[name], pd.DataFrame)
            or (
                name in np.load(
                    filename if filename.endswith(".npz") else filename + ".npz",
                    allow_pickle=True,
                ).files
                and (
                    np.load(
                        filename if filename.endswith(".npz") else filename + ".npz",
                        allow_pickle=True,
                    )[name].shape != ()
                    or np.load(
                        filename if filename.endswith(".npz") else filename + ".npz",
                        allow_pickle=True,
                    )[name][()]
                    is not None
                )
            )
            for name in OLD.old_kwargs.keys()
        ) and 
        all(
            (not isinstance(value, pd.DataFrame))
            or (
                np.load(
                    filename if filename.endswith(".npz") else filename + ".npz",
                    allow_pickle=True,
                )[name].dtype.names is not None
                and len(
                    np.load(
                        filename
                        if filename.endswith(".npz")
                        else filename + ".npz",
                        allow_pickle=True,
                    )[name].dtype.names
                )
                == len(value.columns)
            )
            for name, value in OLD.old_kwargs.items()
        ),
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
===== 0 =====
```
     """
 
     for k in kwargs:
-        if isinstance(kwargs[k], pd.DataFrame):
+        if isinstance(None, pd.DataFrame):
             kwargs[k] = kwargs[k].to_records(index=False)
     np.savez_compressed(filename, **kwargs)
-    return True+    return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(None, pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True

```
===== 1 =====
```
     """
 
     for k in kwargs:
-        if isinstance(kwargs[k], pd.DataFrame):
+        if isinstance(kwargs[k], list):
             kwargs[k] = kwargs[k].to_records(index=False)
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], list):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 2 =====
```
     """
 
     for k in kwargs:
-        if isinstance(kwargs[k], pd.DataFrame):
+        if isinstance(kwargs[k], pd.DataFrame) and 'index' in kwargs[k]:
             kwargs[k] = kwargs[k].to_records(index=False)
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame) and 'index' in kwargs[k]:
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 3 =====
```
     """
 
     for k in kwargs:
-        if isinstance(kwargs[k], pd.DataFrame):
+        if isinstance(kwargs[k], pd.DataFrame) and kwargs[k].empty:
             kwargs[k] = kwargs[k].to_records(index=False)
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame) and kwargs[k].empty:
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 4 =====
```
     """
 
     for k in kwargs:
-        if isinstance(kwargs[k], pd.DataFrame):
+        if isinstance(kwargs[k], pd.Series):
             kwargs[k] = kwargs[k].to_records(index=False)
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.Series):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 5 =====
```
     """
 
     for k in kwargs:
-        if isinstance(kwargs[k], pd.DataFrame):
+        if not isinstance(kwargs[k], pd.DataFrame):
             kwargs[k] = kwargs[k].to_records(index=False)
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if not isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 6 =====
```
 
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
-            kwargs[k] = kwargs[k].to_records(index=False)
+            kwargs[k] = None
     np.savez_compressed(filename, **kwargs)
-    return True+    return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = None
    np.savez_compressed(filename, **kwargs)
    return True

```
===== 7 =====
```
 
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
-            kwargs[k] = kwargs[k].to_records(index=False)
+            kwargs[k] = kwargs[k].astype(str)
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].astype(str)
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 8 =====
```
 
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
-            kwargs[k] = kwargs[k].to_records(index=False)
+            kwargs[k] = kwargs[k].iloc[:, 0]  # Only keep the first column
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].iloc[:, 0]  # Only keep the first column
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 9 =====
```
 
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
-            kwargs[k] = kwargs[k].to_records(index=False)
+            kwargs[k] = kwargs[k].to_dict()
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_dict()
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 10 =====
```
 
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
-            kwargs[k] = kwargs[k].to_records(index=False)
+            kwargs[k] = kwargs[k].to_numpy()
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_numpy()
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 11 =====
```
 
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
-            kwargs[k] = kwargs[k].to_records(index=False)
+            kwargs[k] = kwargs[k].values
     np.savez_compressed(filename, **kwargs)
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].values
    np.savez_compressed(filename, **kwargs)
    return True
```
===== 12 =====
```
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
             kwargs[k] = kwargs[k].to_records(index=False)
-    np.savez_compressed(filename, **kwargs)
-    return True+    np.savez_compressed(filename, )
+    return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, )
    return True

```
===== 13 =====
```
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
             kwargs[k] = kwargs[k].to_records(index=False)
-    np.savez_compressed(filename, **kwargs)
+    np.savez_compressed(filename, **{k: v for k, v in kwargs.items() if k != 'mesh'})
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, **{k: v for k, v in kwargs.items() if k != 'mesh'})
    return True
```
===== 14 =====
```
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
             kwargs[k] = kwargs[k].to_records(index=False)
-    np.savez_compressed(filename, **kwargs)
+    np.savez_compressed(filename, *kwargs.values())
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, *kwargs.values())
    return True
```
===== 15 =====
```
     for k in kwargs:
         if isinstance(kwargs[k], pd.DataFrame):
             kwargs[k] = kwargs[k].to_records(index=False)
-    np.savez_compressed(filename, **kwargs)
+    np.savez_compressed(filename, points=kwargs.get('points'))
     return True
```
```
def write_npz(filename, **kwargs):
    """
    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems
    """

    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    np.savez_compressed(filename, points=kwargs.get('points'))
    return True
```
