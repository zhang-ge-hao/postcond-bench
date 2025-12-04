https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L1783-L1803
```
@icontract.snapshot(lambda root: root.inorder, name="inorder")
@icontract.ensure(
    lambda OLD, root, result: 
    result == all(
        OLD.inorder[i].val == OLD.inorder[len(OLD.inorder) - 1 - i].val for i in range(len(OLD.inorder))
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
===== 0 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is None and right is not None:
             return True
         if left is None or right is None:
             return False
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is not None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
===== 1 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is None and right is not None:
             return True
         if left is None or right is None:
             return False
@@ -18,4 +18,4 @@             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is not None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 2 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is None or right is None:
             return True
         if left is None or right is None:
             return False
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None or right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
===== 3 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is None or right is None:
             return True
         if left is None or right is None:
             return False
@@ -18,4 +18,4 @@             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None or right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 4 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is not None and right is None:
             return True
         if left is None or right is None:
             return False
@@ -18,4 +18,4 @@             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is not None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 5 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is not None and right is not None:
             return True
         if left is None or right is None:
             return False
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is not None and right is not None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
===== 6 =====
```
     """
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
-        if left is None and right is None:
+        if left is not None or right is None:
             return True
         if left is None or right is None:
             return False
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is not None or right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
===== 7 =====
```
 
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
         if left is None and right is None:
-            return True
+            return False
         if left is None or right is None:
             return False
         return (
@@ -18,4 +18,4 @@             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return False
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 8 =====
```
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
         if left is None and right is None:
             return True
-        if left is None or right is None:
+        if left is None or right is not None:
             return False
         return (
             left.val == right.val
@@ -18,4 +18,4 @@             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is not None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 9 =====
```
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
         if left is None and right is None:
             return True
-        if left is None or right is None:
+        if left is not None and right is not None:
             return False
         return (
             left.val == right.val
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is not None and right is not None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
===== 10 =====
```
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
         if left is None and right is None:
             return True
-        if left is None or right is None:
+        if left is not None or right is None:
             return False
         return (
             left.val == right.val
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is not None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)
```
===== 11 =====
```
     def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
         if left is None and right is None:
             return True
-        if left is None or right is None:
+        if left is not None or right is None:
             return False
         return (
             left.val == right.val
@@ -18,4 +18,4 @@             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is not None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 12 =====
```
         if left is None and right is None:
             return True
         if left is None or right is None:
-            return False
+            return True
         return (
             left.val == right.val
             and symmetric_helper(left.left, right.right)
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return True
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 13 =====
```
         if left is None or right is None:
             return False
         return (
-            left.val == right.val
+            left.val != right.val
             and symmetric_helper(left.left, right.right)
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val != right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 14 =====
```
         if left is None or right is None:
             return False
         return (
-            left.val == right.val
-            and symmetric_helper(left.left, right.right)
+            left.val == right.val or symmetric_helper(left.left, right.right)
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val or symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 15 =====
```
             return False
         return (
             left.val == right.val
-            and symmetric_helper(left.left, right.right)
-            and symmetric_helper(left.right, right.left)
+            and symmetric_helper(left.left, right.right) or symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right) or symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, root)

```
===== 16 =====
```
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(None, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(None, root)
```
===== 17 =====
```
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(None, root)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(None, root)

```
===== 18 =====
```
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, None)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, None)
```
===== 19 =====
```
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root, None)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root, None)

```
===== 20 =====
```
             and symmetric_helper(left.right, right.left)
         )
 
-    return symmetric_helper(root, root)+    return symmetric_helper(root.left, root.left)
```
```
def _is_symmetric(root: Optional[Node]) -> bool:
    """Check if the binary tree is symmetric.

    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :return: True if the binary tree is symmetric, False otherwise.
    :rtype: bool
    """

    def symmetric_helper(left: Optional[Node], right: Optional[Node]) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and symmetric_helper(left.left, right.right)
            and symmetric_helper(left.right, right.left)
        )

    return symmetric_helper(root.left, root.left)
```
