https://github.com/cojen/Maker/blob/e2d6d1639ff7abd2d6afce0a63c93bafa076e08a/./src/main/java/org/cojen/maker/BaseType.java#L349-L441
```
//@ ensures \result == Integer.MAX_VALUE || (\result >= 0 && \result <= 19);
//@ ensures this.equals(to) ==> \result == 0;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_BYTE && to.typeCode() == T_SHORT ==> \result == 0;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_BYTE && to.typeCode() == T_INT ==> \result == 0;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_BYTE && to.typeCode() == T_LONG ==> \result == 1;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_BYTE && to.typeCode() == T_FLOAT ==> \result == 2;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_BYTE && to.typeCode() == T_DOUBLE ==> \result == 3;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_SHORT && to.typeCode() == T_INT ==> \result == 0;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_SHORT && to.typeCode() == T_LONG ==> \result == 1;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_SHORT && to.typeCode() == T_FLOAT ==> \result == 2;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_SHORT && to.typeCode() == T_DOUBLE ==> \result == 3;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_CHAR && to.typeCode() == T_INT ==> \result == 0;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_CHAR && to.typeCode() == T_LONG ==> \result == 1;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_CHAR && to.typeCode() == T_FLOAT ==> \result == 2;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_CHAR && to.typeCode() == T_DOUBLE ==> \result == 3;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_INT && to.typeCode() == T_LONG ==> \result == 1;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_INT && to.typeCode() == T_DOUBLE ==> \result == 3;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && this.typeCode() == T_FLOAT && to.typeCode() == T_DOUBLE ==> \result == 4;
//@ ensures this.isPrimitive() && to != null && to.isPrimitive() && !this.equals(to) && !((this.typeCode() == T_BYTE && (to.typeCode() == T_SHORT || to.typeCode() == T_INT || to.typeCode() == T_LONG || to.typeCode() == T_FLOAT || to.typeCode() == T_DOUBLE)) || (this.typeCode() == T_SHORT && (to.typeCode() == T_INT || to.typeCode() == T_LONG || to.typeCode() == T_FLOAT || to.typeCode() == T_DOUBLE)) || (this.typeCode() == T_CHAR && (to.typeCode() == T_INT || to.typeCode() == T_LONG || to.typeCode() == T_FLOAT || to.typeCode() == T_DOUBLE)) || (this.typeCode() == T_INT && (to.typeCode() == T_LONG || to.typeCode() == T_DOUBLE)) || (this.typeCode() == T_FLOAT && to.typeCode() == T_DOUBLE)) ==> \result == Integer.MAX_VALUE;
//@ ensures to != null && this.isPrimitive() && !to.isPrimitive() && \result != Integer.MAX_VALUE ==> (\result >= 5 && \result <= 9);
//@ ensures (\result >= 5 && \result <= 9) ==> (to != null && this.isPrimitive() && !to.isPrimitive());
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == boolean.class && to.classType() == Boolean.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == byte.class && to.classType() == Byte.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == char.class && to.classType() == Character.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == short.class && to.classType() == Short.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == int.class && to.classType() == Integer.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == float.class && to.classType() == Float.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == long.class && to.classType() == Long.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == double.class && to.classType() == Double.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && to.classType() == Number.class ==> \result == 5;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && to.classType() == Object.class ==> \result == 5;
//@ ensures this.isPrimitive() && this.classType() == int.class && to != null && !to.isPrimitive() && to.classType() == Boolean.class ==> \result == Integer.MAX_VALUE;
//@ ensures to != null && !this.isPrimitive() && to.isObject() && to.isAssignableFrom(this) ==> \result == 0;
//@ ensures to != null && !this.isPrimitive() && !to.isObject() && \result != Integer.MAX_VALUE ==> (\result >= 15 && \result <= 19);
//@ ensures to != null && !this.isPrimitive() && to.isObject() && !to.isAssignableFrom(this) && \result != Integer.MAX_VALUE ==> (\result >= 10 && \result <= 14);
//@ ensures !this.isPrimitive() && to != null && to.isObject() && this.classType() == Integer.class && to.classType() == Long.class ==> \result == 11;
//@ ensures !this.isPrimitive() && to != null && !to.isObject() && this.classType() == Integer.class && to.classType() == long.class ==> \result == 16;
//@ ensures this.isPrimitive() && to != null && !to.isPrimitive() && this.classType() == int.class && to.classType() == Long.class ==> \result == 6;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
===== 0 =====
```
      * @return conversion code, which is max value if disallowed
      */
     final int canConvertTo(BaseType to) {
-        if (this.equals(to)) {
+        if (this instanceof Primitive) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this instanceof Primitive) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 1 =====
```
      * @return conversion code, which is max value if disallowed
      */
     final int canConvertTo(BaseType to) {
-        if (this.equals(to)) {
+        if (this.typeCode() == to.typeCode()) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.typeCode() == to.typeCode()) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 2 =====
```
      * @return conversion code, which is max value if disallowed
      */
     final int canConvertTo(BaseType to) {
-        if (this.equals(to)) {
+        if (to == null) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (to == null) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 3 =====
```
             return 0;
         }
 
-        if (this.isPrimitive()) {
+        if (this.unbox() != null) {
             if (to.isPrimitive()) {
                 switch (this.typeCode()) {
                 case T_BYTE:
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.unbox() != null) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 4 =====
```
         }
 
         if (this.isPrimitive()) {
-            if (to.isPrimitive()) {
+            if (to instanceof BaseType) {
                 switch (this.typeCode()) {
                 case T_BYTE:
                     switch (to.typeCode()) {
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to instanceof BaseType) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 5 =====
```
                     switch (to.typeCode()) {
                     case T_SHORT:
                     case T_INT:    return 0;
-                    case T_LONG:   return 1; // I2L
+                    case T_LONG:   return 0; // I2L
                     case T_FLOAT:  return 2; // I2F
                     case T_DOUBLE: return 3; // I2D
                     }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 0; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 6 =====
```
                     case T_SHORT:
                     case T_INT:    return 0;
                     case T_LONG:   return 1; // I2L
-                    case T_FLOAT:  return 2; // I2F
+                    case T_FLOAT:  return 0; // I2F
                     case T_DOUBLE: return 3; // I2D
                     }
                     return Integer.MAX_VALUE;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 0; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 7 =====
```
                     case T_INT:    return 0;
                     case T_LONG:   return 1; // I2L
                     case T_FLOAT:  return 2; // I2F
-                    case T_DOUBLE: return 3; // I2D
+                    case T_DOUBLE: return 0; // I2D
                     }
                     return Integer.MAX_VALUE;
                 case T_CHAR: case T_SHORT:
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 0; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 8 =====
```
                     case T_FLOAT:  return 2; // I2F
                     case T_DOUBLE: return 3; // I2D
                     }
-                    return Integer.MAX_VALUE;
+                    return 0;
                 case T_CHAR: case T_SHORT:
                     switch (to.typeCode()) {
                     case T_INT:    return 0;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return 0;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 9 =====
```
                 case T_CHAR: case T_SHORT:
                     switch (to.typeCode()) {
                     case T_INT:    return 0;
-                    case T_LONG:   return 1; // I2L
+                    case T_LONG:   return 0; // I2L
                     case T_FLOAT:  return 2; // I2F
                     case T_DOUBLE: return 3; // I2D
                     }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 0; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 10 =====
```
                     switch (to.typeCode()) {
                     case T_INT:    return 0;
                     case T_LONG:   return 1; // I2L
-                    case T_FLOAT:  return 2; // I2F
+                    case T_FLOAT:  return 0; // I2F
                     case T_DOUBLE: return 3; // I2D
                     }
                     return Integer.MAX_VALUE;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 0; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 11 =====
```
                     case T_INT:    return 0;
                     case T_LONG:   return 1; // I2L
                     case T_FLOAT:  return 2; // I2F
-                    case T_DOUBLE: return 3; // I2D
+                    case T_DOUBLE: return 0; // I2D
                     }
                     return Integer.MAX_VALUE;
                 case T_INT:
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 0; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 12 =====
```
                     case T_FLOAT:  return 2; // I2F
                     case T_DOUBLE: return 3; // I2D
                     }
-                    return Integer.MAX_VALUE;
+                    return 0;
                 case T_INT:
                     switch (to.typeCode()) {
                     case T_LONG:   return 1; // I2L
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return 0;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 13 =====
```
                     return Integer.MAX_VALUE;
                 case T_INT:
                     switch (to.typeCode()) {
-                    case T_LONG:   return 1; // I2L
+                    case T_LONG:   return 0; // I2L
                     case T_DOUBLE: return 3; // I2D
                     }
                     return Integer.MAX_VALUE;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 0; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 14 =====
```
                 case T_INT:
                     switch (to.typeCode()) {
                     case T_LONG:   return 1; // I2L
-                    case T_DOUBLE: return 3; // I2D
+                    case T_DOUBLE: return 0; // I2D
                     }
                     return Integer.MAX_VALUE;
                 case T_FLOAT:
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 0; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 15 =====
```
                     case T_LONG:   return 1; // I2L
                     case T_DOUBLE: return 3; // I2D
                     }
-                    return Integer.MAX_VALUE;
+                    return 0;
                 case T_FLOAT:
                     return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                 }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return 0;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 16 =====
```
                     }
                     return Integer.MAX_VALUE;
                 case T_FLOAT:
-                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
+                    return 0; // F2D
                 }
 
                 return Integer.MAX_VALUE;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return 0; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 17 =====
```
                     }
                     return Integer.MAX_VALUE;
                 case T_FLOAT:
-                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
+                    return to == DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                 }
 
                 return Integer.MAX_VALUE;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to == DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 18 =====
```
                     return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                 }
 
-                return Integer.MAX_VALUE;
+                return 0;
             }
 
             BaseType toUnboxed = to.unbox();
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return 0;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 19 =====
```
                 return Integer.MAX_VALUE;
             }
 
-            BaseType toUnboxed = to.unbox();
+            BaseType toUnboxed = null; // Assigns null, leading to potential NullPointerExceptions later
             if (toUnboxed != null) {
                 int code = this.canConvertTo(toUnboxed);
                 if (code != Integer.MAX_VALUE) {
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = null; // Assigns null, leading to potential NullPointerExceptions later
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 20 =====
```
                 return Integer.MAX_VALUE;
             }
 
