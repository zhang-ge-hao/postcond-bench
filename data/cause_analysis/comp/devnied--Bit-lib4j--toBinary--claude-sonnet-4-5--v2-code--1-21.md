https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BytesUtils.java#L278-L297
```
//@ ensures (pBytes == null || pBytes.length == 0) ==> \result == null;
//@ ensures (pBytes != null && pBytes.length > 0) ==> \result != null;
//@ ensures (pBytes != null && pBytes.length > 0) ==> \result.length() == pBytes.length * BitUtils.BYTE_SIZE;
//@ ensures \result != null ==> \result.chars().allMatch(c -> c == '0' || c == '1');
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
//@ ensures pBytes == null || pBytes.length == 0 ==> \result == null;
//@ ensures pBytes != null && pBytes.length > 0 ==> \result != null;
//@ ensures pBytes != null && pBytes.length > 0 ==> \result.length() == pBytes.length * BitUtils.BYTE_SIZE;
//@ ensures pBytes != null && pBytes.length > 0 ==> \result.matches("[01]+");
//@ ensures pBytes != null && pBytes.length > 0 ==> new java.math.BigInteger(\result, 2).equals(new java.math.BigInteger(bytesToStringNoSpace(pBytes), HEXA));
```
===== 21: failed =====
```
 			StringBuilder build = new StringBuilder(val.toString(2));
 			// left pad with 0 to fit byte size
 			for (int i = build.length(); i < pBytes.length * BitUtils.BYTE_SIZE; i++) {
-				build.insert(0, 0);
+				build.insert(build.length(), 0);
 			}
 			ret = build.toString();
 		}
```
```
	/**
	 * Convert byte array to binary String
	 *
	 * @param pBytes
	 *            byte array to convert
	 * @return a binary representation of the byte array
	 */
	public static String toBinary(final byte[] pBytes) {
		String ret = null;
		if (pBytes != null && pBytes.length > 0) {
			BigInteger val = new BigInteger(bytesToStringNoSpace(pBytes), HEXA);
			StringBuilder build = new StringBuilder(val.toString(2));
			// left pad with 0 to fit byte size
			for (int i = build.length(); i < pBytes.length * BitUtils.BYTE_SIZE; i++) {
				build.insert(build.length(), 0);
			}
			ret = build.toString();
		}
		return ret;
	}
```
