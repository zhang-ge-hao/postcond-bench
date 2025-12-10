https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/NodeIterator.java#L79-L90
```
//@ ensures \old(next) != null ==> (next == \old(next) && current == \old(current) && previous == \old(previous) && currentParent == \old(currentParent));
//@ ensures next == null || type.isInstance(next);
//@ ensures \old(currentParent) != null && !\old(current).hasParent() ==> current == \old(previous);
//@ ensures !(\old(currentParent) != null && !\old(current).hasParent()) ==> current == \old(current);
//@ ensures previous == \old(previous);
//@ ensures currentParent == \old(currentParent);
//@ ensures \old(next) == null && type == Node.class && \old(current).childNodeSize() > 0 && !(\old(currentParent) != null && !\old(current).hasParent()) ==> next == \old(current).childNode(0);
```
```
//@ ensures \old(next) != null ==> (next == \old(next) && current == \old(current) && previous == \old(previous) && currentParent == \old(currentParent));
//@ ensures next == null || type.isInstance(next);
//@ ensures \old(currentParent) != null && !\old(current).hasParent() ==> current == \old(previous);
//@ ensures !( \old(currentParent) != null && !\old(current).hasParent() ) ==> current == \old(current);
//@ ensures previous == \old(previous);
//@ ensures currentParent == \old(currentParent);
```
[4, 7, 8]
===== 4 =====
```
      If next is not null, looks for and sets next. If next is null after this, we have reached the end.
      */
     private void maybeFindNext() {
-        if (next != null) return;
+        if (root.equals(current)) return; // Incorrectly returns if the current node is the root, skipping valid nodes
 
         //  change detected (removed or replaced), redo from previous
         if (currentParent != null && !current.hasParent())
```
```
    /**
     If next is not null, looks for and sets next. If next is null after this, we have reached the end.
     */
    private void maybeFindNext() {
        if (root.equals(current)) return; // Incorrectly returns if the current node is the root, skipping valid nodes

        //  change detected (removed or replaced), redo from previous
        if (currentParent != null && !current.hasParent())
            current = previous;

        next = findNextNode();
    }
```
===== 7 =====
```
         if (currentParent != null && !current.hasParent())
             current = previous;
 
-        next = findNextNode();
+        next = (T) current.nextSibling(); // Incorrectly assigns the next sibling of the current node, which may not be of type T.
     }
```
```
    /**
     If next is not null, looks for and sets next. If next is null after this, we have reached the end.
     */
    private void maybeFindNext() {
        if (next != null) return;

        //  change detected (removed or replaced), redo from previous
        if (currentParent != null && !current.hasParent())
            current = previous;

        next = (T) current.nextSibling(); // Incorrectly assigns the next sibling of the current node, which may not be of type T.
    }
```
===== 8 =====
```
         if (currentParent != null && !current.hasParent())
             current = previous;
 
-        next = findNextNode();
+        next = null; // Sets next to null, causing hasNext() to always return false after the first call to next().
     }
```
```
    /**
     If next is not null, looks for and sets next. If next is null after this, we have reached the end.
     */
    private void maybeFindNext() {
        if (next != null) return;

        //  change detected (removed or replaced), redo from previous
        if (currentParent != null && !current.hasParent())
            current = previous;

        next = null; // Sets next to null, causing hasNext() to always return false after the first call to next().
    }
```