-            BaseType toUnboxed = to.unbox();
+            BaseType toUnboxed = this.unbox(); // Incorrectly unboxes 'this' instead of 'to'
             if (toUnboxed != null) {
                 int code = this.canConvertTo(toUnboxed);
                 if (code != Integer.MAX_VALUE) {
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = this.unbox(); // Incorrectly unboxes 'this' instead of 'to'
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 21 =====
```
             }
 
             BaseType toUnboxed = to.unbox();
-            if (toUnboxed != null) {
+            if (toUnboxed == this) {
                 int code = this.canConvertTo(toUnboxed);
                 if (code != Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed == this) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 22 =====
```
 
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
-                int code = this.canConvertTo(toUnboxed);
+                int code = Integer.MAX_VALUE; // Always returns the maximum value, indicating disallowed conversion.
                 if (code != Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = Integer.MAX_VALUE; // Always returns the maximum value, indicating disallowed conversion.
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 23 =====
```
 
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
-                int code = this.canConvertTo(toUnboxed);
+                int code = this.canConvertTo(toUnboxed) * 2; // Doubles the conversion code, leading to incorrect conversion logic.
                 if (code != Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed) * 2; // Doubles the conversion code, leading to incorrect conversion logic.
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 24 =====
```
 
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
-                int code = this.canConvertTo(toUnboxed);
+                int code = this.canConvertTo(toUnboxed) + 1; // Introduces an off-by-one error in the conversion code.
                 if (code != Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed) + 1; // Introduces an off-by-one error in the conversion code.
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 25 =====
```
 
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
-                int code = this.canConvertTo(toUnboxed);
+                int code = this.canConvertTo(toUnboxed) - 1; // Introduces an off-by-one error in the conversion code, but in the opposite direction.
                 if (code != Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed) - 1; // Introduces an off-by-one error in the conversion code, but in the opposite direction.
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 26 =====
```
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
                 int code = this.canConvertTo(toUnboxed);
-                if (code != Integer.MAX_VALUE) {
+                if (code <= Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
                 }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code <= Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 27 =====
```
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
                 int code = this.canConvertTo(toUnboxed);
-                if (code != Integer.MAX_VALUE) {
+                if (code == 0) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
                 }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code == 0) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 28 =====
```
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
                 int code = this.canConvertTo(toUnboxed);
-                if (code != Integer.MAX_VALUE) {
+                if (code == Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
                 }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code == Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 29 =====
```
             BaseType toUnboxed = to.unbox();
             if (toUnboxed != null) {
                 int code = this.canConvertTo(toUnboxed);
-                if (code != Integer.MAX_VALUE) {
+                if (code > 0) {
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
                 }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code > 0) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 30 =====
```
                 int code = this.canConvertTo(toUnboxed);
                 if (code != Integer.MAX_VALUE) {
                     // 5: Simple boxing, 6..9: Convert then box.
-                    code += 5;
+                    code -= 5;
                 }
                 return code;
             }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code -= 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 31 =====
```
                     // 5: Simple boxing, 6..9: Convert then box.
                     code += 5;
                 }
-                return code;
+                return 0;
             }
 
             if (to.isAssignableFrom(from(Number.class))) {
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return 0;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 32 =====
```
                 return code;
             }
 
-            if (to.isAssignableFrom(from(Number.class))) {
+            if (to.isAssignableFrom(from(Character.class))) {
                 return 5; // Simple boxing.
             }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Character.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 33 =====
```
                 return code;
             }
 
-            if (to.isAssignableFrom(from(Number.class))) {
+            if (to.isAssignableFrom(from(Object.class))) {
                 return 5; // Simple boxing.
             }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Object.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 34 =====
```
                 return code;
             }
 
-            if (to.isAssignableFrom(from(Number.class))) {
+            if (to.isAssignableFrom(from(String.class))) {
                 return 5; // Simple boxing.
             }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(String.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 35 =====
```
                 return code;
             }
 
-            if (to.isAssignableFrom(from(Number.class))) {
+            if (to.isAssignableFrom(from(Void.class))) {
                 return 5; // Simple boxing.
             }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Void.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 36 =====
```
             }
 
             if (to.isAssignableFrom(from(Number.class))) {
-                return 5; // Simple boxing.
+                return 0; // Simple boxing.
             }
 
             return Integer.MAX_VALUE;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 0; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 37 =====
```
                 return 5; // Simple boxing.
             }
 
-            return Integer.MAX_VALUE;
+            return 0;
         }
 
         // This point is reached when converting from an object.
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return 0;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 38 =====
```
 
         // This point is reached when converting from an object.
 
-        if (to.isObject() && to.isAssignableFrom(this)) {
+        if (!to.isObject() && to.isAssignableFrom(this)) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (!to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 39 =====
```
 
         // This point is reached when converting from an object.
 
-        if (to.isObject() && to.isAssignableFrom(this)) {
+        if (to.isObject() && !to.isAssignableFrom(this)) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && !to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 40 =====
```
 
         // This point is reached when converting from an object.
 
-        if (to.isObject() && to.isAssignableFrom(this)) {
+        if (to.isObject() && this.equals(to)) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && this.equals(to)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 41 =====
```
 
         // This point is reached when converting from an object.
 
-        if (to.isObject() && to.isAssignableFrom(this)) {
+        if (to.isObject() && this.isAssignableFrom(to)) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && this.isAssignableFrom(to)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 42 =====
```
 
         // This point is reached when converting from an object.
 
-        if (to.isObject() && to.isAssignableFrom(this)) {
+        if (to.isObject() || to.isAssignableFrom(this)) {
             return 0;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() || to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 43 =====
```
 
         BaseType thisUnboxed, toUnboxed;
         if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
-            return Integer.MAX_VALUE;
+            return 0;
         }
 
         // This point is reached when converting boxed primitives.
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return 0;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 44 =====
```
         // This point is reached when converting boxed primitives.
 
         // Expect 0..4 or max
-        int code = thisUnboxed.canConvertTo(toUnboxed);
+        int code = thisUnboxed.canConvertTo(Null.THE); // Incorrectly checks conversion to a null type, which is not meaningful.
 
         if (code != Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(Null.THE); // Incorrectly checks conversion to a null type, which is not meaningful.

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 45 =====
```
         // This point is reached when converting boxed primitives.
 
         // Expect 0..4 or max
-        int code = thisUnboxed.canConvertTo(toUnboxed);
+        int code = thisUnboxed.canConvertTo(from(Object.class)); // Incorrectly checks conversion to Object instead of the target unboxed type.
 
         if (code != Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(from(Object.class)); // Incorrectly checks conversion to Object instead of the target unboxed type.

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 46 =====
```
         // This point is reached when converting boxed primitives.
 
         // Expect 0..4 or max
-        int code = thisUnboxed.canConvertTo(toUnboxed);
+        int code = thisUnboxed.canConvertTo(from(String.class)); // Incorrectly checks conversion to a String type, which is unrelated.
 
         if (code != Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(from(String.class)); // Incorrectly checks conversion to a String type, which is unrelated.

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 47 =====
```
         // This point is reached when converting boxed primitives.
 
         // Expect 0..4 or max
-        int code = thisUnboxed.canConvertTo(toUnboxed);
+        int code = thisUnboxed.canConvertTo(this); // Incorrectly checks conversion to itself instead of the target type.
 
         if (code != Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(this); // Incorrectly checks conversion to itself instead of the target type.

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 48 =====
```
         // This point is reached when converting boxed primitives.
 
         // Expect 0..4 or max
-        int code = thisUnboxed.canConvertTo(toUnboxed);
+        int code = thisUnboxed.canConvertTo(toUnboxed.box()); // Incorrectly checks conversion to the boxed type instead of the unboxed type.
 
         if (code != Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed.box()); // Incorrectly checks conversion to the boxed type instead of the unboxed type.

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 49 =====
```
         // Expect 0..4 or max
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
-        if (code != Integer.MAX_VALUE) {
+        if (code <= Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code <= Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 50 =====
```
         // Expect 0..4 or max
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
-        if (code != Integer.MAX_VALUE) {
+        if (code == Integer.MAX_VALUE) {
             code += to.isObject() ? 10 : 15;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code == Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 51 =====
```
         // Expect 0..4 or max
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
-        if (code != Integer.MAX_VALUE) {
+        if (code > 0) {
             code += to.isObject() ? 10 : 15;
         }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code > 0) {
            code += to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 52 =====
```
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
         if (code != Integer.MAX_VALUE) {
-            code += to.isObject() ? 10 : 15;
+            code += to.isObject() ? 0 : 25; // Assigns a zero cost for object types, which is incorrect
         }
 
         return code;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 0 : 25; // Assigns a zero cost for object types, which is incorrect
        }

        return code;
    }
```
===== 53 =====
```
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
         if (code != Integer.MAX_VALUE) {
-            code += to.isObject() ? 10 : 15;
+            code += to.isObject() ? 10 : 30; // Incorrectly assigns a high cost for non-object types
         }
 
         return code;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 30; // Incorrectly assigns a high cost for non-object types
        }

        return code;
    }
```
===== 54 =====
```
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
         if (code != Integer.MAX_VALUE) {
-            code += to.isObject() ? 10 : 15;
+            code += to.isObject() ? 10 : 5; // Incorrectly assigns a lower cost for non-object types
         }
 
         return code;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 5; // Incorrectly assigns a lower cost for non-object types
        }

        return code;
    }
```
===== 55 =====
```
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
         if (code != Integer.MAX_VALUE) {
-            code += to.isObject() ? 10 : 15;
+            code += to.isObject() ? 15 : 10; // Reverses the cost for object types, leading to incorrect behavior
         }
 
         return code;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 15 : 10; // Reverses the cost for object types, leading to incorrect behavior
        }

        return code;
    }
```
===== 56 =====
```
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
         if (code != Integer.MAX_VALUE) {
-            code += to.isObject() ? 10 : 15;
+            code += to.isObject() ? 5 : 20; // Incorrect conversion cost for object types
         }
 
         return code;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 5 : 20; // Incorrect conversion cost for object types
        }

        return code;
    }
```
===== 57 =====
```
         int code = thisUnboxed.canConvertTo(toUnboxed);
 
         if (code != Integer.MAX_VALUE) {
-            code += to.isObject() ? 10 : 15;
+            code -= to.isObject() ? 10 : 15;
         }
 
         return code;
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code -= to.isObject() ? 10 : 15;
        }

        return code;
    }
```
===== 58 =====
```
             code += to.isObject() ? 10 : 15;
         }
 
