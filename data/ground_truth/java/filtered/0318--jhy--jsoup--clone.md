https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Node.java#L948-L984
```
🈚️

Timeout.

//@ ensures \result != null;
//@ ensures \result != this;
//@ ensures this.hasSameValue(\result);
//@ ensures \result.siblingNodes().isEmpty();
//@ ensures \result.nodeStream().count() == this.nodeStream().count();
//@ ensures this.nodeStream().noneMatch(n -> \result.nodeStream().anyMatch(m -> m == n));
//@ ensures \result.nodeStream().allMatch(n -> n.parent() == null || \result.nodeStream().anyMatch(m -> m == n.parent()));
//@ ensures (this instanceof LeafNode) ==> (\result.parent() == null);
//@ ensures (this instanceof Element) ==> (\result.ownerDocument() != null && \result.ownerDocument().childNodes().contains(\result));
```
```
None
```
[0, 1, 2, 3, 4]
===== 0 =====
```
     // because it does call super.clone in doClone - analysis just isn't following
     @Override
     public Node clone() {
-        Node thisClone = doClone(null); // splits for orphan
+        Node thisClone = doClone(ownerDocument()); // uses the document as parent
 
         // Queue up nodes that need their children cloned (BFS).
         final LinkedList<Node> nodesToProcess = new LinkedList<>();
```
```
    /**
     Create a stand-alone, deep copy of this node, and all of its children. The cloned node will have no siblings.
     <p><ul>
     <li>If this node is a {@link LeafNode}, the clone will have no parent.</li>
     <li>If this node is an {@link Element}, the clone will have a simple owning {@link Document} to retain the
     configured output settings and parser.</li>
     </ul></p>
     <p>The cloned node may be adopted into another Document or node structure using
     {@link Element#appendChild(Node)}.</p>

     @return a stand-alone cloned node, including clones of any children
     @see #shallowClone()
     */
    @SuppressWarnings("MethodDoesntCallSuperMethod")
    // because it does call super.clone in doClone - analysis just isn't following
    @Override
    public Node clone() {
        Node thisClone = doClone(ownerDocument()); // uses the document as parent

        // Queue up nodes that need their children cloned (BFS).
        final LinkedList<Node> nodesToProcess = new LinkedList<>();
        nodesToProcess.add(thisClone);

        while (!nodesToProcess.isEmpty()) {
            Node currParent = nodesToProcess.remove();

            final int size = currParent.childNodeSize();
            for (int i = 0; i < size; i++) {
                final List<Node> childNodes = currParent.ensureChildNodes();
                Node childClone = childNodes.get(i).doClone(currParent);
                childNodes.set(i, childClone);
                nodesToProcess.add(childClone);
            }
        }

        return thisClone;
    }
```
===== 1 =====
```
             final int size = currParent.childNodeSize();
             for (int i = 0; i < size; i++) {
                 final List<Node> childNodes = currParent.ensureChildNodes();
-                Node childClone = childNodes.get(i).doClone(currParent);
+                Node childClone = childNodes.get(i).shallowClone(); // This will not clone the children, leading to shared references.
                 childNodes.set(i, childClone);
                 nodesToProcess.add(childClone);
             }
```
```
    /**
     Create a stand-alone, deep copy of this node, and all of its children. The cloned node will have no siblings.
     <p><ul>
     <li>If this node is a {@link LeafNode}, the clone will have no parent.</li>
     <li>If this node is an {@link Element}, the clone will have a simple owning {@link Document} to retain the
     configured output settings and parser.</li>
     </ul></p>
     <p>The cloned node may be adopted into another Document or node structure using
     {@link Element#appendChild(Node)}.</p>

     @return a stand-alone cloned node, including clones of any children
     @see #shallowClone()
     */
    @SuppressWarnings("MethodDoesntCallSuperMethod")
    // because it does call super.clone in doClone - analysis just isn't following
    @Override
    public Node clone() {
        Node thisClone = doClone(null); // splits for orphan

        // Queue up nodes that need their children cloned (BFS).
        final LinkedList<Node> nodesToProcess = new LinkedList<>();
        nodesToProcess.add(thisClone);

        while (!nodesToProcess.isEmpty()) {
            Node currParent = nodesToProcess.remove();

            final int size = currParent.childNodeSize();
            for (int i = 0; i < size; i++) {
                final List<Node> childNodes = currParent.ensureChildNodes();
                Node childClone = childNodes.get(i).shallowClone(); // This will not clone the children, leading to shared references.
                childNodes.set(i, childClone);
                nodesToProcess.add(childClone);
            }
        }

        return thisClone;
    }
```
===== 2 =====
```
             for (int i = 0; i < size; i++) {
                 final List<Node> childNodes = currParent.ensureChildNodes();
                 Node childClone = childNodes.get(i).doClone(currParent);
-                childNodes.set(i, childClone);
+                childNodes.add(i, childClone); // Inserts the clone at the index instead of replacing the existing child
                 nodesToProcess.add(childClone);
             }
         }
```
```
    /**
     Create a stand-alone, deep copy of this node, and all of its children. The cloned node will have no siblings.
     <p><ul>
     <li>If this node is a {@link LeafNode}, the clone will have no parent.</li>
     <li>If this node is an {@link Element}, the clone will have a simple owning {@link Document} to retain the
     configured output settings and parser.</li>
     </ul></p>
     <p>The cloned node may be adopted into another Document or node structure using
     {@link Element#appendChild(Node)}.</p>

     @return a stand-alone cloned node, including clones of any children
     @see #shallowClone()
     */
    @SuppressWarnings("MethodDoesntCallSuperMethod")
    // because it does call super.clone in doClone - analysis just isn't following
    @Override
    public Node clone() {
        Node thisClone = doClone(null); // splits for orphan

        // Queue up nodes that need their children cloned (BFS).
        final LinkedList<Node> nodesToProcess = new LinkedList<>();
        nodesToProcess.add(thisClone);

        while (!nodesToProcess.isEmpty()) {
            Node currParent = nodesToProcess.remove();

            final int size = currParent.childNodeSize();
            for (int i = 0; i < size; i++) {
                final List<Node> childNodes = currParent.ensureChildNodes();
                Node childClone = childNodes.get(i).doClone(currParent);
                childNodes.add(i, childClone); // Inserts the clone at the index instead of replacing the existing child
                nodesToProcess.add(childClone);
            }
        }

        return thisClone;
    }
```
===== 3 =====
```
             for (int i = 0; i < size; i++) {
                 final List<Node> childNodes = currParent.ensureChildNodes();
                 Node childClone = childNodes.get(i).doClone(currParent);
-                childNodes.set(i, childClone);
+                childNodes.set(i, null); // Sets the original child to null instead of replacing it with the clone
                 nodesToProcess.add(childClone);
             }
         }
```
```
    /**
     Create a stand-alone, deep copy of this node, and all of its children. The cloned node will have no siblings.
     <p><ul>
     <li>If this node is a {@link LeafNode}, the clone will have no parent.</li>
     <li>If this node is an {@link Element}, the clone will have a simple owning {@link Document} to retain the
     configured output settings and parser.</li>
     </ul></p>
     <p>The cloned node may be adopted into another Document or node structure using
     {@link Element#appendChild(Node)}.</p>

     @return a stand-alone cloned node, including clones of any children
     @see #shallowClone()
     */
    @SuppressWarnings("MethodDoesntCallSuperMethod")
    // because it does call super.clone in doClone - analysis just isn't following
    @Override
    public Node clone() {
        Node thisClone = doClone(null); // splits for orphan

        // Queue up nodes that need their children cloned (BFS).
        final LinkedList<Node> nodesToProcess = new LinkedList<>();
        nodesToProcess.add(thisClone);

        while (!nodesToProcess.isEmpty()) {
            Node currParent = nodesToProcess.remove();

            final int size = currParent.childNodeSize();
            for (int i = 0; i < size; i++) {
                final List<Node> childNodes = currParent.ensureChildNodes();
                Node childClone = childNodes.get(i).doClone(currParent);
                childNodes.set(i, null); // Sets the original child to null instead of replacing it with the clone
                nodesToProcess.add(childClone);
            }
        }

        return thisClone;
    }
```
===== 4 =====
```
             }
         }
 
-        return thisClone;
+        return null;
     }
```
```
    /**
     Create a stand-alone, deep copy of this node, and all of its children. The cloned node will have no siblings.
     <p><ul>
     <li>If this node is a {@link LeafNode}, the clone will have no parent.</li>
     <li>If this node is an {@link Element}, the clone will have a simple owning {@link Document} to retain the
     configured output settings and parser.</li>
     </ul></p>
     <p>The cloned node may be adopted into another Document or node structure using
     {@link Element#appendChild(Node)}.</p>

     @return a stand-alone cloned node, including clones of any children
     @see #shallowClone()
     */
    @SuppressWarnings("MethodDoesntCallSuperMethod")
    // because it does call super.clone in doClone - analysis just isn't following
    @Override
    public Node clone() {
        Node thisClone = doClone(null); // splits for orphan

        // Queue up nodes that need their children cloned (BFS).
        final LinkedList<Node> nodesToProcess = new LinkedList<>();
        nodesToProcess.add(thisClone);

        while (!nodesToProcess.isEmpty()) {
            Node currParent = nodesToProcess.remove();

            final int size = currParent.childNodeSize();
            for (int i = 0; i < size; i++) {
                final List<Node> childNodes = currParent.ensureChildNodes();
                Node childClone = childNodes.get(i).doClone(currParent);
                childNodes.set(i, childClone);
                nodesToProcess.add(childClone);
            }
        }

        return null;
    }
```
