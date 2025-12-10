https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L164-L216
```
//@ ensures \result != null;
//@ ensures \result.length == (int) Math.ceil(pSize / BYTE_SIZE_F);
//@ ensures currentBitIndex == \old(currentBitIndex) + pSize;
//@ ensures (pShift || pSize % BYTE_SIZE == 0) ==> java.util.stream.IntStream.range(0, \result.length * BYTE_SIZE).allMatch(b -> ((((\result[b / BYTE_SIZE] & 0xFF) >> (BYTE_SIZE - 1 - (b % BYTE_SIZE))) & 1) == (b < pSize ? (((\old(byteTab)[(\old(currentBitIndex) + b) / BYTE_SIZE] & 0xFF) >> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + b) % BYTE_SIZE))) & 1) : 0)));
//@ ensures !pShift && pSize <= BYTE_SIZE && (\old(currentBitIndex) / BYTE_SIZE == (\old(currentBitIndex) + pSize - 1) / BYTE_SIZE) ==> java.util.stream.IntStream.range(0, BYTE_SIZE).allMatch(b -> ((((\result[0] & 0xFF) >> (BYTE_SIZE - 1 - b)) & 1) == ((b >= (\old(currentBitIndex) % BYTE_SIZE) && b < (\old(currentBitIndex) % BYTE_SIZE + pSize)) ? (((\old(byteTab)[\old(currentBitIndex) / BYTE_SIZE] & 0xFF) >> (BYTE_SIZE - 1 - b)) & 1) : 0)));
```
```
//@ ensures \result != null;
//@ ensures \result.length == (int) Math.ceil(pSize / BYTE_SIZE_F);
//@ ensures currentBitIndex == \old(currentBitIndex) + pSize;
```
[1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
===== 1 =====
```
 	public byte[] getNextByte(final int pSize, final boolean pShift) {
 		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];
 
-		if (currentBitIndex % BYTE_SIZE != 0) {
+		if (currentBitIndex % BYTE_SIZE != BYTE_SIZE) {
 			int index = 0;
 			int max = currentBitIndex + pSize;
 			while (currentBitIndex < max) {
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

		if (currentBitIndex % BYTE_SIZE != BYTE_SIZE) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 2 =====
```
 	public byte[] getNextByte(final int pSize, final boolean pShift) {
 		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];
 
-		if (currentBitIndex % BYTE_SIZE != 0) {
+		if (currentBitIndex % BYTE_SIZE < 0) {
 			int index = 0;
 			int max = currentBitIndex + pSize;
 			while (currentBitIndex < max) {
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

		if (currentBitIndex % BYTE_SIZE < 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 3 =====
```
 	public byte[] getNextByte(final int pSize, final boolean pShift) {
 		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];
 
-		if (currentBitIndex % BYTE_SIZE != 0) {
+		if (currentBitIndex % BYTE_SIZE == 0) {
 			int index = 0;
 			int max = currentBitIndex + pSize;
 			while (currentBitIndex < max) {
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

		if (currentBitIndex % BYTE_SIZE == 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 4 =====
```
 	public byte[] getNextByte(final int pSize, final boolean pShift) {
 		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];
 
-		if (currentBitIndex % BYTE_SIZE != 0) {
+		if (currentBitIndex % BYTE_SIZE == 1) {
 			int index = 0;
 			int max = currentBitIndex + pSize;
 			while (currentBitIndex < max) {
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

		if (currentBitIndex % BYTE_SIZE == 1) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 5 =====
```
 	public byte[] getNextByte(final int pSize, final boolean pShift) {
 		byte[] tab = new byte[(int) Math.ceil(pSize / BYTE_SIZE_F)];
 
-		if (currentBitIndex % BYTE_SIZE != 0) {
+		if (currentBitIndex * BYTE_SIZE != 0) {
 			int index = 0;
 			int max = currentBitIndex + pSize;
 			while (currentBitIndex < max) {
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

		if (currentBitIndex * BYTE_SIZE != 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 12 =====
```
 			while (currentBitIndex < max) {
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
-				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
+				int length = Math.min(max - currentBitIndex, BYTE_SIZE - mod); // Ignoring modTab, which may lead to incorrect length calculation
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
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
				int length = Math.min(max - currentBitIndex, BYTE_SIZE - mod); // Ignoring modTab, which may lead to incorrect length calculation
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 13 =====
```
 			while (currentBitIndex < max) {
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
-				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
+				int length = Math.min(max - currentBitIndex, BYTE_SIZE); // Using BYTE_SIZE directly instead of considering modTab
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
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
				int length = Math.min(max - currentBitIndex, BYTE_SIZE); // Using BYTE_SIZE directly instead of considering modTab
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 14 =====
```
 			while (currentBitIndex < max) {
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
-				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
+				int length = Math.min(max - currentBitIndex, Math.max(BYTE_SIZE - mod, BYTE_SIZE - modTab)); // Using Math.max instead of Math.min for one of the parameters
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
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
				int length = Math.min(max - currentBitIndex, Math.max(BYTE_SIZE - mod, BYTE_SIZE - modTab)); // Using Math.max instead of Math.min for one of the parameters
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 15 =====
```
 			while (currentBitIndex < max) {
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
-				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
+				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE + mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
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
				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE + mod, BYTE_SIZE - modTab));
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 16 =====
```
 			while (currentBitIndex < max) {
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
-				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
+				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE + modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
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
				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE + modTab));
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 17 =====
```
 			while (currentBitIndex < max) {
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
-				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
+				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab) + 1); // Adding 1 to the result, which can lead to out-of-bounds access
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
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
				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab) + 1); // Adding 1 to the result, which can lead to out-of-bounds access
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 18 =====
```
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
-				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
+				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length) & 0x00); // Masking with 0, resulting in always 0
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
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
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length) & 0x00); // Masking with 0, resulting in always 0
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 19 =====
```
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
-				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
+				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length) >> 1); // Right shifting the mask, losing bits
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
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
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length) >> 1); // Right shifting the mask, losing bits
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 20 =====
```
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
-				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
+				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length) | 0x01); // Forcing the least significant bit to 1
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
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
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length) | 0x01); // Forcing the least significant bit to 1
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 21 =====
```
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
-				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
+				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & ~getMask(mod, length)); // Using NOT on the mask, inverting the bits
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
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
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & ~getMask(mod, length)); // Using NOT on the mask, inverting the bits
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 22 =====
```
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
-				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
+				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] | getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
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
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] | getMask(mod, length));
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 23 =====
```
 				int mod = currentBitIndex % BYTE_SIZE;
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
-				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
+				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] | getMask(mod, length)); // Using OR instead of AND
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
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
				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] | getMask(mod, length)); // Using OR instead of AND
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 24 =====
```
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
-				if (pShift || pSize % BYTE_SIZE == 0) {
+				if (!pShift && pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
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
				if (!pShift && pSize % BYTE_SIZE == 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 25 =====
```
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
-				if (pShift || pSize % BYTE_SIZE == 0) {
+				if (!pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
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
				if (!pShift || pSize % BYTE_SIZE == 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 26 =====
```
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
-				if (pShift || pSize % BYTE_SIZE == 0) {
+				if (pShift && pSize % BYTE_SIZE != 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
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
				if (pShift && pSize % BYTE_SIZE != 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 27 =====
```
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
-				if (pShift || pSize % BYTE_SIZE == 0) {
+				if (pShift && pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
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
				if (pShift && pSize % BYTE_SIZE == 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 28 =====
```
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
-				if (pShift || pSize % BYTE_SIZE == 0) {
+				if (pShift || pSize % BYTE_SIZE != 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
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
				if (pShift || pSize % BYTE_SIZE != 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 29 =====
```
 				int modTab = index % BYTE_SIZE;
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
-				if (pShift || pSize % BYTE_SIZE == 0) {
+				if (pShift || pSize * BYTE_SIZE == 0) {
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
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
				if (pShift || pSize * BYTE_SIZE == 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 30 =====
```
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
-					if (mod != 0) {
+					if (mod < 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
					if (mod < 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 31 =====
```
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
-					if (mod != 0) {
+					if (mod == 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
					if (mod == 0) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 32 =====
```
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
-					if (mod != 0) {
+					if (mod == 1) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
					if (mod == 1) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 33 =====
```
 				int length = Math.min(max - currentBitIndex, Math.min(BYTE_SIZE - mod, BYTE_SIZE - modTab));
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
-					if (mod != 0) {
+					if (mod == BYTE_SIZE) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
					if (mod == BYTE_SIZE) {
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 34 =====
```
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
-						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
+						val = (byte) (val & DEFAULT_VALUE); // Incorrectly masks the value instead of shifting, leading to incorrect data
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
						val = (byte) (val & DEFAULT_VALUE); // Incorrectly masks the value instead of shifting, leading to incorrect data
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 35 =====
```
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
-						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
+						val = (byte) (val << (mod + 1)); // Shifts left by one more than intended, causing data loss
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
						val = (byte) (val << (mod + 1)); // Shifts left by one more than intended, causing data loss
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 36 =====
```
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
-						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
+						val = (byte) (val << 0); // Shifts left by zero, effectively doing nothing and not modifying the value
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
						val = (byte) (val << 0); // Shifts left by zero, effectively doing nothing and not modifying the value
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 37 =====
```
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
-						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
+						val = (byte) (val << Math.max(mod, BYTE_SIZE - length)); // Uses max instead of min, potentially shifting too much
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
						val = (byte) (val << Math.max(mod, BYTE_SIZE - length)); // Uses max instead of min, potentially shifting too much
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 38 =====
```
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
-						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
+						val = (byte) (val >> Math.min(mod, BYTE_SIZE - length));
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
						val = (byte) (val >> Math.min(mod, BYTE_SIZE - length));
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 39 =====
```
 				byte val = (byte) (byteTab[currentBitIndex / BYTE_SIZE] & getMask(mod, length));
 				if (pShift || pSize % BYTE_SIZE == 0) {
 					if (mod != 0) {
-						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
+						val = (byte) (val >> Math.min(mod, BYTE_SIZE - length)); // Incorrectly shifts right instead of left
 					} else {
 						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
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
						val = (byte) (val >> Math.min(mod, BYTE_SIZE - length)); // Incorrectly shifts right instead of left
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 40 =====
```
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
-						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
+						val = (byte) ((val & DEFAULT_VALUE) << modTab);
 					}
 				}
 				tab[index / BYTE_SIZE] |= val;
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
						val = (byte) ((val & DEFAULT_VALUE) << modTab);
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 41 =====
```
 					if (mod != 0) {
 						val = (byte) (val << Math.min(mod, BYTE_SIZE - length));
 					} else {
-						val = (byte) ((val & DEFAULT_VALUE) >> modTab);
+						val = (byte) ((val | DEFAULT_VALUE) >> modTab);
 					}
 				}
 				tab[index / BYTE_SIZE] |= val;
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
						val = (byte) ((val | DEFAULT_VALUE) >> modTab);
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 42 =====
```
 				currentBitIndex += length;
 				index += length;
 			}
-			if (!pShift && pSize % BYTE_SIZE != 0) {
+			if (!pShift && pSize % BYTE_SIZE == 0) {
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
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
			if (!pShift && pSize % BYTE_SIZE == 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 43 =====
```
 				currentBitIndex += length;
 				index += length;
 			}
-			if (!pShift && pSize % BYTE_SIZE != 0) {
+			if (!pShift && pSize * BYTE_SIZE != 0) {
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
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
			if (!pShift && pSize * BYTE_SIZE != 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 44 =====
```
 				currentBitIndex += length;
 				index += length;
 			}
-			if (!pShift && pSize % BYTE_SIZE != 0) {
+			if (!pShift || pSize % BYTE_SIZE == 0) {
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
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
			if (!pShift || pSize % BYTE_SIZE == 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 45 =====
```
 				currentBitIndex += length;
 				index += length;
 			}
-			if (!pShift && pSize % BYTE_SIZE != 0) {
+			if (pShift && pSize % BYTE_SIZE != 0) {
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
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
			if (pShift && pSize % BYTE_SIZE != 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 46 =====
```
 				currentBitIndex += length;
 				index += length;
 			}
-			if (!pShift && pSize % BYTE_SIZE != 0) {
+			if (pShift && pSize % BYTE_SIZE == 0) {
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
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
			if (pShift && pSize % BYTE_SIZE == 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 47 =====
```
 				currentBitIndex += length;
 				index += length;
 			}
-			if (!pShift && pSize % BYTE_SIZE != 0) {
+			if (pSize % BYTE_SIZE == 0) {
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
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
			if (pSize % BYTE_SIZE == 0) {
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 48 =====
```
 				index += length;
 			}
 			if (!pShift && pSize % BYTE_SIZE != 0) {
-				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
+				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max + pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
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
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max + pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 49 =====
```
 				index += length;
 			}
 			if (!pShift && pSize % BYTE_SIZE != 0) {
-				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
+				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize + 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
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
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize + 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 50 =====
```
 				index += length;
 			}
 			if (!pShift && pSize % BYTE_SIZE != 0) {
-				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
+				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, 0));
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
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
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, 0));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 51 =====
```
 				index += length;
 			}
 			if (!pShift && pSize % BYTE_SIZE != 0) {
-				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
+				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE / 2));
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
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
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE / 2));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 52 =====
```
 				index += length;
 			}
 			if (!pShift && pSize % BYTE_SIZE != 0) {
-				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
+				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) * BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
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
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) * BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 53 =====
```
 				index += length;
 			}
 			if (!pShift && pSize % BYTE_SIZE != 0) {
-				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
+				tab[tab.length - 1] = (byte) (tab[tab.length - 1] | getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
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
				tab[tab.length - 1] = (byte) (tab[tab.length - 1] | getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
			}
		} else {
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 54 =====
```
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
-			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
+			
 			int val = pSize % BYTE_SIZE;
 			if (val == 0) {
 				val = BYTE_SIZE;
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
			
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 55 =====
```
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
-			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
+			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, 0); // Copies zero bytes, resulting in empty output
 			int val = pSize % BYTE_SIZE;
 			if (val == 0) {
 				val = BYTE_SIZE;
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
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, 0); // Copies zero bytes, resulting in empty output
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 56 =====
```
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
-			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
+			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length - (tab.length % 2)); // Copies an even number of bytes, potentially losing data
 			int val = pSize % BYTE_SIZE;
 			if (val == 0) {
 				val = BYTE_SIZE;
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
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length - (tab.length % 2)); // Copies an even number of bytes, potentially losing data
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 57 =====
```
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
-			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
+			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length - 1); // Off-by-one error
 			int val = pSize % BYTE_SIZE;
 			if (val == 0) {
 				val = BYTE_SIZE;
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
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length - 1); // Off-by-one error
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 58 =====
```
 				tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((max - pSize - 1) % BYTE_SIZE, BYTE_SIZE));
 			}
 		} else {
-			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
+			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length / 2); // Only copies half of the data
 			int val = pSize % BYTE_SIZE;
 			if (val == 0) {
 				val = BYTE_SIZE;
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
			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length / 2); // Only copies half of the data
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 59 =====
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
===== 60 =====
```
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
 			int val = pSize % BYTE_SIZE;
-			if (val == 0) {
+			if (val != 0) {
 				val = BYTE_SIZE;
 			}
 			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
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
			int val = pSize % BYTE_SIZE;
			if (val != 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 61 =====
```
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
 			int val = pSize % BYTE_SIZE;
-			if (val == 0) {
+			if (val < BYTE_SIZE) {
 				val = BYTE_SIZE;
 			}
 			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
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
			int val = pSize % BYTE_SIZE;
			if (val < BYTE_SIZE) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 62 =====
```
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
 			int val = pSize % BYTE_SIZE;
-			if (val == 0) {
+			if (val == BYTE_SIZE) {
 				val = BYTE_SIZE;
 			}
 			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
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
			int val = pSize % BYTE_SIZE;
			if (val == BYTE_SIZE) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 63 =====
```
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
 			int val = pSize % BYTE_SIZE;
-			if (val == 0) {
+			if (val > 0) {
 				val = BYTE_SIZE;
 			}
 			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
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
			int val = pSize % BYTE_SIZE;
			if (val > 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 64 =====
```
 		} else {
 			System.arraycopy(byteTab, currentBitIndex / BYTE_SIZE, tab, 0, tab.length);
 			int val = pSize % BYTE_SIZE;
-			if (val == 0) {
+			if (val >= 0) {
 				val = BYTE_SIZE;
 			}
 			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
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
			int val = pSize % BYTE_SIZE;
			if (val >= 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 65 =====
```
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
-			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
+			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((currentBitIndex + 1) % BYTE_SIZE, val));
 			currentBitIndex += pSize;
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask((currentBitIndex + 1) % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 66 =====
```
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
-			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
+			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val + 1));
 			currentBitIndex += pSize;
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val + 1));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 67 =====
```
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
-			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
+			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex * BYTE_SIZE, val));
 			currentBitIndex += pSize;
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex * BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 68 =====
```
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
-			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
+			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & ~getMask(currentBitIndex % BYTE_SIZE, val));
 			currentBitIndex += pSize;
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & ~getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 69 =====
```
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
-			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
+			tab[tab.length - 1] = (byte) (tab[tab.length - 1] ^ getMask(currentBitIndex % BYTE_SIZE, val));
 			currentBitIndex += pSize;
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] ^ getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
===== 70 =====
```
 			if (val == 0) {
 				val = BYTE_SIZE;
 			}
-			tab[tab.length - 1] = (byte) (tab[tab.length - 1] & getMask(currentBitIndex % BYTE_SIZE, val));
+			tab[tab.length - 1] = (byte) (tab[tab.length - 1] | getMask(currentBitIndex % BYTE_SIZE, val));
 			currentBitIndex += pSize;
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
			int val = pSize % BYTE_SIZE;
			if (val == 0) {
				val = BYTE_SIZE;
			}
			tab[tab.length - 1] = (byte) (tab[tab.length - 1] | getMask(currentBitIndex % BYTE_SIZE, val));
			currentBitIndex += pSize;
		}

		return tab;
	}
```
