https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/context.py#L474-L507
```
@icontract.ensure(
    lambda result: isinstance(result, tuple)
)
@icontract.ensure(
    lambda result: all(isinstance(item, ContextItemInfo) for item in result)
)
@icontract.ensure(
    lambda _ARGS, result: len(result) == len(_ARGS) - 1
)
@icontract.ensure(
    lambda _ARGS, result: all(
        item.key == pair[0]
        for item, pair in zip(result, _ARGS[1:])
    )
)
@icontract.ensure(
    lambda _ARGS, result: all(
        item.expected_type == pair[1]
        for item, pair in zip(result, _ARGS[1:])
    )
)
@icontract.ensure(
    lambda result: all(
        isinstance(item.key_in_context, bool)
        for item in result
    )
)
@icontract.ensure(
    lambda self, result: all(
        item.key_in_context == (item.key in self)
        for item in result
    )
)
@icontract.ensure(
    lambda result: all(
        item.key_in_context or (item.is_expected_type is None)
        for item in result
    )
)
@icontract.ensure(
    lambda self, result: all(
        (not (item.key_in_context and item.key in self))
        or (item.is_expected_type
            == isinstance(self[item.key], item.expected_type))
        for item in result
    )
)
@icontract.ensure(
    lambda result: all(
        isinstance(item.has_value, bool)
        for item in result
    )
)
@icontract.ensure(
    lambda self, result: all(
        item.has_value
        == (item.key_in_context and item.key in self and self[item.key] is not None)
        for item in result
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
===== 0 =====
```
         keys_exist = [(key, key in self.keys(), expected_type)
                       for key, expected_type in keys]
 
