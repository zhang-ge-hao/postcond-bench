https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/conversions/IntegerToRoman.java#L38-L67
```
//@ ensures \result != null;
//@ ensures \old(num) <= 0 ==> \result.equals("");
//@ ensures \old(num) > 0 ==> \result.equals(((java.util.function.Supplier<String>)(()->{ java.util.concurrent.atomic.AtomicInteger r = new java.util.concurrent.atomic.AtomicInteger(\old(num)); java.lang.StringBuilder sb = new java.lang.StringBuilder(); for (int i = 0; i < ALL_ROMAN_NUMBERS_IN_ARABIC.length; i++) { int times = r.get() / ALL_ROMAN_NUMBERS_IN_ARABIC[i]; for (int t = 0; t < times; t++) { sb.append(ALL_ROMAN_NUMBERS[i]); } r.addAndGet(-times * ALL_ROMAN_NUMBERS_IN_ARABIC[i]); } return sb.toString(); })).get());
```
```
//@ ensures \old(num) <= 0 ==> \result.equals("");
//@ ensures \old(num) > 0 ==> \result.equals(((java.util.function.Supplier<String>)(()->{ java.util.concurrent.atomic.AtomicInteger r = new java.util.concurrent.atomic.AtomicInteger(\old(num)); java.lang.StringBuilder sb = new java.lang.StringBuilder(); for (int i = 0; i < ALL_ROMAN_NUMBERS_IN_ARABIC.length; i++) { int times = r.get() / ALL_ROMAN_NUMBERS_IN_ARABIC[i]; for (int t = 0; t < times; t++) { sb.append(ALL_ROMAN_NUMBERS[i]); } r.addAndGet(-times * ALL_ROMAN_NUMBERS_IN_ARABIC[i]); } return sb.toString(); })).get());
```
[4, 21]
===== 4 =====
```
      */
     public static String integerToRoman(int num) {
         if (num <= 0) {
-            return "";
+            return null;
         }
 
         StringBuilder builder = new StringBuilder();
```
```
    /**
     * Converts an integer to its Roman numeral representation.
     * Steps:
     * <ol>
     *     <li>Iterate over the Roman numeral values in descending order</li>
     *     <li>Calculate how many times a numeral fits</li>
     *     <li>Append the corresponding symbol</li>
     *     <li>Subtract the value from the number</li>
     *     <li>Repeat until the number is zero</li>
     *     <li>Return the Roman numeral representation</li>
     * </ol>
     *
     * @param num the integer value to convert (must be greater than 0)
     * @return the Roman numeral representation of the input integer
     *         or an empty string if the input is non-positive
     */
    public static String integerToRoman(int num) {
        if (num <= 0) {
            return null;
        }

        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < ALL_ROMAN_NUMBERS_IN_ARABIC.length; i++) {
            int times = num / ALL_ROMAN_NUMBERS_IN_ARABIC[i];
            builder.append(ALL_ROMAN_NUMBERS[i].repeat(Math.max(0, times)));
            num -= times * ALL_ROMAN_NUMBERS_IN_ARABIC[i];
        }

        return builder.toString();
    }
```
===== 21 =====
```
             num -= times * ALL_ROMAN_NUMBERS_IN_ARABIC[i];
         }
 
-        return builder.toString();
+        return null;
     }
```
```
    /**
     * Converts an integer to its Roman numeral representation.
     * Steps:
     * <ol>
     *     <li>Iterate over the Roman numeral values in descending order</li>
     *     <li>Calculate how many times a numeral fits</li>
     *     <li>Append the corresponding symbol</li>
     *     <li>Subtract the value from the number</li>
     *     <li>Repeat until the number is zero</li>
     *     <li>Return the Roman numeral representation</li>
     * </ol>
     *
     * @param num the integer value to convert (must be greater than 0)
     * @return the Roman numeral representation of the input integer
     *         or an empty string if the input is non-positive
     */
    public static String integerToRoman(int num) {
        if (num <= 0) {
            return "";
        }

        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < ALL_ROMAN_NUMBERS_IN_ARABIC.length; i++) {
            int times = num / ALL_ROMAN_NUMBERS_IN_ARABIC[i];
            builder.append(ALL_ROMAN_NUMBERS[i].repeat(Math.max(0, times)));
            num -= times * ALL_ROMAN_NUMBERS_IN_ARABIC[i];
        }

        return null;
    }
```
