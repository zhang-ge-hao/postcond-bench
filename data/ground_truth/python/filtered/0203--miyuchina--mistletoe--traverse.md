https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/utils.py#L6-L33
```
🈚️

yield
```
```
@icontract.snapshot(lambda source: list(source.children or []), name="children")
@icontract.ensure(lambda result, source, klass, depth, include_source, OLD: list(source.children or []) == OLD.children)
@icontract.ensure(lambda result, source, klass, depth, include_source, OLD: depth is None or (isinstance(depth, int) and depth >= 0))
@icontract.ensure(lambda result, source, klass, depth, include_source, OLD: isinstance(include_source, bool))
@icontract.ensure(lambda result, source, klass, depth, include_source, OLD: klass is None or isinstance(klass, type))
@icontract.ensure(lambda result, source, klass, depth, include_source, OLD: hasattr(result, "__iter__"))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
===== 0 =====
```
     Yields:
         A container for an element, its parent and depth
     """
-    current_depth = 0
+    current_depth = 1
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 1
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 1 =====
```
         A container for an element, its parent and depth
     """
     current_depth = 0
-    if include_source and (klass is None or isinstance(source, klass)):
+    if include_source and (klass is None or isinstance(source, klass)) and current_depth > 0:
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)) and current_depth > 0:
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 2 =====
```
         A container for an element, its parent and depth
     """
     current_depth = 0
-    if include_source and (klass is None or isinstance(source, klass)):
+    if include_source and (klass is not None and isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is not None and isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 3 =====
```
         A container for an element, its parent and depth
     """
     current_depth = 0
-    if include_source and (klass is None or isinstance(source, klass)):
+    if include_source and klass is not None and not isinstance(source, klass):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and klass is not None and not isinstance(source, klass):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 4 =====
```
         A container for an element, its parent and depth
     """
     current_depth = 0
