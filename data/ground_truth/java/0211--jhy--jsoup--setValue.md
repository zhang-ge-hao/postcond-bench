https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Attribute.java#L108-L124
```
//@ ensures this.val == val;
//@ ensures \result != null;
//@ ensures \old(parent != null && parent.hasKey(key)) ==> \result.equals(\old(parent != null ? parent.get(key) : ""));
//@ ensures \old(parent == null || !parent.hasKey(key)) && \old(this.val) != null ==> \result.equals(\old(this.val));
//@ ensures \old(parent == null || !parent.hasKey(key)) && \old(this.val) == null ==> \result.equals("");
//@ ensures \old(parent != null && parent.hasKey(key)) && val != null ==> parent.get(key).equals(val);
//@ ensures \old(parent != null && parent.hasKey(key)) && val == null ==> parent.get(key).isEmpty();
//@ ensures val == null ==> getValue().equals("");
//@ ensures val != null ==> getValue().equals(val);
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
===== 0 =====
```
      */
     @Override public String setValue(@Nullable String val) {
         String oldVal = this.val;
-        if (parent != null) {
+        if (parent != null && key.isEmpty()) {
             int i = parent.indexOfKey(this.key);
             if (i != Attributes.NotFound) {
                 oldVal = parent.get(this.key); // trust the container more
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null && key.isEmpty()) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return Attributes.checkNotNull(oldVal);
    }
```
===== 1 =====
```
     @Override public String setValue(@Nullable String val) {
         String oldVal = this.val;
         if (parent != null) {
-            int i = parent.indexOfKey(this.key);
+            int i = parent.indexOfKey(this.key + "extra"); // appending extra characters to the key
             if (i != Attributes.NotFound) {
                 oldVal = parent.get(this.key); // trust the container more
                 parent.vals[i] = val;
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key + "extra"); // appending extra characters to the key
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return Attributes.checkNotNull(oldVal);
    }
```
===== 2 =====
```
     @Override public String setValue(@Nullable String val) {
         String oldVal = this.val;
         if (parent != null) {
-            int i = parent.indexOfKey(this.key);
+            int i = parent.indexOfKey(this.key.toLowerCase()); // converting key to lowercase, which may not match
             if (i != Attributes.NotFound) {
                 oldVal = parent.get(this.key); // trust the container more
                 parent.vals[i] = val;
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key.toLowerCase()); // converting key to lowercase, which may not match
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return Attributes.checkNotNull(oldVal);
    }
```
===== 3 =====
```
         String oldVal = this.val;
         if (parent != null) {
             int i = parent.indexOfKey(this.key);
-            if (i != Attributes.NotFound) {
+            if (i == 0) {
                 oldVal = parent.get(this.key); // trust the container more
                 parent.vals[i] = val;
             }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i == 0) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return Attributes.checkNotNull(oldVal);
    }
```
===== 4 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return "";
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return "";
    }
```
===== 5 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return ""; // returns an empty string instead of the old value
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return ""; // returns an empty string instead of the old value
    }
```
===== 6 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return Attributes.checkNotNull(val); // returns the new value instead of the old value, but checks for null
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return Attributes.checkNotNull(val); // returns the new value instead of the old value, but checks for null
    }
```
===== 7 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return null;
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return null;
    }
```
===== 8 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return null; // introduces a null return value
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return null; // introduces a null return value
    }
```
===== 9 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return oldVal.toUpperCase(); // modifies the old value, changing its case
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return oldVal.toUpperCase(); // modifies the old value, changing its case
    }
```
===== 10 =====
```
             }
         }
         this.val = val;
-        return Attributes.checkNotNull(oldVal);
+        return val; // returns the new value instead of the old value
     }
```
```
    /**
     Set the attribute value.
     @param val the new attribute value; may be null (to set an enabled boolean attribute)
     @return the previous value (if was null; an empty string)
     */
    @Override public String setValue(@Nullable String val) {
        String oldVal = this.val;
        if (parent != null) {
            int i = parent.indexOfKey(this.key);
            if (i != Attributes.NotFound) {
                oldVal = parent.get(this.key); // trust the container more
                parent.vals[i] = val;
            }
        }
        this.val = val;
        return val; // returns the new value instead of the old value
    }
```
