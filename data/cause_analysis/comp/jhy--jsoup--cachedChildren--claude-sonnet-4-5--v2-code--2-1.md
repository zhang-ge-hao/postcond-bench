https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Element.java#L422-L437
```
//@ ensures (attributes == null || !attributes.hasUserData()) ==> \result == null;
//@ ensures \result != null ==> attributes != null;
//@ ensures \result != null ==> attributes.hasUserData();
//@ ensures \result != null ==> ((Integer)attributes.userData().get(childElsMod)) != null && ((Integer)attributes.userData().get(childElsMod)).intValue() == childNodes.modCount();
//@ ensures \result != null ==> attributes.userData().get(childElsKey) != null;
//@ ensures \result != null ==> ((WeakReference<List<Element>>)attributes.userData().get(childElsKey)).get() == \result;
```
```
return value - inner repository type


return value content

repository defined type
```
passed
```
//@ ensures (attributes == null || !attributes.hasUserData()) ==> \result == null;
//@ ensures (\result != null) ==> (attributes != null && attributes.hasUserData());
//@ ensures (\result != null) ==> (attributes.userData().get(childElsKey) instanceof java.lang.ref.WeakReference && ((java.lang.ref.WeakReference)attributes.userData().get(childElsKey)).get() == \result);
//@ ensures (\result != null) ==> (attributes.userData().get(childElsMod) instanceof Integer && ((Integer)attributes.userData().get(childElsMod)).intValue() == childNodes.modCount());
//@ ensures (attributes != null && attributes.hasUserData() && attributes.userData().get(childElsKey) instanceof java.lang.ref.WeakReference && ((java.lang.ref.WeakReference)attributes.userData().get(childElsKey)).get() != null && attributes.userData().get(childElsMod) instanceof Integer && ((Integer)attributes.userData().get(childElsMod)).intValue() == childNodes.modCount()) ==> \result == ((java.lang.ref.WeakReference)attributes.userData().get(childElsKey)).get();
//@ ensures \old(attributes != null && attributes.hasUserData() && attributes.userData().get(childElsKey) instanceof java.lang.ref.WeakReference && ((java.lang.ref.WeakReference)attributes.userData().get(childElsKey)).get() != null && attributes.userData().get(childElsMod) instanceof Integer && ((Integer)attributes.userData().get(childElsMod)).intValue() == childNodes.modCount()) ==> (\result == \old(attributes == null ? null : (((java.lang.ref.WeakReference)attributes.userData().get(childElsKey)) == null ? null : ((java.lang.ref.WeakReference)attributes.userData().get(childElsKey)).get())));

```
===== 1: failed =====
```
     /** returns the cached child els, if they exist, and the modcount of our childnodes matches the stashed modcount */
     @Nullable List<Element> cachedChildren() {
         if (attributes == null || !attributes.hasUserData()) return null; // don't create empty userdata
-        Map<String, Object> userData = attributes.userData();
+        Map<String, Object> userData = attributes.userData(); userData.clear(); // clears the user data, leading to loss of information
         //noinspection unchecked
         WeakReference<List<Element>> ref = (WeakReference<List<Element>>) userData.get(childElsKey);
         if (ref != null) {
```
```
    /** returns the cached child els, if they exist, and the modcount of our childnodes matches the stashed modcount */
    @Nullable List<Element> cachedChildren() {
        if (attributes == null || !attributes.hasUserData()) return null; // don't create empty userdata
        Map<String, Object> userData = attributes.userData(); userData.clear(); // clears the user data, leading to loss of information
        //noinspection unchecked
        WeakReference<List<Element>> ref = (WeakReference<List<Element>>) userData.get(childElsKey);
        if (ref != null) {
            List<Element> els = ref.get();
            if (els != null) {
                Integer modCount = (Integer) userData.get(childElsMod);
                if (modCount != null && modCount == childNodes.modCount())
                    return els;
            }
        }
        return null;
    }
```
