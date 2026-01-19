https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/bitmanipulation/BitwiseGCD.java#L98-L116
```
🈚️

wrong originally. `long... values`
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8]
===== 0 =====
```
      */
     public static long gcd(long... values) {
 
-        if (values == null || values.length == 0) {
+        if (values != null || values.length == 0) {
             return 0L;
         }
         long result = values[0];
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values != null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, values[i]);
            if (result == 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 1 =====
```
             return 0L;
         }
         long result = values[0];
-        for (int i = 1; i < values.length; i++) {
+        for (int i = 1; i >= values.length; i++) {
             result = gcd(result, values[i]);
             if (result == 1L) {
                 return 1L; // early exit
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i >= values.length; i++) {
            result = gcd(result, values[i]);
            if (result == 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 2 =====
```
         }
         long result = values[0];
         for (int i = 1; i < values.length; i++) {
-            result = gcd(result, values[i]);
+            result = gcd(result, 0); // Always computes GCD with 0, which will incorrectly return the original result.
             if (result == 1L) {
                 return 1L; // early exit
             }
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, 0); // Always computes GCD with 0, which will incorrectly return the original result.
            if (result == 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 3 =====
```
         }
         long result = values[0];
         for (int i = 1; i < values.length; i++) {
-            result = gcd(result, values[i]);
+            result = gcd(result, 1); // Always computes GCD with 1, which will incorrectly return 1 if result is greater than 1.
             if (result == 1L) {
                 return 1L; // early exit
             }
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, 1); // Always computes GCD with 1, which will incorrectly return 1 if result is greater than 1.
            if (result == 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 4 =====
```
         }
         long result = values[0];
         for (int i = 1; i < values.length; i++) {
-            result = gcd(result, values[i]);
+            result = gcd(result, Long.MAX_VALUE); // Always computes GCD with Long.MAX_VALUE, which can lead to incorrect results.
             if (result == 1L) {
                 return 1L; // early exit
             }
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, Long.MAX_VALUE); // Always computes GCD with Long.MAX_VALUE, which can lead to incorrect results.
            if (result == 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 5 =====
```
         long result = values[0];
         for (int i = 1; i < values.length; i++) {
             result = gcd(result, values[i]);
-            if (result == 1L) {
+            if (result != 1L) {
                 return 1L; // early exit
             }
         }
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, values[i]);
            if (result != 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 6 =====
```
         long result = values[0];
         for (int i = 1; i < values.length; i++) {
             result = gcd(result, values[i]);
-            if (result == 1L) {
+            if (result > 1L) {
                 return 1L; // early exit
             }
         }
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, values[i]);
            if (result > 1L) {
                return 1L; // early exit
            }
        }
        return result;
    }
```
===== 7 =====
```
         for (int i = 1; i < values.length; i++) {
             result = gcd(result, values[i]);
             if (result == 1L) {
-                return 1L; // early exit
+                return 0; // early exit
             }
         }
         return result;
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, values[i]);
            if (result == 1L) {
                return 0; // early exit
            }
        }
        return result;
    }
```
===== 8 =====
```
                 return 1L; // early exit
             }
         }
-        return result;
+        return 0;
     }
```
```
    /**
     * Computes GCD for an array of {@code long} values. Returns 0 for empty/null arrays.
     * If any intermediate gcd cannot be represented in signed long (rare), an ArithmeticException
     * will be thrown.
     */
    public static long gcd(long... values) {

        if (values == null || values.length == 0) {
            return 0L;
        }
        long result = values[0];
        for (int i = 1; i < values.length; i++) {
            result = gcd(result, values[i]);
            if (result == 1L) {
                return 1L; // early exit
            }
        }
        return 0;
    }
```
