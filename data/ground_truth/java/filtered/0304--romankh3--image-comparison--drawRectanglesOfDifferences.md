https://github.com/romankh3/image-comparison/blob/0e9c63792af31dac63b439554dcc0d35c34e0b78/./src/main/java/com/github/romankh3/image/comparison/ImageComparison.java#L448-L472
```
🈚️

No API.

In this code, drawRectanglesOfDifferences uses the passed Graphics2D object to draw rectangles onto a BufferedImage: the image first calls createGraphics() to create a Graphics2D that is bound to itself, and then all drawRect and fillRect calls modify the pixels of that image directly. However, in the method signature we only receive the Graphics2D and not the underlying BufferedImage, and the Graphics2D API does not provide a way to “look back” and retrieve the target image. As a result, from a specification point of view (e.g., JML postconditions), we can only observe the state of the “pen” such as graphics.getColor(), getStroke(), and getTransform(), but we cannot see what actually happened to the pixels of the underlying BufferedImage. Therefore, we cannot precisely specify in the postcondition which rectangles were drawn or whether they were drawn correctly.

//@ ensures fillDifferenceRectangles ==> (graphics.getColor().getRed() == this.differenceRectangleColor.getRed() && graphics.getColor().getGreen() == this.differenceRectangleColor.getGreen() && graphics.getColor().getBlue() == this.differenceRectangleColor.getBlue() && graphics.getColor().getAlpha() == (int)(percentOpacityDifferenceRectangles / 100 * 255));
//@ ensures !fillDifferenceRectangles ==> (graphics.getColor().getRed() == this.differenceRectangleColor.getRed() && graphics.getColor().getGreen() == this.differenceRectangleColor.getGreen() && graphics.getColor().getBlue() == this.differenceRectangleColor.getBlue() && graphics.getColor().getAlpha() == this.differenceRectangleColor.getAlpha());
//@ ensures graphics.getStroke().equals(\old(graphics.getStroke()));
//@ ensures graphics.getTransform().equals(\old(graphics.getTransform()));
//@ ensures rectangles.equals(\old(rectangles));
//@ ensures maximalRectangleCount == \old(maximalRectangleCount);
//@ ensures percentOpacityDifferenceRectangles == \old(percentOpacityDifferenceRectangles);
//@ ensures fillDifferenceRectangles == \old(fillDifferenceRectangles);
```
```
//@ ensures fillDifferenceRectangles ==> (graphics.getColor().getRed() == this.differenceRectangleColor.getRed() && graphics.getColor().getGreen() == this.differenceRectangleColor.getGreen() && graphics.getColor().getBlue() == this.differenceRectangleColor.getBlue() && graphics.getColor().getAlpha() == (int)(percentOpacityDifferenceRectangles / 100 * 255));
//@ ensures !fillDifferenceRectangles ==> (graphics.getColor().getRed() == this.differenceRectangleColor.getRed() && graphics.getColor().getGreen() == this.differenceRectangleColor.getGreen() && graphics.getColor().getBlue() == this.differenceRectangleColor.getBlue() && graphics.getColor().getAlpha() == this.differenceRectangleColor.getAlpha());
//@ ensures graphics.getStroke().equals(\old(graphics.getStroke()));
//@ ensures graphics.getTransform().equals(\old(graphics.getTransform()));
//@ ensures rectangles.equals(\old(rectangles));
//@ ensures maximalRectangleCount == \old(maximalRectangleCount);
//@ ensures percentOpacityDifferenceRectangles == \old(percentOpacityDifferenceRectangles);
//@ ensures fillDifferenceRectangles == \old(fillDifferenceRectangles);
```
[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 23, 27]
===== 5 =====
```
         List<Rectangle> rectanglesForDraw;
         graphics.setColor(this.differenceRectangleColor);
 
-        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
+        if (maximalRectangleCount < rectangles.size() && maximalRectangleCount != 0) {
             rectanglesForDraw = rectangles.stream()
                     .sorted(Comparator.comparing(Rectangle::size))
                     .skip(rectangles.size() - maximalRectangleCount)
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount < rectangles.size() && maximalRectangleCount != 0) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 6 =====
```
         List<Rectangle> rectanglesForDraw;
         graphics.setColor(this.differenceRectangleColor);
 