-        return tuple(ContextItemInfo(
+        return set(ContextItemInfo(
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return set(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 1 =====
```
                       for key, expected_type in keys]
 
         return tuple(ContextItemInfo(
-            key=k[0],
+            key=None,
             key_in_context=k[1],
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=None,
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 2 =====
```
                       for key, expected_type in keys]
 
         return tuple(ContextItemInfo(
-            key=k[0],
+            key=k[0] + '_suffix',  # This appends a suffix to the key, causing it to not match the original context key.
             key_in_context=k[1],
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0] + '_suffix',  # This appends a suffix to the key, causing it to not match the original context key.
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 3 =====
```
                       for key, expected_type in keys]
 
         return tuple(ContextItemInfo(
-            key=k[0],
+            key=k[0].upper(),  # This changes the key to uppercase, which may not match the original context key.
             key_in_context=k[1],
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0].upper(),  # This changes the key to uppercase, which may not match the original context key.
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 4 =====
```
                       for key, expected_type in keys]
 
         return tuple(ContextItemInfo(
-            key=k[0],
+            key=k[0][::-1],  # This reverses the key string, which will not match the original context key.
             key_in_context=k[1],
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0][::-1],  # This reverses the key string, which will not match the original context key.
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 5 =====
```
                       for key, expected_type in keys]
 
         return tuple(ContextItemInfo(
-            key=k[0],
+            key=k[1],
             key_in_context=k[1],
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[1],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 6 =====
```
 
         return tuple(ContextItemInfo(
             key=k[0],
-            key_in_context=k[1],
+            key_in_context=None,
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=None,
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 7 =====
```
 
         return tuple(ContextItemInfo(
             key=k[0],
-            key_in_context=k[1],
+            key_in_context=None,
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=None,
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 8 =====
```
 
         return tuple(ContextItemInfo(
             key=k[0],
-            key_in_context=k[1],
+            key_in_context=True,
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=True,
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 9 =====
```
 
         return tuple(ContextItemInfo(
             key=k[0],
-            key_in_context=k[1],
+            key_in_context=k[0],  # using the key instead of the existence check
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[0],  # using the key instead of the existence check
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 10 =====
```
 
         return tuple(ContextItemInfo(
             key=k[0],
-            key_in_context=k[1],
+            key_in_context=k[2],
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[2],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 11 =====
```
 
         return tuple(ContextItemInfo(
             key=k[0],
-            key_in_context=k[1],
+            key_in_context=self.get(k[0]),  # using the value instead of existence
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=self.get(k[0]),  # using the value instead of existence
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 12 =====
```
         return tuple(ContextItemInfo(
             key=k[0],
             key_in_context=k[1],
-            expected_type=k[2],
+            expected_type=None,
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=None,
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 13 =====
```
         return tuple(ContextItemInfo(
             key=k[0],
             key_in_context=k[1],
-            expected_type=k[2],
+            expected_type=None,
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=None,
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 14 =====
```
         return tuple(ContextItemInfo(
             key=k[0],
             key_in_context=k[1],
-            expected_type=k[2],
+            expected_type=k[0],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[0],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 15 =====
```
         return tuple(ContextItemInfo(
             key=k[0],
             key_in_context=k[1],
-            expected_type=k[2],
+            expected_type=k[1],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[1],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 16 =====
```
         return tuple(ContextItemInfo(
             key=k[0],
             key_in_context=k[1],
-            expected_type=k[2],
+            expected_type=type(k[2]),
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=type(k[2]),
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 17 =====
```
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
-            is_expected_type=isinstance(self[k[0]], k[2])
+            is_expected_type=False  # Always returns False, leading to incorrect type validation.
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=False  # Always returns False, leading to incorrect type validation.
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 18 =====
```
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
-            is_expected_type=isinstance(self[k[0]], k[2])
-            if k[1] else None,
+            is_expected_type=None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 19 =====
```
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
-            is_expected_type=isinstance(self[k[0]], k[2])
+            is_expected_type=True  # Always returns True, ignoring the actual type check.
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=True  # Always returns True, ignoring the actual type check.
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 20 =====
```
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
-            is_expected_type=isinstance(self[k[0]], k[2])
+            is_expected_type=isinstance(None, k[2])
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(None, k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)

```
===== 21 =====
```
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
-            is_expected_type=isinstance(self[k[0]], k[2])
+            is_expected_type=isinstance(self[k[0]], (int, float))  # Only checks for int or float types, missing others.
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], (int, float))  # Only checks for int or float types, missing others.
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 22 =====
```
             key=k[0],
             key_in_context=k[1],
             expected_type=k[2],
-            is_expected_type=isinstance(self[k[0]], k[2])
+            is_expected_type=isinstance(self[k[0]], str)  # Incorrectly checks if the value is a string only.
             if k[1] else None,
             has_value=k[1] and not self[k[0]] is None
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], str)  # Incorrectly checks if the value is a string only.
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is None
        ) for k in keys_exist)
```
===== 23 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+            has_value=None
+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=None
        ) for k in keys_exist)

```
===== 24 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
+            has_value=k[1] and not self.get(k[0])  # This will evaluate to False for any falsy value
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self.get(k[0])  # This will evaluate to False for any falsy value
        ) for k in keys_exist)
```
===== 25 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+            has_value=k[1] and not self[k[0]] is not None
+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and not self[k[0]] is not None
        ) for k in keys_exist)

```
===== 26 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
+            has_value=k[1] and self.get(k[0]) is None
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and self.get(k[0]) is None
        ) for k in keys_exist)
```
===== 27 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
+            has_value=k[1] and self[k[0]] == ''
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and self[k[0]] == ''
        ) for k in keys_exist)
```
===== 28 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
+            has_value=k[1] and self[k[0]] is None
         ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and self[k[0]] is None
        ) for k in keys_exist)
```
===== 29 =====
```
             expected_type=k[2],
             is_expected_type=isinstance(self[k[0]], k[2])
             if k[1] else None,
-            has_value=k[1] and not self[k[0]] is None
-        ) for k in keys_exist)+            has_value=k[1] and self[k[0]] is None
+        ) for k in keys_exist)
```
```
    def keys_of_type_exist(self, *keys):
        """Check if keys exist in context and if types are as expected.

        Args:
            *keys: *args for keys to check in context.
                   Each arg is a tuple(str, type)

        Returns:
            Tuple of namedtuple ContextItemInfo, same order as *keys.
            ContextItemInfo(key,
                            key_in_context,
                            expected_type,
                            is_expected_type)

            Remember if there is only one key in keys, the return assignment
            needs an extra comma to remind python that it's a tuple:
            # one
            a, = context.keys_of_type_exist('a')
            # > 1
            a, b = context.keys_of_type_exist('a', 'b')

        """
        # k[0] = key name, k[1] = exists, k2 = expected type
        keys_exist = [(key, key in self.keys(), expected_type)
                      for key, expected_type in keys]

        return tuple(ContextItemInfo(
            key=k[0],
            key_in_context=k[1],
            expected_type=k[2],
            is_expected_type=isinstance(self[k[0]], k[2])
            if k[1] else None,
            has_value=k[1] and self[k[0]] is None
        ) for k in keys_exist)

```
