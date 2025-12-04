https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/tarjan.py#L29-L65
```
@icontract.snapshot(lambda self: self.index, name="self_index")
@icontract.snapshot(
    lambda self: {
        node: (
            getattr(node, "index", None),
            getattr(node, "lowlink", None),
            getattr(node, "on_stack", False),
        )
        for node in self.graph.nodes
    },
    name="nodes_state",
)
@icontract.snapshot(lambda sccs: len(sccs), name="sccs_len")
@icontract.snapshot(
    lambda self, vertex, sccs: __import__("functools").reduce(
        lambda R, _: R | {w for v in R for w in self.graph.adjacency_list[v]},
        range(len(self.graph.nodes)),
        {vertex},
    ),
    name="reachable_from_vertex",
)
@icontract.ensure(
    lambda OLD, self, vertex, sccs:
    (
        vertex.index == OLD.self_index
        and vertex.lowlink <= vertex.index
        and self.index >= OLD.self_index + 1
        and len(sccs) >= OLD.sccs_len
        and all(
            (
                (node in self.stack)
                and getattr(node, "on_stack", False) is True
            )
            or (
                (node not in self.stack)
                and getattr(node, "on_stack", False) is False
            )
            for node in self.graph.nodes
        )
        and all(adj.index is not None for adj in self.graph.adjacency_list[vertex])
        and all(
            isinstance(comp, list)
            and len(comp) > 0
            and len({id(n) for n in comp}) == len(comp)
            and all(
                getattr(n, "index", None) is not None
                and getattr(n, "on_stack", False) is False
                for n in comp
            )
            and comp == sorted(comp)
            for comp in sccs[OLD.sccs_len:]
        )
        and (
            (
                vertex.lowlink == vertex.index
                and vertex.on_stack is False
                and len(
                    [1 for comp in sccs[OLD.sccs_len:] if vertex in comp]
                ) == 1
            )
            or (
                vertex.lowlink != vertex.index
                and vertex.on_stack is True
                and not any(vertex in comp for comp in sccs[OLD.sccs_len:])
            )
        )
        and (
            not any(
                OLD.nodes_state[adj][0] is None and adj.index is not None
                for adj in self.graph.adjacency_list[vertex]
            )
            or vertex.lowlink
            <= min(
                adj.lowlink
                for adj in self.graph.adjacency_list[vertex]
                if OLD.nodes_state[adj][0] is None and adj.index is not None
            )
        )
        and (
            not any(
                OLD.nodes_state[adj][0] is not None
                and OLD.nodes_state[adj][2] is True
                for adj in self.graph.adjacency_list[vertex]
            )
            or vertex.lowlink
            <= min(
                adj.index
                for adj in self.graph.adjacency_list[vertex]
                if OLD.nodes_state[adj][0] is not None
                and OLD.nodes_state[adj][2] is True
            )
        )
    )
)
@icontract.ensure(
    lambda OLD, self, vertex, sccs:
    all(
        not (
            OLD.nodes_state[node][0] is None
            and getattr(node, "index", None) is not None
        )
        or node in OLD.reachable_from_vertex
        for node in self.graph.nodes
    )
)
@icontract.ensure(
    lambda OLD, self, vertex, sccs:
    all(isinstance(comp, list) for comp in sccs) and
    (
        (lambda finished_nodes:
            all(
                (
                    any(
                        (u in comp) and (v in comp)
                        for comp in sccs
                    )
                )
                ==
                (
                    v in __import__("functools").reduce(
                        lambda R, _: R | {w for x in R for w in self.graph.adjacency_list[x]},
                        range(len(self.graph.nodes)),
                        {u},
                    )
                    and
                    u in __import__("functools").reduce(
                        lambda R, _: R | {w for x in R for w in self.graph.adjacency_list[x]},
                        range(len(self.graph.nodes)),
                        {v},
                    )
                )
                for u in finished_nodes
                for v in finished_nodes
            )
        )(
            [
                node
                for node in self.graph.nodes
                if getattr(node, "index", None) is not None
                and not getattr(node, "on_stack", False)
            ]
        )
    )
)
```
```
@icontract.snapshot(lambda self: self.index, name="self_index")
@icontract.snapshot(lambda vertex: vertex.index, name="vertex_index")
@icontract.snapshot(lambda sccs: len(sccs), name="sccs_len")
@icontract.ensure(lambda OLD, self, vertex, sccs:
    (
        # vertex.index must equal the saved entry value (assigned at start)
        vertex.index == OLD.self_index
        # lowlink never exceeds index
        and vertex.lowlink <= vertex.index
        # self.index must have advanced by at least one
        and self.index >= OLD.self_index + 1
        # sccs length is non-decreasing
        and len(sccs) >= OLD.sccs_len
        # all newly appended SCCs (if any) are non-empty lists whose members have indices and are not on the stack
        and all(
            isinstance(s, list) and len(s) > 0 and all(getattr(n, "index", None) is not None and getattr(n, "on_stack", True) is False for n in s)
            for s in sccs[OLD.sccs_len:]
        )
        # If this vertex is a root (lowlink == index) it must have been popped and appear in one of the newly appended SCCs;
        # otherwise it must remain on the stack and not be part of any newly appended SCC.
        and (
            (
                vertex.lowlink == vertex.index
                and vertex.on_stack is False
                and any(vertex in s for s in sccs[OLD.sccs_len:])
            )
            or
            (
                vertex.lowlink != vertex.index
                and vertex.on_stack is True
                and not any(vertex in s for s in sccs[OLD.sccs_len:])
            )
        )
    )
)
```
[2, 3, 4, 5, 8, 9, 12, 13, 24, 28, 35, 37, 38, 41, 42, 44]
===== 2 =====
```
         vertex.lowlink = self.index
         self.index += 1
         self.stack.append(vertex)
-        vertex.on_stack = True
+        vertex.on_stack = False
 
         # Consider successors of v
         for adjacent in self.graph.adjacency_list[vertex]:
@@ -34,4 +34,4 @@                 if adjacent == vertex:
                     break
             scc.sort()
-            sccs.append(scc)+            sccs.append(scc)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = False

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)

```
===== 3 =====
```
         vertex.lowlink = self.index
         self.index += 1
         self.stack.append(vertex)
-        vertex.on_stack = True
+        vertex.on_stack = None
 
         # Consider successors of v
         for adjacent in self.graph.adjacency_list[vertex]:
@@ -34,4 +34,4 @@                 if adjacent == vertex:
                     break
             scc.sort()
-            sccs.append(scc)+            sccs.append(scc)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = None

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)

```
===== 4 =====
```
         vertex.on_stack = True
 
         # Consider successors of v
-        for adjacent in self.graph.adjacency_list[vertex]:
+        for adjacent in self.graph.adjacency_list[vertex][:1]:  # Only considers the first successor, ignoring others
             if adjacent.index is None:
                 # Successor w has not yet been visited; recurse on it
                 self.strongconnect(adjacent, sccs)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex][:1]:  # Only considers the first successor, ignoring others
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 5 =====
```
         vertex.on_stack = True
 
         # Consider successors of v
