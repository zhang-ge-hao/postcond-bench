https://github.com/lemire/javaewah/blob/86f37ab370b74282989e40917b2786ad9fb65f94/./src/main/java/com/googlecode/javaewah32/FastAggregation32.java#L252-L276
```
🈚️

originally wrong.

//@ ensures true;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
===== 0 =====
```
                     }
                 }
         );
-        Collections.addAll(pq, bitmaps);
+        
         if(pq.isEmpty()) return new EWAHCompressedBitmap32();
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return pq.poll();
    }
```
===== 1 =====
```
                     }
                 }
         );
-        Collections.addAll(pq, bitmaps);
+        Collections.addAll(pq, new EWAHCompressedBitmap32[0]);
         if(pq.isEmpty()) return new EWAHCompressedBitmap32();
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, new EWAHCompressedBitmap32[0]);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return pq.poll();
    }
```
===== 2 =====
```
                     }
                 }
         );
-        Collections.addAll(pq, bitmaps);
+        pq.offer(bitmaps[0]);
         if(pq.isEmpty()) return new EWAHCompressedBitmap32();
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        pq.offer(bitmaps[0]);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return pq.poll();
    }
```
===== 3 =====
```
                 }
         );
         Collections.addAll(pq, bitmaps);
-        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
+        if(pq.size() <= 1) return new EWAHCompressedBitmap32();
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.size() <= 1) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return pq.poll();
    }
```
===== 4 =====
```
         );
         Collections.addAll(pq, bitmaps);
         if(pq.isEmpty()) return new EWAHCompressedBitmap32();
-        while (pq.size() > 1) {
+        while (pq.size() < 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
             pq.add(x1.or(x2));
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() < 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return pq.poll();
    }
```
===== 5 =====
```
         );
         Collections.addAll(pq, bitmaps);
         if(pq.isEmpty()) return new EWAHCompressedBitmap32();
-        while (pq.size() > 1) {
+        while (pq.size() > 2) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
             pq.add(x1.or(x2));
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 2) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return pq.poll();
    }
```
===== 6 =====
```
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
-            pq.add(x1.or(x2));
+            
         }
         return pq.poll();
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            
        }
        return pq.poll();
    }
```
===== 7 =====
```
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
-            pq.add(x1.or(x2));
+            pq.add(x1); // Adds only the first bitmap, ignoring the second
         }
         return pq.poll();
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1); // Adds only the first bitmap, ignoring the second
        }
        return pq.poll();
    }
```
===== 8 =====
```
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
-            pq.add(x1.or(x2));
+            pq.add(x1.and(x2)); // Incorrectly uses AND instead of OR
         }
         return pq.poll();
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.and(x2)); // Incorrectly uses AND instead of OR
        }
        return pq.poll();
    }
```
===== 9 =====
```
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
-            pq.add(x1.or(x2));
+            pq.add(x1.or(x1)); // Incorrectly adds the OR of the same bitmap, leading to incorrect results
         }
         return pq.poll();
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x1)); // Incorrectly adds the OR of the same bitmap, leading to incorrect results
        }
        return pq.poll();
    }
```
===== 10 =====
```
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
-            pq.add(x1.or(x2));
+            pq.add(x1.xor(x2)); // Incorrectly uses XOR instead of OR
         }
         return pq.poll();
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.xor(x2)); // Incorrectly uses XOR instead of OR
        }
        return pq.poll();
    }
```
===== 11 =====
```
         while (pq.size() > 1) {
             EWAHCompressedBitmap32 x1 = pq.poll();
             EWAHCompressedBitmap32 x2 = pq.poll();
-            pq.add(x1.or(x2));
+            pq.add(x2); // Adds only the second bitmap, ignoring the first
         }
         return pq.poll();
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x2); // Adds only the second bitmap, ignoring the first
        }
        return pq.poll();
    }
```
===== 12 =====
```
             EWAHCompressedBitmap32 x2 = pq.poll();
             pq.add(x1.or(x2));
         }
-        return pq.poll();
+        return new EWAHCompressedBitmap32(); // This will return a new empty bitmap instead of the aggregated result.
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return new EWAHCompressedBitmap32(); // This will return a new empty bitmap instead of the aggregated result.
    }
```
===== 13 =====
```
             EWAHCompressedBitmap32 x2 = pq.poll();
             pq.add(x1.or(x2));
         }
-        return pq.poll();
+        return null;
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return null;
    }
```
===== 14 =====
```
             EWAHCompressedBitmap32 x2 = pq.poll();
             pq.add(x1.or(x2));
         }
-        return pq.poll();
+        return null; // This will return a null value instead of the expected bitmap.
     }
```
```
    /**
     * Simple algorithm that computes the OR aggregate.
     * 
     * @param bitmaps input bitmaps
     * @return new bitmap containing the aggregate
     */
    public static EWAHCompressedBitmap32 or(final EWAHCompressedBitmap32... bitmaps) {
        PriorityQueue<EWAHCompressedBitmap32> pq = new PriorityQueue<EWAHCompressedBitmap32>(bitmaps.length,
                new Comparator<EWAHCompressedBitmap32>() {
                    @Override
                    public int compare(EWAHCompressedBitmap32 a, EWAHCompressedBitmap32 b) {
                        return a.sizeInBytes()
                                - b.sizeInBytes();
                    }
                }
        );
        Collections.addAll(pq, bitmaps);
        if(pq.isEmpty()) return new EWAHCompressedBitmap32();
        while (pq.size() > 1) {
            EWAHCompressedBitmap32 x1 = pq.poll();
            EWAHCompressedBitmap32 x2 = pq.poll();
            pq.add(x1.or(x2));
        }
        return null; // This will return a null value instead of the expected bitmap.
    }
```
