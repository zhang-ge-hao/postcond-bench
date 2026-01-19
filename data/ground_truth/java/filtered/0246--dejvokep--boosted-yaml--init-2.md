https://github.com/dejvokep/boosted-yaml/blob/fd45ba039337485d5081ba47c1a1116e52a3160c/./src/main/java/dev/dejvokep/boostedyaml/block/implementation/Section.java#L192-L221
```
🈚️

It's hard.

//@ ensures getRoot() == root;
//@ ensures !isRoot() || keyNode == null;
//@ ensures getStoredValue().size() == valueNode.getValue().size();
//@ ensures getStoredValue().values().stream().allMatch(b -> b != null && (b instanceof Section || b instanceof TerminatedBlock));
//@ ensures getStoredValue().values().stream().filter(b -> b instanceof Section).allMatch(b -> ((Section) b).getRoot() == root && ((Section) b).getParent() == this);
//@ ensures getStoredValue().entrySet().stream().filter((java.util.Map.Entry e) -> e.getValue() instanceof Section).allMatch((java.util.Map.Entry e) -> ((Section) e.getValue()).getRoute().equals(getSubRoute(e.getKey())));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
===== 0 =====
```
             throw new IllegalArgumentException("Root sections cannot have a key node!");
 
         //Call superclass
-        super.init(keyNode, valueNode);
+        
         //Set
         this.root = root;
         resetDefaults();
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 1 =====
```
             throw new IllegalArgumentException("Root sections cannot have a key node!");
 
         //Call superclass
-        super.init(keyNode, valueNode);
+        super.init(keyNode, null);
         //Set
         this.root = root;
         resetDefaults();
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, null);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 2 =====
```
             throw new IllegalArgumentException("Root sections cannot have a key node!");
 
         //Call superclass
-        super.init(keyNode, valueNode);
+        super.init(valueNode, keyNode);
         //Set
         this.root = root;
         resetDefaults();
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(valueNode, keyNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 3 =====
```
         super.init(keyNode, valueNode);
         //Set
         this.root = root;
-        resetDefaults();
+        
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 4 =====
```
         super.init(keyNode, valueNode);
         //Set
         this.root = root;
-        resetDefaults();
+        defaults = null;
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        defaults = null;
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 5 =====
```
         super.init(keyNode, valueNode);
         //Set
         this.root = root;
-        resetDefaults();
+        this.name = "defaultName";
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        this.name = "defaultName";
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 6 =====
```
         super.init(keyNode, valueNode);
         //Set
         this.root = root;
-        resetDefaults();
+        this.parent = null;
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        this.parent = null;
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 7 =====
```
         super.init(keyNode, valueNode);
         //Set
         this.root = root;
-        resetDefaults();
+        this.route = null;
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        this.route = null;
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 8 =====
```
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
-            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
+            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = "stringValue"; // value is a string instead of the expected type
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = "stringValue"; // value is a string instead of the expected type
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 9 =====
```
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
-            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
+            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode()) instanceof Map ? new Section(root, this, getSubRoute(key), null, (Map<?, ?>) constructor.getConstructed(tuple.getValueNode())) : null; // value is null if not a Map
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode()) instanceof Map ? new Section(root, this, getSubRoute(key), null, (Map<?, ?>) constructor.getConstructed(tuple.getValueNode())) : null; // value is null if not a Map
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 10 =====
```
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
-            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
+            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode()).toString(); // value is converted to a string
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode()).toString(); // value is converted to a string
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 11 =====
```
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
-            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
+            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = new ArrayList<>(); // value is an empty list instead of the expected type
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = new ArrayList<>(); // value is an empty list instead of the expected type
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 12 =====
```
         //Loop through all mappings
         for (NodeTuple tuple : valueNode.getValue()) {
             //Key and value
-            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
+            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = null; // value is set to null
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = null; // value is set to null
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 13 =====
```
             //Key and value
             Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
             //Add
-            getStoredValue().put(key, value instanceof Map ?
-                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
-                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
+            
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            
        }
    }
```
===== 14 =====
```
             Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
             //Add
             getStoredValue().put(key, value instanceof Map ?
-                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
+                    new Section(root, this, getSubRoute(key), null, (MappingNode) tuple.getValueNode(), constructor) :
                     new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), null, (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 15 =====
```
             Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
             //Add
             getStoredValue().put(key, value instanceof Map ?
-                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
+                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) {
+    // Intentionally left empty to simulate a defect
+} :
                     new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) {
    // Intentionally left empty to simulate a defect
} :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
        }
    }
```
===== 16 =====
```
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
-                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
+                    new TerminatedBlock(null, tuple.getValueNode(), value));
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(null, tuple.getValueNode(), value));
        }
    }
```
===== 17 =====
```
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
-                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
+                    new TerminatedBlock(tuple.getKeyNode(), null, value));
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), null, value));
        }
    }
```
===== 18 =====
```
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
-                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
+                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), "Invalid Value"));
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), "Invalid Value"));
        }
    }
```
===== 19 =====
```
             //Add
             getStoredValue().put(key, value instanceof Map ?
                     new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
-                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), value));
+                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), null));
         }
     }
```
```
    /**
     * Initializes this section, and it's contents using the given parameters, while also initializing the superclass by
     * calling {@link Block#init(Node, Node)}.
     *
     * @param root        the root file of this section
     * @param keyNode     node which represents the key to this section, used <b>only</b> to retrieve comments (will
     *                    throw an {@link IllegalArgumentException} if provided and this {@link #isRoot() is the root})
     * @param valueNode   node which represents this section's contents
     * @param constructor constructor used to construct all the nodes contained within the root file, used to retrieve
     *                    Java instances of the nodes
     */
    protected void init(@NotNull YamlDocument root, @Nullable Node keyNode, @NotNull MappingNode valueNode, @NotNull ExtendedConstructor constructor) {
        if (root == this && keyNode != null)
            throw new IllegalArgumentException("Root sections cannot have a key node!");

        //Call superclass
        super.init(keyNode, valueNode);
        //Set
        this.root = root;
        resetDefaults();
        //Loop through all mappings
        for (NodeTuple tuple : valueNode.getValue()) {
            //Key and value
            Object key = adaptKey(constructor.getConstructed(tuple.getKeyNode())), value = constructor.getConstructed(tuple.getValueNode());
            //Add
            getStoredValue().put(key, value instanceof Map ?
                    new Section(root, this, getSubRoute(key), tuple.getKeyNode(), (MappingNode) tuple.getValueNode(), constructor) :
                    new TerminatedBlock(tuple.getKeyNode(), tuple.getValueNode(), null));
        }
    }
```
