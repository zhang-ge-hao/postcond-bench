https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/context.py#L509-L589
```
🈚️

It's hard

@icontract.snapshot(lambda self, add_me: deepcopy(self),
                    name="ctx_before")
@icontract.ensure(
    # 用 exec 在一个 namespace 里跑一遍“规格版 merge”，然后比较结果
    lambda self, add_me, result, ctx_before:
        (lambda ns: (
            exec(
                # 这段字符串里的代码就是“正确版本”的 merge 逻辑，
                # 只不过是对 spec_ctx 操作，而不是对 self 操作。
                "spec_ctx = ctx_before\n"
                "\n"
                "def merge_recurse(current, add_me_):\n"
                "    for k, v in add_me_.items():\n"
                "        # 关键：用根上下文 spec_ctx 做格式化\n"
                "        k = spec_ctx.get_formatted_value(k)\n"
                "\n"
                "        if isinstance(v, (str, SpecialTagDirective)):\n"
                "            # 字符串或 SpecialTagDirective：格式化后覆盖\n"
                "            current[k] = spec_ctx.get_formatted_value(v)\n"
                "        elif isinstance(v, (bytes, bytearray)):\n"
                "            # bytes：不可格式化/合并，直接覆盖\n"
                "            current[k] = v\n"
                "        elif k in current:\n"
                "            # 当前 context 已经有这个 key，按类型合并\n"
                "            if types.are_all_this_type(Mapping, current[k], v):\n"
                "                # dict：递归 merge\n"
                "                merge_recurse(current[k], v)\n"
                "            elif types.are_all_this_type(list, current[k], v):\n"
                "                # list：extend，右边先格式化\n"
                "                current[k].extend(\n"
                "                    spec_ctx.get_formatted_value(v)\n"
                "                )\n"
                "            elif types.are_all_this_type(tuple, current[k], v):\n"
                "                # tuple：拼接\n"
                "                current[k] = (\n"
                "                    current[k] + spec_ctx.get_formatted_value(v)\n"
                "                )\n"
                "            elif types.are_all_this_type(Set, current[k], v):\n"
                "                # set：并集\n"
                "                current[k] = (\n"
                "                    current[k] | spec_ctx.get_formatted_value(v)\n"
                "                )\n"
                "            else:\n"
                "                # 其他类型：右边格式化后覆盖\n"
                "                current[k] = spec_ctx.get_formatted_value(v)\n"
                "        else:\n"
                "            # 原 context 中没有这个 key：格式化后直接放进去\n"
                "            current[k] = spec_ctx.get_formatted_value(v)\n"
                "\n"
                "# 从根开始按规格逻辑跑一遍 merge\n"
                "merge_recurse(spec_ctx, add_me)\n"
                "# ok 表示规格结果与实际 self 是否一致\n"
                "ok = (spec_ctx == self)\n",
                ns
            ),
            ns['ok']
        )[1])(
            {
                # 初始 namespace，给 exec 里的代码提供需要用到的符号
                "self": self,
                "add_me": add_me,
                # 用 deepcopy(ctx_before) 避免把 snapshot 本身改坏
                "ctx_before": deepcopy(ctx_before),
                "SpecialTagDirective": SpecialTagDirective,
                "Mapping": Mapping,
                "Set": Set,
                "types": types,
            }
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
===== 0 =====
```
             """
             for k, v in add_me.items():
                 # key supports interpolation
-                k = self.get_formatted_value(k)
+                k = None
 
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = None

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 1 =====
```
             """
             for k, v in add_me.items():
                 # key supports interpolation
-                k = self.get_formatted_value(k)
+                k = self.get_formatted_value(None)
 
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(None)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 2 =====
```
             """
             for k, v in add_me.items():
                 # key supports interpolation
-                k = self.get_formatted_value(k)
+                k = self.get_formatted_value(k) if k in self else k
 
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k) if k in self else k

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 3 =====
```
                 k = self.get_formatted_value(k)
 
                 # str not mergable, so it doesn't matter if it exists in dest
