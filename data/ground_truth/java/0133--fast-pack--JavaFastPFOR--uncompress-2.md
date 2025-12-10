https://github.com/fast-pack/JavaFastPFOR/blob/922d46c2a28598c22a4729df0dba5b71eef498b7/./src/main/java/me/lemire/longcompression/LongAs2IntsCodec.java#L109-L187
```
//@ ensures inlength == 0 ==> (inpos.get() == \old(inpos.get()) && outpos.get() == \old(outpos.get()) && java.util.stream.IntStream.range(0, in.length).allMatch(i -> in[i] == \old(java.util.Arrays.copyOf(in, in.length))[i]) && java.util.stream.IntStream.range(0, out.length).allMatch(i -> out[i] == \old(java.util.Arrays.copyOf(out, out.length))[i]));
//@ ensures inlength > 0 ==> inpos.get() == \old(inpos.get()) + inlength;
//@ ensures outpos.get() >= \old(outpos.get());
//@ ensures java.util.stream.IntStream.range(0, in.length).allMatch(i -> in[i] == \old(java.util.Arrays.copyOf(in, in.length))[i]);
//@ ensures inlength > 0 ==> java.util.stream.IntStream.range(0, \old(outpos.get())).allMatch(i -> out[i] == \old(java.util.Arrays.copyOf(out, out.length))[i]);
//@ ensures inlength > 0 ==> outpos.get() > \old(outpos.get());
//@ ensures inlength > 0 ==> java.util.stream.IntStream.of(0).allMatch(__dummy -> { int oldInPos = \old(inpos.get()); int oldOutPos = \old(outpos.get()); int longIndex = oldInPos; int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]); int[] compressedHighParts = new int[nbCompressedHighParts]; boolean highPart = false; for (int i = 0; i < nbCompressedHighParts; i++) { int nextInt; if (highPart) { nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]); } else { nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]); } compressedHighParts[i] = nextInt; highPart = !highPart; } int[] buffer = new int[in.length * 16 + 1]; IntWrapper highPartsOutPosition = new IntWrapper(); highPartsCodec.uncompress(compressedHighParts, new IntWrapper(), compressedHighParts.length, buffer, highPartsOutPosition); int[] highParts = java.util.Arrays.copyOf(buffer, highPartsOutPosition.get()); int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts; int nbCompressedLowParts; if (highPart) { nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]); } else { nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]); } highPart = !highPart; int[] compressedLowParts = new int[nbCompressedLowParts]; for (int i = 0; i < nbCompressedLowParts; i++) { int nextInt; if (highPart) { nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]); } else { nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]); } compressedLowParts[i] = nextInt; highPart = !highPart; } IntWrapper lowPartsOutPosition = new IntWrapper(); lowPartsCodec.uncompress(compressedLowParts, new IntWrapper(), compressedLowParts.length, buffer, lowPartsOutPosition); int[] lowParts = java.util.Arrays.copyOf(buffer, lowPartsOutPosition.get()); if (highParts.length != lowParts.length) return false; int produced = highParts.length; if (outpos.get() != oldOutPos + produced) return false; for (int i = 0; i < produced; i++) { if (out[oldOutPos + i] != RoaringIntPacking.pack(highParts[i], lowParts[i])) return false; } return true; });
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
===== 0 =====
```
             return;
         }
 
-        int longIndex = inpos.get();
+        int longIndex = 0; // Always starts from the beginning, ignoring inpos
 
         int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
         int[] compressedHighParts = new int[nbCompressedHighParts];
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = 0; // Always starts from the beginning, ignoring inpos

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 1 =====
```
                 compressedHighParts.length,
                 buffer,
                 highPartsOutPosition);
-        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());
+        int[] highParts = new int[highPartsOutPosition.get()]; // Allocates an array but does not copy the data
 
         // +1 as we initially read nbCompressedHighParts
         int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = new int[highPartsOutPosition.get()]; // Allocates an array but does not copy the data

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 2 =====
```
                 compressedLowParts.length,
                 buffer,
                 lowPartsOutPosition);
