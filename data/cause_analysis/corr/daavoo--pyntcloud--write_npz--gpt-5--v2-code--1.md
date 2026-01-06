https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/io/npz.py#L27-L46
```
@icontract.snapshot(lambda filename: filename, name="filename_before")
@icontract.snapshot(lambda kwargs: dict(kwargs), name="kwargs_before")
@icontract.ensure(lambda result: result is True)
@icontract.ensure(lambda filename, CONTRACT_SNAPSHOT_filename_before: filename == CONTRACT_SNAPSHOT_filename_before)
@icontract.ensure(lambda kwargs, kwargs_before: set(kwargs.keys()) == set(kwargs_before.keys()))
@icontract.ensure(lambda kwargs, kwargs_before: all((isinstance(kwargs_before[k], pd.DataFrame)) or (kwargs[k] is kwargs_before[k]) for k in kwargs_before))
@icontract.ensure(lambda kwargs, kwargs_before: all((not isinstance(kwargs_before[k], pd.DataFrame)) or (isinstance(kwargs[k], np.ndarray) and (kwargs[k].dtype.names is not None) and not isinstance(kwargs[k], pd.DataFrame)) for k in kwargs_before))
@icontract.ensure(lambda kwargs, kwargs_before: all((not isinstance(kwargs_before[k], pd.DataFrame)) or (len(kwargs[k]) == len(kwargs_before[k])) for k in kwargs_before))
@icontract.ensure(lambda kwargs, kwargs_before: all((not isinstance(kwargs_before[k], pd.DataFrame)) or (kwargs[k].dtype.names is not None and len(kwargs[k].dtype.names) == len(kwargs_before[k].columns)) for k in kwargs_before))
```
```
limited spec

kwargs
```
failed
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
