https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/geometry/WusLine.java#L74-L133
```
//@ ensures \result != null;
//@ ensures \result.size() >= 4;
//@ ensures (\result.size() % 2) == 0;
//@ ensures (\result.size() >= 2 && \old(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> (\result.get(0).point.y == \result.get(1).point.y && \result.get(1).point.x == \result.get(0).point.x + 1);
//@ ensures (\result.size() >= 2 && \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)))) ==> (\result.get(0).point.x == \result.get(1).point.x && \result.get(1).point.y == \result.get(0).point.y + 1);
//@ ensures (\result.size() >= 2 && \old(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> (\result.get(\result.size() - 2).point.y == \result.get(\result.size() - 1).point.y && \result.get(\result.size() - 1).point.x == \result.get(\result.size() - 2).point.x + 1);
//@ ensures (\result.size() >= 2 && \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)))) ==> (\result.get(\result.size() - 2).point.x == \result.get(\result.size() - 1).point.x && \result.get(\result.size() - 1).point.y == \result.get(\result.size() - 2).point.y + 1);
//@ ensures (\result.size() >= 2 && \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)))) ==> (\result.get(0).point.x <= \result.get(\result.size() - 2).point.x);
//@ ensures (\result.size() >= 2 && \old(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> (\result.get(0).point.y <= \result.get(\result.size() - 2).point.y);
//@ ensures (\result.size() >= 1) ==> (\result.get(0).intensity >= 0.0 && \result.get(0).intensity <= 1.0 && \result.get(\result.size() - 1).intensity >= 0.0 && \result.get(\result.size() - 1).intensity <= 1.0);
//@ ensures \result.stream().allMatch(p -> p.intensity >= 0.0 && p.intensity <= 1.0);
//@ ensures \result.stream().anyMatch(p -> p.point.x == \old(x0) && p.point.y == \old(y0));
//@ ensures \result.stream().anyMatch(p -> p.point.x == \old(x1) && p.point.y == \old(y1));
//@ ensures \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> \result.stream().allMatch(p -> p.point.x >= Math.min(\old(x0), \old(x1)) && p.point.x <= Math.max(\old(x0), \old(x1)));
//@ ensures \old(Math.abs(y1 - y0) > Math.abs(x1 - x0)) ==> \result.stream().allMatch(p -> p.point.y >= Math.min(\old(y0), \old(y1)) && p.point.y <= Math.max(\old(y0), \old(y1)));
//@ ensures \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)) && x0 != x1) ==> \result.size() == 2 * (Math.abs(\old(x1 - x0)) + 1);
//@ ensures \old(Math.abs(y1 - y0) > Math.abs(x1 - x0) && y0 != y1) ==> \result.size() == 2 * (Math.abs(\old(y1 - y0)) + 1);
//@ ensures \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)) && x0 != x1) ==> ((int) \result.stream().map(p -> p.point.x).distinct().count()) == (Math.abs(\old(x1 - x0)) + 1);
//@ ensures \old(Math.abs(y1 - y0) > Math.abs(x1 - x0) && y0 != y1) ==> ((int) \result.stream().map(p -> p.point.y).distinct().count()) == (Math.abs(\old(y1 - y0)) + 1);
```
```
//@ ensures \result != null;
//@ ensures \result.size() >= 4;
//@ ensures (\result.size() % 2) == 0;
//@ ensures (\result.size() >= 2 && \old(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> (\result.get(0).point.y == \result.get(1).point.y && \result.get(1).point.x == \result.get(0).point.x + 1);
//@ ensures (\result.size() >= 2 && \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)))) ==> (\result.get(0).point.x == \result.get(1).point.x && \result.get(1).point.y == \result.get(0).point.y + 1);
//@ ensures (\result.size() >= 2 && \old(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> (\result.get(\result.size() - 2).point.y == \result.get(\result.size() - 1).point.y && \result.get(\result.size() - 1).point.x == \result.get(\result.size() - 2).point.x + 1);
//@ ensures (\result.size() >= 2 && \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)))) ==> (\result.get(\result.size() - 2).point.x == \result.get(\result.size() - 1).point.x && \result.get(\result.size() - 1).point.y == \result.get(\result.size() - 2).point.y + 1);
//@ ensures (\result.size() >= 2 && \old(!(Math.abs(y1 - y0) > Math.abs(x1 - x0)))) ==> (\result.get(0).point.x <= \result.get(\result.size() - 2).point.x);
//@ ensures (\result.size() >= 2 && \old(Math.abs(y1 - y0) > Math.abs(x1 - x0))) ==> (\result.get(0).point.y <= \result.get(\result.size() - 2).point.y);
//@ ensures (\result.size() >= 1) ==> (\result.get(0).intensity >= 0.0 && \result.get(0).intensity <= 1.0 && \result.get(\result.size() - 1).intensity >= 0.0 && \result.get(\result.size() - 1).intensity <= 1.0);
```
[6, 7, 8, 15, 17, 18, 19, 21, 22, 25, 26, 27, 28]
===== 6 =====
```
         // Determine if the line is steep (more vertical than horizontal)
         boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);
 
-        if (steep) {
+        if (!steep) {
             // For steep lines, swap x and y coordinates to iterate along y-axis
             int temp = x0;
             x0 = y0;
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (!steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 7 =====
```
         // Determine if the line is steep (more vertical than horizontal)
         boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);
 
