https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/backtracking/FloodFill.java#L34-L61
```
🈚️

It's hard.

//@ ensures !(newColor != oldColor && 0 <= x && x < image.length && 0 <= y && y < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor) || image[x][y] == newColor;
//@ ensures !(0 <= x && x < image.length && 0 <= y && y < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) != oldColor) || image[x][y] == \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1);
//@ ensures !(newColor != oldColor && 0 < x && x < image.length - 1 && image[x - 1].length == image[x].length && image[x + 1].length == image[x].length && 0 <= y && y + 2 < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y + 1 && y + 1 < image[x].length) ? image[x][y + 1] : oldColor + 1) == oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y && y < image[x - 1].length) ? image[x - 1][y] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y + 1 && y + 1 < image[x - 1].length) ? image[x - 1][y + 1] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y + 2 && y + 2 < image[x - 1].length) ? image[x - 1][y + 2] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y + 2 && y + 2 < image[x].length) ? image[x][y + 2] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y && y < image[x + 1].length) ? image[x + 1][y] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y + 1 && y + 1 < image[x + 1].length) ? image[x + 1][y + 1] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y + 2 && y + 2 < image[x + 1].length) ? image[x + 1][y + 2] : oldColor + 1) != oldColor) || image[x][y + 1] == newColor;
//@ ensures !(newColor != oldColor && 0 < x && x < image.length - 1 && image[x - 1].length == image[x].length && image[x + 1].length == image[x].length && 2 <= y && y < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y - 1 && y - 1 < image[x].length) ? image[x][y - 1] : oldColor + 1) == oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y - 2 && y - 2 < image[x - 1].length) ? image[x - 1][y - 2] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y - 1 && y - 1 < image[x - 1].length) ? image[x - 1][y - 1] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y && y < image[x - 1].length) ? image[x - 1][y] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y - 2 && y - 2 < image[x].length) ? image[x][y - 2] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y - 2 && y - 2 < image[x + 1].length) ? image[x + 1][y - 2] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y - 1 && y - 1 < image[x + 1].length) ? image[x + 1][y - 1] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y && y < image[x + 1].length) ? image[x + 1][y] : oldColor + 1) != oldColor) || image[x][y - 1] == newColor;
//@ ensures !(newColor != oldColor && 0 <= x && x + 2 < image.length && image[x + 1].length == image[x].length && image[x + 2].length == image[x].length && 0 < y && y + 1 < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y && y < image[x + 1].length) ? image[x + 1][y] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y - 1 && y - 1 < image[x].length) ? image[x][y - 1] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y + 1 && y + 1 < image[x].length) ? image[x][y + 1] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y - 1 && y - 1 < image[x + 1].length) ? image[x + 1][y - 1] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y + 1 && y + 1 < image[x + 1].length) ? image[x + 1][y + 1] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y - 1 && y - 1 < image[x + 2].length) ? image[x + 2][y - 1] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y && y < image[x + 2].length) ? image[x + 2][y] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y + 1 && y + 1 < image[x + 2].length) ? image[x + 2][y + 1] : oldColor + 1) != oldColor) || image[x + 1][y] == newColor;
//@ ensures !(newColor != oldColor && 2 <= x && x < image.length && image[x - 1].length == image[x].length && image[x - 2].length == image[x].length && 0 < y && y + 1 < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y && y < image[x - 1].length) ? image[x - 1][y] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y - 1 && y - 1 < image[x].length) ? image[x][y - 1] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y + 1 && y + 1 < image[x].length) ? image[x][y + 1] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y - 1 && y - 1 < image[x - 1].length) ? image[x - 1][y - 1] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y + 1 && y + 1 < image[x - 1].length) ? image[x - 1][y + 1] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y - 1 && y - 1 < image[x - 2].length) ? image[x - 2][y - 1] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y && y < image[x - 2].length) ? image[x - 2][y] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y + 1 && y + 1 < image[x - 2].length) ? image[x - 2][y + 1] : oldColor + 1) != oldColor) || image[x - 1][y] == newColor;
//@ ensures !(newColor != oldColor && 0 <= x && x + 2 < image.length && image[x + 1].length == image[x].length && image[x + 2].length == image[x].length && 0 <= y && y + 2 < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y + 1 && y + 1 < image[x + 1].length) ? image[x + 1][y + 1] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y + 1 && y + 1 < image[x].length) ? image[x][y + 1] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y + 2 && y + 2 < image[x].length) ? image[x][y + 2] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y && y < image[x + 1].length) ? image[x + 1][y] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y + 2 && y + 2 < image[x + 1].length) ? image[x + 1][y + 2] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y && y < image[x + 2].length) ? image[x + 2][y] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y + 1 && y + 1 < image[x + 2].length) ? image[x + 2][y + 1] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y + 2 && y + 2 < image[x + 2].length) ? image[x + 2][y + 2] : oldColor + 1) != oldColor) || image[x + 1][y + 1] == newColor;
//@ ensures !(newColor != oldColor && 0 <= x && x + 2 < image.length && image[x + 1].length == image[x].length && image[x + 2].length == image[x].length && 2 <= y && y < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y - 1 && y - 1 < image[x + 1].length) ? image[x + 1][y - 1] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y - 1 && y - 1 < image[x].length) ? image[x][y - 1] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y - 2 && y - 2 < image[x].length) ? image[x][y - 2] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y && y < image[x + 1].length) ? image[x + 1][y] : oldColor + 1) != oldColor && \old((0 <= x + 1 && x + 1 < image.length && 0 <= y - 2 && y - 2 < image[x + 1].length) ? image[x + 1][y - 2] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y && y < image[x + 2].length) ? image[x + 2][y] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y - 1 && y - 1 < image[x + 2].length) ? image[x + 2][y - 1] : oldColor + 1) != oldColor && \old((0 <= x + 2 && x + 2 < image.length && 0 <= y - 2 && y - 2 < image[x + 2].length) ? image[x + 2][y - 2] : oldColor + 1) != oldColor) || image[x + 1][y - 1] == newColor;
//@ ensures !(newColor != oldColor && 2 <= x && x < image.length && image[x - 1].length == image[x].length && image[x - 2].length == image[x].length && 0 <= y && y + 2 < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y + 1 && y + 1 < image[x - 1].length) ? image[x - 1][y + 1] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y + 1 && y + 1 < image[x].length) ? image[x][y + 1] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y + 2 && y + 2 < image[x].length) ? image[x][y + 2] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y && y < image[x - 1].length) ? image[x - 1][y] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y + 2 && y + 2 < image[x - 1].length) ? image[x - 1][y + 2] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y && y < image[x - 2].length) ? image[x - 2][y] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y + 1 && y + 1 < image[x - 2].length) ? image[x - 2][y + 1] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y + 2 && y + 2 < image[x - 2].length) ? image[x - 2][y + 2] : oldColor + 1) != oldColor) || image[x - 1][y + 1] == newColor;
//@ ensures !(newColor != oldColor && 2 <= x && x < image.length && image[x - 1].length == image[x].length && image[x - 2].length == image[x].length && 2 <= y && y < image[x].length && \old((0 <= x && x < image.length && 0 <= y && y < image[x].length) ? image[x][y] : oldColor + 1) == oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y - 1 && y - 1 < image[x - 1].length) ? image[x - 1][y - 1] : oldColor + 1) == oldColor && \old((0 <= x && x < image.length && 0 <= y - 1 && y - 1 < image[x].length) ? image[x][y - 1] : oldColor + 1) != oldColor && \old((0 <= x && x < image.length && 0 <= y - 2 && y - 2 < image[x].length) ? image[x][y - 2] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y && y < image[x - 1].length) ? image[x - 1][y] : oldColor + 1) != oldColor && \old((0 <= x - 1 && x - 1 < image.length && 0 <= y - 2 && y - 2 < image[x - 1].length) ? image[x - 1][y - 2] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y && y < image[x - 2].length) ? image[x - 2][y] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y - 1 && y - 1 < image[x - 2].length) ? image[x - 2][y - 1] : oldColor + 1) != oldColor && \old((0 <= x - 2 && x - 2 < image.length && 0 <= y - 2 && y - 2 < image[x - 2].length) ? image[x - 2][y - 2] : oldColor + 1) != oldColor) || image[x - 1][y - 1] == newColor;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
===== 0 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y < image[x].length || getPixel(image, x, y) != oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y < image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 1 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image.length || getPixel(image, x, y) != oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image.length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 2 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) == oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) == oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 3 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x < 0 || x >= image.length || y <= 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y <= 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 4 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x < 0 || x >= image.length || y >= 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y >= 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 5 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x <= 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x <= 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 6 =====
```
      * @param oldColor The old color which is to be replaced in the image
      */
     public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
