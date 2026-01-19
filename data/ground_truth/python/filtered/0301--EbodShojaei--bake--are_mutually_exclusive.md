https://github.com/EbodShojaei/bake/blob/8de354fea3723526e682811000b50dde29b02d45/./mbake/utils/line_utils.py#L1349-L1376
```
🈚️

Error will be catched.

specified error process


@icontract.ensure(
    lambda context1, context2, result:
    result
    == (
        # 如果两个 context 完全相同 -> 一定不互斥
        False
        if context1 == context2
        # 如果有一个是空的（无条件），另一个非空 -> 也不互斥
        else False
        if (not context1 or not context2)
        # 否则，从外到内逐层比较，只要某一层分支不同就互斥
        else any(
            context1[i] != context2[i]
            for i in range(min(len(context1), len(context2)))
        )
    )
)
```
```
@icontract.ensure(lambda result, context1, context2: (context1 != context2) or (result is False))
@icontract.ensure(lambda result, context1, context2: (context1 and context2) or (result is False))
@icontract.ensure(lambda result, context1, context2: (not (context1 and context2 and context1 != context2)) or (result == any(context1[i] != context2[i] for i in range(min(len(context1), len(context2))))))
@icontract.ensure(lambda result, context1, context2: (not result) or (context1 and context2 and context1 != context2 and any(context1[i] != context2[i] for i in range(min(len(context1), len(context2))))))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
===== 0 =====
```
             True if contexts are mutually exclusive
         """
         # If contexts are identical, not mutually exclusive
-        if context1 == context2:
+        if context1 != context2:
             return False
 
         # If one context is empty and the other not, not mutually exclusive
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 != context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 1 =====
```
             True if contexts are mutually exclusive
         """
         # If contexts are identical, not mutually exclusive
-        if context1 == context2:
+        if context1 != context2:
             return False
 
         # If one context is empty and the other not, not mutually exclusive
@@ -25,4 +25,4 @@         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] != context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 != context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))

```
===== 2 =====
```
             True if contexts are mutually exclusive
         """
         # If contexts are identical, not mutually exclusive
-        if context1 == context2:
+        if context1 and context2:
             return False
 
         # If one context is empty and the other not, not mutually exclusive
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 and context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 3 =====
```
             True if contexts are mutually exclusive
         """
         # If contexts are identical, not mutually exclusive
-        if context1 == context2:
+        if len(context1) == len(context2):
             return False
 
         # If one context is empty and the other not, not mutually exclusive
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if len(context1) == len(context2):
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 4 =====
```
         """
         # If contexts are identical, not mutually exclusive
         if context1 == context2:
-            return False
+            return True
 
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
@@ -25,4 +25,4 @@         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] != context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return True

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))

```
===== 5 =====
```
 
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
-        if not context1 or not context2:
+        if context1 and context2:
             return False
 
         # Compare contexts level by level
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if context1 and context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 6 =====
```
 
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
-        if not context1 or not context2:
+        if context1 or context2:
             return False
 
         # Compare contexts level by level
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if context1 or context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 7 =====
```
 
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
-        if not context1 or not context2:
+        if context1 or not context2:
             return False
 
         # Compare contexts level by level
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] != context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))

```
===== 8 =====
```
 
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
-        if not context1 or not context2:
+        if len(context1) == len(context2):
             return False
 
         # Compare contexts level by level
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if len(context1) == len(context2):
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 9 =====
```
 
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
-        if not context1 or not context2:
+        if not context1 or context2:
             return False
 
         # Compare contexts level by level
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] != context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))

```
===== 10 =====
```
         # If one context is empty and the other not, not mutually exclusive
         # in the sense that one is unconditional and the other is conditional
         if not context1 or not context2:
-            return False
+            return True
 
         # Compare contexts level by level
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] != context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return True

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))

```
===== 11 =====
```
             return False
 
         # Compare contexts level by level
-        min_len = min(len(context1), len(context2))
+        min_len = 0  # Sets min_len to zero, which will always lead to incorrect behavior
 
         # If contexts differ at any level, mutually exclusive
         return any(context1[i] != context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = 0  # Sets min_len to zero, which will always lead to incorrect behavior

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] != context2[i] for i in range(min_len))
```
===== 12 =====
```
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return all(context1[i] == context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return all(context1[i] == context2[i] for i in range(min_len))
```
===== 13 =====
```
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] == context2[i] for i in range(len(context1)))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] == context2[i] for i in range(len(context1)))
```
===== 14 =====
```
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] == context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] == context2[i] for i in range(min_len))
```
===== 15 =====
```
         min_len = min(len(context1), len(context2))
 
         # If contexts differ at any level, mutually exclusive
-        return any(context1[i] != context2[i] for i in range(min_len))+        return any(context1[i] == context2[i] for i in range(min_len))
```
```
    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.

        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.

        Args:
            context1: First conditional context
            context2: Second conditional context

        Returns:
            True if contexts are mutually exclusive
        """
        # If contexts are identical, not mutually exclusive
        if context1 == context2:
            return False

        # If one context is empty and the other not, not mutually exclusive
        # in the sense that one is unconditional and the other is conditional
        if not context1 or not context2:
            return False

        # Compare contexts level by level
        min_len = min(len(context1), len(context2))

        # If contexts differ at any level, mutually exclusive
        return any(context1[i] == context2[i] for i in range(min_len))

```
