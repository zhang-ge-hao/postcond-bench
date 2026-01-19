https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/Switcher.java#L257-L288
```
🈚️

originally wrong. `Object... keys`
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
 
         Label defaultLabel = mm.label();
 
-        switchObject(mm, mm.param(0), defaultLabel, keys, labels);
+        
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(i);
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 1 =====
```
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
-            mm.return_(i);
+            
         }
         defaultLabel.here();
         mm.return_(-1);
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 2 =====
```
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
-            mm.return_(i);
+            mm.return_(-2); // Returns a constant negative value instead of the matched index
         }
         defaultLabel.here();
         mm.return_(-1);
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(-2); // Returns a constant negative value instead of the matched index
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 3 =====
```
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
-            mm.return_(i);
+            mm.return_(0); // Always returns 0 regardless of the case matched
         }
         defaultLabel.here();
         mm.return_(-1);
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(0); // Always returns 0 regardless of the case matched
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 4 =====
```
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
-            mm.return_(i);
+            mm.return_(Integer.MAX_VALUE); // Returns a constant maximum integer value, which is invalid
         }
         defaultLabel.here();
         mm.return_(-1);
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(Integer.MAX_VALUE); // Returns a constant maximum integer value, which is invalid
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 5 =====
```
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
-            mm.return_(i);
+            mm.return_(i + 1); // Off by one error, returns the next index instead of the current
         }
         defaultLabel.here();
         mm.return_(-1);
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(i + 1); // Off by one error, returns the next index instead of the current
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 6 =====
```
 
         for (int i=0; i<labels.length; i++) {
             labels[i].here();
-            mm.return_(i);
+            mm.return_(keys.length); // Returns the length of keys instead of the matched index
         }
         defaultLabel.here();
         mm.return_(-1);
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(keys.length); // Returns the length of keys instead of the matched index
        }
        defaultLabel.here();
        mm.return_(-1);

        return new ConstantCallSite(mm.finish());
    }
```
===== 7 =====
```
             mm.return_(i);
         }
         defaultLabel.here();
-        mm.return_(-1);
+        mm.return_(0); // Returns 0 instead of -1, which may not represent an invalid case.
 
         return new ConstantCallSite(mm.finish());
     }
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(i);
        }
        defaultLabel.here();
        mm.return_(0); // Returns 0 instead of -1, which may not represent an invalid case.

        return new ConstantCallSite(mm.finish());
    }
```
===== 8 =====
```
             mm.return_(i);
         }
         defaultLabel.here();
-        mm.return_(-1);
+        mm.return_(1); // Returns 1 instead of -1, potentially indicating a valid case when it should not.
 
         return new ConstantCallSite(mm.finish());
     }
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(i);
        }
        defaultLabel.here();
        mm.return_(1); // Returns 1 instead of -1, potentially indicating a valid case when it should not.

        return new ConstantCallSite(mm.finish());
    }
```
===== 9 =====
```
         defaultLabel.here();
         mm.return_(-1);
 
-        return new ConstantCallSite(mm.finish());
+        return null;
     }
```
```
    /**
     * Bootstrap method which makes a method that accepts a single argument and returns a
     * zero-based ordinal value corresponding to one of the case keys. If none match, -1 is
     * returned.
     */
    public static CallSite ordinals(MethodHandles.Lookup lookup, String name, MethodType type,
                                    Object... keys)
    {
        if (type.returnType() != int.class || type.parameterCount() != 1) {
            throw new IllegalArgumentException();
        }

        MethodMaker mm = MethodMaker.begin(lookup, name, type);

        var labels = new Label[keys.length];
        for (int i=0; i<labels.length; i++) {
            labels[i] = mm.label();
        }

        Label defaultLabel = mm.label();

        switchObject(mm, mm.param(0), defaultLabel, keys, labels);

        for (int i=0; i<labels.length; i++) {
            labels[i].here();
            mm.return_(i);
        }
        defaultLabel.here();
        mm.return_(-1);

        return null;
    }
```