-        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
+        if (maximalRectangleCount <= 0 && maximalRectangleCount < rectangles.size()) {
             rectanglesForDraw = rectangles.stream()
                     .sorted(Comparator.comparing(Rectangle::size))
                     .skip(rectangles.size() - maximalRectangleCount)
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount <= 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 7 =====
```
         List<Rectangle> rectanglesForDraw;
         graphics.setColor(this.differenceRectangleColor);
 
-        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
+        if (maximalRectangleCount == rectangles.size()) {
             rectanglesForDraw = rectangles.stream()
                     .sorted(Comparator.comparing(Rectangle::size))
                     .skip(rectangles.size() - maximalRectangleCount)
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount == rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 8 =====
```
 
         if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
             rectanglesForDraw = rectangles.stream()
-                    .sorted(Comparator.comparing(Rectangle::size))
+                    .sorted(Comparator.comparing(Rectangle::getHeight).reversed())
                     .skip(rectangles.size() - maximalRectangleCount)
                     .collect(Collectors.toList());
         } else {
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::getHeight).reversed())
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 9 =====
```
 
         if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
             rectanglesForDraw = rectangles.stream()
-                    .sorted(Comparator.comparing(Rectangle::size))
+                    .sorted(Comparator.comparing(Rectangle::size).reversed())
                     .skip(rectangles.size() - maximalRectangleCount)
                     .collect(Collectors.toList());
         } else {
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size).reversed())
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 10 =====
```
 
         if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
             rectanglesForDraw = rectangles.stream()
-                    .sorted(Comparator.comparing(Rectangle::size))
+                    .sorted(Comparator.comparingInt(rectangle -> rectangle.getMinPoint().x))
                     .skip(rectangles.size() - maximalRectangleCount)
                     .collect(Collectors.toList());
         } else {
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparingInt(rectangle -> rectangle.getMinPoint().x))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 11 =====
```
         if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
             rectanglesForDraw = rectangles.stream()
                     .sorted(Comparator.comparing(Rectangle::size))
-                    .skip(rectangles.size() - maximalRectangleCount)
+                    .skip(rectangles.size() + maximalRectangleCount)
                     .collect(Collectors.toList());
         } else {
             rectanglesForDraw = new ArrayList<>(rectangles);
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() + maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 12 =====
```
             rectanglesForDraw = rectangles.stream()
                     .sorted(Comparator.comparing(Rectangle::size))
                     .skip(rectangles.size() - maximalRectangleCount)
-                    .collect(Collectors.toList());
+                    .collect(Collectors.toList()).subList(0, 1);
         } else {
             rectanglesForDraw = new ArrayList<>(rectangles);
         }
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList()).subList(0, 1);
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 13 =====
```
             rectanglesForDraw = new ArrayList<>(rectangles);
         }
 
-        draw(graphics, rectanglesForDraw);
+        
 
         if (fillDifferenceRectangles) {
             fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 14 =====
```
             rectanglesForDraw = new ArrayList<>(rectangles);
         }
 
-        draw(graphics, rectanglesForDraw);
+        draw(graphics, new ArrayList<Rectangle>()); // Passing an empty list
 
         if (fillDifferenceRectangles) {
             fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, new ArrayList<Rectangle>()); // Passing an empty list

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 15 =====
```
             rectanglesForDraw = new ArrayList<>(rectangles);
         }
 
-        draw(graphics, rectanglesForDraw);
+        draw(graphics, rectangles); // Using the original rectangles instead of rectanglesForDraw
 
         if (fillDifferenceRectangles) {
             fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectangles); // Using the original rectangles instead of rectanglesForDraw

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 16 =====
```
             rectanglesForDraw = new ArrayList<>(rectangles);
         }
 
-        draw(graphics, rectanglesForDraw);
+        graphics.drawRect(0, 0, 1, 1); // Drawing a single pixel rectangle instead of the actual rectangles
 
         if (fillDifferenceRectangles) {
             fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        graphics.drawRect(0, 0, 1, 1); // Drawing a single pixel rectangle instead of the actual rectangles

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
        }
    }
```
===== 23 =====
```
         draw(graphics, rectanglesForDraw);
 
         if (fillDifferenceRectangles) {
-            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
+            fillRectangles(graphics, new ArrayList<>(), percentOpacityDifferenceRectangles);
         }
     }
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, new ArrayList<>(), percentOpacityDifferenceRectangles);
        }
    }
```
===== 27 =====
```
         draw(graphics, rectanglesForDraw);
 
         if (fillDifferenceRectangles) {
-            fillRectangles(graphics, rectanglesForDraw, percentOpacityDifferenceRectangles);
+            fillRectangles(graphics, rectanglesForDraw.subList(0, 1), percentOpacityDifferenceRectangles);
         }
     }
```
```
    /**
     * Draw rectangles with the differences.
     *
     * @param rectangles the collection of the {@link Rectangle} of differences.
     * @param graphics   prepared {@link Graphics2D}object.
     */
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        graphics.setColor(this.differenceRectangleColor);

        if (maximalRectangleCount > 0 && maximalRectangleCount < rectangles.size()) {
            rectanglesForDraw = rectangles.stream()
                    .sorted(Comparator.comparing(Rectangle::size))
                    .skip(rectangles.size() - maximalRectangleCount)
                    .collect(Collectors.toList());
        } else {
            rectanglesForDraw = new ArrayList<>(rectangles);
        }

        draw(graphics, rectanglesForDraw);

        if (fillDifferenceRectangles) {
            fillRectangles(graphics, rectanglesForDraw.subList(0, 1), percentOpacityDifferenceRectangles);
        }
    }
```
