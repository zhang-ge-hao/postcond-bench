https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/tarjan.py#L29-L65
```
@icontract.snapshot(lambda sccs: len(sccs), name="old_len")
@icontract.snapshot(lambda sccs: [list(comp) for comp in sccs], name="old_sccs")
@icontract.snapshot(lambda sccs: set(v for comp in sccs for v in comp), name="old_members")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda OLD, sccs: len(sccs) >= OLD.old_len)
@icontract.ensure(lambda OLD, sccs: sccs[:OLD.old_len] == OLD.old_sccs)
@icontract.ensure(lambda OLD, sccs: all(len(comp) > 0 for comp in sccs[OLD.old_len:]))
@icontract.ensure(lambda OLD, sccs: all(v not in OLD.old_members for comp in sccs[OLD.old_len:] for v in comp))
@icontract.ensure(lambda OLD, vertex, sccs: (vertex in OLD.old_members) or any(vertex in comp for comp in sccs[OLD.old_len:]))
```
```
Hallucination.

In Tarjan’s algorithm, a call to strongconnect(vertex, sccs) does not guarantee that an SCC containing vertex will be appended when that call returns. Many vertices are not SCC roots, so their call returns while they are still on the stack, waiting for an ancestor root call to pop them and create the SCC.

In the failure, vertex is E, sccs didn’t grow (sccs[OLD.old_len:] is empty), and E wasn’t in the old SCC members—this is a normal “non-root vertex” situation. So the contract should allow: either vertex was already in old SCCs, or it appears in newly appended SCCs, or it remains on_stack.
```
icontract_fail
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