-                if isinstance(v, (str, SpecialTagDirective)):
+                if isinstance(v, (list, tuple)):  # Incorrectly checks for list or tuple types instead of string or SpecialTagDirective
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
                 elif isinstance(v, (bytes, bytearray)):
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (list, tuple)):  # Incorrectly checks for list or tuple types instead of string or SpecialTagDirective
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 4 =====
```
                 k = self.get_formatted_value(k)
 
                 # str not mergable, so it doesn't matter if it exists in dest
-                if isinstance(v, (str, SpecialTagDirective)):
+                if isinstance(v, (str, dict)):  # Incorrectly allows dicts to be processed as strings
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
                 elif isinstance(v, (bytes, bytearray)):
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, dict)):  # Incorrectly allows dicts to be processed as strings
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 5 =====
```
                 k = self.get_formatted_value(k)
 
                 # str not mergable, so it doesn't matter if it exists in dest
-                if isinstance(v, (str, SpecialTagDirective)):
+                if not isinstance(v, (str, SpecialTagDirective)):  # Negates the condition, leading to incorrect handling of valid types
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
                 elif isinstance(v, (bytes, bytearray)):
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if not isinstance(v, (str, SpecialTagDirective)):  # Negates the condition, leading to incorrect handling of valid types
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 6 =====
```
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = None
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = None
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 7 =====
```
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = None  # This sets the value to None, effectively removing it from the context.
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = None  # This sets the value to None, effectively removing it from the context.
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 8 =====
```
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = self.get_formatted_value(None)
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(None)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 9 =====
```
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = self.get_formatted_value(v) if isinstance(v, str) else v  # Only formats if v is a string, ignoring other types.
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v) if isinstance(v, str) else v  # Only formats if v is a string, ignoring other types.
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 10 =====
```
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = self.get_formatted_value(v) if k not in current else current[k]  # This only updates if the key is not already in current, potentially leaving some values unchanged.
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v) if k not in current else current[k]  # This only updates if the key is not already in current, potentially leaving some values unchanged.
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 11 =====
```
                 # str not mergable, so it doesn't matter if it exists in dest
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = v  # This directly assigns the raw value without formatting.
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = v  # This directly assigns the raw value without formatting.
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 12 =====
```
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
-                elif isinstance(v, (bytes, bytearray)):
+                elif isinstance(v, (dict, set)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
                     current[k] = v
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (dict, set)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 13 =====
```
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
-                elif isinstance(v, (bytes, bytearray)):
+                elif isinstance(v, (list, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
                     current[k] = v
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (list, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 14 =====
```
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
-                elif isinstance(v, (bytes, bytearray)):
+                elif isinstance(v, (str, list)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
                     current[k] = v
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (str, list)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 15 =====
```
                 if isinstance(v, (str, SpecialTagDirective)):
                     # just overwrite dest - str adds/edits indiscriminately
                     current[k] = self.get_formatted_value(v)
-                elif isinstance(v, (bytes, bytearray)):
+                elif isinstance(v, (tuple, frozenset)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
                     current[k] = v
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (tuple, frozenset)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 16 =====
```
                 elif isinstance(v, (bytes, bytearray)):
                     # bytes aren't mergable or formattable
                     # only here to prevent the elif on enumerables catching it
-                    current[k] = v
+                    current[k] = None
                 # deal with things that are mergable - exists already in dest
                 elif k in current:
                     if types.are_all_this_type(Mapping, current[k], v):
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = None
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 17 =====
```
                     current[k] = v
                 # deal with things that are mergable - exists already in dest
                 elif k in current:
-                    if types.are_all_this_type(Mapping, current[k], v):
+                    if isinstance(current[k], dict) and not isinstance(v, Mapping):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if isinstance(current[k], dict) and not isinstance(v, Mapping):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 18 =====
```
                     current[k] = v
                 # deal with things that are mergable - exists already in dest
                 elif k in current:
-                    if types.are_all_this_type(Mapping, current[k], v):
+                    if types.are_all_this_type(Mapping, None, v):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, None, v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 19 =====
```
                     current[k] = v
                 # deal with things that are mergable - exists already in dest
                 elif k in current:
-                    if types.are_all_this_type(Mapping, current[k], v):
+                    if types.are_all_this_type(Mapping, current[k], None):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], None):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 20 =====
```
                     if types.are_all_this_type(Mapping, current[k], v):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
-                        merge_recurse(current[k], v)
+                        current[k] = self.get_formatted_value(v)  # Overwrites instead of merging
                     elif types.are_all_this_type(list, current[k], v):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        current[k] = self.get_formatted_value(v)  # Overwrites instead of merging
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 21 =====
```
                     if types.are_all_this_type(Mapping, current[k], v):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
-                        merge_recurse(current[k], v)
+                        current[k] = self.get_formatted_value(v) if isinstance(v, list) else current[k]  # Only updates if v is a list
                     elif types.are_all_this_type(list, current[k], v):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        current[k] = self.get_formatted_value(v) if isinstance(v, list) else current[k]  # Only updates if v is a list
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 22 =====
```
                     if types.are_all_this_type(Mapping, current[k], v):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
-                        merge_recurse(current[k], v)
+                        current[k] = v  # Directly assigns the new value, ignoring the existing one
                     elif types.are_all_this_type(list, current[k], v):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        current[k] = v  # Directly assigns the new value, ignoring the existing one
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 23 =====
```
                     if types.are_all_this_type(Mapping, current[k], v):
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
-                        merge_recurse(current[k], v)
+                        current[k] = {**current[k], **self.get_formatted_value(v)}  # Incorrectly attempts to merge as a dict
                     elif types.are_all_this_type(list, current[k], v):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        current[k] = {**current[k], **self.get_formatted_value(v)}  # Incorrectly attempts to merge as a dict
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 24 =====
```
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
-                    elif types.are_all_this_type(list, current[k], v):
+                    elif types.are_all_this_type(Mapping, current[k], v):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
                         current[k].extend(
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(Mapping, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 25 =====
```
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
-                    elif types.are_all_this_type(list, current[k], v):
+                    elif types.are_all_this_type(list, None, v):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
                         current[k].extend(
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, None, v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 26 =====
```
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
-                    elif types.are_all_this_type(list, current[k], v):
+                    elif types.are_all_this_type(list, current[k], None):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
                         current[k].extend(
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], None):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 27 =====
```
                         # it's dict-y, thus recurse through it to merge since
                         # it exists in dest
                         merge_recurse(current[k], v)
-                    elif types.are_all_this_type(list, current[k], v):
+                    elif types.are_all_this_type(list, current[k], v) and isinstance(current[k], dict):
                         # it's list-y. Extend mutates existing list since it
                         # exists in dest
                         current[k].extend(
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v) and isinstance(current[k], dict):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 28 =====
```
                         # exists in dest
                         current[k].extend(
                             self.get_formatted_value(v))
-                    elif types.are_all_this_type(tuple, current[k], v):
+                    elif types.are_all_this_type(Mapping, current[k], v):  # Incorrectly checks for Mapping instead of tuple
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(Mapping, current[k], v):  # Incorrectly checks for Mapping instead of tuple
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 29 =====
```
                         # exists in dest
                         current[k].extend(
                             self.get_formatted_value(v))
-                    elif types.are_all_this_type(tuple, current[k], v):
+                    elif types.are_all_this_type(list, current[k], v):  # Incorrectly checks for list instead of tuple
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(list, current[k], v):  # Incorrectly checks for list instead of tuple
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 30 =====
```
                         # exists in dest
                         current[k].extend(
                             self.get_formatted_value(v))
-                    elif types.are_all_this_type(tuple, current[k], v):
+                    elif types.are_all_this_type(str, current[k], v):  # Incorrectly checks for string instead of tuple
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(str, current[k], v):  # Incorrectly checks for string instead of tuple
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 31 =====
```
                         # exists in dest
                         current[k].extend(
                             self.get_formatted_value(v))
-                    elif types.are_all_this_type(tuple, current[k], v):
+                    elif types.are_all_this_type(tuple, None, v):
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, None, v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 32 =====
```
                         # exists in dest
                         current[k].extend(
                             self.get_formatted_value(v))
-                    elif types.are_all_this_type(tuple, current[k], v):
+                    elif types.are_all_this_type(tuple, current[k], None):
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], None):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 33 =====
```
                             self.get_formatted_value(v))
                     elif types.are_all_this_type(tuple, current[k], v):
                         # concatenate tuples
-                        current[k] = (
-                            current[k] + self.get_formatted_value(v))
+                        current[k] = None
                     elif types.are_all_this_type(Set, current[k], v):
                         # join sets
                         current[k] = (
@@ -78,4 +77,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = None
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 34 =====
```
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
-                    elif types.are_all_this_type(Set, current[k], v):
+                    elif types.are_all_this_type(Mapping, current[k], v):  # Incorrectly checks for Mapping instead of Set
                         # join sets
                         current[k] = (
                             current[k] | self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Mapping, current[k], v):  # Incorrectly checks for Mapping instead of Set
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 35 =====
```
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
-                    elif types.are_all_this_type(Set, current[k], v):
+                    elif types.are_all_this_type(Set, None, v):
                         # join sets
                         current[k] = (
                             current[k] | self.get_formatted_value(v))
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, None, v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 36 =====
```
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
-                    elif types.are_all_this_type(Set, current[k], v):
+                    elif types.are_all_this_type(Set, current[k], None):
                         # join sets
                         current[k] = (
                             current[k] | self.get_formatted_value(v))
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], None):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 37 =====
```
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
-                    elif types.are_all_this_type(Set, current[k], v):
+                    elif types.are_all_this_type(Set, current[k], v) and isinstance(current[k], list):  # Adds an unnecessary condition that can lead to incorrect behavior
                         # join sets
                         current[k] = (
                             current[k] | self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v) and isinstance(current[k], list):  # Adds an unnecessary condition that can lead to incorrect behavior
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 38 =====
```
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
-                    elif types.are_all_this_type(Set, current[k], v):
+                    elif types.are_all_this_type(list, current[k], v):  # Incorrectly checks for list instead of Set
                         # join sets
                         current[k] = (
                             current[k] | self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(list, current[k], v):  # Incorrectly checks for list instead of Set
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 39 =====
```
                         # concatenate tuples
                         current[k] = (
                             current[k] + self.get_formatted_value(v))
-                    elif types.are_all_this_type(Set, current[k], v):
+                    elif types.are_all_this_type(tuple, current[k], v):  # Incorrectly checks for tuple instead of Set
                         # join sets
                         current[k] = (
                             current[k] | self.get_formatted_value(v))
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):  # Incorrectly checks for tuple instead of Set
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 40 =====
```
                             current[k] + self.get_formatted_value(v))
                     elif types.are_all_this_type(Set, current[k], v):
                         # join sets
-                        current[k] = (
-                            current[k] | self.get_formatted_value(v))
+                        current[k] = None
                     else:
                         # at this point it's not mergable
                         current[k] = self.get_formatted_value(v)
@@ -78,4 +77,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = None
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 41 =====
```
                     elif types.are_all_this_type(Set, current[k], v):
                         # join sets
                         current[k] = (
-                            current[k] | self.get_formatted_value(v))
+                            current[k] & self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
                         current[k] = self.get_formatted_value(v)
@@ -78,4 +78,4 @@                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] & self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 42 =====
```
                             current[k] | self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
-                        current[k] = self.get_formatted_value(v)
+                        current[k] = None
                 else:
                     # at this point it's not mergable, nor in context
                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = None
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 43 =====
```
                             current[k] | self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
-                        current[k] = self.get_formatted_value(v)
+                        current[k] = None  # This will set the value to None, losing the original data.
                 else:
                     # at this point it's not mergable, nor in context
                     current[k] = self.get_formatted_value(v)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = None  # This will set the value to None, losing the original data.
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 44 =====
```
                             current[k] | self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
-                        current[k] = self.get_formatted_value(v)
+                        current[k] = self.get_formatted_value(None)
                 else:
                     # at this point it's not mergable, nor in context
                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(None)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 45 =====
```
                             current[k] | self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
-                        current[k] = self.get_formatted_value(v)
+                        current[k] = self.get_formatted_value(v) if isinstance(v, str) else v  # This will only format if v is a string, ignoring other types.
                 else:
                     # at this point it's not mergable, nor in context
                     current[k] = self.get_formatted_value(v)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v) if isinstance(v, str) else v  # This will only format if v is a string, ignoring other types.
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 46 =====
```
                             current[k] | self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
-                        current[k] = self.get_formatted_value(v)
+                        current[k] = self.get_formatted_value(v) if k not in current else current[k]  # This will skip updating if the key already exists, potentially leaving old values.
                 else:
                     # at this point it's not mergable, nor in context
                     current[k] = self.get_formatted_value(v)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v) if k not in current else current[k]  # This will skip updating if the key already exists, potentially leaving old values.
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 47 =====
```
                             current[k] | self.get_formatted_value(v))
                     else:
                         # at this point it's not mergable