-        for adjacent in self.graph.adjacency_list[vertex]:
+        for adjacent in self.graph.nodes:  # Iterates over all nodes instead of just the successors
             if adjacent.index is None:
                 # Successor w has not yet been visited; recurse on it
                 self.strongconnect(adjacent, sccs)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.nodes:  # Iterates over all nodes instead of just the successors
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 8 =====
```
             if adjacent.index is None:
                 # Successor w has not yet been visited; recurse on it
                 self.strongconnect(adjacent, sccs)
-                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
+                vertex.lowlink = min(vertex.lowlink, adjacent.index)
             elif adjacent.on_stack:
                 # Successor w is in stack S and hence in the current SCC
                 # If w is not on stack, then (v, w) is a cross-edge in the DFS
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.index)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 9 =====
```
             if adjacent.index is None:
                 # Successor w has not yet been visited; recurse on it
                 self.strongconnect(adjacent, sccs)
-                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
+                vertex.lowlink = vertex.index
             elif adjacent.on_stack:
                 # Successor w is in stack S and hence in the current SCC
                 # If w is not on stack, then (v, w) is a cross-edge in the DFS
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = vertex.index
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 12 =====
```
                 # tree and must be ignored
                 # Note: The next line may look odd - but is correct.
                 # It says w.index not w.lowlink; that is deliberate and from the original paper
-                vertex.lowlink = min(vertex.lowlink, adjacent.index)
+                vertex.lowlink = max(vertex.lowlink, adjacent.lowlink)
 
         # If v is a root node, pop the stack and generate an SCC
         if vertex.lowlink == vertex.index:
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = max(vertex.lowlink, adjacent.lowlink)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 13 =====
```
                 # tree and must be ignored
                 # Note: The next line may look odd - but is correct.
                 # It says w.index not w.lowlink; that is deliberate and from the original paper