-        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
+        int[] lowParts = new int[lowPartsOutPosition.get()]; // Allocates an array of the correct size but does not copy the data
         assert highParts.length == lowParts.length;
 
         int outposition = outpos.get();
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = new int[lowPartsOutPosition.get()]; // Allocates an array of the correct size but does not copy the data
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 3 =====
```
         int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
         assert highParts.length == lowParts.length;
 
-        int outposition = outpos.get();
+        int outposition = 0; // Resetting output position to zero
         for (int i = 0; i < highParts.length; i++) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = 0; // Resetting output position to zero
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 4 =====
```
         int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
         assert highParts.length == lowParts.length;
 
-        int outposition = outpos.get();
+        int outposition = outpos.get() * 2; // Incorrect scaling of output position
         for (int i = 0; i < highParts.length; i++) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get() * 2; // Incorrect scaling of output position
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 5 =====
```
         int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
         assert highParts.length == lowParts.length;
 
-        int outposition = outpos.get();
+        int outposition = outpos.get() / 2; // Incorrect halving of output position
         for (int i = 0; i < highParts.length; i++) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get() / 2; // Incorrect halving of output position
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 6 =====
```
         assert highParts.length == lowParts.length;
 
         int outposition = outpos.get();
-        for (int i = 0; i < highParts.length; i++) {
+        for (int i = 0; i < highParts.length - 1; i++) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length - 1; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 7 =====
```
         assert highParts.length == lowParts.length;
 
         int outposition = outpos.get();
-        for (int i = 0; i < highParts.length; i++) {
+        for (int i = 0; i < highParts.length; i += 2) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i += 2) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 8 =====
```
         assert highParts.length == lowParts.length;
 
         int outposition = outpos.get();
-        for (int i = 0; i < highParts.length; i++) {
+        for (int i = 0; i >= highParts.length; i++) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i >= highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 9 =====
```
         assert highParts.length == lowParts.length;
 
         int outposition = outpos.get();
-        for (int i = 0; i < highParts.length; i++) {
+        for (int i = 1; i < highParts.length; i++) {
             out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
         }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 1; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 10 =====
```
 
         int outposition = outpos.get();
         for (int i = 0; i < highParts.length; i++) {
-            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
+            out[outposition++] = RoaringIntPacking.pack(0, lowParts[i]); // Always packs high part as 0
         }
 
         inpos.add(inlength);
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(0, lowParts[i]); // Always packs high part as 0
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 11 =====
```
 
         int outposition = outpos.get();
         for (int i = 0; i < highParts.length; i++) {
-            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
+            out[outposition++] = RoaringIntPacking.pack(highParts[i] + 1, lowParts[i]); // Introduces an off-by-one error in high part
         }
 
         inpos.add(inlength);
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i] + 1, lowParts[i]); // Introduces an off-by-one error in high part
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 12 =====
```
 
         int outposition = outpos.get();
         for (int i = 0; i < highParts.length; i++) {
-            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
+            out[outposition++] = RoaringIntPacking.pack(highParts[i] - 1, lowParts[i] - 1); // Introduces an off-by-one error in both parts
         }
 
         inpos.add(inlength);
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i] - 1, lowParts[i] - 1); // Introduces an off-by-one error in both parts
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 13 =====
```
 
         int outposition = outpos.get();
         for (int i = 0; i < highParts.length; i++) {
-            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
+            out[outposition++] = RoaringIntPacking.pack(highParts[i], 0); // Always packs low part as 0
         }
 
         inpos.add(inlength);
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], 0); // Always packs low part as 0
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 14 =====
```
 
         int outposition = outpos.get();
         for (int i = 0; i < highParts.length; i++) {
-            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
+            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i] + 1); // Introduces an off-by-one error in low part
         }
 
         inpos.add(inlength);
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i] + 1); // Introduces an off-by-one error in low part
        }

        inpos.add(inlength);
        outpos.set(outposition);
    }
```
===== 15 =====
```
         }
 
         inpos.add(inlength);
-        outpos.set(outposition);
+        
     }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        
    }
