https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L1106-L1133
```
//@ ensures \result != null;
//@ ensures !\result.isEmpty();
//@ ensures !\result.startsWith(" ");
//@ ensures !\result.endsWith(" ");
//@ ensures \result.indexOf("null") == -1;
//@ ensures \result.indexOf("  >") == -1;
//@ ensures \result.startsWith("#") || \result.endsWith(cssSelectorComponent());
//@ ensures ownerDocument() == null && !\old(id()).isEmpty() ==> \result.equals("#" + escapeCssIdentifier(\old(id())));
//@ ensures ownerDocument() != null && !id().isEmpty() && ownerDocument().select("#" + escapeCssIdentifier(id())).size() == 1 && ownerDocument().select("#" + escapeCssIdentifier(id())).get(0) == this ==> \result.equals("#" + escapeCssIdentifier(id()));
//@ ensures ownerDocument() != null && ownerDocument().nodeName().equals("#document") ==> \result.indexOf(escapeCssIdentifier("#root")) == -1;
//@ ensures ownerDocument() != null && parent() != null && !parent().id().isEmpty() && ownerDocument().select("#" + escapeCssIdentifier(parent().id())).size() == 1 && ownerDocument().select("#" + escapeCssIdentifier(parent().id())).get(0) == parent() ==> \result.startsWith("#" + escapeCssIdentifier(parent().id()));
//@ ensures ownerDocument() == null || (ownerDocument().select(\result).size() == 1 && ownerDocument().select(\result).get(0) == this);
```
```
//@ ensures \result != null;
//@ ensures !\result.isEmpty();
//@ ensures \result.startsWith("#") || \result.endsWith(cssSelectorComponent());
//@ ensures ownerDocument() == null && !\old(id()).isEmpty() ==> \result.equals("#" + \old(id()));
//@ ensures \result.indexOf("null") == -1;
//@ ensures !\result.startsWith(" ");
```
[1, 2, 11, 12, 16, 18, 19, 20, 21, 26, 27, 28, 29]
===== 1 =====
```
      @return the CSS Path that can be used to retrieve the element in a selector.
      */
     public String cssSelector() {
-        Document ownerDoc = ownerDocument();
+        Document ownerDoc = null; // This will lead to a NullPointerException when ownerDoc is used later.
         String idSel = uniqueIdSelector(ownerDoc);
         if (!idSel.isEmpty()) return idSel;
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = null; // This will lead to a NullPointerException when ownerDoc is used later.
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 2 =====
```
      */
     public String cssSelector() {
         Document ownerDoc = ownerDocument();
-        String idSel = uniqueIdSelector(ownerDoc);
+        String idSel = uniqueIdSelector(null); // Passing null will not raise an exception but will lead to incorrect behavior.
         if (!idSel.isEmpty()) return idSel;
 
         // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(null); // Passing null will not raise an exception but will lead to incorrect behavior.
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 11 =====
```
         // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
         StringBuilder selector = StringUtil.borrowBuilder();
         Element el = this;
-        while (el != null && !(el instanceof Document)) {
+        while (el != null && el instanceof Element) {
             idSel = el.uniqueIdSelector(ownerDoc);
             if (!idSel.isEmpty()) {
                 selector.insert(0, idSel);
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && el instanceof Element) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 12 =====
```
         // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
         StringBuilder selector = StringUtil.borrowBuilder();
         Element el = this;
-        while (el != null && !(el instanceof Document)) {
+        while (el != null && el instanceof Node) {
             idSel = el.uniqueIdSelector(ownerDoc);
             if (!idSel.isEmpty()) {
                 selector.insert(0, idSel);
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && el instanceof Node) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 16 =====
```
         StringBuilder selector = StringUtil.borrowBuilder();
         Element el = this;
         while (el != null && !(el instanceof Document)) {
-            idSel = el.uniqueIdSelector(ownerDoc);
+            idSel = el.uniqueIdSelector(null); // Passing null instead of the owner document may lead to incorrect behavior.
             if (!idSel.isEmpty()) {
                 selector.insert(0, idSel);
                 break; // found a unique ID to use as ancestor; stop
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(null); // Passing null instead of the owner document may lead to incorrect behavior.
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 18 =====
```
         StringBuilder selector = StringUtil.borrowBuilder();
         Element el = this;
         while (el != null && !(el instanceof Document)) {
-            idSel = el.uniqueIdSelector(ownerDoc);
+            idSel = el.uniqueIdSelector(ownerDoc).replace("#", "."); // Replacing the ID selector with a class selector will change the intended selection.
             if (!idSel.isEmpty()) {
                 selector.insert(0, idSel);
                 break; // found a unique ID to use as ancestor; stop
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc).replace("#", "."); // Replacing the ID selector with a class selector will change the intended selection.
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 19 =====
```
         StringBuilder selector = StringUtil.borrowBuilder();
         Element el = this;
         while (el != null && !(el instanceof Document)) {
-            idSel = el.uniqueIdSelector(ownerDoc);
+            idSel = el.uniqueIdSelector(ownerDoc).toUpperCase(); // Converting the selector to uppercase may cause it to fail to match the intended element.
             if (!idSel.isEmpty()) {
                 selector.insert(0, idSel);
                 break; // found a unique ID to use as ancestor; stop
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc).toUpperCase(); // Converting the selector to uppercase may cause it to fail to match the intended element.
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 20 =====
```
         Element el = this;
         while (el != null && !(el instanceof Document)) {
             idSel = el.uniqueIdSelector(ownerDoc);
-            if (!idSel.isEmpty()) {
+            if (idSel == null) {
                 selector.insert(0, idSel);
                 break; // found a unique ID to use as ancestor; stop
             }
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (idSel == null) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 21 =====
```
         Element el = this;
         while (el != null && !(el instanceof Document)) {
             idSel = el.uniqueIdSelector(ownerDoc);
-            if (!idSel.isEmpty()) {
+            if (idSel.contains(" ")) {
                 selector.insert(0, idSel);
                 break; // found a unique ID to use as ancestor; stop
             }
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (idSel.contains(" ")) {
                selector.insert(0, idSel);
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 26 =====
```
         while (el != null && !(el instanceof Document)) {
             idSel = el.uniqueIdSelector(ownerDoc);
             if (!idSel.isEmpty()) {
-                selector.insert(0, idSel);
+                selector.insert(0, idSel + " "); // This adds a space before the ID, which will make the selector invalid.
                 break; // found a unique ID to use as ancestor; stop
             }
             selector.insert(0, el.cssSelectorComponent());
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel + " "); // This adds a space before the ID, which will make the selector invalid.
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 27 =====
```
         while (el != null && !(el instanceof Document)) {
             idSel = el.uniqueIdSelector(ownerDoc);
             if (!idSel.isEmpty()) {
-                selector.insert(0, idSel);
+                selector.insert(0, idSel + " > "); // This adds a child combinator, which may not be appropriate for the selector context.
                 break; // found a unique ID to use as ancestor; stop
             }
             selector.insert(0, el.cssSelectorComponent());
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel + " > "); // This adds a child combinator, which may not be appropriate for the selector context.
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 28 =====
```
         while (el != null && !(el instanceof Document)) {
             idSel = el.uniqueIdSelector(ownerDoc);
             if (!idSel.isEmpty()) {
-                selector.insert(0, idSel);
+                selector.insert(0, idSel.replace("#", ".")); // This incorrectly changes the ID selector to a class selector.
                 break; // found a unique ID to use as ancestor; stop
             }
             selector.insert(0, el.cssSelectorComponent());
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel.replace("#", ".")); // This incorrectly changes the ID selector to a class selector.
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
===== 29 =====
```
         while (el != null && !(el instanceof Document)) {
             idSel = el.uniqueIdSelector(ownerDoc);
             if (!idSel.isEmpty()) {
-                selector.insert(0, idSel);
+                selector.insert(0, idSel.toUpperCase()); // This changes the case of the ID, potentially breaking the selector match.
                 break; // found a unique ID to use as ancestor; stop
             }
             selector.insert(0, el.cssSelectorComponent());
```
```
    /**
     Get a CSS selector that will uniquely select this element.
     <p>
     If the element has an ID, returns #id; otherwise returns the parent (if any) CSS selector, followed by
     {@literal '>'}, followed by a unique selector for the element (tag.class.class:nth-child(n)).
     </p>

     @return the CSS Path that can be used to retrieve the element in a selector.
     */
    public String cssSelector() {
        Document ownerDoc = ownerDocument();
        String idSel = uniqueIdSelector(ownerDoc);
        if (!idSel.isEmpty()) return idSel;

        // No unique ID, work up the parent stack and find either a unique ID to hang from, or just a GP > Parent > Child chain
        StringBuilder selector = StringUtil.borrowBuilder();
        Element el = this;
        while (el != null && !(el instanceof Document)) {
            idSel = el.uniqueIdSelector(ownerDoc);
            if (!idSel.isEmpty()) {
                selector.insert(0, idSel.toUpperCase()); // This changes the case of the ID, potentially breaking the selector match.
                break; // found a unique ID to use as ancestor; stop
            }
            selector.insert(0, el.cssSelectorComponent());
            el = el.parent();
        }
        return StringUtil.releaseBuilder(selector);
    }
```