-        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
+        if (newColor == oldColor || x >= 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
             return;
         }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x >= 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 7 =====
```
             return;
         }
 
-        putPixel(image, x, y, newColor);
+        putPixel(image, x, y, newColor + 1);
 
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor + 1);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 8 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 9 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y + 1, newColor, oldColor); // Incorrectly checks the bottom-right diagonal instead of the bottom pixel.
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor); // Incorrectly checks the bottom-right diagonal instead of the bottom pixel.
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 10 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y - 1, newColor, oldColor); // Incorrectly checks the top-right diagonal instead of the bottom pixel.
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x + 1, y - 1, newColor, oldColor); // Incorrectly checks the top-right diagonal instead of the bottom pixel.
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 11 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        floodFill(image, x - 1, y - 1, newColor, oldColor); // Incorrectly checks the top-left diagonal instead of the bottom pixel.
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor); // Incorrectly checks the top-left diagonal instead of the bottom pixel.
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 12 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        floodFill(image, x, y - 1, newColor, newColor); // Uses newColor instead of oldColor, leading to incorrect behavior.
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, newColor); // Uses newColor instead of oldColor, leading to incorrect behavior.
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 13 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        floodFill(image, x, y - 1, newColor, oldColor);
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 14 =====
```
         /* Recursively check for horizontally & vertically adjacent coordinates */
         floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y, newColor, oldColor);
