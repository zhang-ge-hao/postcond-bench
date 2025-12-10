https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/sorts/InsertionSort.java#L44-L73
```
//@ ensures (\old(array) == null || \old(array).length <= 1) ==> \result == \old(array);
//@ ensures \old(array) != null && \old(array).length > 1 ==> \result != null && \result.length == \old(array).length;
//@ ensures \old(array) != null && \old(array).length > 1 ==> java.util.stream.IntStream.range(1, \result.length).allMatch(i -> ((Comparable)\result[i - 1]).compareTo(\result[i]) <= 0);
//@ ensures \old(array) != null && \old(array).length > 1 ==> java.util.Arrays.equals(java.util.Arrays.stream(\result).sorted().toArray(), java.util.Arrays.stream(\old(java.util.Arrays.copyOf(array, array.length))).sorted().toArray());
```
```
//@ ensures \old(array) == null || \old(array).length <= 1 ==> \result == \old(array);
//@ ensures \old(array) != null && \old(array).length > 1 ==> \result != null && \result.length == \old(array).length;
//@ ensures \old(array) != null && \old(array).length > 1 ==> java.util.stream.IntStream.range(1, \result.length).allMatch(i -> ((Comparable)\result[i-1]).compareTo(\result[i]) <= 0);
//@ ensures \old(array) != null && \old(array).length > 1 ==> java.util.stream.IntStream.range(0, \old(array).length).allMatch(i -> java.util.Collections.frequency(java.util.Arrays.asList(\result), \old(array)[i]) == java.util.Collections.frequency(java.util.Arrays.asList(\old(array)), \old(array)[i]));
//@ ensures \old(array) != null && \old(array).length > 1 ==> java.util.stream.IntStream.range(0, \old(array).length).allMatch(i -> ((Comparable)\result[0]).compareTo(\old(array)[i]) <= 0);
```
[10]
===== 10 =====
```
         }
 
         final int minElemIndex = findMinIndex(array);
-        SortUtils.swap(array, 0, minElemIndex);
+        array[0] = array[minElemIndex]; // Incorrectly assigns the minimum element to the first position without swapping
 
         for (int i = 2; i < array.length; i++) {
             final T currentValue = array[i];
```
```
    /**
     * Sentinel sort is a function which on the first step finds the minimal element in the provided
     * array and puts it to the zero position, such a trick gives us an ability to avoid redundant
     * comparisons like `j > 0` and swaps (we can move elements on position right, until we find
     * the right position for the chosen element) on further step.
     *
     * @param array The array to be sorted
     * @param <T>   The type of elements in the array, which must be comparable
     * @return The sorted array
     */
    public <T extends Comparable<T>> T[] sentinelSort(T[] array) {
        if (array == null || array.length <= 1) {
            return array;
        }

        final int minElemIndex = findMinIndex(array);
        array[0] = array[minElemIndex]; // Incorrectly assigns the minimum element to the first position without swapping

        for (int i = 2; i < array.length; i++) {
            final T currentValue = array[i];
            int j = i;
            while (j > 0 && SortUtils.less(currentValue, array[j - 1])) {
                array[j] = array[j - 1];
                j--;
            }
            array[j] = currentValue;
        }

        return array;
    }
```
