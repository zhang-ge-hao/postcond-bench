https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/main/Enforcer.java#L488-L520
```
🈚️

originally wrong. `String... domain`
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
===== 0 =====
```
     public List<String> getImplicitRolesForUser(String name, String... domain) {
         List<String> res = new ArrayList<>();
         Deque<String> queue = new LinkedList<>();
-        queue.offerLast(name);
+        
 
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 1 =====
```
     public List<String> getImplicitRolesForUser(String name, String... domain) {
         List<String> res = new ArrayList<>();
         Deque<String> queue = new LinkedList<>();
-        queue.offerLast(name);
+        queue.clear();
 
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.clear();

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 2 =====
```
     public List<String> getImplicitRolesForUser(String name, String... domain) {
         List<String> res = new ArrayList<>();
         Deque<String> queue = new LinkedList<>();
-        queue.offerLast(name);
+        queue.offerLast("dummyRole");
 
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast("dummyRole");

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 3 =====
```
     public List<String> getImplicitRolesForUser(String name, String... domain) {
         List<String> res = new ArrayList<>();
         Deque<String> queue = new LinkedList<>();
-        queue.offerLast(name);
+        queue.pollLast();
 
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.pollLast();

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 4 =====
```
         Deque<String> queue = new LinkedList<>();
         queue.offerLast(name);
 
-        while (!queue.isEmpty()) {
+        for (int i = 0; i < queue.size(); i++) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        for (int i = 0; i < queue.size(); i++) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 5 =====
```
         Deque<String> queue = new LinkedList<>();
         queue.offerLast(name);
 
-        while (!queue.isEmpty()) {
+        if (!queue.isEmpty() && res.size() < 10) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        if (!queue.isEmpty() && res.size() < 10) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 6 =====
```
         Deque<String> queue = new LinkedList<>();
         queue.offerLast(name);
 
-        while (!queue.isEmpty()) {
+        if (queue.isEmpty()) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        if (queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 7 =====
```
         queue.offerLast(name);
 
         while (!queue.isEmpty()) {
-            name = queue.pollFirst();
+            name = queue.pollFirst() + "extra";
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst() + "extra";
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 8 =====
```
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
-                List<String> roles = rm.getRoles(name, domain);
+                List<String> roles = Collections.singletonList("defaultRole"); // Always returns a single default role, ignoring actual roles
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = Collections.singletonList("defaultRole"); // Always returns a single default role, ignoring actual roles
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 9 =====
```
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
-                List<String> roles = rm.getRoles(name, domain);
+                List<String> roles = new ArrayList<>(); // Initializes an empty list instead of fetching roles
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = new ArrayList<>(); // Initializes an empty list instead of fetching roles
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 10 =====
```
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
-                List<String> roles = rm.getRoles(name, domain);
+                List<String> roles = rm.getRoles(name); // Omits the domain parameter, potentially leading to incorrect role retrieval
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name); // Omits the domain parameter, potentially leading to incorrect role retrieval
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 11 =====
```
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
-                List<String> roles = rm.getRoles(name, domain);
+                List<String> roles = rm.getRoles(name, "invalidDomain"); // Uses an invalid domain, which may lead to unexpected results
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, "invalidDomain"); // Uses an invalid domain, which may lead to unexpected results
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 12 =====
```
         while (!queue.isEmpty()) {
             name = queue.pollFirst();
             for (RoleManager rm : rmMap.values()) {
-                List<String> roles = rm.getRoles(name, domain);
+                List<String> roles = rm.getUsers(name, domain); // Incorrectly retrieves users instead of roles
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getUsers(name, domain); // Incorrectly retrieves users instead of roles
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 13 =====
```
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
-                    if (res.contains(role)) continue;
+                    if (!res.contains(role)) continue;
                     res.add(role);
                     queue.offerLast(role);
                 }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (!res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 14 =====
```
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
-                    if (res.contains(role)) continue;
+                    if (res.indexOf(role) == -1) continue;
                     res.add(role);
                     queue.offerLast(role);
                 }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.indexOf(role) == -1) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 15 =====
```
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
-                    if (res.contains(role)) continue;
+                    if (res.size() == 0) continue;
                     res.add(role);
                     queue.offerLast(role);
                 }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.size() == 0) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 16 =====
```
             for (RoleManager rm : rmMap.values()) {
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
-                    if (res.contains(role)) continue;
+                    if (role.equals("admin")) continue;
                     res.add(role);
                     queue.offerLast(role);
                 }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (role.equals("admin")) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 17 =====
```
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
                     if (res.contains(role)) continue;
-                    res.add(role);
+                    
                     queue.offerLast(role);
                 }
             }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 18 =====
```
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
                     if (res.contains(role)) continue;
-                    res.add(role);
+                    res.add(name); // Incorrectly adds the user's name instead of the role.
                     queue.offerLast(role);
                 }
             }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(name); // Incorrectly adds the user's name instead of the role.
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 19 =====
```
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
                     if (res.contains(role)) continue;
-                    res.add(role);
+                    res.add(role + "_added"); // Modifies the role by appending a suffix, which changes its identity.
                     queue.offerLast(role);
                 }
             }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role + "_added"); // Modifies the role by appending a suffix, which changes its identity.
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 20 =====
```
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
                     if (res.contains(role)) continue;
-                    res.add(role);
+                    res.add(role.substring(0, 1)); // Adds only the first character of the role, losing the actual role information.
                     queue.offerLast(role);
                 }
             }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role.substring(0, 1)); // Adds only the first character of the role, losing the actual role information.
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 21 =====
```
                 List<String> roles = rm.getRoles(name, domain);
                 for (String role : roles) {
                     if (res.contains(role)) continue;
-                    res.add(role);
+                    res.add(role.toUpperCase()); // Adds the role in uppercase, which may not match the expected role format.
                     queue.offerLast(role);
                 }
             }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role.toUpperCase()); // Adds the role in uppercase, which may not match the expected role format.
                    queue.offerLast(role);
                }
            }
        }

        return res;
    }
```
===== 22 =====
```
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
-                    queue.offerLast(role);
+                    
                 }
             }
         }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    
                }
            }
        }

        return res;
    }
```
===== 23 =====
```
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
-                    queue.offerLast(role);
+                    queue.offerLast(""); // Adds an empty string, which may lead to unexpected behavior
                 }
             }
         }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(""); // Adds an empty string, which may lead to unexpected behavior
                }
            }
        }

        return res;
    }
```
===== 24 =====
```
                 for (String role : roles) {
                     if (res.contains(role)) continue;
                     res.add(role);
-                    queue.offerLast(role);
+                    queue.offerLast(name); // Incorrectly adds the user instead of the role
                 }
             }
         }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(name); // Incorrectly adds the user instead of the role
                }
            }
        }

        return res;
    }
```
===== 25 =====
```
             }
         }
 
-        return res;
+        return java.util.Collections.emptyList();
     }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return java.util.Collections.emptyList();
    }
```
===== 26 =====
```
             }
         }
 
-        return res;
+        return null;
     }
```
```
    /**
     * getImplicitRolesForUser gets implicit roles that a user has.
     * Compared to getRolesForUser(), this function retrieves indirect roles besides direct roles.
     * For example:
     * g, alice, role:admin
     * g, role:admin, role:user
     * <p>
     * getRolesForUser("alice") can only get: ["role:admin"].
     * But getImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
     *
     * @param name   the user.
     * @param domain the user's domain.
     * @return implicit roles that a user has.
     */
    public List<String> getImplicitRolesForUser(String name, String... domain) {
        List<String> res = new ArrayList<>();
        Deque<String> queue = new LinkedList<>();
        queue.offerLast(name);

        while (!queue.isEmpty()) {
            name = queue.pollFirst();
            for (RoleManager rm : rmMap.values()) {
                List<String> roles = rm.getRoles(name, domain);
                for (String role : roles) {
                    if (res.contains(role)) continue;
                    res.add(role);
                    queue.offerLast(role);
                }
            }
        }

        return null;
    }
```
