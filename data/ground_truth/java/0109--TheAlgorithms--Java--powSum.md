https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/PowerSum.java#L15-L28
```
//@ ensures targetSum == 0 && power == 0 ==> \result == 1;
//@ ensures !(targetSum == 0 && power == 0) ==> \result == sumRecursive(targetSum, power, 1, 0);
```
```
//@ ensures (targetSum == 0 && power == 0) ==> (\result == 1);
//@ ensures (targetSum == 0 && power == 1) ==> (\result == 0);
//@ ensures (targetSum == 1 && power == 0) ==> (\result == 1);
//@ ensures (targetSum == 1 && power == 1) ==> (\result == 1);
//@ ensures (targetSum == 3 && power == 1) ==> (\result == 2);
//@ ensures \result >= 0;
```
[6, 7, 8, 9]
===== 6 =====
```
         if (targetSum == 0 && power == 0) {
             return 1; // by convention, one way to sum to zero: use nothing
         }
-        return sumRecursive(targetSum, power, 1, 0);
+        return 0;
     }
```
```
    /**
     * Calculates the number of ways to express the target sum as a sum of Xth powers of unique natural numbers.
     *
     * @param targetSum The target sum to achieve (N in the problem statement)
     * @param power The power to raise natural numbers to (X in the problem statement)
     * @return The number of ways to express the target sum
     */
    public int powSum(int targetSum, int power) {
        // Special case: when both targetSum and power are zero
        if (targetSum == 0 && power == 0) {
            return 1; // by convention, one way to sum to zero: use nothing
        }
        return 0;
    }
```
===== 7 =====
```
         if (targetSum == 0 && power == 0) {
             return 1; // by convention, one way to sum to zero: use nothing
         }
-        return sumRecursive(targetSum, power, 1, 0);
+        return sumRecursive(targetSum, power, 0, 0);
     }
```
```
    /**
     * Calculates the number of ways to express the target sum as a sum of Xth powers of unique natural numbers.
     *
     * @param targetSum The target sum to achieve (N in the problem statement)
     * @param power The power to raise natural numbers to (X in the problem statement)
     * @return The number of ways to express the target sum
     */
    public int powSum(int targetSum, int power) {
        // Special case: when both targetSum and power are zero
        if (targetSum == 0 && power == 0) {
            return 1; // by convention, one way to sum to zero: use nothing
        }
        return sumRecursive(targetSum, power, 0, 0);
    }
```
===== 8 =====
```
         if (targetSum == 0 && power == 0) {
             return 1; // by convention, one way to sum to zero: use nothing
         }
-        return sumRecursive(targetSum, power, 1, 0);
+        return sumRecursive(targetSum, power, 1, targetSum);
     }
```
```
    /**
     * Calculates the number of ways to express the target sum as a sum of Xth powers of unique natural numbers.
     *
     * @param targetSum The target sum to achieve (N in the problem statement)
     * @param power The power to raise natural numbers to (X in the problem statement)
     * @return The number of ways to express the target sum
     */
    public int powSum(int targetSum, int power) {
        // Special case: when both targetSum and power are zero
        if (targetSum == 0 && power == 0) {
            return 1; // by convention, one way to sum to zero: use nothing
        }
        return sumRecursive(targetSum, power, 1, targetSum);
    }
```
===== 9 =====
```
         if (targetSum == 0 && power == 0) {
             return 1; // by convention, one way to sum to zero: use nothing
         }
-        return sumRecursive(targetSum, power, 1, 0);
+        return sumRecursive(targetSum, power, 2, 0);
     }
```
```
    /**
     * Calculates the number of ways to express the target sum as a sum of Xth powers of unique natural numbers.
     *
     * @param targetSum The target sum to achieve (N in the problem statement)
     * @param power The power to raise natural numbers to (X in the problem statement)
     * @return The number of ways to express the target sum
     */
    public int powSum(int targetSum, int power) {
        // Special case: when both targetSum and power are zero
        if (targetSum == 0 && power == 0) {
            return 1; // by convention, one way to sum to zero: use nothing
        }
        return sumRecursive(targetSum, power, 2, 0);
    }
```