-        if (steep) {
+        if (steep || true) {
             // For steep lines, swap x and y coordinates to iterate along y-axis
             int temp = x0;
             x0 = y0;
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep || true) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 8 =====
```
         // Determine if the line is steep (more vertical than horizontal)
         boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);
 
-        if (steep) {
+        if (x0 < x1) {
             // For steep lines, swap x and y coordinates to iterate along y-axis
             int temp = x0;
             x0 = y0;
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (x0 < x1) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 15 =====
```
         double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;
 
         // Process the first endpoint
-        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
+        EndpointData firstEndpoint = processEndpoint(x1, y1, gradient, true);
         addEndpointPixels(pixels, firstEndpoint, steep);
 
         // Process the second endpoint
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x1, y1, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 17 =====
```
         addEndpointPixels(pixels, firstEndpoint, steep);
 
         // Process the second endpoint
-        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
+        EndpointData secondEndpoint = processEndpoint(x0, y0, gradient, false);
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x0, y0, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 18 =====
```
         addEndpointPixels(pixels, firstEndpoint, steep);
 
         // Process the second endpoint
-        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
+        EndpointData secondEndpoint = processEndpoint(x0, y1, gradient, true);
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x0, y1, gradient, true);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 19 =====
```
         addEndpointPixels(pixels, firstEndpoint, steep);
 
         // Process the second endpoint
-        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
+        EndpointData secondEndpoint = processEndpoint(x1, y0, gradient, false);
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y0, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 21 =====
```
 
         // Process the second endpoint
         EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
-        addEndpointPixels(pixels, secondEndpoint, steep);
+        addEndpointPixels(pixels, firstEndpoint, false);
 
         // Draw the main line between endpoints
         drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, firstEndpoint, false);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 22 =====
```
 
         // Process the second endpoint
         EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
-        addEndpointPixels(pixels, secondEndpoint, steep);
+        addEndpointPixels(pixels, firstEndpoint, steep);
 
         // Draw the main line between endpoints
         drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
===== 25 =====
```
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
-        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);
+        
 
         return pixels;
     }
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        

        return pixels;
    }
```
===== 26 =====
```
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
-        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);
+        drawMainLine(pixels, firstEndpoint, firstEndpoint, gradient, steep);
 
         return pixels;
     }
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, firstEndpoint, firstEndpoint, gradient, steep);

        return pixels;
    }
```
===== 27 =====
```
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
-        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);
+        drawMainLine(pixels, secondEndpoint, firstEndpoint, gradient, steep);
 
         return pixels;
     }
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, secondEndpoint, firstEndpoint, gradient, steep);

        return pixels;
    }
```
===== 28 =====
```
         addEndpointPixels(pixels, secondEndpoint, steep);
 
         // Draw the main line between endpoints
-        drawMainLine(pixels, firstEndpoint, secondEndpoint, gradient, steep);
+        drawMainLine(pixels, secondEndpoint, secondEndpoint, gradient, steep);
 
         return pixels;
     }
```
```
    /**
     * Draws an anti-aliased line using Wu's algorithm.
     *
     * The algorithm produces smooth lines by drawing pairs of pixels at each
     * x-coordinate (or y-coordinate for steep lines), with intensities based on
     * the line's distance from pixel centers.
     *
     * @param x0 the x-coordinate of the line's start point
     * @param y0 the y-coordinate of the line's start point
     * @param x1 the x-coordinate of the line's end point
     * @param y1 the y-coordinate of the line's end point
     * @return a list of {@link Pixel} objects representing the anti-aliased line,
     *         ordered from start to end
     */
    public static List<Pixel> drawLine(int x0, int y0, int x1, int y1) {
        List<Pixel> pixels = new ArrayList<>();

        // Determine if the line is steep (more vertical than horizontal)
        boolean steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

        if (steep) {
            // For steep lines, swap x and y coordinates to iterate along y-axis
            int temp = x0;
            x0 = y0;
            y0 = temp;

            temp = x1;
            x1 = y1;
            y1 = temp;
        }

        if (x0 > x1) {
            // Ensure we always draw from left to right
            int temp = x0;
            x0 = x1;
            x1 = temp;

            temp = y0;
            y0 = y1;
            y1 = temp;
        }

        // Calculate the line's slope
        double deltaX = x1 - (double) x0;
        double deltaY = y1 - (double) y0;
        double gradient = (deltaX == 0) ? 1.0 : deltaY / deltaX;

        // Process the first endpoint
        EndpointData firstEndpoint = processEndpoint(x0, y0, gradient, true);
        addEndpointPixels(pixels, firstEndpoint, steep);

        // Process the second endpoint
        EndpointData secondEndpoint = processEndpoint(x1, y1, gradient, false);
        addEndpointPixels(pixels, secondEndpoint, steep);

        // Draw the main line between endpoints
        drawMainLine(pixels, secondEndpoint, secondEndpoint, gradient, steep);

        return pixels;
    }
```
