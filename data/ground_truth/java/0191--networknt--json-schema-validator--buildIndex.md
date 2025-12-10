https://github.com/networknt/json-schema-validator/blob/a8bda4c9f43f17f657513083c0ae6f9690e51b9b/./src/main/java/com/networknt/schema/output/HierarchicalOutputUnitFormatter.java#L125-L178
```
//@ ensures \old(index.containsKey(key.getEvaluationPath())) ==> index == \old(index) && root == \old(root);
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.containsKey(key.getEvaluationPath());
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()) != null;
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> key.getEvaluationPath().toString().equals(index.get(key.getEvaluationPath()).get(key.getInstanceLocation()).getEvaluationPath());
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()).getInstanceLocation().equals(key.getInstanceLocation().toString());
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()).isValid() == true;
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.values().stream().anyMatch(m -> m.values().stream().anyMatch(u -> u.getDetails() != null && u.getDetails().contains(index.get(key.getEvaluationPath()).get(key.getInstanceLocation()))));
//@ ensures key.getInstanceLocation() == null || key.getInstanceLocation().getParent() == null || !keys.keySet().stream().anyMatch(p -> keys.get(p) != null && keys.get(p).contains(key.getInstanceLocation().getParent())) || (index.get(key.getEvaluationPath()) != null && index.get(key.getEvaluationPath()).get(key.getInstanceLocation()) != null && index.entrySet().stream().anyMatch(e -> keys.get(e.getKey()) != null && keys.get(e.getKey()).contains(key.getInstanceLocation().getParent()) && e.getValue().get(key.getInstanceLocation().getParent()) != null && e.getValue().get(key.getInstanceLocation().getParent()).getDetails() != null && e.getValue().get(key.getInstanceLocation().getParent()).getDetails().contains(index.get(key.getEvaluationPath()).get(key.getInstanceLocation()))));
//@ ensures \old(root.getDetails() == null || root.getDetails().isEmpty() ? null : root.getDetails().get(0)) == null || (root.getDetails() != null && !root.getDetails().isEmpty() && root.getDetails().get(0) == \old(root.getDetails() == null || root.getDetails().isEmpty() ? null : root.getDetails().get(0)));
```
```
//@ ensures \old(index.containsKey(key.getEvaluationPath())) ==> index == \old(index) && root == \old(root);
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.containsKey(key.getEvaluationPath());
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()) != null;
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()).getEvaluationPath().equals(key.getEvaluationPath().toString());
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()).getInstanceLocation().equals(key.getInstanceLocation().toString());
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> index.get(key.getEvaluationPath()).get(key.getInstanceLocation()).isValid() == true;
//@ ensures \old(!index.containsKey(key.getEvaluationPath())) ==> (index.values().stream().anyMatch(m -> m.values().stream().anyMatch(u -> u.getDetails() != null && u.getDetails().contains(index.get(key.getEvaluationPath()).get(key.getInstanceLocation())))));
```
[10, 13, 16, 21, 27, 30, 33, 34, 35, 36, 37, 39]
===== 10 =====
```
         Deque<JsonNodePath> stack = new ArrayDeque<>();
         while (path != null && path.getElement(-1) != null) {
             stack.push(path);
-            path = path.getParent();
+            path = null; // This will cause the loop to terminate immediately, skipping the intended parent path traversal.
         }
 
         OutputUnit parent = root;
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = null; // This will cause the loop to terminate immediately, skipping the intended parent path traversal.
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 13 =====
```
 
         OutputUnit parent = root;
         while (!stack.isEmpty()) {
-            JsonNodePath current = stack.pop();
+            JsonNodePath current = stack.removeLast(); // This will throw an exception if the stack is empty, but it will not compile.
             if (!index.containsKey(current) && keys.containsKey(current)) {
                 // the index doesn't contain this path but this is a path with data
                 for (JsonNodePath instanceLocation : keys.get(current)) {
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.removeLast(); // This will throw an exception if the stack is empty, but it will not compile.
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 16 =====
```
                 for (JsonNodePath instanceLocation : keys.get(current)) {
                     OutputUnit child = new OutputUnit();
                     child.setValid(true);
-                    child.setEvaluationPath(current.toString());
+                    
                     child.setInstanceLocation(instanceLocation.toString());
                     index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                     if (parent.getDetails() == null) {
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 21 =====
```
                 for (JsonNodePath instanceLocation : keys.get(current)) {
                     OutputUnit child = new OutputUnit();
                     child.setValid(true);
-                    child.setEvaluationPath(current.toString());
+                    child.setEvaluationPath(null);
                     child.setInstanceLocation(instanceLocation.toString());
                     index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                     if (parent.getDetails() == null) {
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(null);
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 27 =====
```
                     child.setValid(true);
                     child.setEvaluationPath(current.toString());
                     child.setInstanceLocation(instanceLocation.toString());
-                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
+                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, new OutputUnit()); // Creates a new OutputUnit without setting any properties
                     if (parent.getDetails() == null) {
                         parent.setDetails(new ArrayList<>());
                     }
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, new OutputUnit()); // Creates a new OutputUnit without setting any properties
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 30 =====
```
                     if (parent.getDetails() == null) {
                         parent.setDetails(new ArrayList<>());
                     }
-                    parent.getDetails().add(child);
+                    parent.getDetails().add(0, child);
                 }
             }
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(0, child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 33 =====
```
             // If exists in the index this is the new parent
             // Otherwise this is an evaluation path with no data and hence should be skipped
             // InstanceLocation to OutputUnit
-            Map<JsonNodePath, OutputUnit> result = index.get(current);
+            Map<JsonNodePath, OutputUnit> result = index.get(key.getEvaluationPath());
             if (result != null) {
                 for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                     if (key.getInstanceLocation().startsWith(entry.getKey())) {
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(key.getEvaluationPath());
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 34 =====
```
             // If exists in the index this is the new parent
             // Otherwise this is an evaluation path with no data and hence should be skipped
             // InstanceLocation to OutputUnit
-            Map<JsonNodePath, OutputUnit> result = index.get(current);
+            Map<JsonNodePath, OutputUnit> result = new LinkedHashMap<>();
             if (result != null) {
                 for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                     if (key.getInstanceLocation().startsWith(entry.getKey())) {
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = new LinkedHashMap<>();
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 35 =====
```
             // Otherwise this is an evaluation path with no data and hence should be skipped
             // InstanceLocation to OutputUnit
             Map<JsonNodePath, OutputUnit> result = index.get(current);
-            if (result != null) {
+            if (result != null && result.size() < 1) {
                 for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                     if (key.getInstanceLocation().startsWith(entry.getKey())) {
                         parent = entry.getValue();
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null && result.size() < 1) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 36 =====
```
             Map<JsonNodePath, OutputUnit> result = index.get(current);
             if (result != null) {
                 for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
-                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
+                    if (entry.getKey().startsWith(key.getInstanceLocation())) {
                         parent = entry.getValue();
                         break;
                     }
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (entry.getKey().startsWith(key.getInstanceLocation())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 37 =====
```
             Map<JsonNodePath, OutputUnit> result = index.get(current);
             if (result != null) {
                 for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
-                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
+                    if (key.getInstanceLocation().equals(entry.getKey())) {
                         parent = entry.getValue();
                         break;
                     }
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().equals(entry.getKey())) {
                        parent = entry.getValue();
                        break;
                    }
                }
            }
        }
    }
```
===== 39 =====
```
             if (result != null) {
                 for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                     if (key.getInstanceLocation().startsWith(entry.getKey())) {
-                        parent = entry.getValue();
+                        parent = root; // Incorrectly sets parent back to the root, losing the context of the current hierarchy
                         break;
                     }
                 }
```
```
    /**
     * Builds in the index of evaluation path to output units to be populated later
     * and modify the root to add the appropriate children.
     * 
     * @param key   the current key to process
     * @param index contains all the mappings from evaluation path to output units
     * @param keys  that contain all the evaluation paths with instance data
     * @param root  the root output unit
     */
    protected static void buildIndex(OutputUnitKey key, Map<JsonNodePath, Map<JsonNodePath, OutputUnit>> index,
            Map<JsonNodePath, Set<JsonNodePath>> keys, OutputUnit root) {
        if (index.containsKey(key.getEvaluationPath())) {
            return;
        }
        // Ensure the path is created
        JsonNodePath path = key.getEvaluationPath();
        Deque<JsonNodePath> stack = new ArrayDeque<>();
        while (path != null && path.getElement(-1) != null) {
            stack.push(path);
            path = path.getParent();
        }

        OutputUnit parent = root;
        while (!stack.isEmpty()) {
            JsonNodePath current = stack.pop();
            if (!index.containsKey(current) && keys.containsKey(current)) {
                // the index doesn't contain this path but this is a path with data
                for (JsonNodePath instanceLocation : keys.get(current)) {
                    OutputUnit child = new OutputUnit();
                    child.setValid(true);
                    child.setEvaluationPath(current.toString());
                    child.setInstanceLocation(instanceLocation.toString());
                    index.computeIfAbsent(current, n -> new LinkedHashMap<>()).put(instanceLocation, child);
                    if (parent.getDetails() == null) {
                        parent.setDetails(new ArrayList<>());
                    }
                    parent.getDetails().add(child);
                }
            }

            // If exists in the index this is the new parent
            // Otherwise this is an evaluation path with no data and hence should be skipped
            // InstanceLocation to OutputUnit
            Map<JsonNodePath, OutputUnit> result = index.get(current);
            if (result != null) {
                for (Entry<JsonNodePath, OutputUnit> entry : result.entrySet()) {
                    if (key.getInstanceLocation().startsWith(entry.getKey())) {
                        parent = root; // Incorrectly sets parent back to the root, losing the context of the current hierarchy
                        break;
                    }
                }
            }
        }
    }
```