-        floodFill(image, x, y + 1, newColor, oldColor);
+        floodFill(image, x, y, newColor, oldColor); // Calls floodFill on the same pixel, causing infinite recursion if not handled.
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y, newColor, oldColor); // Calls floodFill on the same pixel, causing infinite recursion if not handled.
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 15 =====
```
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
-        floodFill(image, x + 1, y - 1, newColor, oldColor);
+        
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 16 =====
```
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
-        floodFill(image, x + 1, y - 1, newColor, oldColor);
+        floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 17 =====
```
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
-        floodFill(image, x + 1, y - 1, newColor, oldColor);
+        floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 18 =====
```
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
-        floodFill(image, x + 1, y - 1, newColor, oldColor);
+        floodFill(image, x - 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x - 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 19 =====
```
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
-        floodFill(image, x + 1, y - 1, newColor, oldColor);
+        floodFill(image, x, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 20 =====
```
         floodFill(image, x, y - 1, newColor, oldColor);
 
         /* Recursively check for diagonally adjacent coordinates  */
-        floodFill(image, x + 1, y - 1, newColor, oldColor);
+        floodFill(image, x, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 21 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 22 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 23 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 24 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 25 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x - 1, y - 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 26 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x - 1, y, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 27 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 28 =====
```
 
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
-        floodFill(image, x - 1, y + 1, newColor, oldColor);
+        floodFill(image, x, y - 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 29 =====
```
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
-        floodFill(image, x + 1, y + 1, newColor, oldColor);
+        
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 30 =====
```
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
-        floodFill(image, x + 1, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 31 =====
```
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
-        floodFill(image, x + 1, y + 1, newColor, oldColor);
+        floodFill(image, x + 1, y, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 32 =====
```
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
-        floodFill(image, x + 1, y + 1, newColor, oldColor);
+        floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 33 =====
```
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
-        floodFill(image, x + 1, y + 1, newColor, oldColor);
+        floodFill(image, x - 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 34 =====
```
         /* Recursively check for diagonally adjacent coordinates  */
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
-        floodFill(image, x + 1, y + 1, newColor, oldColor);
+        floodFill(image, x, y + 1, newColor, oldColor);
         floodFill(image, x - 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y - 1, newColor, oldColor);
    }
```
===== 35 =====
```
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
-        floodFill(image, x - 1, y - 1, newColor, oldColor);
+        
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        
    }
```
===== 36 =====
```
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
-        floodFill(image, x - 1, y - 1, newColor, oldColor);
+        floodFill(image, x + 1, y + 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
    }
```
===== 37 =====
```
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
-        floodFill(image, x - 1, y - 1, newColor, oldColor);
+        floodFill(image, x + 1, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y - 1, newColor, oldColor);
    }
```
===== 38 =====
```
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
-        floodFill(image, x - 1, y - 1, newColor, oldColor);
+        floodFill(image, x - 1, y + 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
    }
```
===== 39 =====
```
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
-        floodFill(image, x - 1, y - 1, newColor, oldColor);
+        floodFill(image, x - 1, y, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
    }
```
===== 40 =====
```
         floodFill(image, x + 1, y - 1, newColor, oldColor);
         floodFill(image, x - 1, y + 1, newColor, oldColor);
         floodFill(image, x + 1, y + 1, newColor, oldColor);
-        floodFill(image, x - 1, y - 1, newColor, oldColor);
+        floodFill(image, x, y - 1, newColor, oldColor);
     }
```
```
    /**
     * Fill the 2D image with new color
     *
     * @param image The image to be filled
     * @param x The x co-ordinate at which color is to be filled
     * @param y The y co-ordinate at which color is to be filled
     * @param newColor The new color which to be filled in the image
     * @param oldColor The old color which is to be replaced in the image
     */
    public static void floodFill(final int[][] image, final int x, final int y, final int newColor, final int oldColor) {
        if (newColor == oldColor || x < 0 || x >= image.length || y < 0 || y >= image[x].length || getPixel(image, x, y) != oldColor) {
            return;
        }

        putPixel(image, x, y, newColor);

        /* Recursively check for horizontally & vertically adjacent coordinates */
        floodFill(image, x + 1, y, newColor, oldColor);
        floodFill(image, x - 1, y, newColor, oldColor);
        floodFill(image, x, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);

        /* Recursively check for diagonally adjacent coordinates  */
        floodFill(image, x + 1, y - 1, newColor, oldColor);
        floodFill(image, x - 1, y + 1, newColor, oldColor);
        floodFill(image, x + 1, y + 1, newColor, oldColor);
        floodFill(image, x, y - 1, newColor, oldColor);
    }
```
