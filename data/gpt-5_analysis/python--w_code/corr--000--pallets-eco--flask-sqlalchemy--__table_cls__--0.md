https://github.com/pallets-eco/flask-sqlalchemy/blob/168cb4b7b50fe5176307a10d873781bfafc6eeda/./src/flask_sqlalchemy/model.py#L152-L191
```
@icontract.snapshot(lambda _ARGS, _KWARGS: (_ARGS[0] if _KWARGS.get("schema") is None else f"{_KWARGS.get('schema')}.{_ARGS[0]}"), name="key")
@icontract.snapshot(lambda _ARGS: any((isinstance(arg, sa.Column) and getattr(arg, "primary_key", False)) or isinstance(arg, sa.PrimaryKeyConstraint) for arg in _ARGS), name="has_pk")
@icontract.snapshot(lambda cls: any("__table__" in base.__dict__ for base in cls.__mro__[1:-1]), name="base_has_table")
@icontract.ensure(lambda result: (result is None) or isinstance(result, sa.Table))
@icontract.ensure(lambda OLD, cls, result: (result is not None) or (OLD.base_has_table and (not OLD.has_pk) and (OLD.key not in cls.metadata.tables)))
@icontract.ensure(lambda OLD, cls, result: ((OLD.key in cls.metadata.tables) or OLD.has_pk or (not OLD.base_has_table)) or (result is not None))
@icontract.ensure(lambda cls, result: (result is not None) or ("__tablename__" not in cls.__dict__))
```
```
limited logical rigor.
Two post-conditions conflict with each other, the first one is correct.
---
@icontract.ensure(lambda OLD, cls, result: (result is not None) or (OLD.base_has_table and (not OLD.has_pk) and (OLD.key not in cls.metadata.tables)))
@icontract.ensure(lambda OLD, cls, result: ((OLD.key in cls.metadata.tables) or OLD.has_pk or (not OLD.base_has_table)) or (result is not None))
```
icontract_fail
```
@icontract.snapshot(
    lambda _ARGS, _KWARGS: (_KWARGS.get("schema") is None and _ARGS[1]) 
    or f"{_KWARGS.get('schema')}.{_ARGS[1]}", 
    name="key",
)
@icontract.snapshot(
    lambda _ARGS, _KWARGS: (
        ((_KWARGS.get("schema") is None and _ARGS[1]) 
         or f"{_KWARGS.get('schema')}.{_ARGS[1]}")
        in _ARGS[0].metadata.tables
    ),
    name="key_in_meta",
)
@icontract.snapshot(
    lambda _ARGS, _KWARGS: any(
        (
            isinstance(a, sa.Column) and getattr(a, "primary_key", False)
        ) or isinstance(a, sa.PrimaryKeyConstraint)
        for a in _ARGS[1:]
    ),
    name="has_pk",
)
@icontract.snapshot(
    lambda _ARGS, _KWARGS: any(
        "__table__" in base.__dict__ for base in _ARGS[0].__mro__[1:-1]
    ),
    name="base_has_table",
)
@icontract.ensure(
    lambda result, OLD: isinstance(result, sa.Table)
    == (OLD.key_in_meta or OLD.has_pk or (not OLD.base_has_table))
)
@icontract.ensure(
    lambda result, cls: (result is not None) or ("__tablename__" not in cls.__dict__)
)
@icontract.ensure(
    lambda result, OLD: (not OLD.key_in_meta and not OLD.has_pk and OLD.base_has_table)
    <= (result is None)
)
@icontract.ensure(
    lambda result, OLD: (
        result is None
        or (isinstance(result, sa.Table) and result.key == OLD.key)
    )
)
@icontract.ensure(
    lambda result, cls, OLD: (
        not OLD.key_in_meta
        or (
            isinstance(result, sa.Table)
            and result is cls.metadata.tables[OLD.key]
        )
    )
)

```
