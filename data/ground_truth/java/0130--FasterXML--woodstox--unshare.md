https://github.com/FasterXML/woodstox/blob/98d841d459d2a371c447e45f561b5f642717f4e0/./src/main/java/com/ctc/wstx/util/TextBuffer.java#L1144-L1173
```
//@ ensures \old(mInputStart) >= 0 ==> mInputLen == 0;
//@ ensures \old(mInputStart) >= 0 ==> mInputBuffer == null;
//@ ensures \old(mInputStart) >= 0 ==> mInputStart == -1;
//@ ensures \old(mInputStart) >= 0 ==> mSegmentSize == 0;
//@ ensures \old(mInputStart) >= 0 ==> mCurrentSize == \old(mInputLen);
//@ ensures mCurrentSegment != null ==> (\old(mInputStart) >= 0 ==> mCurrentSegment != null);
//@ ensures mCurrentSegment != null ==>  (\old(mInputStart) >= 0 ==> mCurrentSegment.length >= \old(mInputLen) + needExtra);
//@ ensures mCurrentSegment != null ==> (\old(mInputStart) >= 0 ==> size() == \old(mInputLen));
//@ ensures mCurrentSegment != null ==> (\old(mInputStart) >= 0 && \old(mInputLen) > 0 ==> java.util.stream.IntStream.range(0, \old(mInputLen)).allMatch(i -> mCurrentSegment[i] == \old(mInputBuffer)[\old(mInputStart) + i]));
//@ ensures mCurrentSegment != null ==> (\old(mInputStart) >= 0 && \old(mCurrentSegment) != null && \old(mCurrentSegment == null ? null : mCurrentSegment.length) >= \old(mInputLen) + needExtra ==> mCurrentSegment == \old(mCurrentSegment == null ? null : mCurrentSegment));
//@ ensures mCurrentSegment != null ==> (\old(mInputStart) >= 0 && (\old(mCurrentSegment == null ? null : mCurrentSegment) == null || \old(mCurrentSegment == null ? null : mCurrentSegment.length) < \old(mInputLen) + needExtra) ==> mCurrentSegment != \old(mCurrentSegment == null ? null : mCurrentSegment));
//@ ensures mResultString == \old(mResultString);
//@ ensures mResultArray == \old(mResultArray);
//@ ensures mSegments == \old(mSegments);
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
         if (mCurrentSegment == null || needed > mCurrentSegment.length) {
             mCurrentSegment = allocBuffer(needed);
         }
-        if (len > 0) {
+        if (len < 0) {
             System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
         }
         mSegmentSize = 0;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len < 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 1 =====
```
         if (mCurrentSegment == null || needed > mCurrentSegment.length) {
             mCurrentSegment = allocBuffer(needed);
         }
-        if (len > 0) {
+        if (len <= 0) {
             System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
         }
         mSegmentSize = 0;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len <= 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 2 =====
```
         if (mCurrentSegment == null || needed > mCurrentSegment.length) {
             mCurrentSegment = allocBuffer(needed);
         }
-        if (len > 0) {
+        if (len == 0) {
             System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
         }
         mSegmentSize = 0;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len == 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 3 =====
```
             mCurrentSegment = allocBuffer(needed);
         }
         if (len > 0) {
-            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
+            
         }
         mSegmentSize = 0;
         mCurrentSize = len;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len > 0) {
            
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 4 =====
```
             mCurrentSegment = allocBuffer(needed);
         }
         if (len > 0) {
-            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
+            System.arraycopy(inputBuf, start, mCurrentSegment, 0, 0); // Copies zero characters, effectively doing nothing and leaving mCurrentSegment unchanged.
         }
         mSegmentSize = 0;
         mCurrentSize = len;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len > 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, 0); // Copies zero characters, effectively doing nothing and leaving mCurrentSegment unchanged.
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 5 =====
```
             mCurrentSegment = allocBuffer(needed);
         }
         if (len > 0) {
-            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
+            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len - 1); // Copies one less character than intended, potentially losing the last character.
         }
         mSegmentSize = 0;
         mCurrentSize = len;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len > 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len - 1); // Copies one less character than intended, potentially losing the last character.
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 6 =====
```
             mCurrentSegment = allocBuffer(needed);
         }
         if (len > 0) {
-            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
+            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len / 2); // Only copies half of the intended characters, resulting in incomplete data.
         }
         mSegmentSize = 0;
         mCurrentSize = len;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len > 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len / 2); // Only copies half of the intended characters, resulting in incomplete data.
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
===== 7 =====
```
             mCurrentSegment = allocBuffer(needed);
         }
         if (len > 0) {
-            System.arraycopy(inputBuf, start, mCurrentSegment, 0, len);
+            System.arraycopy(inputBuf, start, mCurrentSegment, 1, len); // Offsets the copy by 1, potentially losing the first character.
         }
         mSegmentSize = 0;
         mCurrentSize = len;
```
```
    /*
    //////////////////////////////////////////////
    // Internal methods:
    //////////////////////////////////////////////
     */

    /**
     * Method called if/when we need to append content when we have been
     * initialized to use shared buffer.
     */
    public void unshare(int needExtra)
    {
        int len = mInputLen;
        mInputLen = 0;
        char[] inputBuf = mInputBuffer;
        mInputBuffer = null;
        int start = mInputStart;
        mInputStart = -1;

        // Is buffer big enough, or do we need to reallocate?
        int needed = len+needExtra;
        if (mCurrentSegment == null || needed > mCurrentSegment.length) {
            mCurrentSegment = allocBuffer(needed);
        }
        if (len > 0) {
            System.arraycopy(inputBuf, start, mCurrentSegment, 1, len); // Offsets the copy by 1, potentially losing the first character.
        }
        mSegmentSize = 0;
        mCurrentSize = len;
    }
```
