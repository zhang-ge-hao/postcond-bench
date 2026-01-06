https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L164-L216
```
// @ ensures \result != null;
// @ ensures byteTab == \old(byteTab);
// @ ensures size == \old(size);
// @ ensures (pSize >= 0) ==> (currentBitIndex == \old(currentBitIndex) + ((size > \old(currentBitIndex)) ? Math.min(pSize, size - \old(currentBitIndex)) : 0));
// @ ensures (pSize >= 0) ==> (\result.length == ((Math.min(pSize, Math.max(0, size - \old(currentBitIndex)))) + 7) / 8);
// @ ensures (pSize >= 0) ==> (currentBitIndex <= size);
// @ ensures (pSize >= 0) ==> (currentBitIndex >= \old(currentBitIndex));
// @ ensures (pSize >= 0 && \old(currentBitIndex) >= size) ==> (\result.length == 0 && currentBitIndex == \old(currentBitIndex));
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
//@ ensures \result != null;
//@ ensures \result.length == (int) Math.ceil(pSize / BYTE_SIZE_F);
//@ ensures currentBitIndex == \old(currentBitIndex) + pSize;
//@ ensures (pShift || pSize % BYTE_SIZE == 0) ==> java.util.stream.IntStream.range(0, \result.length * BYTE_SIZE).allMatch(b -> ((((\result[b / BYTE_SIZE] & 0xFF) >> (BYTE_SIZE - 1 - (b % BYTE_SIZE))) & 1) == (b < pSize ? (((\old(byteTab)[(\old(currentBitIndex) + b) / BYTE_SIZE] & 0xFF) >> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + b) % BYTE_SIZE))) & 1) : 0)));
//@ ensures !pShift && pSize <= BYTE_SIZE && (\old(currentBitIndex) / BYTE_SIZE == (\old(currentBitIndex) + pSize - 1) / BYTE_SIZE) ==> java.util.stream.IntStream.range(0, BYTE_SIZE).allMatch(b -> ((((\result[0] & 0xFF) >> (BYTE_SIZE - 1 - b)) & 1) == ((b >= (\old(currentBitIndex) % BYTE_SIZE) && b < (\old(currentBitIndex) % BYTE_SIZE + pSize)) ? (((\old(byteTab)[\old(currentBitIndex) / BYTE_SIZE] & 0xFF) >> (BYTE_SIZE - 1 - b)) & 1) : 0)));

```
===== 59: failed =====
```
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
-			int val = pSize % BYTE_SIZE;
+			int val = pSize * BYTE_SIZE;
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
```
```
	/**
	 * Method to get The next bytes with the specified size
	 *
	 * @param pSize
	 *            the size in bit to read
	 * @param pShift
	 *            boolean to indicate if the data read will be shift to the
	 *            left.<br>
	 *            <ul>
	 *            <li>if true : (Ex 10110000b if we start read 2 bit at index 2
	 *            the returned data will be 11000000b)</li>
	 *            <li>if false : (Ex 10110000b if we start read 2 bit at index 2
	 *            the returned data will be 00110000b)</li>
	 *            </ul>
	 * @return a byte array
	 */
	public byte[] getNextByte(final int pSize, final boolean pShift) {
		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];

		if (currentBitIndex % BYTE_SIZE != 0) {
			int index = 0;
			int max = currentBitIndex + pSize;
			while (currentBitIndex < max) {
				int mod = currentBitIndex % BYTE_SIZE;
				int modTab = index % BYTE_SIZE;
				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
				if (pShift || pSize % BYTE_SIZE == 0) {
					if (mod != 0) {
						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
					} else {
						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
					}
				}
				tab[index / BYTE_SIZE] |= val;
				currentBitIndex += length;
				index += length;
			}
			if (!pShift && pSize % BYTE_SIZE != 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize * BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
