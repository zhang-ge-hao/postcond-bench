https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/model/Policy.java#L411-L428
```
//@ ensures model.equals(\old(model));
//@ ensures savePolicyToText().equals(\old(savePolicyToText()));
//@ ensures !model.containsKey("g") || model.get("g").entrySet().stream().allMatch(e -> condRmMap.get(e.getKey()) == null || (e.getValue().condRM == condRmMap.get(e.getKey()) && e.getValue().rm == condRmMap.get(e.getKey()) && e.getValue().policy.stream().allMatch(rule -> condRmMap.get(e.getKey()).hasLink(rule.get(0), rule.get(1)))));
```
```
//@ ensures model.equals(\old(model));
//@ ensures savePolicyToText().equals(\old(savePolicyToText()));
//@ ensures \old(model.containsKey("g")) ==> (model.containsKey("g") && model.get("g").entrySet().stream().allMatch(e -> (condRmMap.get(e.getKey()) == null) || (e.getValue().condRM == condRmMap.get(e.getKey()) && e.getValue().rm == condRmMap.get(e.getKey()))));
```
[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13]
===== 1 =====
```
      */
     public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
         printPolicy();
-        if (model.containsKey("g")) {
+        if (!model.containsKey("g")) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                 String ptype = entry.getKey();
                 Assertion ast = entry.getValue();
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (!model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 2 =====
```
      */
     public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
         printPolicy();
-        if (model.containsKey("g")) {
+        if (model.containsKey("g") && model.get("g").isEmpty()) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                 String ptype = entry.getKey();
                 Assertion ast = entry.getValue();
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g") && model.get("g").isEmpty()) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 3 =====
```
      */
     public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
         printPolicy();
-        if (model.containsKey("g")) {
+        if (model.containsKey("g") && model.get("g").size() < 1) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                 String ptype = entry.getKey();
                 Assertion ast = entry.getValue();
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g") && model.get("g").size() < 1) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 4 =====
```
     public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
         printPolicy();
         if (model.containsKey("g")) {
-            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
+            for (Map.Entry<String, Assertion> entry : model.get("p").entrySet()) {
                 String ptype = entry.getKey();
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("p").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 5 =====
```
         printPolicy();
         if (model.containsKey("g")) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
-                String ptype = entry.getKey();
+                String ptype = "default"; // Assigning a constant value instead of the actual key
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = "default"; // Assigning a constant value instead of the actual key
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 6 =====
```
         printPolicy();
         if (model.containsKey("g")) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
-                String ptype = entry.getKey();
+                String ptype = entry.getKey() + "_suffix"; // Modifying the key by appending a suffix
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey() + "_suffix"; // Modifying the key by appending a suffix
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 7 =====
```
         printPolicy();
         if (model.containsKey("g")) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
-                String ptype = entry.getKey();
+                String ptype = entry.getKey().toUpperCase(); // Changing the case of the key, which may not match expected values
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey().toUpperCase(); // Changing the case of the key, which may not match expected values
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 8 =====
```
         printPolicy();
         if (model.containsKey("g")) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
-                String ptype = entry.getKey();
+                String ptype = entry.getValue().toString(); // Using the value instead of the key
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getValue().toString(); // Using the value instead of the key
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 9 =====
```
         printPolicy();
         if (model.containsKey("g")) {
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
-                String ptype = entry.getKey();
+                String ptype = null; // Setting ptype to null, which will cause a NullPointerException later
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = null; // Setting ptype to null, which will cause a NullPointerException later
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 11 =====
```
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                 String ptype = entry.getKey();
                 Assertion ast = entry.getValue();
-                if (condRmMap.get(ptype) != null){
+                if (condRmMap.get(ptype) == null) {
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
                     ast.buildConditionalRoleLinks(condRm);
                 }
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) == null) {
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 12 =====
```
             for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                 String ptype = entry.getKey();
                 Assertion ast = entry.getValue();
-                if (condRmMap.get(ptype) != null){
+                if (condRmMap.get(ptype) == null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
                     ast.buildConditionalRoleLinks(condRm);
                 }
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) == null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    ast.buildConditionalRoleLinks(condRm);
                }
            }
        }
    }
```
===== 13 =====
```
                 Assertion ast = entry.getValue();
                 if (condRmMap.get(ptype) != null){
                     ConditionalRoleManager condRm = condRmMap.get(ptype);
-                    ast.buildConditionalRoleLinks(condRm);
+                    
                 }
             }
         }
```
```
    /**
     * buildConditionalRoleLinks initializes the roles in RBAC.
     *
     * @param condRmMap a map of conditional role managers that manage the role links and their conditions.
     */
    public void buildConditionalRoleLinks(Map<String, ConditionalRoleManager> condRmMap){
        printPolicy();
        if (model.containsKey("g")) {
            for (Map.Entry<String, Assertion> entry : model.get("g").entrySet()) {
                String ptype = entry.getKey();
                Assertion ast = entry.getValue();
                if (condRmMap.get(ptype) != null){
                    ConditionalRoleManager condRm = condRmMap.get(ptype);
                    
                }
            }
        }
    }
```
