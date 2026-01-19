https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/cycle_detection.py#L22-L35
```
🈚️

It's hard

```
```
@icontract.snapshot(lambda traversal_states: traversal_states.copy())
@icontract.ensure(lambda OLD, traversal_states, vertex, result:
                 (OLD.traversal_states[vertex] != TraversalState.GRAY)
                 or (result and traversal_states == OLD.traversal_states))
@icontract.ensure(lambda traversal_states, vertex, result:
                 (not result) or (traversal_states[vertex] == TraversalState.GRAY))
@icontract.ensure(lambda traversal_states, vertex, result:
                 result or (traversal_states[vertex] == TraversalState.BLACK))
@icontract.ensure(lambda OLD, traversal_states, vertex, result:
                 (not result)
                 or (OLD.traversal_states[vertex] == TraversalState.GRAY)
                 or any(v != vertex and traversal_states[v] == TraversalState.GRAY
                        for v in traversal_states))
```
[3, 5, 8, 9]
===== 3 =====
```
     :param: traversal_states: for each vertex, the state it is in
     """
     if traversal_states[vertex] == TraversalState.GRAY:
-        return True
+        return False
     traversal_states[vertex] = TraversalState.GRAY
     for neighbor in graph[vertex]:
         if is_in_cycle(graph, traversal_states, neighbor):
             return True
     traversal_states[vertex] = TraversalState.BLACK
-    return False+    return False
```
```
def is_in_cycle(graph, traversal_states, vertex):
    """
    Determines if the given vertex is in a cycle.

    :param: traversal_states: for each vertex, the state it is in
    """
    if traversal_states[vertex] == TraversalState.GRAY:
        return False
    traversal_states[vertex] = TraversalState.GRAY
    for neighbor in graph[vertex]:
        if is_in_cycle(graph, traversal_states, neighbor):
            return True
    traversal_states[vertex] = TraversalState.BLACK
    return False

```
===== 5 =====
```
         return True
     traversal_states[vertex] = TraversalState.GRAY
     for neighbor in graph[vertex]:
-        if is_in_cycle(graph, traversal_states, neighbor):
+        if is_in_cycle(graph, traversal_states, neighbor) and traversal_states[neighbor] == TraversalState.WHITE:
             return True
     traversal_states[vertex] = TraversalState.BLACK
     return False
```
```
def is_in_cycle(graph, traversal_states, vertex):
    """
    Determines if the given vertex is in a cycle.

    :param: traversal_states: for each vertex, the state it is in
    """
    if traversal_states[vertex] == TraversalState.GRAY:
        return True
    traversal_states[vertex] = TraversalState.GRAY
    for neighbor in graph[vertex]:
        if is_in_cycle(graph, traversal_states, neighbor) and traversal_states[neighbor] == TraversalState.WHITE:
            return True
    traversal_states[vertex] = TraversalState.BLACK
    return False
```
===== 8 =====
```
     traversal_states[vertex] = TraversalState.GRAY
     for neighbor in graph[vertex]:
         if is_in_cycle(graph, traversal_states, neighbor):
-            return True
+            return False
     traversal_states[vertex] = TraversalState.BLACK
-    return False+    return False
```
```
def is_in_cycle(graph, traversal_states, vertex):
    """
    Determines if the given vertex is in a cycle.

    :param: traversal_states: for each vertex, the state it is in
    """
    if traversal_states[vertex] == TraversalState.GRAY:
        return True
    traversal_states[vertex] = TraversalState.GRAY
    for neighbor in graph[vertex]:
        if is_in_cycle(graph, traversal_states, neighbor):
            return False
    traversal_states[vertex] = TraversalState.BLACK
    return False

```
===== 9 =====
```
         if is_in_cycle(graph, traversal_states, neighbor):
             return True
     traversal_states[vertex] = TraversalState.BLACK
-    return False+    return True
```
```
def is_in_cycle(graph, traversal_states, vertex):
    """
    Determines if the given vertex is in a cycle.

    :param: traversal_states: for each vertex, the state it is in
    """
    if traversal_states[vertex] == TraversalState.GRAY:
        return True
    traversal_states[vertex] = TraversalState.GRAY
    for neighbor in graph[vertex]:
        if is_in_cycle(graph, traversal_states, neighbor):
            return True
    traversal_states[vertex] = TraversalState.BLACK
    return True

```
