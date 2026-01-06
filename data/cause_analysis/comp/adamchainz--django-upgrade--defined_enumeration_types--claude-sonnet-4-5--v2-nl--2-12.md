https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/fixers/model_field_choices.py#L33-L63
```
@icontract.ensure(lambda result: isinstance(result, set))
@icontract.ensure(lambda result: all(isinstance(name, str) for name in result))
@icontract.ensure(lambda result: all(name.isidentifier() for name in result))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.snapshot(
    lambda module: (
        lambda d=defaultdict(set): (
            [
                d[node.module].update(
                    name.name
                    for name in node.names
                    if name.asname is None and name.name != "*"
                )
                for node in module.body
                if isinstance(node, ast.ImportFrom)
                and node.level == 0
                and node.module is not None
            ],
            d,
        )[1]
    )(),
    name="from_imports",
)
@icontract.snapshot(
    lambda module: {
        node.name: node.lineno
        for node in module.body
        if isinstance(node, ast.ClassDef)
    },
    name="class_lines",
)
@icontract.snapshot(
    lambda module: {
        node.name: node.bases
        for node in module.body
        if isinstance(node, ast.ClassDef)
    },
    name="class_bases",
)
@icontract.ensure(
    lambda OLD, module, up_to_line, result:
        result is not None
        and module in module_defined_enumeration_types
        and isinstance(module_defined_enumeration_types[module], dict)
        and module_defined_enumeration_types[module]
        == {
            name: OLD.class_lines[name]
            for name, bases in OLD.class_bases.items()
            if any(_is_django_choices_type(OLD.from_imports, base) for base in bases)
        }
        and result
        == {
            name
            for name, line in module_defined_enumeration_types[module].items()
            if line <= up_to_line
        }
)

```
===== 12: failed =====
```
         for node in module.body:
             if (
                 isinstance(node, ast.ImportFrom)
-                and node.level == 0
+                and node.level > 0
                 and node.module is not None
             ):
                 from_imports[node.module].update(
```
```
def defined_enumeration_types(module: ast.Module, up_to_line: int) -> set[str]:
    """
    Return a set of enumeration type class names defined in the given module, up to a line number.
    """
    if module not in module_defined_enumeration_types:
        enum_dict = {}
        from_imports: defaultdict[str, set[str]] = defaultdict(set)
        for node in module.body:
            if (
                isinstance(node, ast.ImportFrom)
                and node.level > 0
                and node.module is not None
            ):
                from_imports[node.module].update(
                    name.name
                    for name in node.names
                    if name.asname is None and name.name != "*"
                )
            elif isinstance(node, ast.ClassDef):
                # Check if the class inherits from one of Django's choice types
                for base in node.bases:
                    if _is_django_choices_type(from_imports, base):
                        enum_dict[node.name] = node.lineno
                        break
        module_defined_enumeration_types[module] = enum_dict

    return {
        name
        for name, line in module_defined_enumeration_types[module].items()
        if line <= up_to_line
    }
```
