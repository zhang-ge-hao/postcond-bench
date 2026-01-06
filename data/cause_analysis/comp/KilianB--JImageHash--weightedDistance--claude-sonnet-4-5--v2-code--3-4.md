https://github.com/KilianB/JImageHash/blob/c41bd3daca951e9397dff10a6143cfa981069cab/./src/main/java/dev/brachtendorf/jimagehash/hash/FuzzyHash.java#L357-L388
```
//@ ensures \result >= 0.0;
//@ ensures hashLength > 0 ==> \result == (java.util.stream.IntStream.range(0, hashLength).mapToDouble(bit -> h.getBitUnsafe(bit) ? bitDistance[bit] : 1.0 - bitDistance[bit]).sum()) / hashLength;
```
```
missing attribute validation


return value content
and
missing attribute validation

return value is double
primitive-like/scalar types
```
passed
```
//@ ensures hashLength > 0 ==> 0.0 <= \result && \result <= 1.0;
//@ ensures \old(dirtyDistance) ==> !dirtyDistance;
//@ ensures \old(!dirtyDistance) ==> java.util.Arrays.equals(bitDistance, \old(bitDistance));
//@ ensures \old(dirtyDistance) ==> java.util.stream.IntStream.range(0, hashLength).allMatch(i -> bitDistance[i] == (bits[i] > 0 ? (numHashesAdded - bits[i]) / 2d / numHashesAdded : ((numHashesAdded + bits[i]) / 2d - bits[i]) / numHashesAdded));
//@ ensures hashLength > 0 ==> \result == java.util.stream.IntStream.range(0, hashLength).mapToDouble(i -> (h.getBitUnsafe(hashLength - 1 - i) ? bitDistance[hashLength - 1 - i] : 1 - bitDistance[hashLength - 1 - i])).sum() / hashLength;
```
===== 4: failed =====
```
 	 */
 	public double weightedDistance(Hash h) {
 
-		ensureUpToDateDistance();
+		for (int i = 0; i < bitDistance.length; i++) { bitDistance[i] = 0; } // Sets all distances to zero, causing incorrect distance calculations
 
 		double hammingDistance = 0;
 		for (int bit = hashLength - 1; bit >= 0; bit--) {
```
```
	/**
	 * Calculate the normalized weighted distance between the supplied hash and this
	 * hash.
	 * 
	 * Opposed to the hamming distance the weighted distance takes partial bits into
	 * account.
	 * 
	 * e.g. if this fuzzy hashes first bit hash a probability of 70% being a 0 it
	 * will have a weighted distance of .7 if it's a 1.
	 * 
	 * Be aware that this method id much more expensive than calculating the simple
	 * distance between 2 ordinary hashes. (1 quick xor vs multiple calculations per
	 * bit).
	 * 
	 * @param h The hash to calculate the distance to
	 * @return similarity value ranging between [0 - 1]
	 */
	public double weightedDistance(Hash h) {

		for (int i = 0; i < bitDistance.length; i++) { bitDistance[i] = 0; } // Sets all distances to zero, causing incorrect distance calculations

		double hammingDistance = 0;
		for (int bit = hashLength - 1; bit >= 0; bit--) {

			if (h.getBitUnsafe(bit)) {
				hammingDistance += bitDistance[bit];
			} else {
				hammingDistance += 1 - bitDistance[bit];
			}
		}
		return hammingDistance / hashLength;
	}
```
