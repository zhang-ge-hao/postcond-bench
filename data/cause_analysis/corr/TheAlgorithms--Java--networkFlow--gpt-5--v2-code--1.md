https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/FordFulkerson.java#L20-L74
```
// @ ensures capacity == \old(capacity);
// @ ensures flow == \old(flow);
// @ ensures vertexCount == \old(vertexCount) && source == \old(source) && sink == \old(sink);
// @ ensures java.util.stream.IntStream.range(0, vertexCount).allMatch(i -> java.util.stream.IntStream.range(0, vertexCount).allMatch(j -> capacity[i][j] == \old(capacity[i][j])));
// @ ensures java.util.stream.IntStream.range(0, vertexCount).allMatch(i -> java.util.stream.IntStream.range(0, vertexCount).allMatch(j -> flow[i][j] + flow[j][i] == \old(flow[i][j] + flow[j][i])));
// @ ensures (source != sink) ==> (\result >= 0);
// @ ensures (source != sink) ==> (\result == java.util.stream.IntStream.range(0, vertexCount).map(j -> flow[source][j]).sum() - java.util.stream.IntStream.range(0, vertexCount).map(j -> \old(flow[source][j])).sum());
// @ ensures (source != sink) ==> (\result == java.util.stream.IntStream.range(0, vertexCount).map(i -> flow[i][sink]).sum() - java.util.stream.IntStream.range(0, vertexCount).map(i -> \old(flow[i][sink])).sum());
// @ ensures (source != sink) ==> (java.util.stream.IntStream.range(0, vertexCount).filter(v -> v != source && v != sink).allMatch(v -> java.util.stream.IntStream.range(0, vertexCount).map(j -> flow[v][j]).sum() - java.util.stream.IntStream.range(0, vertexCount).map(j -> \old(flow[v][j])).sum() == 0));
```
```
limited spec

.map(j -> \old(flow[v][j])).sum() 
```
compile_failure
```
//@ ensures \result == java.util.Arrays.stream(flow[source]).sum();
//@ ensures \result == java.util.stream.IntStream.range(0, vertexCount).map(i -> flow[i][sink]).sum();
//@ ensures \result >= 0 && \result < Integer.MAX_VALUE/2;
//@ ensures java.util.stream.IntStream.range(0, vertexCount).allMatch(i -> java.util.stream.IntStream.range(0, vertexCount).allMatch(j -> flow[i][j] + flow[j][i] == 0));
//@ ensures java.util.stream.IntStream.range(0, vertexCount).allMatch(i -> java.util.stream.IntStream.range(0, vertexCount).allMatch(j -> flow[i][j] <= capacity[i][j] && flow[i][j] >= -capacity[j][i]));
//@ ensures java.util.stream.IntStream.range(0, vertexCount).allMatch(v -> (v == source || v == sink) ? true : (java.util.Arrays.stream(flow[v]).sum() == java.util.stream.IntStream.range(0, vertexCount).map(i -> flow[i][v]).sum()));
//@ ensures (new java.util.function.Supplier<Boolean>(){ public Boolean get(){ int n = vertexCount; boolean[] vis = new boolean[n]; java.util.ArrayDeque<Integer> q = new java.util.ArrayDeque<>(); q.add(source); vis[source]=true; int[][] cap = \old(capacity); while(!q.isEmpty()){ int cur = q.remove(); for(int j=0;j<n;j++){ if(!vis[j] && cap[cur][j] > 0){ vis[j]=true; q.add(j); } } } return vis[sink]; } }).get() ==> \result > 0;
```
