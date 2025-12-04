https://github.com/pallets-eco/flask-sqlalchemy/blob/168cb4b7b50fe5176307a10d873781bfafc6eeda/./src/flask_sqlalchemy/model.py#L152-L191
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
```
@icontract.snapshot(lambda _ARGS, _KWARGS: (_KWARGS.get("schema") is None and _ARGS[1]) or f"{_KWARGS.get('schema')}.{_ARGS[1]}", name="key")
@icontract.snapshot(lambda _ARGS, _KWARGS: (((_KWARGS.get("schema") is None and _ARGS[1]) or f"{_KWARGS.get('schema')}.{_ARGS[1]}") in _ARGS[0].metadata.tables), name="key_in_meta")
@icontract.snapshot(lambda _ARGS, _KWARGS: any(((isinstance(a, sa.Column) and getattr(a, "primary_key", False)) or isinstance(a, sa.PrimaryKeyConstraint)) for a in _ARGS[1:]), name="has_pk")
@icontract.snapshot(lambda _ARGS, _KWARGS: any("__table__" in base.__dict__ for base in _ARGS[0].__mro__[1:-1]), name="base_has_table")
@icontract.ensure(lambda result, OLD: isinstance(result, sa.Table) == (OLD.key_in_meta or OLD.has_pk or (not OLD.base_has_table)))
@icontract.ensure(lambda result, cls: (result is not None) or ("__tablename__" not in cls.__dict__))
@icontract.ensure(lambda result, OLD: (not OLD.key_in_meta and not OLD.has_pk and OLD.base_has_table) <= (result is None))
```
[3, 11]
===== 3 =====
```
         # Check if a table with this name already exists. Allows reflected tables to be
         # applied to models by name.
         if key in cls.metadata.tables:
-            return sa.Table(*args, **kwargs)
+            return sa.Table(*args, **kwargs, schema='default')  # This will force the table to be created in a 'default' schema, which may not be intended.
 
         # If a primary key is found, create a table for joined-table inheritance.
         for arg in args:
```
```
    def __table_cls__(cls, *args: t.Any, **kwargs: t.Any) -> sa.Table | None:
        """This is called by SQLAlchemy during mapper setup. It determines the final
        table object that the model will use.

        If no primary key is found, that indicates single-table inheritance, so no table
        will be created and ``__tablename__`` will be unset.
        """
        schema = kwargs.get("schema")

        if schema is None:
            key = args[0]
        else:
            key = f"{schema}.{args[0]}"

        # Check if a table with this name already exists. Allows reflected tables to be
        # applied to models by name.
        if key in cls.metadata.tables:
            return sa.Table(*args, **kwargs, schema='default')  # This will force the table to be created in a 'default' schema, which may not be intended.

        # If a primary key is found, create a table for joined-table inheritance.
        for arg in args:
            if (isinstance(arg, sa.Column) and arg.primary_key) or isinstance(
                arg, sa.PrimaryKeyConstraint
            ):
                return sa.Table(*args, **kwargs)

        # If no base classes define a table, return one that's missing a primary key
        # so SQLAlchemy shows the correct error.
        for base in cls.__mro__[1:-1]:
            if "__table__" in base.__dict__:
                break
        else:
            return sa.Table(*args, **kwargs)

        # Single-table inheritance, use the parent table name. __init__ will unset
        # __table__ based on this.
        if "__tablename__" in cls.__dict__:
            del cls.__tablename__

        return None
```
===== 11 =====
```
             if (isinstance(arg, sa.Column) and arg.primary_key) or isinstance(
                 arg, sa.PrimaryKeyConstraint
             ):
-                return sa.Table(*args, **kwargs)
+                return sa.Table(*args, **kwargs, schema='invalid_schema')  # This will create a table in a non-existent schema, causing issues when trying to access it.
 
         # If no base classes define a table, return one that's missing a primary key
         # so SQLAlchemy shows the correct error.
```
```
    def __table_cls__(cls, *args: t.Any, **kwargs: t.Any) -> sa.Table | None:
        """This is called by SQLAlchemy during mapper setup. It determines the final
        table object that the model will use.

        If no primary key is found, that indicates single-table inheritance, so no table
        will be created and ``__tablename__`` will be unset.
        """
        schema = kwargs.get("schema")

        if schema is None:
            key = args[0]
        else:
            key = f"{schema}.{args[0]}"

        # Check if a table with this name already exists. Allows reflected tables to be
        # applied to models by name.
        if key in cls.metadata.tables:
            return sa.Table(*args, **kwargs)

        # If a primary key is found, create a table for joined-table inheritance.
        for arg in args:
            if (isinstance(arg, sa.Column) and arg.primary_key) or isinstance(
                arg, sa.PrimaryKeyConstraint
            ):
                return sa.Table(*args, **kwargs, schema='invalid_schema')  # This will create a table in a non-existent schema, causing issues when trying to access it.

        # If no base classes define a table, return one that's missing a primary key
        # so SQLAlchemy shows the correct error.
        for base in cls.__mro__[1:-1]:
            if "__table__" in base.__dict__:
                break
        else:
            return sa.Table(*args, **kwargs)

        # Single-table inheritance, use the parent table name. __init__ will unset
        # __table__ based on this.
        if "__tablename__" in cls.__dict__:
            del cls.__tablename__

        return None
```
