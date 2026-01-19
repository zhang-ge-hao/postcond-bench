https://github.com/langchain-ai/langchain-mcp-adapters/blob/7eb40987dda5ae90c2db4052cf260ab2c54f6168/./langchain_mcp_adapters/tools.py#L185-L206
```
🈚️

Failed: DID NOT RAISE <class 'NotImplementedError'>

specified error process

@icontract.snapshot(
    lambda tool:
        [
            field
            for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
            if any(
                isinstance(arg, InjectedToolArg)
                or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
                for arg in get_args(field_info)[1:]
            )
        ],
    name="res"
)
@icontract.ensure(
    lambda result, OLD: all(f1 == f2 for f1, f2 in zip(OLD.res, result))
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
===== 0 =====
```
 
     def _is_injected_arg_type(type_: type) -> bool:
         return any(
-            isinstance(arg, InjectedToolArg)
+            arg == InjectedToolArg
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
             for arg in get_args(type_)[1:]
         )
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            arg == InjectedToolArg
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 1 =====
```
 
     def _is_injected_arg_type(type_: type) -> bool:
         return any(
-            isinstance(arg, InjectedToolArg)
+            arg is None
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
             for arg in get_args(type_)[1:]
         )
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            arg is None
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 2 =====
```
 
     def _is_injected_arg_type(type_: type) -> bool:
         return any(
-            isinstance(arg, InjectedToolArg)
+            isinstance(None, InjectedToolArg)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
             for arg in get_args(type_)[1:]
         )
@@ -19,4 +19,4 @@         field
         for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
         if _is_injected_arg_type(field_info)
-    ]+    ]
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(None, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]

```
===== 3 =====
```
 
     def _is_injected_arg_type(type_: type) -> bool:
         return any(
-            isinstance(arg, InjectedToolArg)
-            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
+            isinstance(arg, InjectedToolArg) and (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
             for arg in get_args(type_)[1:]
         )
 
@@ -19,4 +18,4 @@         field
         for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
         if _is_injected_arg_type(field_info)
-    ]+    ]
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg) and (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]

```
===== 4 =====
```
 
     def _is_injected_arg_type(type_: type) -> bool:
         return any(
-            isinstance(arg, InjectedToolArg)
+            isinstance(arg, int)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
             for arg in get_args(type_)[1:]
         )
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, int)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 5 =====
```
 
     def _is_injected_arg_type(type_: type) -> bool:
         return any(
-            isinstance(arg, InjectedToolArg)
+            isinstance(arg, str)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
             for arg in get_args(type_)[1:]
         )
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, str)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 6 =====
```
         return any(
             isinstance(arg, InjectedToolArg)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
-            for arg in get_args(type_)[1:]
+            for arg in get_args(None)[1:]
         )
 
     return [
         field
         for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
         if _is_injected_arg_type(field_info)
-    ]+    ]
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(None)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]

```
===== 7 =====
```
         return any(
             isinstance(arg, InjectedToolArg)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
-            for arg in get_args(type_)[1:]
+            for arg in get_args(type_)[0:1]
         )
 
     return [
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[0:1]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 8 =====
```
         return any(
             isinstance(arg, InjectedToolArg)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
-            for arg in get_args(type_)[1:]
+            for arg in get_args(type_)[1:-1]
         )
 
     return [
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:-1]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 9 =====
```
         return any(
             isinstance(arg, InjectedToolArg)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
-            for arg in get_args(type_)[1:]
+            for arg in get_args(type_)[2:]
         )
 
     return [
         field
         for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
         if _is_injected_arg_type(field_info)
-    ]+    ]
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[2:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]

```
===== 10 =====
```
         return any(
             isinstance(arg, InjectedToolArg)
             or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
-            for arg in get_args(type_)[1:]
+            for arg in get_args(type_)[::2]
         )
 
     return [
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[::2]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(field_info)
    ]
```
===== 11 =====
```
     return [
         field
         for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
-        if _is_injected_arg_type(field_info)
-    ]+        if _is_injected_arg_type(None)
+    ]
```
```
def _get_injected_args(tool: BaseTool) -> list[str]:
    """Get the list of injected argument names from a LangChain tool.

    Args:
        tool: The LangChain tool to inspect.

    Returns:
        A list of injected argument names.
    """

    def _is_injected_arg_type(type_: type) -> bool:
        return any(
            isinstance(arg, InjectedToolArg)
            or (isinstance(arg, type) and issubclass(arg, InjectedToolArg))
            for arg in get_args(type_)[1:]
        )

    return [
        field
        for field, field_info in get_all_basemodel_annotations(tool.args_schema).items()
        if _is_injected_arg_type(None)
    ]

```
