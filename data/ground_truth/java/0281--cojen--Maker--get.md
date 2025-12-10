https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/WeakCache.java#L39-L59
```
//@ ensures (Object)\result == (new java.util.function.Supplier<Object>() { public Object get() { Entry[] entries = mEntries; int idx = key.hashCode() & (entries.length - 1); for (Entry e = entries[idx]; e != null; e = e.mNext) { if (e.mKey.equals(key)) { return e.get(); } } return null; } }).get();
//@ ensures (Object)\result == \old((new java.util.function.Supplier<Object>() { public Object get() { Entry[] entries = mEntries; int idx = key.hashCode() & (entries.length - 1); for (Entry e = entries[idx]; e != null; e = e.mNext) { if (e.mKey.equals(key)) { return e.get(); } } return null; } }).get());
```
```
//@ ensures (Object)\result == (new java.util.function.Supplier<Object>() { public Object get() { Entry[] entries = mEntries; int idx = key.hashCode() & (entries.length - 1); for (Entry e = entries[idx]; e != null; e = e.mNext) { if (e.mKey.equals(key)) { return e.get(); } } return null; } }).get();
```
[0, 7]
===== 0 =====
```
      * Double check with synchronization.
      */
     public V get(K key) {
-        Object ref = poll();
+        Object ref = mEntries[0]; // This incorrectly assigns a cache entry instead of a weak reference, causing cleanup to malfunction.
         if (ref != null) {
             synchronized (this) {
                 cleanup(ref);
```
```
    /**
     * Can be called without explicit synchronization, but entries can appear to go missing.
     * Double check with synchronization.
     */
    public V get(K key) {
        Object ref = mEntries[0]; // This incorrectly assigns a cache entry instead of a weak reference, causing cleanup to malfunction.
        if (ref != null) {
            synchronized (this) {
                cleanup(ref);
            }
        }

        var entries = mEntries;
        for (var e = entries[key.hashCode() & (entries.length - 1)]; e != null; e = e.mNext) {
            if (e.mKey.equals(key)) {
                return e.get();
            }
        }

        return null;
    }
```
===== 7 =====
```
         var entries = mEntries;
         for (var e = entries[key.hashCode() & (entries.length - 1)]; e != null; e = e.mNext) {
             if (e.mKey.equals(key)) {
-                return e.get();
+                e.clear(); return null; // Clears the entry and returns null, losing the value.
             }
         }
```
```
    /**
     * Can be called without explicit synchronization, but entries can appear to go missing.
     * Double check with synchronization.
     */
    public V get(K key) {
        Object ref = poll();
        if (ref != null) {
            synchronized (this) {
                cleanup(ref);
            }
        }

        var entries = mEntries;
        for (var e = entries[key.hashCode() & (entries.length - 1)]; e != null; e = e.mNext) {
            if (e.mKey.equals(key)) {
                e.clear(); return null; // Clears the entry and returns null, losing the value.
            }
        }

        return null;
    }
```
