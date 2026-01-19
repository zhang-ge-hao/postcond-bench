https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/main/Enforcer.java#L375-L392
```
🈚️

originally wrong.

//@ ensures true;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
         Assertion ast = entry.getValue();
         String[] args = new String[ast.tokens.length];
         args[0] = user;
-        int index = getDomainIndex(pType);
+        int index = 0; // This will always set index to 0, ignoring the actual domain index.
         if (domain.length > 0 && index < ast.tokens.length) {
             args[index] = domain[0];
         }
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = 0; // This will always set index to 0, ignoring the actual domain index.
        if (domain.length > 0 && index < ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 1 =====
```
         Assertion ast = entry.getValue();
         String[] args = new String[ast.tokens.length];
         args[0] = user;
-        int index = getDomainIndex(pType);
+        int index = getDomainIndex(pType) * 2; // This will incorrectly double the index, leading to incorrect behavior.
         if (domain.length > 0 && index < ast.tokens.length) {
             args[index] = domain[0];
         }
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType) * 2; // This will incorrectly double the index, leading to incorrect behavior.
        if (domain.length > 0 && index < ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 2 =====
```
         Assertion ast = entry.getValue();
         String[] args = new String[ast.tokens.length];
         args[0] = user;
-        int index = getDomainIndex(pType);
+        int index = getDomainIndex(pType) + 1; // This will incorrectly increment the index, potentially causing out-of-bounds access.
         if (domain.length > 0 && index < ast.tokens.length) {
             args[index] = domain[0];
         }
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType) + 1; // This will incorrectly increment the index, potentially causing out-of-bounds access.
        if (domain.length > 0 && index < ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 3 =====
```
         Assertion ast = entry.getValue();
         String[] args = new String[ast.tokens.length];
         args[0] = user;
-        int index = getDomainIndex(pType);
+        int index = getDomainIndex(pType) - 1; // This will incorrectly decrement the index, potentially leading to negative indexing.
         if (domain.length > 0 && index < ast.tokens.length) {
             args[index] = domain[0];
         }
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType) - 1; // This will incorrectly decrement the index, potentially leading to negative indexing.
        if (domain.length > 0 && index < ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 4 =====
```
         String[] args = new String[ast.tokens.length];
         args[0] = user;
         int index = getDomainIndex(pType);
-        if (domain.length > 0 && index < ast.tokens.length) {
+        if (domain.length <= 0 && index < ast.tokens.length) {
             args[index] = domain[0];
         }
         return args;
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType);
        if (domain.length <= 0 && index < ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 5 =====
```
         String[] args = new String[ast.tokens.length];
         args[0] = user;
         int index = getDomainIndex(pType);
-        if (domain.length > 0 && index < ast.tokens.length) {
+        if (domain.length == 0 && index < ast.tokens.length) {
             args[index] = domain[0];
         }
         return args;
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType);
        if (domain.length == 0 && index < ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 6 =====
```
         String[] args = new String[ast.tokens.length];
         args[0] = user;
         int index = getDomainIndex(pType);
-        if (domain.length > 0 && index < ast.tokens.length) {
+        if (domain.length > 0 && index == ast.tokens.length) {
             args[index] = domain[0];
         }
         return args;
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType);
        if (domain.length > 0 && index == ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
===== 7 =====
```
         String[] args = new String[ast.tokens.length];
         args[0] = user;
         int index = getDomainIndex(pType);
-        if (domain.length > 0 && index < ast.tokens.length) {
+        if (domain.length > 0 && index >= ast.tokens.length) {
             args[index] = domain[0];
         }
         return args;
```
```
    /**
     * get the match field value, used to field filters.
     * @param entry  the entry of pType:assertion.
     * @param pType  the named policy
     * @param user   the user.
     * @param domain domain.
     * @return the match field.
     */
    private String[] getPermissionsPackFunc(Map.Entry<String, Assertion> entry, String pType, String user, String... domain) {
        Assertion ast = entry.getValue();
        String[] args = new String[ast.tokens.length];
        args[0] = user;
        int index = getDomainIndex(pType);
        if (domain.length > 0 && index >= ast.tokens.length) {
            args[index] = domain[0];
        }
        return args;
    }
```
