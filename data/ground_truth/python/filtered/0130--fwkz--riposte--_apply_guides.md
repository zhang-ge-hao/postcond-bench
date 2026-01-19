https://github.com/fwkz/riposte/blob/174bded8ccd665556b163e5c5633d0900715740f/./riposte/command.py#L67-L89
```
🈚️

The below calls mock util, and the mock util use iterator.

@icontract.ensure(
    lambda self, bound_arguments, result:
    result
    == [
        processed_arg
        for name, value in bound_arguments.arguments.items()
        for processed_arg in (
            # 对 *varargs 的特殊处理
            self._process_arguments(name, *value)
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            )
            # 对普通参数
            else self._process_arguments(name, value)
        )
    ]
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
===== 0 =====
```
         processed = []
         for name, value in bound_arguments.arguments.items():
             if (
-                bound_arguments.signature.parameters[name].kind
+                bound_arguments.signature.parameters[name].annotation
                 is inspect.Parameter.VAR_POSITIONAL
             ):
                 arguments = self._process_arguments(name, *value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].annotation
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 1 =====
```
         processed = []
         for name, value in bound_arguments.arguments.items():
             if (
-                bound_arguments.signature.parameters[name].kind
+                bound_arguments.signature.parameters[name].default
                 is inspect.Parameter.VAR_POSITIONAL
             ):
                 arguments = self._process_arguments(name, *value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].default
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 2 =====
```
         processed = []
         for name, value in bound_arguments.arguments.items():
             if (
-                bound_arguments.signature.parameters[name].kind
+                bound_arguments.signature.parameters[name].kind == inspect.Parameter.KEYWORD_ONLY
                 is inspect.Parameter.VAR_POSITIONAL
             ):
                 arguments = self._process_arguments(name, *value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind == inspect.Parameter.KEYWORD_ONLY
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 3 =====
```
         processed = []
         for name, value in bound_arguments.arguments.items():
             if (
-                bound_arguments.signature.parameters[name].kind
+                bound_arguments.signature.parameters[name].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                 is inspect.Parameter.VAR_POSITIONAL
             ):
                 arguments = self._process_arguments(name, *value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 4 =====
```
         processed = []
         for name, value in bound_arguments.arguments.items():
             if (
-                bound_arguments.signature.parameters[name].kind
+                bound_arguments.signature.parameters[name].name
                 is inspect.Parameter.VAR_POSITIONAL
             ):
                 arguments = self._process_arguments(name, *value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].name
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 5 =====
```
         for name, value in bound_arguments.arguments.items():
             if (
                 bound_arguments.signature.parameters[name].kind
-                is inspect.Parameter.VAR_POSITIONAL
+                is inspect.Parameter.KEYWORD_ONLY
             ):
                 arguments = self._process_arguments(name, *value)
             else:
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.KEYWORD_ONLY
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 6 =====
```
         for name, value in bound_arguments.arguments.items():
             if (
                 bound_arguments.signature.parameters[name].kind
-                is inspect.Parameter.VAR_POSITIONAL
+                is inspect.Parameter.POSITIONAL_ONLY
             ):
                 arguments = self._process_arguments(name, *value)
             else:
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.POSITIONAL_ONLY
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 7 =====
```
         for name, value in bound_arguments.arguments.items():
             if (
                 bound_arguments.signature.parameters[name].kind
-                is inspect.Parameter.VAR_POSITIONAL
+                is inspect.Parameter.VAR_KEYWORD
             ):
                 arguments = self._process_arguments(name, *value)
             else:
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_KEYWORD
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 8 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(*value)
             else:
                 arguments = self._process_arguments(name, value)
 
             processed.extend(arguments)
 
-        return processed+        return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(*value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed

```
===== 9 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(None, *value)
             else:
                 arguments = self._process_arguments(name, value)
 
             processed.extend(arguments)
 
-        return processed+        return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(None, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed

```
===== 10 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(name)  # Not passing any value, leading to incorrect processing
             else:
                 arguments = self._process_arguments(name, value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name)  # Not passing any value, leading to incorrect processing
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 11 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(name, )
             else:
                 arguments = self._process_arguments(name, value)
 
             processed.extend(arguments)
 
-        return processed+        return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, )
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed

```
===== 12 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(name, *value, "extra_arg")  # Adding an extra argument that shouldn't be there
             else:
                 arguments = self._process_arguments(name, value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value, "extra_arg")  # Adding an extra argument that shouldn't be there
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 13 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(name, value)  # Missing unpacking of value
             else:
                 arguments = self._process_arguments(name, value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, value)  # Missing unpacking of value
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 14 =====
```
                 bound_arguments.signature.parameters[name].kind
                 is inspect.Parameter.VAR_POSITIONAL
             ):
-                arguments = self._process_arguments(name, *value)
+                arguments = self._process_arguments(name, value[0])  # Only processing the first element of value
             else:
                 arguments = self._process_arguments(name, value)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, value[0])  # Only processing the first element of value
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments)

        return processed
```
===== 15 =====
```
             ):
                 arguments = self._process_arguments(name, *value)
             else:
-                arguments = self._process_arguments(name, value)
+                arguments = self._process_arguments(None, value)
 
             processed.extend(arguments)
 
-        return processed+        return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(None, value)

            processed.extend(arguments)

        return processed

```
===== 16 =====
```
             ):
                 arguments = self._process_arguments(name, *value)
             else:
-                arguments = self._process_arguments(name, value)
+                arguments = self._process_arguments(name, )
 
             processed.extend(arguments)
 
-        return processed+        return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, )

            processed.extend(arguments)

        return processed

```
===== 17 =====
```
             ):
                 arguments = self._process_arguments(name, *value)
             else:
-                arguments = self._process_arguments(name, value)
+                arguments = self._process_arguments(name, value) + ["default"]  # Adds a default value instead of processing
 
             processed.extend(arguments)
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value) + ["default"]  # Adds a default value instead of processing

            processed.extend(arguments)

        return processed
```
===== 18 =====
```
             ):
                 arguments = self._process_arguments(name, *value)
             else:
-                arguments = self._process_arguments(name, value)
+                arguments = self._process_arguments(value)
 
             processed.extend(arguments)
 
-        return processed+        return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(value)

            processed.extend(arguments)

        return processed

```
===== 19 =====
```
             else:
                 arguments = self._process_arguments(name, value)
 
-            processed.extend(arguments)
+            processed.append(arguments)  # This will create a nested list instead of a flat list.
 
         return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.append(arguments)  # This will create a nested list instead of a flat list.

        return processed
```
===== 20 =====
```
             else:
                 arguments = self._process_arguments(name, value)
 
-            processed.extend(arguments)
+            processed.append(value)  # This will append the original value instead of the processed arguments.
 
         return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.append(value)  # This will append the original value instead of the processed arguments.

        return processed
```
===== 21 =====
```
             else:
                 arguments = self._process_arguments(name, value)
 
-            processed.extend(arguments)
+            processed.extend([])  # This will effectively do nothing, leaving processed unchanged.
 
         return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend([])  # This will effectively do nothing, leaving processed unchanged.

        return processed
```
===== 22 =====
```
             else:
                 arguments = self._process_arguments(name, value)
 
-            processed.extend(arguments)
+            processed.extend(arguments[:1])  # This will only add the first element of arguments, losing others.
 
         return processed
```
```
    def _apply_guides(self, bound_arguments: inspect.BoundArguments) -> List:
        """Apply guide functions.

        Apply guide functions to values of type `str` delivered by user
        using `input()`.

        Assumes that `args` have been already validated `_bind_arguments`,
        hence `args` is matching `_func` signature, (`args <= parameters`)

        """
        processed = []
        for name, value in bound_arguments.arguments.items():
            if (
                bound_arguments.signature.parameters[name].kind
                is inspect.Parameter.VAR_POSITIONAL
            ):
                arguments = self._process_arguments(name, *value)
            else:
                arguments = self._process_arguments(name, value)

            processed.extend(arguments[:1])  # This will only add the first element of arguments, losing others.

        return processed
```
