https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/graphs/TwoSat.java#L149-L190
```
//@ ensures isSolved;
//@ ensures variableAssignments.length == numberOfVariables + 1;
//@ ensures hasSolution ==> java.util.stream.IntStream.range(1, graph.length).allMatch(u -> graph[u].stream().allMatch(v -> (!(u <= numberOfVariables ? variableAssignments[u] : !variableAssignments[u - numberOfVariables]) || (v <= numberOfVariables ? variableAssignments[v] : !variableAssignments[v - numberOfVariables]))));
//@ ensures hasSolution || java.util.stream.IntStream.range(1, numberOfVariables + 1).anyMatch(i -> { int lit = i; int notLit = i + numberOfVariables; int limit = graph.length; java.util.Set<Integer> startLit = java.util.Collections.singleton(lit); java.util.Set<Integer> startNot = java.util.Collections.singleton(notLit); boolean reachLitToNot = java.util.stream.Stream.iterate(startLit, s -> s.stream().flatMap(v -> graph[v].stream()).collect(java.util.stream.Collectors.toSet())).limit(limit).anyMatch(s -> s.contains(notLit)); boolean reachNotToLit = java.util.stream.Stream.iterate(startNot, s -> s.stream().flatMap(v -> graph[v].stream()).collect(java.util.stream.Collectors.toSet())).limit(limit).anyMatch(s -> s.contains(lit)); return reachLitToNot && reachNotToLit; });
//@ ensures ((java.util.function.Supplier<Boolean>)() -> { int n = 2 * numberOfVariables + 1; boolean[] visited = new boolean[n]; int[] comp = new int[n]; java.util.Stack<Integer> st = new java.util.Stack<>(); for (int i = 1; i < n; i++) { if (!visited[i]) { java.util.Stack<Integer> dfs = new java.util.Stack<>(); dfs.push(i); while (!dfs.isEmpty()) { int u = dfs.pop(); if (!visited[u]) { visited[u] = true; for (int idx = 0; idx < graph[u].size(); idx++) { int v = graph[u].get(idx); if (!visited[v]) { dfs.push(v); } } st.push(u); } } } } java.util.Arrays.fill(visited, false); int sccId = 0; while (!st.isEmpty()) { int node = st.pop(); if (!visited[node]) { java.util.Stack<Integer> dfs2 = new java.util.Stack<>(); dfs2.push(node); while (!dfs2.isEmpty()) { int u = dfs2.pop(); if (!visited[u]) { visited[u] = true; comp[u] = sccId; for (int idx = 0; idx < graphTranspose[u].size(); idx++) { int v = graphTranspose[u].get(idx); if (!visited[v]) { dfs2.push(v); } } } } sccId++; } } boolean specHasSol = true; boolean[] specAssign = new boolean[numberOfVariables + 1]; for (int i = 1; i <= numberOfVariables; i++) { int notI = i + numberOfVariables; if (comp[i] == comp[notI]) { specHasSol = false; break; } specAssign[i] = comp[i] > comp[notI]; } if (specHasSol != hasSolution) { return false; } if (!specHasSol) { return true; } for (int i = 1; i <= numberOfVariables; i++) { if (specAssign[i] != variableAssignments[i]) { return false; } } return true; }).get();
```
```
//@ ensures isSolved;
//@ ensures variableAssignments.length == numberOfVariables + 1;
//@ ensures hasSolution ==> java.util.stream.IntStream.range(1, graph.length).allMatch(u -> graph[u].stream().allMatch(v -> (!(u <= numberOfVariables ? variableAssignments[u] : !variableAssignments[u - numberOfVariables]) || (v <= numberOfVariables ? variableAssignments[v] : !variableAssignments[v - numberOfVariables]))));
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 29, 31, 32, 33, 37]
===== 0 =====
```
         Stack<Integer> topologicalOrder = new Stack<>();
 
         // Step 1: Perform DFS to get topological order
