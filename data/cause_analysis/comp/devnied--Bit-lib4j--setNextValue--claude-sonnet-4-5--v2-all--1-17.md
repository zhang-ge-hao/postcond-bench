https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L577-L613
```
//@ ensures getCurrentBitIndex() == \old(getCurrentBitIndex()) + pLength;
//@ ensures getSize() == \old(getSize());
//@ ensures byteTab.length == \old(byteTab.length);
//@ ensures pValue >= (long) Math.pow(2, Math.min(pLength, pMaxSize)) ==> (\old(currentBitIndex) >= 0 && \old(currentBitIndex) + pLength <= size);
//@ ensures pValue < (long) Math.pow(2, Math.min(pLength, pMaxSize)) ==> (\old(currentBitIndex) >= 0 && \old(currentBitIndex) + pLength <= size);
//@ ensures pLength > 0 ==> getCurrentBitIndex() > \old(getCurrentBitIndex());
//@ ensures pLength == 0 ==> getCurrentBitIndex() == \old(getCurrentBitIndex());
```
```
missing attribute validation

`byteTab` 
built-in container of scalars
```
passed
```
//@ ensures currentBitIndex >= pLength && currentBitIndex <= size;
//@ ensures java.util.stream.IntStream.range(0, pLength).allMatch(i -> (((byteTab[(currentBitIndex - pLength + i) / BYTE_SIZE] >> (BYTE_SIZE - 1 - ((currentBitIndex - pLength + i) % BYTE_SIZE))) & 1) == ((((pValue > (long)java.lang.Math.pow(2, java.lang.Math.min(pLength, pMaxSize))) ? (long)java.lang.Math.pow(2, java.lang.Math.min(pLength, pMaxSize)) - 1L : pValue) >> (pLength - 1 - i)) & 1L)));

```
===== 17: failed =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod == 0 && writeSize < BYTE_SIZE || pLength <= BYTE_SIZE) {
 				// shift left value
 				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
 			} else {
```
```
	/**
	 * Add Value to the current position with the specified size
	 *
	 * @param pValue
	 *            value to add
	 * @param pLength
	 *            length of the value
	 * @param pMaxSize
	 *            max size in bits
	 */
	private void setNextValue(final long pValue, final int pLength, final int pMaxSize) {
		long value = pValue;
		// Set to max value if pValue cannot be stored on pLength bits.
		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
		if (pValue > bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize < BYTE_SIZE || pLength <= BYTE_SIZE) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