-                        current[k] = self.get_formatted_value(v)
+                        current[k] = v  # This will assign the raw value from add_me, bypassing formatting.
                 else:
                     # at this point it's not mergable, nor in context
                     current[k] = self.get_formatted_value(v)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = v  # This will assign the raw value from add_me, bypassing formatting.
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 48 =====
```
                         current[k] = self.get_formatted_value(v)
                 else:
                     # at this point it's not mergable, nor in context
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = None
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = None

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 49 =====
```
                         current[k] = self.get_formatted_value(v)
                 else:
                     # at this point it's not mergable, nor in context
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = None  # This will set the key to None, losing the value from add_me.
 
         # first iteration starts at context dict root
         merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = None  # This will set the key to None, losing the value from add_me.

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 50 =====
```
                         current[k] = self.get_formatted_value(v)
                 else:
                     # at this point it's not mergable, nor in context
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = self.get_formatted_value(None)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(None)

        # first iteration starts at context dict root
        merge_recurse(self, add_me)

```
===== 51 =====
```
                         current[k] = self.get_formatted_value(v)
                 else:
                     # at this point it's not mergable, nor in context
-                    current[k] = self.get_formatted_value(v)
+                    current[k] = self.get_formatted_value(v) if isinstance(v, str) else v  # This will only set the value if it's a string, ignoring other types.
 
         # first iteration starts at context dict root
         merge_recurse(self, add_me)
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v) if isinstance(v, str) else v  # This will only set the value if it's a string, ignoring other types.

        # first iteration starts at context dict root
        merge_recurse(self, add_me)
```
===== 52 =====
```
                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, {k: v for k, v in add_me.items() if isinstance(v, dict)})
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, {k: v for k, v in add_me.items() if isinstance(v, dict)})
```
===== 53 =====
```
                     current[k] = self.get_formatted_value(v)
 
         # first iteration starts at context dict root
-        merge_recurse(self, add_me)+        merge_recurse(self, {k: v for k, v in add_me.items() if k not in self})
```
```
    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.

        Bottom-up merge where add_me merges into context. Applies string
        interpolation where the type is a string. Where a key exists in
        context already, add_me's value will overwrite what's in context
        already.

        Supports nested hierarchy. add_me can contains dicts/lists/enumerables
        that contain other enumerables et. It doesn't restrict levels of
        nesting, so if you really want to go crazy with the levels you can, but
        you might blow your stack.

        If something from add_me exists in context already, but add_me's value
        is of a different type, add_me will overwrite context. Do note this.
        i.e if you had context['int_key'] == 1 and
        add_me['int_key'] == 'clearly not a number', the end result would be
        context['int_key'] == 'clearly not a number'

        If add_me contains lists/sets/tuples, this merges these
        additively, meaning it appends values from add_me to the existing
        sequence.

        Args:
            add_me: dict. Merge this dict into context.

        Returns:
            None. All operations mutate this instance of context.

        """
        def merge_recurse(current, add_me):
            """Walk the current context tree in recursive inner function.

            On 1st iteration, current = self(i.e root of context)
            On subsequent recursive iterations, current is wherever you're at
            in the nested context hierarchy.

            Args:
                current: dict. Destination of merge.
                add_me: dict. Merge this to current.
            """
            for k, v in add_me.items():
                # key supports interpolation
                k = self.get_formatted_value(k)

                # str not mergable, so it doesn't matter if it exists in dest
                if isinstance(v, (str, SpecialTagDirective)):
                    # just overwrite dest - str adds/edits indiscriminately
                    current[k] = self.get_formatted_value(v)
                elif isinstance(v, (bytes, bytearray)):
                    # bytes aren't mergable or formattable
                    # only here to prevent the elif on enumerables catching it
                    current[k] = v
                # deal with things that are mergable - exists already in dest
                elif k in current:
                    if types.are_all_this_type(Mapping, current[k], v):
                        # it's dict-y, thus recurse through it to merge since
                        # it exists in dest
                        merge_recurse(current[k], v)
                    elif types.are_all_this_type(list, current[k], v):
                        # it's list-y. Extend mutates existing list since it
                        # exists in dest
                        current[k].extend(
                            self.get_formatted_value(v))
                    elif types.are_all_this_type(tuple, current[k], v):
                        # concatenate tuples
                        current[k] = (
                            current[k] + self.get_formatted_value(v))
                    elif types.are_all_this_type(Set, current[k], v):
                        # join sets
                        current[k] = (
                            current[k] | self.get_formatted_value(v))
                    else:
                        # at this point it's not mergable
                        current[k] = self.get_formatted_value(v)
                else:
                    # at this point it's not mergable, nor in context
                    current[k] = self.get_formatted_value(v)

        # first iteration starts at context dict root
        merge_recurse(self, {k: v for k, v in add_me.items() if k not in self})
```