-                vertex.lowlink = min(vertex.lowlink, adjacent.index)
+                vertex.lowlink = min(vertex.lowlink, adjacent.index + 1)
 
         # If v is a root node, pop the stack and generate an SCC
         if vertex.lowlink == vertex.index:
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index + 1)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 24 =====
```
             # start a new strongly connected component
             scc = []
             while True:
-                adjacent = self.stack.pop()
+                adjacent = vertex  # Incorrectly assigns the current vertex instead of popping from the stack
                 adjacent.on_stack = False
                 scc.append(adjacent)
                 if adjacent == vertex:
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = vertex  # Incorrectly assigns the current vertex instead of popping from the stack
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 28 =====
```
             while True:
                 adjacent = self.stack.pop()
                 adjacent.on_stack = False
-                scc.append(adjacent)
+                scc.append(vertex)  # Incorrectly appends the root vertex instead of the adjacent vertex
                 if adjacent == vertex:
                     break
             scc.sort()
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(vertex)  # Incorrectly appends the root vertex instead of the adjacent vertex
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc)
```
===== 35 =====
```
                 scc.append(adjacent)
                 if adjacent == vertex:
                     break
-            scc.sort()
+            scc.append(vertex)
             sccs.append(scc)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.append(vertex)
            sccs.append(scc)
```
===== 37 =====
```
                 scc.append(adjacent)
                 if adjacent == vertex:
                     break
-            scc.sort()
+            scc.reverse()
             sccs.append(scc)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.reverse()
            sccs.append(scc)
```
===== 38 =====
```
                 scc.append(adjacent)
                 if adjacent == vertex:
                     break
-            scc.sort()
+            scc.sort(reverse=True)
             sccs.append(scc)
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort(reverse=True)
            sccs.append(scc)
```
===== 41 =====
```
                 if adjacent == vertex:
                     break
             scc.sort()
-            sccs.append(scc)+            sccs.append(scc * 2)  # Appending the SCC twice, duplicating its contents
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc * 2)  # Appending the SCC twice, duplicating its contents
```
===== 42 =====
```
                 if adjacent == vertex:
                     break
             scc.sort()
-            sccs.append(scc)+            sccs.append(scc + [vertex])  # Appending the SCC with the vertex added again
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc + [vertex])  # Appending the SCC with the vertex added again
```
===== 44 =====
```
                 if adjacent == vertex:
                     break
             scc.sort()
-            sccs.append(scc)+            sccs.append(scc[::-1])  # Appending the SCC in reverse order
```
```
    def strongconnect(self, vertex, sccs):
        """
        Given a vertex, adds all successors of the given vertex to the same connected component
        """
        # Set the depth index for v to the smallest unused index
        vertex.index = self.index
        vertex.lowlink = self.index
        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent in self.graph.adjacency_list[vertex]:
            if adjacent.index is None:
                # Successor w has not yet been visited; recurse on it
                self.strongconnect(adjacent, sccs)
                vertex.lowlink = min(vertex.lowlink, adjacent.lowlink)
            elif adjacent.on_stack:
                # Successor w is in stack S and hence in the current SCC
                # If w is not on stack, then (v, w) is a cross-edge in the DFS
                # tree and must be ignored
                # Note: The next line may look odd - but is correct.
                # It says w.index not w.lowlink; that is deliberate and from the original paper
                vertex.lowlink = min(vertex.lowlink, adjacent.index)

        # If v is a root node, pop the stack and generate an SCC
        if vertex.lowlink == vertex.index:
            # start a new strongly connected component
            scc = []
            while True:
                adjacent = self.stack.pop()
                adjacent.on_stack = False
                scc.append(adjacent)
                if adjacent == vertex:
                    break
            scc.sort()
            sccs.append(scc[::-1])  # Appending the SCC in reverse order
```
