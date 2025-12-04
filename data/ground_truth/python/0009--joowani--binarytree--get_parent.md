https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/./binarytree/__init__.py#L2131-L2180
```
@icontract.ensure(
    lambda result, root, child:
        result is (
            None
            if root is None or child is None
            else next(
                (
                    node
                    for node in root.levelorder
                    if node.left is child or node.right is child
                ),
                None,
            )
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
===== 0 =====
```
           4
         <BLANKLINE>
     """
-    if child is None:
+    if child is not None:
         return None
 
     stack: List[Optional[Node]] = [root]
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is not None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 1 =====
```
           4
         <BLANKLINE>
     """
-    if child is None:
+    if child is not None:
         return None
 
     stack: List[Optional[Node]] = [root]
@@ -47,4 +47,4 @@             else:
                 stack.append(node.left)
                 stack.append(node.right)
-    return None+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is not None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None

```
===== 2 =====
```
           4
         <BLANKLINE>
     """
-    if child is None:
+    if child is root:
         return None
 
     stack: List[Optional[Node]] = [root]
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is root:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 3 =====
```
           4
         <BLANKLINE>
     """
-    if child is None:
+    if child.left is None and child.right is None:
         return None
 
     stack: List[Optional[Node]] = [root]
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child.left is None and child.right is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 4 =====
```
     if child is None:
         return None
 
-    stack: List[Optional[Node]] = [root]
+    stack: List[Optional[Node]] = None
 
     while stack:
         node = stack.pop()
@@ -47,4 +47,4 @@             else:
                 stack.append(node.left)
                 stack.append(node.right)
-    return None+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = None

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None

```
===== 5 =====
```
 
     stack: List[Optional[Node]] = [root]
 
-    while stack:
+    while not stack:
         node = stack.pop()
         if node:
             if node.left is child or node.right is child:
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while not stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 6 =====
```
 
     while stack:
         node = stack.pop()
-        if node:
+        if node is None:
             if node.left is child or node.right is child:
                 return node
             else:
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node is None:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 7 =====
```
 
     while stack:
         node = stack.pop()
-        if node:
+        if node.left and node.right:
             if node.left is child or node.right is child:
                 return node
             else:
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node.left and node.right:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 8 =====
```
 
     while stack:
         node = stack.pop()
-        if node:
+        if not node:
             if node.left is child or node.right is child:
                 return node
             else:
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if not node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 9 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node is child:
                 return node
             else:
                 stack.append(node.left)
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 10 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node.left is child and node.right is child:
                 return node
             else:
                 stack.append(node.left)
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child and node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 11 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node.left is child and node.right is child:
                 return node
             else:
                 stack.append(node.left)
                 stack.append(node.right)
-    return None+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child and node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None

```
===== 12 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node.left is child or node.left is child:
                 return node
             else:
                 stack.append(node.left)
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.left is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 13 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node.left is child or node.right is not child:
                 return node
             else:
                 stack.append(node.left)
                 stack.append(node.right)
-    return None+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is not child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None

```
===== 14 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node.left is not None and node.right is not None:
                 return node
             else:
                 stack.append(node.left)
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is not None and node.right is not None:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None
```
===== 15 =====
```
     while stack:
         node = stack.pop()
         if node:
-            if node.left is child or node.right is child:
+            if node.left is not child or node.right is child:
                 return node
             else:
                 stack.append(node.left)
                 stack.append(node.right)
-    return None+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is not child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.right)
    return None

```
===== 16 =====
```
             if node.left is child or node.right is child:
                 return node
             else:
-                stack.append(node.left)
+                stack.append(None)
                 stack.append(node.right)
-    return None+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(None)
                stack.append(node.right)
    return None

```
===== 17 =====
```
             if node.left is child or node.right is child:
                 return node
             else:
-                stack.append(node.left)
+                stack.append(None)  # Appending None instead of the left child
                 stack.append(node.right)
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(None)  # Appending None instead of the left child
                stack.append(node.right)
    return None
```
===== 18 =====
```
             if node.left is child or node.right is child:
                 return node
             else:
-                stack.append(node.left)
+                stack.append(node.left if node.right is None else None)  # Conditional append that may skip the left child
                 stack.append(node.right)
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left if node.right is None else None)  # Conditional append that may skip the left child
                stack.append(node.right)
    return None
```
===== 19 =====
```
             if node.left is child or node.right is child:
                 return node
             else:
-                stack.append(node.left)
+                stack.append(node.right)  # Incorrectly appending the right child instead of the left
                 stack.append(node.right)
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.right)  # Incorrectly appending the right child instead of the left
                stack.append(node.right)
    return None
```
===== 20 =====
```
                 return node
             else:
                 stack.append(node.left)
-                stack.append(node.right)
-    return None+                stack.append(None)
+    return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(None)
    return None

```
===== 21 =====
```
                 return node
             else:
                 stack.append(node.left)
-                stack.append(node.right)
+                stack.append(None)  # This will add a None value to the stack, potentially causing incorrect behavior.
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(None)  # This will add a None value to the stack, potentially causing incorrect behavior.
    return None
```
===== 22 =====
```
                 return node
             else:
                 stack.append(node.left)
-                stack.append(node.right)
+                stack.append(node.left if node.left is not None else node.right)  # This will add the left child if it exists, otherwise the right child, which may not be intended.
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.left if node.left is not None else node.right)  # This will add the left child if it exists, otherwise the right child, which may not be intended.
    return None
```
===== 23 =====
```
                 return node
             else:
                 stack.append(node.left)
-                stack.append(node.right)
+                stack.append(node.left if node.right is None else None)  # This will conditionally add a child, potentially skipping the right child.
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.left if node.right is None else None)  # This will conditionally add a child, potentially skipping the right child.
    return None
```
===== 24 =====
```
                 return node
             else:
                 stack.append(node.left)
-                stack.append(node.right)
+                stack.append(node.left)  # This will cause the left child to be added instead of the right child.
     return None
```
```
def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
    """Search the binary tree and return the parent of given child.

    :param root: Root node of the binary tree.
    :type: binarytree.Node | None
    :param child: Child node.
    :rtype: binarytree.Node | None
    :return: Parent node, or None if missing.
    :rtype: binarytree.Node | None

    **Example**:

    .. doctest::

        >>> from binarytree import Node, get_parent
        >>>
        >>> root = Node(1)
        >>> root.left = Node(2)
        >>> root.right = Node(3)
        >>> root.left.right = Node(4)
        >>>
        >>> print(root)
        <BLANKLINE>
          __1
         /   \\
        2     3
         \\
          4
        <BLANKLINE>
        >>> print(get_parent(root, root.left.right))
        <BLANKLINE>
        2
         \\
          4
        <BLANKLINE>
    """
    if child is None:
        return None

    stack: List[Optional[Node]] = [root]

    while stack:
        node = stack.pop()
        if node:
            if node.left is child or node.right is child:
                return node
            else:
                stack.append(node.left)
                stack.append(node.left)  # This will cause the left child to be added instead of the right child.
    return None
```
