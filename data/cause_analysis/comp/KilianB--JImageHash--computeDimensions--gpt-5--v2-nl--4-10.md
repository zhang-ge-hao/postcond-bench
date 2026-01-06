https://github.com/KilianB/JImageHash/blob/c41bd3daca951e9397dff10a6143cfa981069cab/./src/main/java/dev/brachtendorf/jimagehash/hashAlgorithms/DifferenceHash.java#L144-L169
```
// @ ensures this.width >= 0;
// @ ensures this.height >= 0;
// @ ensures bitResolution > 0 ==> (this.width > 0 && this.height > 0);
// @ ensures this.width <= Math.max(1, bitResolution);
// @ ensures this.height <= Math.max(1, bitResolution);
// @ ensures bitResolution > 0 ==> Math.abs(this.width - this.height) <= bitResolution;
// @ ensures this.precision == \old(this.precision);
```
```
missing attribute validation

this.height
```
passed
```
//@ ensures (((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1) < \old(bitResolution)) ==> (width == (int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1 && height == (int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1);
//@ ensures (!(((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1) < \old(bitResolution)) && ((((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1))) < \old(bitResolution)) || ((((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1))) - \old(bitResolution)) > ((((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1)) - \old(bitResolution))))) ==> (width == (int) Math.round(Math.sqrt(\old(bitResolution) + 1)) && height == (int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1);
//@ ensures (!(((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1) < \old(bitResolution)) && !((((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1))) < \old(bitResolution)) || ((((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1))) - \old(bitResolution)) > ((((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) - 1) * ((int) Math.round(Math.sqrt(\old(bitResolution) + 1)) + 1)) - \old(bitResolution)))) ) ==> (width == (int) Math.round(Math.sqrt(\old(bitResolution) + 1)) && height == (int) Math.round(Math.sqrt(\old(bitResolution) + 1)));
```
===== 10: failed =====
```
 			this.width++;
 			this.height++;
 		} else {
-			if (normalBound < bitResolution || (normalBound - bitResolution) > (higherBound - bitResolution)) {
+			if (normalBound < bitResolution && (normalBound - bitResolution) == (higherBound - bitResolution)) {
 				this.height++;
 			}
 		}
```
```
	/**
	 * Compute the dimension for the resize operation. We want to get to close to a
	 * quadratic images as possible to counteract scaling bias.
	 * 
	 * @param bitResolution the desired resolution
	 */
	private void computeDimensions(int bitResolution) {
		int dimension = (int) Math.round(Math.sqrt(bitResolution + 1));

		// width //height
		int normalBound = (dimension - 1) * (dimension);
		int higherBound = (dimension - 1) * (dimension + 1);

		this.width = dimension;
		this.height = dimension;

		if (higherBound < bitResolution) {
			this.width++;
			this.height++;
		} else {
			if (normalBound < bitResolution && (normalBound - bitResolution) == (higherBound - bitResolution)) {
				this.height++;
			}
		}

	}
```
