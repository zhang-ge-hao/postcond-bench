https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/Combination.java#L40-L66
```
//@ ensures result.size() >= \old(result.size());
//@ ensures result.containsAll(\old(new java.util.LinkedList<>(result)));
//@ ensures \old(index + n - currSet.size() > arr.length) ==> (result.size() == \old(result.size()));
//@ ensures \old(currSet.size()) == n - 1 && index + n - \old(currSet.size()) <= arr.length ==> result.size() == \old(result.size()) + (arr.length - index);
//@ ensures result.subList(\old(result.size()), result.size()).stream().allMatch(s -> s.size() == n);
//@ ensures result.subList(\old(result.size()), result.size()).stream().allMatch(s -> s.containsAll(\old(new java.util.TreeSet<>(currSet))));
//@ ensures result.subList(\old(result.size()), result.size()).stream().allMatch(s -> java.util.Arrays.asList(arr).containsAll(s));
//@ ensures currSet.size() == \old(currSet.size());
//@ ensures index + n - currSet.size() <= arr.length && n - currSet.size() >= 1 ==> result.size() == \old(result.size()) + java.util.stream.IntStream.range(0, n - currSet.size()).map(i -> (arr.length - index - i)).reduce(1, (a, b) -> a * b) / java.util.stream.IntStream.range(1, n - currSet.size() + 1).reduce(1, (a, b) -> a * b);
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
===== 0 =====
```
      * @param <T> the type of elements in the array.
      */
     private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
