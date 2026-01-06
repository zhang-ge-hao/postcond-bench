https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/graph/bellman_ford.py#L5-L38
```
@icontract.snapshot(lambda graph: {node: dict(edges) for node, edges in graph.items()}, name="original_graph")
@icontract.snapshot(lambda source: source, name="original_source")
@icontract.ensure(lambda result: isinstance(result, bool))
@icontract.ensure(lambda graph, original_graph: graph == original_graph, "Graph should not be modified")
@icontract.ensure(lambda source, original_source: source == original_source, "Source should not be modified")
```
```
limited spec

original_graph
```
failed
```
@icontract.ensure(lambda result, graph, source: (lambda d, edges: result == (not any(d[u] + w < d[v] and d[u] < float('inf') for (u, v, w) in edges)))(__import__('functools').reduce(lambda d, _: {v: min([d[v]] + [d[u] + w for (u, vv, w) in [(u_, v_, w_) for u_ in graph for (v_, w_) in graph[u_].items()] if vv == v]) for v in graph}, range(max(0, len(graph) - 1)), {n: (0 if n == source else float('inf')) for n in graph}), [(u, v, w) for u in graph for (v, w) in graph[u].items()]))
```