-    if include_source and (klass is None or isinstance(source, klass)):
+    if include_source or (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source or (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 5 =====
```
         A container for an element, its parent and depth
     """
     current_depth = 0
-    if include_source and (klass is None or isinstance(source, klass)):
+    if not include_source or (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if not include_source or (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 6 =====
```
     """
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
-        yield TraverseResult(source, None, current_depth)
+        yield TraverseResult(None, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(None, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 7 =====
```
     """
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
-        yield TraverseResult(source, None, current_depth)
+        yield TraverseResult(source, None, None)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, None)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 8 =====
```
     """
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
-        yield TraverseResult(source, None, current_depth)
+        yield TraverseResult(source, None, current_depth + 1)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth + 1)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 9 =====
```
     """
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
-        yield TraverseResult(source, None, current_depth)
+        yield TraverseResult(source, None, current_depth - 1)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth - 1)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 10 =====
```
     """
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
-        yield TraverseResult(source, None, current_depth)
+        yield TraverseResult(source, source, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, source, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 11 =====
```
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
-    next_children = [(source, c) for c in source.children or []]
+    next_children = None
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
         new_children = []
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = None
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 12 =====
```
     current_depth = 0
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
-    next_children = [(source, c) for c in source.children or []]
+    next_children = [(source, c) for c in source.children and []]
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
         new_children = []
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children and []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 13 =====
```
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
-    while next_children and (depth is None or current_depth < depth):
+    while next_children and (depth is None or current_depth <= depth):
         current_depth += 1
         new_children = []
         for parent, child in next_children:
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth <= depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 14 =====
```
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
-    while next_children and (depth is None or current_depth < depth):
+    while next_children and (depth is None or current_depth <= depth):
         current_depth += 1
         new_children = []
         for parent, child in next_children:
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth <= depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 15 =====
```
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
-    while next_children and (depth is None or current_depth < depth):
+    while next_children and (depth is None or current_depth > depth):
         current_depth += 1
         new_children = []
         for parent, child in next_children:
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth > depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 16 =====
```
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
-    while next_children and (depth is None or current_depth < depth):
+    while next_children and (depth is not None and current_depth <= depth):
         current_depth += 1
         new_children = []
         for parent, child in next_children:
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is not None and current_depth <= depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 17 =====
```
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
-    while next_children and (depth is None or current_depth < depth):
+    while next_children and (depth is not None and current_depth >= depth):
         current_depth += 1
         new_children = []
         for parent, child in next_children:
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is not None and current_depth >= depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 18 =====
```
     if include_source and (klass is None or isinstance(source, klass)):
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
-    while next_children and (depth is None or current_depth < depth):
+    while next_children and depth is not None and current_depth < depth:
         current_depth += 1
         new_children = []
         for parent, child in next_children:
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and depth is not None and current_depth < depth:
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 19 =====
```
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
-        current_depth += 1
+        current_depth += 2
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 2
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 20 =====
```
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
-        current_depth += 1
+        current_depth -= 1
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth -= 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 21 =====
```
         yield TraverseResult(source, None, current_depth)
     next_children = [(source, c) for c in source.children or []]
     while next_children and (depth is None or current_depth < depth):
-        current_depth += 1
+        current_depth = 1
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
@@ -25,4 +25,4 @@             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth = 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 22 =====
```
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
         new_children = []
-        for parent, child in next_children:
+        for parent, child in next_children[:1]:  # Only processes the first child
             if klass is None or isinstance(child, klass):
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children[:1]:  # Only processes the first child
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 23 =====
```
     while next_children and (depth is None or current_depth < depth):
         current_depth += 1
         new_children = []
-        for parent, child in next_children:
+        for parent, child in reversed(next_children):  # Processes children in reverse order
             if klass is None or isinstance(child, klass):
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in reversed(next_children):  # Processes children in reverse order
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 24 =====
```
         current_depth += 1
         new_children = []
         for parent, child in next_children:
-            if klass is None or isinstance(child, klass):
+            if klass is None or isinstance(None, klass):
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(None, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 25 =====
```
         current_depth += 1
         new_children = []
         for parent, child in next_children:
-            if klass is None or isinstance(child, klass):
+            if klass is None or isinstance(child, object):  # Always true for any child, yields all children regardless of klass
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, object):  # Always true for any child, yields all children regardless of klass
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 26 =====
```
         current_depth += 1
         new_children = []
         for parent, child in next_children:
-            if klass is None or isinstance(child, klass):
+            if klass is None or not isinstance(child, klass):  # Inverts the condition, yields incorrect nodes
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or not isinstance(child, klass):  # Inverts the condition, yields incorrect nodes
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 27 =====
```
         current_depth += 1
         new_children = []
         for parent, child in next_children:
-            if klass is None or isinstance(child, klass):
+            if klass is not None and isinstance(child, klass):  # Incorrect logic: should yield only if klass is None or matches
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is not None and isinstance(child, klass):  # Incorrect logic: should yield only if klass is None or matches
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 28 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(None, parent, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(None, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 29 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(child, None, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, None, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 30 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(child, None, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, None, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 31 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(child, parent, None)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, None)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 32 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(child, parent, None)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, None)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children

```
===== 33 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(child, parent, current_depth + 1)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth + 1)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 34 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(child, parent, current_depth - 1)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth - 1)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 35 =====
```
         new_children = []
         for parent, child in next_children:
             if klass is None or isinstance(child, klass):
-                yield TraverseResult(child, parent, current_depth)
+                yield TraverseResult(parent, child, current_depth)
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(parent, child, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 36 =====
```
             if klass is None or isinstance(child, klass):
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
-                [(child, c) for c in child.children or []]
+                [(child, c) for c in child.children and []]
             )
-        next_children = new_children+        next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children and []]
            )
        next_children = new_children

```
===== 37 =====
```
             if klass is None or isinstance(child, klass):
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
-                [(child, c) for c in child.children or []]
+                [(child, c) for c in child.children if isinstance(c, str)]
             )
         next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children if isinstance(c, str)]
            )
        next_children = new_children
```
===== 38 =====
```
             if klass is None or isinstance(child, klass):
                 yield TraverseResult(child, parent, current_depth)
             new_children.extend(
-                [(child, c) for c in child.children or []]
+                [(parent, c) for c in child.children or []]
             )
         next_children = new_children
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(parent, c) for c in child.children or []]
            )
        next_children = new_children
```
===== 39 =====
```
             new_children.extend(
                 [(child, c) for c in child.children or []]
             )
-        next_children = new_children+        next_children = None
```
```
def traverse(source, klass=None, depth=None, include_source=False):
    """Traverse the syntax tree, recursively yielding children.

    Args:

        source: The source syntax token
        klass: filter children by a certain token class
        depth (int): The depth to recurse into the tree
        include_source (bool): whether to first yield the source element
                               (provided it passes any given ``klass`` filter)

    Yields:
        A container for an element, its parent and depth
    """
    current_depth = 0
    if include_source and (klass is None or isinstance(source, klass)):
        yield TraverseResult(source, None, current_depth)
    next_children = [(source, c) for c in source.children or []]
    while next_children and (depth is None or current_depth < depth):
        current_depth += 1
        new_children = []
        for parent, child in next_children:
            if klass is None or isinstance(child, klass):
                yield TraverseResult(child, parent, current_depth)
            new_children.extend(
                [(child, c) for c in child.children or []]
            )
        next_children = None

```