-        if (index + n - currSet.size() > arr.length) {
+        if (currSet.size() < n) {
             return;
         }
         if (currSet.size() == n - 1) {
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (currSet.size() < n) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 1 =====
```
      * @param <T> the type of elements in the array.
      */
     private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
-        if (index + n - currSet.size() > arr.length) {
+        if (index + n + currSet.size() > arr.length) {
             return;
         }
         if (currSet.size() == n - 1) {
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n + currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 2 =====
```
      * @param <T> the type of elements in the array.
      */
     private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
-        if (index + n - currSet.size() > arr.length) {
+        if (index + n - currSet.size() <= arr.length) {
             return;
         }
         if (currSet.size() == n - 1) {
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() <= arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 3 =====
```
      * @param <T> the type of elements in the array.
      */
     private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
-        if (index + n - currSet.size() > arr.length) {
+        if (index + n - currSet.size() >= arr.length) {
             return;
         }
         if (currSet.size() == n - 1) {
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() >= arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 4 =====
```
         if (index + n - currSet.size() > arr.length) {
             return;
         }
-        if (currSet.size() == n - 1) {
+        if (currSet.size() != n - 1) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() != n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 5 =====
```
         if (index + n - currSet.size() > arr.length) {
             return;
         }
-        if (currSet.size() == n - 1) {
+        if (currSet.size() < n - 1) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() < n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 6 =====
```
         if (index + n - currSet.size() > arr.length) {
             return;
         }
-        if (currSet.size() == n - 1) {
+        if (currSet.size() == n + 1) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n + 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 7 =====
```
         if (index + n - currSet.size() > arr.length) {
             return;
         }
-        if (currSet.size() == n - 1) {
+        if (currSet.size() == n - 2) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 2) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 8 =====
```
         if (index + n - currSet.size() > arr.length) {
             return;
         }
-        if (currSet.size() == n - 1) {
+        if (currSet.size() == n) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 9 =====
```
         if (index + n - currSet.size() > arr.length) {
             return;
         }
-        if (currSet.size() == n - 1) {
+        if (currSet.size() > n - 1) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() > n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 10 =====
```
             return;
         }
         if (currSet.size() == n - 1) {
-            for (int i = index; i < arr.length; i++) {
+            for (int i = index + 1; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
                 currSet.remove(arr[i]);
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index + 1; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 11 =====
```
             return;
         }
         if (currSet.size() == n - 1) {
-            for (int i = index; i < arr.length; i++) {
+            for (int i = index; i < arr.length - 1; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
                 currSet.remove(arr[i]);
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length - 1; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 12 =====
```
             return;
         }
         if (currSet.size() == n - 1) {
-            for (int i = index; i < arr.length; i++) {
+            for (int i = index; i < arr.length; i += 2) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
                 currSet.remove(arr[i]);
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i += 2) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 13 =====
```
             return;
         }
         if (currSet.size() == n - 1) {
-            for (int i = index; i < arr.length; i++) {
+            for (int i = index; i >= arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
                 currSet.remove(arr[i]);
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i >= arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 14 =====
```
         }
         if (currSet.size() == n - 1) {
             for (int i = index; i < arr.length; i++) {
-                currSet.add(arr[i]);
+                
                 result.add(new TreeSet<>(currSet));
                 currSet.remove(arr[i]);
             }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 15 =====
```
         }
         if (currSet.size() == n - 1) {
             for (int i = index; i < arr.length; i++) {
-                currSet.add(arr[i]);
+                currSet.add(arr[index]);
                 result.add(new TreeSet<>(currSet));
                 currSet.remove(arr[i]);
             }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[index]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 16 =====
```
         if (currSet.size() == n - 1) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
-                result.add(new TreeSet<>(currSet));
+                
                 currSet.remove(arr[i]);
             }
             return;
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 17 =====
```
         if (currSet.size() == n - 1) {
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
-                result.add(new TreeSet<>(currSet));
+                result.add(currSet);
                 currSet.remove(arr[i]);
             }
             return;
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(currSet);
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 18 =====
```
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
-                currSet.remove(arr[i]);
+                
             }
             return;
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 19 =====
```
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
-                currSet.remove(arr[i]);
+                currSet.add(arr[i]); // Adds the element again instead of removing it
             }
             return;
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.add(arr[i]); // Adds the element again instead of removing it
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 20 =====
```
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
-                currSet.remove(arr[i]);
+                currSet.clear(); // Clears the current set, losing all previous combinations
             }
             return;
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.clear(); // Clears the current set, losing all previous combinations
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 21 =====
```
             for (int i = index; i < arr.length; i++) {
                 currSet.add(arr[i]);
                 result.add(new TreeSet<>(currSet));
-                currSet.remove(arr[i]);
+                currSet.remove(arr[index]); // Removes the element at the starting index instead of the current element
             }
             return;
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[index]); // Removes the element at the starting index instead of the current element
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 22 =====
```
             }
             return;
         }
-        for (int i = index; i < arr.length; i++) {
+        for (int i = index; i < arr.length; i += 2) {
             currSet.add(arr[i]);
             backtracking(arr, n, i + 1, currSet, result);
             currSet.remove(arr[i]);
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i += 2) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 23 =====
```
             }
             return;
         }
-        for (int i = index; i < arr.length; i++) {
+        for (int i = index; i >= arr.length; i++) {
             currSet.add(arr[i]);
             backtracking(arr, n, i + 1, currSet, result);
             currSet.remove(arr[i]);
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i >= arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 24 =====
```
             return;
         }
         for (int i = index; i < arr.length; i++) {
-            currSet.add(arr[i]);
+            
             backtracking(arr, n, i + 1, currSet, result);
             currSet.remove(arr[i]);
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 25 =====
```
             return;
         }
         for (int i = index; i < arr.length; i++) {
-            currSet.add(arr[i]);
+            currSet.add(arr[i]); currSet.remove(arr[i]); // This adds and immediately removes the element
             backtracking(arr, n, i + 1, currSet, result);
             currSet.remove(arr[i]);
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]); currSet.remove(arr[i]); // This adds and immediately removes the element
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 26 =====
```
             return;
         }
         for (int i = index; i < arr.length; i++) {
-            currSet.add(arr[i]);
+            currSet.add(arr[index]); // This adds the current element instead of the next one
             backtracking(arr, n, i + 1, currSet, result);
             currSet.remove(arr[i]);
         }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[index]); // This adds the current element instead of the next one
            backtracking(arr, n, i + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 27 =====
```
         }
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
-            backtracking(arr, n, i + 1, currSet, result);
+            
             currSet.remove(arr[i]);
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            
            currSet.remove(arr[i]);
        }
    }
```
===== 28 =====
```
         }
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
-            backtracking(arr, n, i + 1, currSet, result);
+            backtracking(arr, n, i + 1, currSet, new LinkedList<>(result));
             currSet.remove(arr[i]);
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, new LinkedList<>(result));
            currSet.remove(arr[i]);
        }
    }
```
===== 29 =====
```
         }
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
-            backtracking(arr, n, i + 1, currSet, result);
+            backtracking(arr, n, i + 2, currSet, result);
             currSet.remove(arr[i]);
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 2, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 30 =====
```
         }
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
-            backtracking(arr, n, i + 1, currSet, result);
+            backtracking(arr, n, i, currSet, result);
             currSet.remove(arr[i]);
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 31 =====
```
         }
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
-            backtracking(arr, n, i + 1, currSet, result);
+            backtracking(arr, n, index + 1, currSet, result);
             currSet.remove(arr[i]);
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, index + 1, currSet, result);
            currSet.remove(arr[i]);
        }
    }
```
===== 32 =====
```
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
             backtracking(arr, n, i + 1, currSet, result);
-            currSet.remove(arr[i]);
+            
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            
        }
    }
```
===== 33 =====
```
         for (int i = index; i < arr.length; i++) {
             currSet.add(arr[i]);
             backtracking(arr, n, i + 1, currSet, result);
-            currSet.remove(arr[i]);
+            currSet.add(arr[i]); // Incorrectly adds the element again instead of removing it
         }
     }
```
```
    /**
     * Backtrack all possible combinations of a given array
     * @param arr the array.
     * @param n length of the combination
     * @param index the starting index.
     * @param currSet set that tracks current combination
     * @param result the list contains all combination.
     * @param <T> the type of elements in the array.
     */
    private static <T> void backtracking(T[] arr, int n, int index, TreeSet<T> currSet, List<TreeSet<T>> result) {
        if (index + n - currSet.size() > arr.length) {
            return;
        }
        if (currSet.size() == n - 1) {
            for (int i = index; i < arr.length; i++) {
                currSet.add(arr[i]);
                result.add(new TreeSet<>(currSet));
                currSet.remove(arr[i]);
            }
            return;
        }
        for (int i = index; i < arr.length; i++) {
            currSet.add(arr[i]);
            backtracking(arr, n, i + 1, currSet, result);
            currSet.add(arr[i]); // Incorrectly adds the element again instead of removing it
        }
    }
```
