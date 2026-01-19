https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/factory/standard/RandomBasedFactory.java#L90-L123
```
🈚️

Random used.

//@ ensures \result != null;
//@ ensures \result.version() == this.version.getValue();
//@ ensures (\result.getLeastSignificantBits() & 0xC000000000000000L) == 0x8000000000000000L;
//@ ensures (\result.getMostSignificantBits() & 0xFFFFFFFF00000000L) != 0L;
//@ ensures (\result.getMostSignificantBits() & 0x000000000000000FL) != 0L;
//@ ensures (\result.getLeastSignificantBits() & 0x00000000FFFFFFFFL) != 0L;
//@ ensures (\result.getLeastSignificantBits() & 0x00000000FFFFFFFFL) != 0x00000000FFFFFFFFL;
//@ ensures (\result.getLeastSignificantBits() & 0x000000000000000FL) != 0L;
```
```
//@ ensures \result != null;
//@ ensures \result.version() == this.version.getValue();
//@ ensures (\result.getLeastSignificantBits() & 0xC000000000000000L) == 0x8000000000000000L
```
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15]
===== 1 =====
```
 				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
 				return toUuid(msb, lsb);
 			} else {
-				final long msb = this.random.nextLong();
+				final long msb = this.random.nextLong() % 100; // Reduces the range of generated values
 				final long lsb = this.random.nextLong();
 				return toUuid(msb, lsb);
 			}
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong() % 100; // Reduces the range of generated values
				final long lsb = this.random.nextLong();
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 2 =====
```
 				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
 				return toUuid(msb, lsb);
 			} else {
-				final long msb = this.random.nextLong();
+				final long msb = this.random.nextLong() & 0xFFFFFFFFFFFFFFF0L; // Forces the last 4 bits to be zero
 				final long lsb = this.random.nextLong();
 				return toUuid(msb, lsb);
 			}
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong() & 0xFFFFFFFFFFFFFFF0L; // Forces the last 4 bits to be zero
				final long lsb = this.random.nextLong();
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 3 =====
```
 				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
 				return toUuid(msb, lsb);
 			} else {
-				final long msb = this.random.nextLong();
+				final long msb = this.random.nextLong() + 1; // Introduces a bias by adding 1
 				final long lsb = this.random.nextLong();
 				return toUuid(msb, lsb);
 			}
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong() + 1; // Introduces a bias by adding 1
				final long lsb = this.random.nextLong();
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 4 =====
```
 				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
 				return toUuid(msb, lsb);
 			} else {
-				final long msb = this.random.nextLong();
+				final long msb = this.random.nextLong() ^ 0xFFFFFFFFFFFFFFFFL; // Inverts all bits, leading to unexpected values
 				final long lsb = this.random.nextLong();
 				return toUuid(msb, lsb);
 			}
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong() ^ 0xFFFFFFFFFFFFFFFFL; // Inverts all bits, leading to unexpected values
				final long lsb = this.random.nextLong();
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 5 =====
```
 				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
 				return toUuid(msb, lsb);
 			} else {
-				final long msb = this.random.nextLong();
+				final long msb = this.random.nextLong() | 0x8000000000000000L; // Sets the most significant bit to 1
 				final long lsb = this.random.nextLong();
 				return toUuid(msb, lsb);
 			}
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong() | 0x8000000000000000L; // Sets the most significant bit to 1
				final long lsb = this.random.nextLong();
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 6 =====
```
 				return toUuid(msb, lsb);
 			} else {
 				final long msb = this.random.nextLong();
-				final long lsb = this.random.nextLong();
+				final long lsb = 0; // Setting lsb to zero, resulting in a UUID that is not unique
 				return toUuid(msb, lsb);
 			}
 		} finally {
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = 0; // Setting lsb to zero, resulting in a UUID that is not unique
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 7 =====
```
 				return toUuid(msb, lsb);
 			} else {
 				final long msb = this.random.nextLong();
-				final long lsb = this.random.nextLong();
+				final long lsb = this.random.nextLong() & 0xFFFFFFFF00000000L; // Masking the upper half, leading to incorrect UUID
 				return toUuid(msb, lsb);
 			}
 		} finally {
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong() & 0xFFFFFFFF00000000L; // Masking the upper half, leading to incorrect UUID
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 8 =====
```
 				return toUuid(msb, lsb);
 			} else {
 				final long msb = this.random.nextLong();
-				final long lsb = this.random.nextLong();
+				final long lsb = this.random.nextLong() + 1; // Incrementing the value, which may lead to duplicate UUIDs
 				return toUuid(msb, lsb);
 			}
 		} finally {
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong() + 1; // Incrementing the value, which may lead to duplicate UUIDs
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 9 =====
```
 				return toUuid(msb, lsb);
 			} else {
 				final long msb = this.random.nextLong();
-				final long lsb = this.random.nextLong();
+				final long lsb = this.random.nextLong() - 1; // Decrementing the value, which may lead to duplicate UUIDs
 				return toUuid(msb, lsb);
 			}
 		} finally {
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong() - 1; // Decrementing the value, which may lead to duplicate UUIDs
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 10 =====
```
 				return toUuid(msb, lsb);
 			} else {
 				final long msb = this.random.nextLong();
-				final long lsb = this.random.nextLong();
+				final long lsb = this.random.nextLong() | 0x00000000FFFFFFFFL; // Setting the lower half to a fixed value, leading to non-unique UUIDs
 				return toUuid(msb, lsb);
 			}
 		} finally {
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong() | 0x00000000FFFFFFFFL; // Setting the lower half to a fixed value, leading to non-unique UUIDs
				return toUuid(msb, lsb);
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 11 =====
```
 			} else {
 				final long msb = this.random.nextLong();
 				final long lsb = this.random.nextLong();
-				return toUuid(msb, lsb);
+				return UUID.randomUUID(); // Generates a completely random UUID instead of using msb and lsb
 			}
 		} finally {
 			lock.unlock();
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong();
				return UUID.randomUUID(); // Generates a completely random UUID instead of using msb and lsb
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 13 =====
```
 			} else {
 				final long msb = this.random.nextLong();
 				final long lsb = this.random.nextLong();
-				return toUuid(msb, lsb);
+				return toUuid(lsb, msb); // Swapped the order of msb and lsb
 			}
 		} finally {
 			lock.unlock();
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong();
				return toUuid(lsb, msb); // Swapped the order of msb and lsb
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 14 =====
```
 			} else {
 				final long msb = this.random.nextLong();
 				final long lsb = this.random.nextLong();
-				return toUuid(msb, lsb);
+				return toUuid(msb, 0); // Sets lsb to 0, resulting in a non-unique UUID
 			}
 		} finally {
 			lock.unlock();
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong();
				return toUuid(msb, 0); // Sets lsb to 0, resulting in a non-unique UUID
			}
		} finally {
			lock.unlock();
		}
	}
```
===== 15 =====
```
 			} else {
 				final long msb = this.random.nextLong();
 				final long lsb = this.random.nextLong();
-				return toUuid(msb, lsb);
+				return toUuid(msb, lsb & 0xFFFFFFFFFFFFFFF0L); // Modifies lsb to clear the last 4 bits, affecting UUID version
 			}
 		} finally {
 			lock.unlock();
```
```
	/**
	 * Returns a random-based UUID.
	 * 
	 * ### RFC 9562 - 4.4. Algorithms for Creating a UUID from Truly Random or
	 * Pseudo-Random Numbers
	 * 
	 * (1) Set the two most significant bits (bits 6 and 7) of the
	 * clock_seq_hi_and_reserved to zero and one, respectively.
	 * 
	 * (2) Set the four most significant bits (bits 12 through 15) of the
	 * time_hi_and_version field to the 4-bit version number from Section 4.1.3.
	 * 
	 * (3) Set all the other bits to randomly (or pseudo-randomly) chosen values.
	 * 
	 * @return a random-based UUID
	 */
	@Override
	public UUID create() {
		lock.lock();
		try {
			if (this.random instanceof SafeRandom) {
				final byte[] bytes = this.random.nextBytes(16);
				final long msb = ByteUtil.toNumber(bytes, 0, 8);
				final long lsb = ByteUtil.toNumber(bytes, 8, 16);
				return toUuid(msb, lsb);
			} else {
				final long msb = this.random.nextLong();
				final long lsb = this.random.nextLong();
				return toUuid(msb, lsb & 0xFFFFFFFFFFFFFFF0L); // Modifies lsb to clear the last 4 bits, affecting UUID version
			}
		} finally {
			lock.unlock();
		}
	}
```