```
===== 16 =====
```
         }
 
         inpos.add(inlength);
-        outpos.set(outposition);
+        outpos.set(0); // Resets the output position to zero, losing all previous data
     }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(0); // Resets the output position to zero, losing all previous data
    }
```
===== 17 =====
```
         }
 
         inpos.add(inlength);
-        outpos.set(outposition);
+        outpos.set(outposition * 2); // Sets the output position to double the correct value
     }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition * 2); // Sets the output position to double the correct value
    }
```
===== 18 =====
```
         }
 
         inpos.add(inlength);
-        outpos.set(outposition);
+        outpos.set(outposition + 1); // Incorrectly increments the output position
     }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition + 1); // Incorrectly increments the output position
    }
```
===== 19 =====
```
         }
 
         inpos.add(inlength);
-        outpos.set(outposition);
+        outpos.set(outposition + lowParts.length); // Incorrectly adds the length of lowParts to the output position
     }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition + lowParts.length); // Incorrectly adds the length of lowParts to the output position
    }
```
===== 20 =====
```
         }
 
         inpos.add(inlength);
-        outpos.set(outposition);
+        outpos.set(outposition - 1); // Incorrectly decrements the output position
     }
```
```
    /**
     * inlength is ignored by this codec. We may rely on it instead of storing the compressedLowPart length
     */
    @Override
    public void uncompress(long[] in, IntWrapper inpos, int inlength, long[] out, IntWrapper outpos) {
        if (inlength == 0) {
            return;
        }

        int longIndex = inpos.get();

        int nbCompressedHighParts = RoaringIntPacking.high(in[longIndex]);
        int[] compressedHighParts = new int[nbCompressedHighParts];

        // !highPart as we just read the highPart for nbCompressedHighParts
        boolean highPart = false;
        for (int i = 0; i < nbCompressedHighParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[longIndex + (i + 1) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[longIndex + (i + 1) / 2]);
            }
            compressedHighParts[i] = nextInt;

            highPart = !highPart;
        }

        // TODO What would be a relevant buffer size?
        int[] buffer = new int[inlength * 16];

        IntWrapper highPartsOutPosition = new IntWrapper();
        highPartsCodec.uncompress(compressedHighParts,
                new IntWrapper(),
                compressedHighParts.length,
                buffer,
                highPartsOutPosition);
        int[] highParts = Arrays.copyOf(buffer, highPartsOutPosition.get());

        // +1 as we initially read nbCompressedHighParts
        int intIndexNbCompressedLowParts = longIndex * 2 + 1 + nbCompressedHighParts;
        int nbCompressedLowParts;
        if (highPart) {
            nbCompressedLowParts = RoaringIntPacking.high(in[intIndexNbCompressedLowParts / 2]);
        } else {
            nbCompressedLowParts = RoaringIntPacking.low(in[intIndexNbCompressedLowParts / 2]);
        }
        highPart = !highPart;

        int[] compressedLowParts = new int[nbCompressedLowParts];
        for (int i = 0; i < nbCompressedLowParts; i++) {
            int nextInt;
            if (highPart) {
                nextInt = RoaringIntPacking.high(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            } else {
                nextInt = RoaringIntPacking.low(in[(intIndexNbCompressedLowParts + 1 + i) / 2]);
            }
            compressedLowParts[i] = nextInt;

            highPart = !highPart;
        }

        IntWrapper lowPartsOutPosition = new IntWrapper();
        lowPartsCodec.uncompress(compressedLowParts,
                new IntWrapper(),
                compressedLowParts.length,
                buffer,
                lowPartsOutPosition);
        int[] lowParts = Arrays.copyOf(buffer, lowPartsOutPosition.get());
        assert highParts.length == lowParts.length;

        int outposition = outpos.get();
        for (int i = 0; i < highParts.length; i++) {
            out[outposition++] = RoaringIntPacking.pack(highParts[i], lowParts[i]);
        }

        inpos.add(inlength);
        outpos.set(outposition - 1); // Incorrectly decrements the output position
    }
```
