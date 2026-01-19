https://github.com/lemire/javaewah/blob/86f37ab370b74282989e40917b2786ad9fb65f94/./src/main/java/com/googlecode/javaewah32/IteratorUtil32.java#L53-L72
```
🈚️

Iterator
```
```
//@ ensures i.getRunningLength() == 0 && i.getNumberOfLiteralWords() == 0;
//@ ensures ((EWAHCompressedBitmap32)c).cardinality() >= \old(((EWAHCompressedBitmap32)c).cardinality());
//@ ensures (((EWAHCompressedBitmap32)c).sizeInBits() - \old(((EWAHCompressedBitmap32)c).sizeInBits())) % com.googlecode.javaewah32.EWAHCompressedBitmap32.WORD_IN_BITS == 0;
```
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
===== 1 =====
```
      */
     public static void materialize(final IteratingRLW32 i,
                                    final BitmapStorage32 c) {
-        while (true) {
+        while (i.next()) {
             if (i.getRunningLength() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (i.next()) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 2 =====
```
     public static void materialize(final IteratingRLW32 i,
                                    final BitmapStorage32 c) {
         while (true) {
-            if (i.getRunningLength() > 0) {
+            if (i.getNumberOfLiteralWords() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getNumberOfLiteralWords() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 3 =====
```
     public static void materialize(final IteratingRLW32 i,
                                    final BitmapStorage32 c) {
         while (true) {
-            if (i.getRunningLength() > 0) {
+            if (i.getRunningBit()) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningBit()) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 4 =====
```
     public static void materialize(final IteratingRLW32 i,
                                    final BitmapStorage32 c) {
         while (true) {
-            if (i.getRunningLength() > 0) {
+            if (i.getRunningLength() < 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() < 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 5 =====
```
     public static void materialize(final IteratingRLW32 i,
                                    final BitmapStorage32 c) {
         while (true) {
-            if (i.getRunningLength() > 0) {
+            if (i.getRunningLength() <= 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() <= 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 6 =====
```
     public static void materialize(final IteratingRLW32 i,
                                    final BitmapStorage32 c) {
         while (true) {
-            if (i.getRunningLength() > 0) {
+            if (i.getRunningLength() == 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() == 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 7 =====
```
                                    final BitmapStorage32 c) {
         while (true) {
             if (i.getRunningLength() > 0) {
-                c.addStreamOfEmptyWords(i.getRunningBit(),
-                        i.getRunningLength());
+                
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 8 =====
```
         while (true) {
             if (i.getRunningLength() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
-                        i.getRunningLength());
+                        i.getRunningLength() % 2);
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength() % 2);
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 9 =====
```
         while (true) {
             if (i.getRunningLength() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
-                        i.getRunningLength());
+                        i.getRunningLength() * 2);
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength() * 2);
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 10 =====
```
         while (true) {
             if (i.getRunningLength() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
-                        i.getRunningLength());
+                        i.getRunningLength() + 1);
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength() + 1);
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 11 =====
```
         while (true) {
             if (i.getRunningLength() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
-                        i.getRunningLength());
+                        i.getRunningLength() - 1);
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength() - 1);
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 12 =====
```
         while (true) {
             if (i.getRunningLength() > 0) {
                 c.addStreamOfEmptyWords(i.getRunningBit(),
-                        i.getRunningLength());
+                        i.getRunningLength() / 2);
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength() / 2);
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 13 =====
```
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
-            int il = i.getNumberOfLiteralWords();
+            int il = 0; // Sets il to zero, causing no literal words to be processed
             for (int k = 0; k < il ; ++k)
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = 0; // Sets il to zero, causing no literal words to be processed
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 14 =====
```
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
-            int il = i.getNumberOfLiteralWords();
+            int il = i.getNumberOfLiteralWords() + 1; // Off-by-one error, leading to potential ArrayIndexOutOfBounds
             for (int k = 0; k < il ; ++k)
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords() + 1; // Off-by-one error, leading to potential ArrayIndexOutOfBounds
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 15 =====
```
                 c.addStreamOfEmptyWords(i.getRunningBit(),
                         i.getRunningLength());
             }
-            int il = i.getNumberOfLiteralWords();
+            int il = i.getNumberOfLiteralWords() - 1; // Off-by-one error, may skip the last literal word
             for (int k = 0; k < il ; ++k)
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords() - 1; // Off-by-one error, may skip the last literal word
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 16 =====
```
                         i.getRunningLength());
             }
             int il = i.getNumberOfLiteralWords();
-            for (int k = 0; k < il ; ++k)
+            for (int k = 0; k < il - 1; ++k)  // Off-by-one error, misses the last literal word
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
                 break;
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il - 1; ++k)  // Off-by-one error, misses the last literal word
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 17 =====
```
                         i.getRunningLength());
             }
             int il = i.getNumberOfLiteralWords();
-            for (int k = 0; k < il ; ++k)
+            for (int k = 0; k < il; k += 2)  // Iterates over every second literal word, missing half of them
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
                 break;
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il; k += 2)  // Iterates over every second literal word, missing half of them
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 18 =====
```
                         i.getRunningLength());
             }
             int il = i.getNumberOfLiteralWords();
-            for (int k = 0; k < il ; ++k)
+            for (int k = 0; k <= il ; ++k)
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
                 break;
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k <= il ; ++k)
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 19 =====
```
                         i.getRunningLength());
             }
             int il = i.getNumberOfLiteralWords();
-            for (int k = 0; k < il ; ++k)
+            for (int k = 0; k <= il; ++k)  // Off-by-one error, may access out of bounds
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
                 break;
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k <= il; ++k)  // Off-by-one error, may access out of bounds
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 20 =====
```
                         i.getRunningLength());
             }
             int il = i.getNumberOfLiteralWords();
-            for (int k = 0; k < il ; ++k)
+            for (int k = 1; k < il; ++k)  // Skips the first literal word, potentially missing data
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
                 break;
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 1; k < il; ++k)  // Skips the first literal word, potentially missing data
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 21 =====
```
                         i.getRunningLength());
             }
             int il = i.getNumberOfLiteralWords();
-            for (int k = 0; k < il ; ++k)
+            for (int k = il - 1; k >= 0; --k)  // Reverses the iteration order, which may lead to incorrect processing
                 c.addWord(i.getLiteralWordAt(k));
             if (!i.next())
                 break;
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = il - 1; k >= 0; --k)  // Reverses the iteration order, which may lead to incorrect processing
                c.addWord(i.getLiteralWordAt(k));
            if (!i.next())
                break;
        }
    }
```
===== 22 =====
```
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
-                c.addWord(i.getLiteralWordAt(k));
+                c.addWord(0); // Always adds a zero instead of the actual literal word
             if (!i.next())
                 break;
         }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(0); // Always adds a zero instead of the actual literal word
            if (!i.next())
                break;
        }
    }
```
===== 23 =====
```
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
-                c.addWord(i.getLiteralWordAt(k));
+                c.addWord(i.getLiteralWordAt(k) & 0xFFFFFFFE); // Forces the least significant bit to zero
             if (!i.next())
                 break;
         }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k) & 0xFFFFFFFE); // Forces the least significant bit to zero
            if (!i.next())
                break;
        }
    }
```
===== 24 =====
```
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
-                c.addWord(i.getLiteralWordAt(k));
+                c.addWord(i.getLiteralWordAt(k) + 1); // Adds one more than the actual literal word
             if (!i.next())
                 break;
         }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k) + 1); // Adds one more than the actual literal word
            if (!i.next())
                break;
        }
    }
```
===== 25 =====
```
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
-                c.addWord(i.getLiteralWordAt(k));
+                c.addWord(i.getLiteralWordAt(k) - 1); // Subtracts one from the actual literal word
             if (!i.next())
                 break;
         }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k) - 1); // Subtracts one from the actual literal word
            if (!i.next())
                break;
        }
    }
```
===== 26 =====
```
             }
             int il = i.getNumberOfLiteralWords();
             for (int k = 0; k < il ; ++k)
-                c.addWord(i.getLiteralWordAt(k));
+                c.addWord(i.getLiteralWordAt(k) | 0x00000001); // Forces the least significant bit to one
             if (!i.next())
                 break;
         }
```
```
    /**
     * Turn an iterator into a bitmap
     *
     * @param i iterator we wish to materialize
     * @param c where we write
     */
    public static void materialize(final IteratingRLW32 i,
                                   final BitmapStorage32 c) {
        while (true) {
            if (i.getRunningLength() > 0) {
                c.addStreamOfEmptyWords(i.getRunningBit(),
                        i.getRunningLength());
            }
            int il = i.getNumberOfLiteralWords();
            for (int k = 0; k < il ; ++k)
                c.addWord(i.getLiteralWordAt(k) | 0x00000001); // Forces the least significant bit to one
            if (!i.next())
                break;
        }
    }
```
