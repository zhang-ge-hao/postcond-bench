https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L577-L613
```
//@ ensures currentBitIndex >= pLength && currentBitIndex <= size;
//@ ensures java.util.stream.IntStream.range(0, pLength).allMatch(i -> (((byteTab[(currentBitIndex - pLength + i) / BYTE_SIZE] >> (BYTE_SIZE - 1 - ((currentBitIndex - pLength + i) % BYTE_SIZE))) & 1) == ((((pValue > (long)java.lang.Math.pow(2, java.lang.Math.min(pLength, pMaxSize))) ? (long)java.lang.Math.pow(2, java.lang.Math.min(pLength, pMaxSize)) - 1L : pValue) >> (pLength - 1 - i)) & 1L)));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
===== 0 =====
```
 	private void setNextValue(final long pValue, final int pLength, final int pMaxSize) {
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
-		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
+		long bitMax = (long) Math.pow(2, Math.max(pLength, pMaxSize)); // Incorrect: uses max instead of min, leading to larger than necessary bitMax.
 		if (pValue > bitMax) {
 			value = bitMax - 1;
 		}
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
		long bitMax = (long) Math.pow(2, Math.max(pLength, pMaxSize)); // Incorrect: uses max instead of min, leading to larger than necessary bitMax.
		if (pValue > bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 1 =====
```
 	private void setNextValue(final long pValue, final int pLength, final int pMaxSize) {
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
-		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
+		long bitMax = (long) Math.pow(2, pLength + pMaxSize); // Incorrect: adds pLength and pMaxSize, resulting in an excessively large bitMax.
 		if (pValue > bitMax) {
 			value = bitMax - 1;
 		}
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
		long bitMax = (long) Math.pow(2, pLength + pMaxSize); // Incorrect: adds pLength and pMaxSize, resulting in an excessively large bitMax.
		if (pValue > bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 2 =====
```
 	private void setNextValue(final long pValue, final int pLength, final int pMaxSize) {
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
-		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
+		long bitMax = (long) Math.pow(2, pMaxSize); // Incorrect: ignores pLength, leading to incorrect bit size handling.
 		if (pValue > bitMax) {
 			value = bitMax - 1;
 		}
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
		long bitMax = (long) Math.pow(2, pMaxSize); // Incorrect: ignores pLength, leading to incorrect bit size handling.
		if (pValue > bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 3 =====
```
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
-		if (pValue > bitMax) {
+		if (pValue != bitMax) {
 			value = bitMax - 1;
 		}
 		// size to wrote
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
		if (pValue != bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 4 =====
```
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
-		if (pValue > bitMax) {
+		if (pValue < bitMax) {
 			value = bitMax - 1;
 		}
 		// size to wrote
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
		if (pValue < bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 5 =====
```
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
-		if (pValue > bitMax) {
+		if (pValue <= bitMax) {
 			value = bitMax - 1;
 		}
 		// size to wrote
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
		if (pValue <= bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 6 =====
```
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
-		if (pValue > bitMax) {
+		if (pValue == bitMax) {
 			value = bitMax - 1;
 		}
 		// size to wrote
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
		if (pValue == bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 7 =====
```
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
-		if (pValue > bitMax) {
+		if (pValue >= 0) {
 			value = bitMax - 1;
 		}
 		// size to wrote
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
		if (pValue >= 0) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 8 =====
```
 		long value = pValue;
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
-		if (pValue > bitMax) {
+		if (pValue >= bitMax) {
 			value = bitMax - 1;
 		}
 		// size to wrote
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
		if (pValue >= bitMax) {
			value = bitMax - 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 9 =====
```
 		// Set to max value if pValue cannot be stored on pLength bits.
 		long bitMax = (long) Math.pow(2, Math.min(pLength, pMaxSize));
 		if (pValue > bitMax) {
-			value = bitMax - 1;
+			value = bitMax + 1;
 		}
 		// size to wrote
 		int writeSize = pLength;
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
			value = bitMax + 1;
		}
		// size to wrote
		int writeSize = pLength;
		while (writeSize > 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 10 =====
```
 		}
 		// size to wrote
 		int writeSize = pLength;
-		while (writeSize > 0) {
+		while (writeSize < 0) {
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
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
		while (writeSize < 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 11 =====
```
 		}
 		// size to wrote
 		int writeSize = pLength;
-		while (writeSize > 0) {
+		while (writeSize <= 0) {
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
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
		while (writeSize <= 0) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 12 =====
```
 		}
 		// size to wrote
 		int writeSize = pLength;
-		while (writeSize > 0) {
+		while (writeSize > 1) {
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
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
		while (writeSize > 1) {
			// modulo
			int mod = currentBitIndex % BYTE_SIZE;
			byte ret = 0;
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 13 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod != 0 && writeSize <= BYTE_SIZE && pLength < BYTE_SIZE - mod) {
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
			if (mod != 0 && writeSize <= BYTE_SIZE && pLength < BYTE_SIZE - mod) {
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
===== 14 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod != 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
			if (mod != 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 15 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod == 0 && writeSize < BYTE_SIZE && pLength <= BYTE_SIZE - mod) {
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
			if (mod == 0 && writeSize < BYTE_SIZE && pLength <= BYTE_SIZE - mod) {
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
===== 16 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod == 0 && writeSize < BYTE_SIZE && pLength > BYTE_SIZE - mod) {
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
			if (mod == 0 && writeSize < BYTE_SIZE && pLength > BYTE_SIZE - mod) {
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
===== 17 =====
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
===== 18 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE + mod) {
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE + mod) {
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
===== 19 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod == 0 && writeSize <= BYTE_SIZE || pLength >= BYTE_SIZE - mod) {
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength >= BYTE_SIZE - mod) {
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
===== 20 =====
```
 			// modulo
 			int mod = currentBitIndex % BYTE_SIZE;
 			byte ret = 0;
-			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
+			if (mod == 0 && writeSize > BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
			if (mod == 0 && writeSize > BYTE_SIZE || pLength < BYTE_SIZE - mod) {
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
===== 21 =====
```
 			byte ret = 0;
 			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
 				// shift left value
-				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
+				ret = (byte) (value << BYTE_SIZE + (writeSize + mod));
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE + (writeSize + mod));
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
===== 22 =====
```
 			byte ret = 0;
 			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
 				// shift left value
-				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
+				ret = (byte) (value << BYTE_SIZE - (writeSize - mod));
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize - mod));
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
===== 23 =====
```
 			byte ret = 0;
 			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
 				// shift left value
-				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
+				ret = (byte) (value >> BYTE_SIZE - (writeSize + mod));
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value >> BYTE_SIZE - (writeSize + mod));
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
===== 24 =====
```
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
-				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
+				ret = (byte) (value << writeSize - length - (BYTE_SIZE - length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
 			long val = Math.min(writeSize, BYTE_SIZE - mod);
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value << writeSize - length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 25 =====
```
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
-				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
+				ret = (byte) (value >> writeSize + length - (BYTE_SIZE - length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
 			long val = Math.min(writeSize, BYTE_SIZE - mod);
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize + length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 26 =====
```
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
-				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
+				ret = (byte) (value >> writeSize - length + (BYTE_SIZE - length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
 			long val = Math.min(writeSize, BYTE_SIZE - mod);
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length + (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 27 =====
```
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
-				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
+				ret = (byte) (value >> writeSize - length - (BYTE_SIZE + length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
 			long val = Math.min(writeSize, BYTE_SIZE - mod);
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE + length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 28 =====
```
 			} else {
 				// shift right
 				long length = Long.toBinaryString(value).length();
-				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
+				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length + mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
 			long val = Math.min(writeSize, BYTE_SIZE - mod);
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length + mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE - mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 29 =====
```
 				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
-			long val = Math.min(writeSize, BYTE_SIZE - mod);
+			long val = Math.min(writeSize, BYTE_SIZE + mod);
 			writeSize -= val;
 			currentBitIndex += val;
 		}
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE + mod);
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 30 =====
```
 				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
-			long val = Math.min(writeSize, BYTE_SIZE - mod);
+			long val = Math.min(writeSize, BYTE_SIZE); // This ignores the mod value, which can lead to incorrect bit alignment.
 			writeSize -= val;
 			currentBitIndex += val;
 		}
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = Math.min(writeSize, BYTE_SIZE); // This ignores the mod value, which can lead to incorrect bit alignment.
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
===== 31 =====
```
 				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
 			}
 			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
-			long val = Math.min(writeSize, BYTE_SIZE - mod);
+			long val = writeSize; // This ignores the BYTE_SIZE limit, potentially causing an overflow.
 			writeSize -= val;
 			currentBitIndex += val;
 		}
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
			if (mod == 0 && writeSize <= BYTE_SIZE || pLength < BYTE_SIZE - mod) {
				// shift left value
				ret = (byte) (value << BYTE_SIZE - (writeSize + mod));
			} else {
				// shift right
				long length = Long.toBinaryString(value).length();
				ret = (byte) (value >> writeSize - length - (BYTE_SIZE - length - mod));
			}
			byteTab[currentBitIndex / BYTE_SIZE] |= ret;
			long val = writeSize; // This ignores the BYTE_SIZE limit, potentially causing an overflow.
			writeSize -= val;
			currentBitIndex += val;
		}
	}
```
