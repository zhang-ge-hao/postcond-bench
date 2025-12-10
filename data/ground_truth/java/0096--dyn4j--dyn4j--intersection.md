https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AABB.java#L406-L433
```
//@ ensures \result == this;
//@ ensures (Math.max(\old(this.minX), \old(aabb.minX)) <= Math.min(\old(this.maxX), \old(aabb.maxX)) && Math.max(\old(this.minY), \old(aabb.minY)) <= Math.min(\old(this.maxY), \old(aabb.maxY))) ==> (this.minX == Math.max(\old(this.minX), \old(aabb.minX)) && this.minY == Math.max(\old(this.minY), \old(aabb.minY)) && this.maxX == Math.min(\old(this.maxX), \old(aabb.maxX)) && this.maxY == Math.min(\old(this.maxY), \old(aabb.maxY)));
//@ ensures !(Math.max(\old(this.minX), \old(aabb.minX)) <= Math.min(\old(this.maxX), \old(aabb.maxX)) && Math.max(\old(this.minY), \old(aabb.minY)) <= Math.min(\old(this.maxY), \old(aabb.maxY))) ==> (this.minX == 0.0 && this.minY == 0.0 && this.maxX == 0.0 && this.maxY == 0.0);
//@ ensures this.minX <= this.maxX && this.minY <= this.maxY;
```
```
//@ ensures (Math.max(\old(this.minX), \old(aabb.minX)) <= Math.min(\old(this.maxX), \old(aabb.maxX)) && Math.max(\old(this.minY), \old(aabb.minY)) <= Math.min(\old(this.maxY), \old(aabb.maxY))) ==> (this.minX == Math.max(\old(this.minX), \old(aabb.minX)) && this.minY == Math.max(\old(this.minY), \old(aabb.minY)) && this.maxX == Math.min(\old(this.maxX), \old(aabb.maxX)) && this.maxY == Math.min(\old(this.maxY), \old(aabb.maxY)) && this.minX >= \old(this.minX) && this.minX >= \old(aabb.minX) && this.minY >= \old(this.minY) && this.minY >= \old(aabb.minY) && this.maxX <= \old(this.maxX) && this.maxX <= \old(aabb.maxX) && this.maxY <= \old(this.maxY) && this.maxY <= \old(aabb.maxY) && this.maxX - this.minX >= 0.0 && this.maxY - this.minY >= 0.0 && this.maxX - this.minX <= \old(this.maxX - this.minX) && this.maxX - this.minX <= \old(aabb.maxX - aabb.minX) && this.maxY - this.minY <= \old(this.maxY - this.minY) && this.maxY - this.minY <= \old(aabb.maxY - aabb.minY));
```
[21, 23, 24]
===== 21 =====
```
 		this.maxY = Math.min(this.maxY, aabb.maxY);
 		
 		// check for a bad AABB
-		if (this.minX > this.maxX || this.minY > this.maxY) {
+		if (this.minX == this.maxX && this.minY == this.maxY) {
 			// the two AABBs were not overlapping
 			// set this AABB to a degenerate one
 			this.minX = 0.0;
```
```
	/**
	 * Performs the intersection of this {@link AABB} and the given {@link AABB} placing
	 * the result into this {@link AABB} and then returns this {@link AABB}.
	 * <p>
	 * If the given {@link AABB} does not overlap this {@link AABB}, this {@link AABB} is
	 * set to a zero {@link AABB}.
	 * @param aabb the {@link AABB} to intersect
	 * @return {@link AABB}
	 * @since 3.1.1
	 */
	public AABB intersection(AABB aabb) {
		this.minX = Math.max(this.minX, aabb.minX);
		this.minY = Math.max(this.minY, aabb.minY);
		this.maxX = Math.min(this.maxX, aabb.maxX);
		this.maxY = Math.min(this.maxY, aabb.maxY);
		
		// check for a bad AABB
		if (this.minX == this.maxX && this.minY == this.maxY) {
			// the two AABBs were not overlapping
			// set this AABB to a degenerate one
			this.minX = 0.0;
			this.minY = 0.0;
			this.maxX = 0.0;
			this.maxY = 0.0;
		}
		
		return this;
	}
```
===== 23 =====
```
 		this.maxY = Math.min(this.maxY, aabb.maxY);
 		
 		// check for a bad AABB
-		if (this.minX > this.maxX || this.minY > this.maxY) {
+		if (this.minX >= this.maxX && this.minY <= this.maxY) {
 			// the two AABBs were not overlapping
 			// set this AABB to a degenerate one
 			this.minX = 0.0;
```
```
	/**
	 * Performs the intersection of this {@link AABB} and the given {@link AABB} placing
	 * the result into this {@link AABB} and then returns this {@link AABB}.
	 * <p>
	 * If the given {@link AABB} does not overlap this {@link AABB}, this {@link AABB} is
	 * set to a zero {@link AABB}.
	 * @param aabb the {@link AABB} to intersect
	 * @return {@link AABB}
	 * @since 3.1.1
	 */
	public AABB intersection(AABB aabb) {
		this.minX = Math.max(this.minX, aabb.minX);
		this.minY = Math.max(this.minY, aabb.minY);
		this.maxX = Math.min(this.maxX, aabb.maxX);
		this.maxY = Math.min(this.maxY, aabb.maxY);
		
		// check for a bad AABB
		if (this.minX >= this.maxX && this.minY <= this.maxY) {
			// the two AABBs were not overlapping
			// set this AABB to a degenerate one
			this.minX = 0.0;
			this.minY = 0.0;
			this.maxX = 0.0;
			this.maxY = 0.0;
		}
		
		return this;
	}
```
===== 24 =====
```
 			this.maxY = 0.0;
 		}
 		
-		return this;
+		return null;
 	}
```
```
	/**
	 * Performs the intersection of this {@link AABB} and the given {@link AABB} placing
	 * the result into this {@link AABB} and then returns this {@link AABB}.
	 * <p>
	 * If the given {@link AABB} does not overlap this {@link AABB}, this {@link AABB} is
	 * set to a zero {@link AABB}.
	 * @param aabb the {@link AABB} to intersect
	 * @return {@link AABB}
	 * @since 3.1.1
	 */
	public AABB intersection(AABB aabb) {
		this.minX = Math.max(this.minX, aabb.minX);
		this.minY = Math.max(this.minY, aabb.minY);
		this.maxX = Math.min(this.maxX, aabb.maxX);
		this.maxY = Math.min(this.maxY, aabb.maxY);
		
		// check for a bad AABB
		if (this.minX > this.maxX || this.minY > this.maxY) {
			// the two AABBs were not overlapping
			// set this AABB to a degenerate one
			this.minX = 0.0;
			this.minY = 0.0;
			this.maxX = 0.0;
			this.maxY = 0.0;
		}
		
		return null;
	}
```