-        for (int i = 1; i < n; i++) {
+        for (int i = 1; i < n - 1; i++) {
             if (!visited[i]) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n - 1; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 1 =====
```
         Stack<Integer> topologicalOrder = new Stack<>();
 
         // Step 1: Perform DFS to get topological order
-        for (int i = 1; i < n; i++) {
+        for (int i = 1; i < n; i += 2) {
             if (!visited[i]) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i += 2) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 2 =====
```
         Stack<Integer> topologicalOrder = new Stack<>();
 
         // Step 1: Perform DFS to get topological order
-        for (int i = 1; i < n; i++) {
+        for (int i = 1; i >= n; i++) {
             if (!visited[i]) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i >= n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 3 =====
```
         Stack<Integer> topologicalOrder = new Stack<>();
 
         // Step 1: Perform DFS to get topological order
-        for (int i = 1; i < n; i++) {
+        for (int i = 2; i < n; i++) {
             if (!visited[i]) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 2; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 4 =====
```
 
         // Step 1: Perform DFS to get topological order
         for (int i = 1; i < n; i++) {
-            if (!visited[i]) {
+            if (i % 2 == 0) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (i % 2 == 0) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 5 =====
```
 
         // Step 1: Perform DFS to get topological order
         for (int i = 1; i < n; i++) {
-            if (!visited[i]) {
+            if (i == 1) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (i == 1) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 6 =====
```
 
         // Step 1: Perform DFS to get topological order
         for (int i = 1; i < n; i++) {
-            if (!visited[i]) {
+            if (visited[i]) {
                 dfsForTopologicalOrder(i, visited, topologicalOrder);
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 7 =====
```
         // Step 1: Perform DFS to get topological order
         for (int i = 1; i < n; i++) {
             if (!visited[i]) {
-                dfsForTopologicalOrder(i, visited, topologicalOrder);
+                
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 8 =====
```
         // Step 1: Perform DFS to get topological order
         for (int i = 1; i < n; i++) {
             if (!visited[i]) {
-                dfsForTopologicalOrder(i, visited, topologicalOrder);
+                dfsForTopologicalOrder(1, visited, topologicalOrder);
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(1, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 9 =====
```
         // Step 1: Perform DFS to get topological order
         for (int i = 1; i < n; i++) {
             if (!visited[i]) {
-                dfsForTopologicalOrder(i, visited, topologicalOrder);
+                dfsForTopologicalOrder(i - 1, visited, topologicalOrder);
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i - 1, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 10 =====
```
             }
         }
 
-        Arrays.fill(visited, false);
+        
         int sccId = 0;
 
         // Step 2: Find SCCs on transposed graph
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 11 =====
```
             }
         }
 
-        Arrays.fill(visited, false);
+        Arrays.fill(visited, true);
         int sccId = 0;
 
         // Step 2: Find SCCs on transposed graph
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, true);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 12 =====
```
             }
         }
 
-        Arrays.fill(visited, false);
+        for (int i = 0; i < n; i++) { visited[i] = true; }
         int sccId = 0;
 
         // Step 2: Find SCCs on transposed graph
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        for (int i = 0; i < n; i++) { visited[i] = true; }
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 13 =====
```
         int sccId = 0;
 
         // Step 2: Find SCCs on transposed graph
-        while (!topologicalOrder.isEmpty()) {
+        for (int i = 0; i < topologicalOrder.size(); i++) {
             int node = topologicalOrder.pop();
             if (!visited[node]) {
                 dfsForScc(node, visited, component, sccId);
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        for (int i = 0; i < topologicalOrder.size(); i++) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 14 =====
```
         int sccId = 0;
 
         // Step 2: Find SCCs on transposed graph
-        while (!topologicalOrder.isEmpty()) {
+        if (topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
             if (!visited[node]) {
                 dfsForScc(node, visited, component, sccId);
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        if (topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 15 =====
```
 
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
-            int node = topologicalOrder.pop();
+            int node = topologicalOrder.pop() - 1; // This also modifies the node value, which can lead to incorrect processing of the graph.
             if (!visited[node]) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop() - 1; // This also modifies the node value, which can lead to incorrect processing of the graph.
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 16 =====
```
 
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
-            int node = topologicalOrder.pop();
+            int node = topologicalOrder.pop(); topologicalOrder.clear(); // This clears the stack, preventing further processing of remaining nodes.
             if (!visited[node]) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop(); topologicalOrder.clear(); // This clears the stack, preventing further processing of remaining nodes.
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 17 =====
```
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
-            if (!visited[node]) {
+            if (component[node] != 0) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (component[node] != 0) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 18 =====
```
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
-            if (!visited[node]) {
+            if (node < 1 || node >= n) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (node < 1 || node >= n) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 19 =====
```
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
-            if (!visited[node]) {
+            if (sccId == 0) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (sccId == 0) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 20 =====
```
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
-            if (!visited[node]) {
+            if (topologicalOrder.isEmpty()) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (topologicalOrder.isEmpty()) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 21 =====
```
         // Step 2: Find SCCs on transposed graph
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
-            if (!visited[node]) {
+            if (visited[node]) {
                 dfsForScc(node, visited, component, sccId);
                 sccId++;
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 22 =====
```
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
             if (!visited[node]) {
-                dfsForScc(node, visited, component, sccId);
+                
                 sccId++;
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 24 =====
```
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
             if (!visited[node]) {
-                dfsForScc(node, visited, component, sccId);
+                sccId++; // Increments the SCC ID without performing DFS, potentially causing incorrect component assignments
                 sccId++;
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                sccId++; // Increments the SCC ID without performing DFS, potentially causing incorrect component assignments
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 25 =====
```
         while (!topologicalOrder.isEmpty()) {
             int node = topologicalOrder.pop();
             if (!visited[node]) {
-                dfsForScc(node, visited, component, sccId);
+                visited[node] = false; // Incorrectly marks the node as unvisited, leading to incorrect SCC identification
                 sccId++;
             }
         }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                visited[node] = false; // Incorrectly marks the node as unvisited, leading to incorrect SCC identification
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 29 =====
```
 
         // Step 3: Check for contradictions and assign values
         for (int i = 1; i <= numberOfVariables; i++) {
-            int notI = negate(i);
+            int notI = i; // Incorrectly assigns notI to i instead of its negation
             if (component[i] == component[notI]) {
                 hasSolution = false;
                 return;
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = i; // Incorrectly assigns notI to i instead of its negation
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 31 =====
```
 
         // Step 3: Check for contradictions and assign values
         for (int i = 1; i <= numberOfVariables; i++) {
-            int notI = negate(i);
+            int notI = negate(i + numberOfVariables); // Incorrectly adds the number of variables to i before negating
             if (component[i] == component[notI]) {
                 hasSolution = false;
                 return;
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i + numberOfVariables); // Incorrectly adds the number of variables to i before negating
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 32 =====
```
 
         // Step 3: Check for contradictions and assign values
         for (int i = 1; i <= numberOfVariables; i++) {
-            int notI = negate(i);
+            int notI = negate(i - 1); // Incorrectly negates the variable index minus one
             if (component[i] == component[notI]) {
                 hasSolution = false;
                 return;
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i - 1); // Incorrectly negates the variable index minus one
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 33 =====
```
 
         // Step 3: Check for contradictions and assign values
         for (int i = 1; i <= numberOfVariables; i++) {
-            int notI = negate(i);
+            int notI = negate(negate(i)); // Double negation, which results in the original variable instead of its negation
             if (component[i] == component[notI]) {
                 hasSolution = false;
                 return;
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(negate(i)); // Double negation, which results in the original variable instead of its negation
            if (component[i] == component[notI]) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
===== 37 =====
```
         // Step 3: Check for contradictions and assign values
         for (int i = 1; i <= numberOfVariables; i++) {
             int notI = negate(i);
-            if (component[i] == component[notI]) {
+            if (component[notI] == 0) {
                 hasSolution = false;
                 return;
             }
```
```
    /**
     * Solves the 2-SAT problem using Kosaraju's algorithm to find SCCs
     * and determines whether a satisfying assignment exists.
     */
    void solve() {
        isSolved = true;
        int n = 2 * numberOfVariables + 1;

        boolean[] visited = new boolean[n];
        int[] component = new int[n];
        Stack<Integer> topologicalOrder = new Stack<>();

        // Step 1: Perform DFS to get topological order
        for (int i = 1; i < n; i++) {
            if (!visited[i]) {
                dfsForTopologicalOrder(i, visited, topologicalOrder);
            }
        }

        Arrays.fill(visited, false);
        int sccId = 0;

        // Step 2: Find SCCs on transposed graph
        while (!topologicalOrder.isEmpty()) {
            int node = topologicalOrder.pop();
            if (!visited[node]) {
                dfsForScc(node, visited, component, sccId);
                sccId++;
            }
        }

        // Step 3: Check for contradictions and assign values
        for (int i = 1; i <= numberOfVariables; i++) {
            int notI = negate(i);
            if (component[notI] == 0) {
                hasSolution = false;
                return;
            }
            // If SCC(i) > SCC(¬i), then variable i is true.
            variableAssignments[i] = component[i] > component[notI];
        }
    }
```
