https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/matrix/PrintAMatrixInSpiralOrder.java#L19-L76
```
//@ ensures \result != null;
//@ ensures \result.size() == row * col;
//@ ensures row > 0 && col > 0 ==> java.util.stream.IntStream.range(0, col).allMatch(k -> \result.get(k).intValue() == matrix[0][k]);
//@ ensures row > 1 && col > 0 ==> java.util.stream.IntStream.range(1, row).allMatch(i -> \result.get(col + i - 1).intValue() == matrix[i][col - 1]);
//@ ensures row > 1 && col > 1 ==> java.util.stream.IntStream.range(0, col - 1).allMatch(j -> \result.get(col + row - 1 + j).intValue() == matrix[row - 1][col - 2 - j]);
//@ ensures java.util.stream.IntStream.range(0, java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()).size()).allMatch(k -> java.util.Collections.frequency(java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()), java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()).get(k)) == java.util.Collections.frequency(\result, java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()).get(k)));
//@ ensures row > 2 && col > 1 ==> java.util.stream.IntStream.range(0, row - 2).allMatch(k -> \result.get(2 * col + row - 2 + k).intValue() == matrix[row - 2 - k][0]);
```
```
//@ ensures \result != null;
//@ ensures \result.size() == row * col;
//@ ensures row > 0 && col > 0 ==> java.util.stream.IntStream.range(0, col).allMatch(k -> \result.get(k).intValue() == matrix[0][k]);
//@ ensures row > 1 && col > 0 ==> java.util.stream.IntStream.range(1, row).allMatch(i -> \result.get(col + i - 1).intValue() == matrix[i][col - 1]);
//@ ensures row > 1 && col > 1 ==> java.util.stream.IntStream.range(0, col - 1).allMatch(j -> \result.get(col + row - 1 + j).intValue() == matrix[row - 1][col - 2 - j]);
//@ ensures java.util.stream.IntStream.range(0, java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()).size()).allMatch(k -> java.util.Collections.frequency(java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()), java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()).get(k)) == java.util.Collections.frequency(\result, java.util.stream.IntStream.range(0, row).boxed().flatMap(ii -> java.util.stream.IntStream.range(0, col).mapToObj(jj -> matrix[ii][jj])).collect(java.util.stream.Collectors.toList()).get(k)));
```
[25, 28, 29]
===== 25 =====
```
                 row--;
             }
             // print columns from first except printed elements
-            if (c < col) {
+            if (c < col && r >= row) {
                 for (i = row - 1; i >= r; i--) {
                     result.add(matrix[i][c]);
                 }
```
```
    /**
     * Returns the elements of the given matrix in spiral order.
     *
     * @param matrix the 2D array to traverse in spiral order
     * @param row    the number of rows in the matrix
     * @param col    the number of columns in the matrix
     * @return a list containing the elements of the matrix in spiral order
     *
     *         <p>
     *         Example:
     *
     *         <pre>
     * int[][] matrix = {
     *   {1, 2, 3},
     *   {4, 5, 6},
     *   {7, 8, 9}
     * };
     * print(matrix, 3, 3) returns [1, 2, 3, 6, 9, 8, 7, 4, 5]
     *         </pre>
     *         </p>
     */
    public List<Integer> print(int[][] matrix, int row, int col) {
        // r traverses matrix row wise from first
        int r = 0;
        // c traverses matrix column wise from first
        int c = 0;
        int i;
        List<Integer> result = new ArrayList<>();
        while (r < row && c < col) {
            // print first row of matrix
            for (i = c; i < col; i++) {
                result.add(matrix[r][i]);
            }
            // increase r by one because first row printed
            r++;
            // print last column
            for (i = r; i < row; i++) {
                result.add(matrix[i][col - 1]);
            }
            // decrease col by one because last column has been printed
            col--;
            // print rows from last except printed elements
            if (r < row) {
                for (i = col - 1; i >= c; i--) {
                    result.add(matrix[row - 1][i]);
                }
                row--;
            }
            // print columns from first except printed elements
            if (c < col && r >= row) {
                for (i = row - 1; i >= r; i--) {
                    result.add(matrix[i][c]);
                }
                c++;
            }
        }
        return result;
    }
```
===== 28 =====
```
                 row--;
             }
             // print columns from first except printed elements
-            if (c < col) {
+            if (r >= row) {
                 for (i = row - 1; i >= r; i--) {
                     result.add(matrix[i][c]);
                 }
```
```
    /**
     * Returns the elements of the given matrix in spiral order.
     *
     * @param matrix the 2D array to traverse in spiral order
     * @param row    the number of rows in the matrix
     * @param col    the number of columns in the matrix
     * @return a list containing the elements of the matrix in spiral order
     *
     *         <p>
     *         Example:
     *
     *         <pre>
     * int[][] matrix = {
     *   {1, 2, 3},
     *   {4, 5, 6},
     *   {7, 8, 9}
     * };
     * print(matrix, 3, 3) returns [1, 2, 3, 6, 9, 8, 7, 4, 5]
     *         </pre>
     *         </p>
     */
    public List<Integer> print(int[][] matrix, int row, int col) {
        // r traverses matrix row wise from first
        int r = 0;
        // c traverses matrix column wise from first
        int c = 0;
        int i;
        List<Integer> result = new ArrayList<>();
        while (r < row && c < col) {
            // print first row of matrix
            for (i = c; i < col; i++) {
                result.add(matrix[r][i]);
            }
            // increase r by one because first row printed
            r++;
            // print last column
            for (i = r; i < row; i++) {
                result.add(matrix[i][col - 1]);
            }
            // decrease col by one because last column has been printed
            col--;
            // print rows from last except printed elements
            if (r < row) {
                for (i = col - 1; i >= c; i--) {
                    result.add(matrix[row - 1][i]);
                }
                row--;
            }
            // print columns from first except printed elements
            if (r >= row) {
                for (i = row - 1; i >= r; i--) {
                    result.add(matrix[i][c]);
                }
                c++;
            }
        }
        return result;
    }
```
===== 29 =====
```
             }
             // print columns from first except printed elements
             if (c < col) {
-                for (i = row - 1; i >= r; i--) {
+                for (i = r; i < row; i++) {
                     result.add(matrix[i][c]);
                 }
                 c++;
```
```
    /**
     * Returns the elements of the given matrix in spiral order.
     *
     * @param matrix the 2D array to traverse in spiral order
     * @param row    the number of rows in the matrix
     * @param col    the number of columns in the matrix
     * @return a list containing the elements of the matrix in spiral order
     *
     *         <p>
     *         Example:
     *
     *         <pre>
     * int[][] matrix = {
     *   {1, 2, 3},
     *   {4, 5, 6},
     *   {7, 8, 9}
     * };
     * print(matrix, 3, 3) returns [1, 2, 3, 6, 9, 8, 7, 4, 5]
     *         </pre>
     *         </p>
     */
    public List<Integer> print(int[][] matrix, int row, int col) {
        // r traverses matrix row wise from first
        int r = 0;
        // c traverses matrix column wise from first
        int c = 0;
        int i;
        List<Integer> result = new ArrayList<>();
        while (r < row && c < col) {
            // print first row of matrix
            for (i = c; i < col; i++) {
                result.add(matrix[r][i]);
            }
            // increase r by one because first row printed
            r++;
            // print last column
            for (i = r; i < row; i++) {
                result.add(matrix[i][col - 1]);
            }
            // decrease col by one because last column has been printed
            col--;
            // print rows from last except printed elements
            if (r < row) {
                for (i = col - 1; i >= c; i--) {
                    result.add(matrix[row - 1][i]);
                }
                row--;
            }
            // print columns from first except printed elements
            if (c < col) {
                for (i = r; i < row; i++) {
                    result.add(matrix[i][c]);
                }
                c++;
            }
        }
        return result;
    }
```
