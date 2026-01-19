https://github.com/j-easy/easy-random/blob/51150d4621c4ec6d534d99e6a71eeaeb2e11caaf/./src/main/java/org/jeasy/random/util/ReflectionUtils.java#L157-L178
```
🈚️

originally wrong. cannot write post-condition due to try catch dealing.

//@ ensures \result == new Object() { Object v(){ try { if (getReadMethod(field).isPresent()) { return getter.get().invoke(object) } else { return getFieldValue(object, field) } } catch (IllegalAccessException | InvocationTargetException e) { return getFieldValue(object, field) } } }.v();
```
```
None
```
[0, 1, 2, 3, 4]
===== 0 =====
```
      */
     public static Object getProperty(final Object object, final Field field) throws IllegalAccessException {
         try {
-            Optional<Method> getter = getReadMethod(field);
+            Optional<Method> getter = getReadMethod(field.getDeclaringClass().getDeclaredFields()[0]); // Incorrectly retrieves the read method for a different field.
             if (getter.isPresent()) {
                 return getter.get().invoke(object);
             } else {
```
```
    /**
     * Get a value of a field of a target object. If the target object provides
     * a getter for the field, this getter will be used. Otherwise, the field
     * will be get using reflection.
     *
     * @param object instance to get the property value
     * @param field  field to get the property value
     * @throws IllegalAccessException if the property cannot be retrieved
     */
    public static Object getProperty(final Object object, final Field field) throws IllegalAccessException {
        try {
            Optional<Method> getter = getReadMethod(field.getDeclaringClass().getDeclaredFields()[0]); // Incorrectly retrieves the read method for a different field.
            if (getter.isPresent()) {
                return getter.get().invoke(object);
            } else {
                return getFieldValue(object, field);
            }
        } catch (IllegalAccessException | InvocationTargetException  e) {
            // otherwise, get field using reflection
            return getFieldValue(object, field);
        }
    }
```
===== 1 =====
```
             if (getter.isPresent()) {
                 return getter.get().invoke(object);
             } else {
-                return getFieldValue(object, field);
+                return new Object(); // This will return a new Object instance instead of the field's value.
             }
         } catch (IllegalAccessException | InvocationTargetException  e) {
             // otherwise, get field using reflection
```
```
    /**
     * Get a value of a field of a target object. If the target object provides
     * a getter for the field, this getter will be used. Otherwise, the field
     * will be get using reflection.
     *
     * @param object instance to get the property value
     * @param field  field to get the property value
     * @throws IllegalAccessException if the property cannot be retrieved
     */
    public static Object getProperty(final Object object, final Field field) throws IllegalAccessException {
        try {
            Optional<Method> getter = getReadMethod(field);
            if (getter.isPresent()) {
                return getter.get().invoke(object);
            } else {
                return new Object(); // This will return a new Object instance instead of the field's value.
            }
        } catch (IllegalAccessException | InvocationTargetException  e) {
            // otherwise, get field using reflection
            return getFieldValue(object, field);
        }
    }
```
===== 2 =====
```
             if (getter.isPresent()) {
                 return getter.get().invoke(object);
             } else {
-                return getFieldValue(object, field);
+                return null; // This will cause a NullPointerException when the value is accessed.
             }
         } catch (IllegalAccessException | InvocationTargetException  e) {
             // otherwise, get field using reflection
```
```
    /**
     * Get a value of a field of a target object. If the target object provides
     * a getter for the field, this getter will be used. Otherwise, the field
     * will be get using reflection.
     *
     * @param object instance to get the property value
     * @param field  field to get the property value
     * @throws IllegalAccessException if the property cannot be retrieved
     */
    public static Object getProperty(final Object object, final Field field) throws IllegalAccessException {
        try {
            Optional<Method> getter = getReadMethod(field);
            if (getter.isPresent()) {
                return getter.get().invoke(object);
            } else {
                return null; // This will cause a NullPointerException when the value is accessed.
            }
        } catch (IllegalAccessException | InvocationTargetException  e) {
            // otherwise, get field using reflection
            return getFieldValue(object, field);
        }
    }
```
===== 3 =====
```
             }
         } catch (IllegalAccessException | InvocationTargetException  e) {
             // otherwise, get field using reflection
-            return getFieldValue(object, field);
+            return "default"; // Returns a hardcoded string instead of the actual field value
         }
     }
```
```
    /**
     * Get a value of a field of a target object. If the target object provides
     * a getter for the field, this getter will be used. Otherwise, the field
     * will be get using reflection.
     *
     * @param object instance to get the property value
     * @param field  field to get the property value
     * @throws IllegalAccessException if the property cannot be retrieved
     */
    public static Object getProperty(final Object object, final Field field) throws IllegalAccessException {
        try {
            Optional<Method> getter = getReadMethod(field);
            if (getter.isPresent()) {
                return getter.get().invoke(object);
            } else {
                return getFieldValue(object, field);
            }
        } catch (IllegalAccessException | InvocationTargetException  e) {
            // otherwise, get field using reflection
            return "default"; // Returns a hardcoded string instead of the actual field value
        }
    }
```
===== 4 =====
```
             }
         } catch (IllegalAccessException | InvocationTargetException  e) {
             // otherwise, get field using reflection
-            return getFieldValue(object, field);
+            return new Object(); // Returns a new Object instance instead of the actual field value
         }
     }
```
```
    /**
     * Get a value of a field of a target object. If the target object provides
     * a getter for the field, this getter will be used. Otherwise, the field
     * will be get using reflection.
     *
     * @param object instance to get the property value
     * @param field  field to get the property value
     * @throws IllegalAccessException if the property cannot be retrieved
     */
    public static Object getProperty(final Object object, final Field field) throws IllegalAccessException {
        try {
            Optional<Method> getter = getReadMethod(field);
            if (getter.isPresent()) {
                return getter.get().invoke(object);
            } else {
                return getFieldValue(object, field);
            }
        } catch (IllegalAccessException | InvocationTargetException  e) {
            // otherwise, get field using reflection
            return new Object(); // Returns a new Object instance instead of the actual field value
        }
    }
```