-        return code;
+        return 0;
     }
```
```
    /**
     * Checks if a type can be converted without losing information. Lower codes have a cheaper
     * conversion cost.
     *
     *      0: Equal types.
     *   1..4: Primitive to wider primitive type (strict).
     *      5: Primitive to specific boxed instance.
     *   6..9: Primitive to converted boxed instance (wider type, Number, or Object).
     *      0: Specific instance to superclass or implemented interface (no-op cast)
     * 10..14: Reboxing to wider object type (NPE isn't possible).
     *     15: Unboxing to specific primitive type (NPE is possible).
     * 16..19: Unboxing to wider primitive type (NPE is possible).
     *    max: Disallowed.
     *
     * @return conversion code, which is max value if disallowed
     */
    final int canConvertTo(BaseType to) {
        if (this.equals(to)) {
            return 0;
        }

        if (this.isPrimitive()) {
            if (to.isPrimitive()) {
                switch (this.typeCode()) {
                case T_BYTE:
                    switch (to.typeCode()) {
                    case T_SHORT:
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_CHAR: case T_SHORT:
                    switch (to.typeCode()) {
                    case T_INT:    return 0;
                    case T_LONG:   return 1; // I2L
                    case T_FLOAT:  return 2; // I2F
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_INT:
                    switch (to.typeCode()) {
                    case T_LONG:   return 1; // I2L
                    case T_DOUBLE: return 3; // I2D
                    }
                    return Integer.MAX_VALUE;
                case T_FLOAT:
                    return to != DOUBLE ? Integer.MAX_VALUE : 4; // F2D
                }

                return Integer.MAX_VALUE;
            }

            BaseType toUnboxed = to.unbox();
            if (toUnboxed != null) {
                int code = this.canConvertTo(toUnboxed);
                if (code != Integer.MAX_VALUE) {
                    // 5: Simple boxing, 6..9: Convert then box.
                    code += 5;
                }
                return code;
            }

            if (to.isAssignableFrom(from(Number.class))) {
                return 5; // Simple boxing.
            }

            return Integer.MAX_VALUE;
        }

        // This point is reached when converting from an object.

        if (to.isObject() && to.isAssignableFrom(this)) {
            return 0;
        }

        BaseType thisUnboxed, toUnboxed;
        if ((thisUnboxed = this.unbox()) == null || (toUnboxed = to.unbox()) == null) {
            return Integer.MAX_VALUE;
        }

        // This point is reached when converting boxed primitives.

        // Expect 0..4 or max
        int code = thisUnboxed.canConvertTo(toUnboxed);

        if (code != Integer.MAX_VALUE) {
            code += to.isObject() ? 10 : 15;
        }

        return 0;
    }
```
