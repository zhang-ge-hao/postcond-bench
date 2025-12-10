https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L749-L766
```
//@ ensures \result == null <==> (!evaluator.matches(\old(this).root(), \old(this)) && !\old(this).parents().stream().anyMatch(p -> evaluator.matches(\old(this).root(), p)));
//@ ensures \result != null ==> evaluator.matches(\old(this).root(), \result);
//@ ensures \result != null ==> (\result == \old(this) || \old(this).parents().contains(\result));
//@ ensures \result != null && \result != \old(this) ==> !evaluator.matches(\old(this).root(), \old(this));
//@ ensures \result != null && \result != \old(this) ==> \old(this).parents().subList(0, \old(this).parents().indexOf(\result)).stream().noneMatch(p -> evaluator.matches(\old(this).root(), p));
```
```
//@ ensures \result == null <==> (!evaluator.matches(\old(this).root(), \old(this)) && !\old(this).parents().stream().anyMatch(p -> evaluator.matches(\old(this).root(), p)));
//@ ensures \result != null ==> evaluator.matches(\old(this).root(), \result);
//@ ensures \result != null ==> (\result == \old(this) || \old(this).parents().contains(\result));
//@ ensures \result != null && \result != \old(this) ==> \old(this).parents().subList(0, \old(this).parents().indexOf(\result)).stream().noneMatch(p -> evaluator.matches(\old(this).root(), p));
```
[0]
===== 0 =====
```
     public @Nullable Element closest(Evaluator evaluator) {
         Validate.notNull(evaluator);
         Element el = this;
-        final Element root = root();
+        final Element root = this; // Incorrectly assigns itself instead of the root element.
         do {
             if (evaluator.matches(root, el))
                 return el;
```
```
    /**
     * Find the closest element up the tree of parents that matches the specified evaluator. Will return itself, an
     * ancestor, or {@code null} if there is no such matching element.
     * @param evaluator a query evaluator
     * @return the closest ancestor element (possibly itself) that matches the provided evaluator. {@code null} if not
     * found.
     */
    public @Nullable Element closest(Evaluator evaluator) {
        Validate.notNull(evaluator);
        Element el = this;
        final Element root = this; // Incorrectly assigns itself instead of the root element.
        do {
            if (evaluator.matches(root, el))
                return el;
            el = el.parent();
        } while (el != null);
        return null;
    }
```
