https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/Bayazit.java#L404-L449
```
//@ ensures \result == (( (isReflex(polygon.get(i == 0 ? polygon.size() - 1 : i - 1), polygon.get(i), polygon.get(i + 1 == polygon.size() ? 0 : i + 1)) ? !(leftOn(polygon.get(i), polygon.get(i == 0 ? polygon.size() - 1 : i - 1), polygon.get(j)) && rightOn(polygon.get(i), polygon.get(i + 1 == polygon.size() ? 0 : i + 1), polygon.get(j))) : !(rightOn(polygon.get(i), polygon.get(i + 1 == polygon.size() ? 0 : i + 1), polygon.get(j)) || leftOn(polygon.get(i), polygon.get(i == 0 ? polygon.size() - 1 : i - 1), polygon.get(j)))) && (isReflex(polygon.get(j == 0 ? polygon.size() - 1 : j - 1), polygon.get(j), polygon.get(j + 1 == polygon.size() ? 0 : j + 1)) ? !(leftOn(polygon.get(j), polygon.get(j == 0 ? polygon.size() - 1 : j - 1), polygon.get(i)) && rightOn(polygon.get(j), polygon.get(j + 1 == polygon.size() ? 0 : j + 1), polygon.get(i))) : !(rightOn(polygon.get(j), polygon.get(j + 1 == polygon.size() ? 0 : j + 1), polygon.get(i)) || leftOn(polygon.get(j), polygon.get(j == 0 ? polygon.size() - 1 : j - 1), polygon.get(i)))) && java.util.stream.IntStream.range(0, polygon.size()).allMatch(k -> (k == i || k == j || ((k + 1 == polygon.size() ? 0 : k + 1) == i) || ((k + 1 == polygon.size() ? 0 : k + 1) == j)) || Segment.getSegmentIntersection(polygon.get(i), polygon.get(j), polygon.get(k), polygon.get(k + 1 == polygon.size() ? 0 : k + 1)) == null)));
```
```
//@ ensures \result ==> !((this.isReflex(\old(polygon).get((j + \old(polygon).size() - 1) % \old(polygon).size()), \old(polygon).get(j), \old(polygon).get((j + 1) % \old(polygon).size())) && leftOn(\old(polygon).get(j), \old(polygon).get((j + \old(polygon).size() - 1) % \old(polygon).size()), \old(polygon).get(i)) && rightOn(\old(polygon).get(j), \old(polygon).get((j + 1) % \old(polygon).size()), \old(polygon).get(i))) || (!this.isReflex(\old(polygon).get((j + \old(polygon).size() - 1) % \old(polygon).size()), \old(polygon).get(j), \old(polygon).get((j + 1) % \old(polygon).size())) && (rightOn(\old(polygon).get(j), \old(polygon).get((j + 1) % \old(polygon).size()), \old(polygon).get(i)) || leftOn(\old(polygon).get(j), \old(polygon).get((j + \old(polygon).size() - 1) % \old(polygon).size()), \old(polygon).get(i))))) 
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 25, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
===== 0 =====
```
 		Vector2 iv0, iv, iv1;
 		Vector2 jv0, jv, jv1;
 		
-		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
+		iv0 = polygon.get(i + 1 == s ? 0 : i + 1);
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i + 1 == s ? 0 : i + 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 1 =====
```
 		Vector2 iv0, iv, iv1;
 		Vector2 jv0, jv, jv1;
 		
-		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
+		iv0 = polygon.get(i - 1 < 0 ? 0 : i - 1);
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i - 1 < 0 ? 0 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 2 =====
```
 		Vector2 iv0, iv, iv1;
 		Vector2 jv0, jv, jv1;
 		
-		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
+		iv0 = polygon.get(i == 0 ? 1 : i - 1);
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 3 =====
```
 		Vector2 iv0, iv, iv1;
 		Vector2 jv0, jv, jv1;
 		
-		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
+		iv0 = polygon.get(i == 0 ? s - 1 : i + 1);
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i + 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 4 =====
```
 		Vector2 iv0, iv, iv1;
 		Vector2 jv0, jv, jv1;
 		
-		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
+		iv0 = polygon.get(i == s - 1 ? 0 : i + 1);
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == s - 1 ? 0 : i + 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 5 =====
```
 		Vector2 jv0, jv, jv1;
 		
 		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
-		iv = polygon.get(i);
+		iv = polygon.get((i + 2) % polygon.size()); // This will skip one vertex and reference the vertex after the next one.
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get((i + 2) % polygon.size()); // This will skip one vertex and reference the vertex after the next one.
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 6 =====
```
 		Vector2 jv0, jv, jv1;
 		
 		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
-		iv = polygon.get(i);
+		iv = polygon.get((i + s - 1) % s); // This will reference the last vertex instead of the current one when i is 0.
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get((i + s - 1) % s); // This will reference the last vertex instead of the current one when i is 0.
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 7 =====
```
 		Vector2 jv0, jv, jv1;
 		
 		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
-		iv = polygon.get(i);
+		iv = polygon.get(i + 1); // This will cause iv to reference the next vertex instead of the current one.
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i + 1); // This will cause iv to reference the next vertex instead of the current one.
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 8 =====
```
 		
 		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
 		iv = polygon.get(i);
-		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
+		iv1 = polygon.get(i + 1 != s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
 		jv = polygon.get(j);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 != s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 9 =====
```
 		
 		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
 		iv = polygon.get(i);
-		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
+		iv1 = polygon.get(i); // Assigns the same vertex as iv, leading to incorrect reflex checks
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
 		jv = polygon.get(j);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i); // Assigns the same vertex as iv, leading to incorrect reflex checks
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 10 =====
```
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
-		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
+		jv0 = polygon.get(j + 1 == s ? 0 : j + 1);
 		jv = polygon.get(j);
 		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j + 1 == s ? 0 : j + 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 11 =====
```
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
-		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
+		jv0 = polygon.get(j + 2 >= s ? 0 : j + 1);
 		jv = polygon.get(j);
 		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j + 2 >= s ? 0 : j + 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 12 =====
```
 		iv = polygon.get(i);
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
-		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
+		jv0 = polygon.get(j == s ? 0 : j);
 		jv = polygon.get(j);
 		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == s ? 0 : j);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 13 =====
```
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
-		jv = polygon.get(j);
+		jv = polygon.get((j + 1) % polygon.size()); // Gets the next vertex instead of the current one
 		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
 		
 		// can i see j
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get((j + 1) % polygon.size()); // Gets the next vertex instead of the current one
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 15 =====
```
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
-		jv = polygon.get(j);
+		jv = polygon.get((j - 1 + polygon.size()) % polygon.size()); // Gets the previous vertex instead of the current one
 		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
 		
 		// can i see j
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get((j - 1 + polygon.size()) % polygon.size()); // Gets the previous vertex instead of the current one
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 16 =====
```
 		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
-		jv = polygon.get(j);
+		jv = polygon.get(i); // Incorrectly assigns the vertex at index i instead of j
 		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
 		
 		// can i see j
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(i); // Incorrectly assigns the vertex at index i instead of j
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 18 =====
```
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
 		jv = polygon.get(j);
-		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
+		jv1 = polygon.get(j - 1 < 0 ? s - 1 : j - 1);
 		
 		// can i see j
 		if (this.isReflex(iv0, iv, iv1)) {
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j - 1 < 0 ? s - 1 : j - 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 19 =====
```
 		
 		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
 		jv = polygon.get(j);
-		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
+		jv1 = polygon.get(j); // Using the same index, which may lead to incorrect behavior
 		
 		// can i see j
 		if (this.isReflex(iv0, iv, iv1)) {
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j); // Using the same index, which may lead to incorrect behavior
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 21 =====
```
 		
 		// can i see j
 		if (this.isReflex(iv0, iv, iv1)) {
-			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
+			if (right(iv, iv0, jv) || left(iv, iv1, jv)) return false;
 		} else {
 			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (right(iv, iv0, jv) || left(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 22 =====
```
 		
 		// can i see j
 		if (this.isReflex(iv0, iv, iv1)) {
-			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
+			if (rightOn(iv, iv0, jv) && left(iv, iv1, jv)) return false;
 		} else {
 			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (rightOn(iv, iv0, jv) && left(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 23 =====
```
 			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
 		}
 		// can j see i
-		if (this.isReflex(jv0, jv, jv1)) {
+		if (this.isReflex(jv0, jv, iv1)) {
 			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
 		} else {
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, iv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 24 =====
```
 			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
 		}
 		// can j see i
-		if (this.isReflex(jv0, jv, jv1)) {
+		if (this.isReflex(jv0, jv, jv0)) {
 			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
 		} else {
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv0)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 25 =====
```
 		}
 		// can j see i
 		if (this.isReflex(jv0, jv, jv1)) {
-			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
+			if (leftOn(jv, jv0, iv) && leftOn(jv, jv1, iv)) return false;
 		} else {
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && leftOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 27 =====
```
 		}
 		// can j see i
 		if (this.isReflex(jv0, jv, jv1)) {
-			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
+			if (leftOn(jv, jv0, iv) || rightOn(jv, jv1, iv)) return false;
 		} else {
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) || rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 28 =====
```
 		}
 		// can j see i
 		if (this.isReflex(jv0, jv, jv1)) {
-			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
+			if (right(jv, jv0, iv) || left(jv, jv1, iv)) return false;
 		} else {
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (right(jv, jv0, iv) || left(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 30 =====
```
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
 		}
 		// make sure the segment from i to j doesn't intersect any edges
-		for (int k = 0; k < s; k++) {
+		for (int k = 0; k < s; k += 2) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
 			if (k == i || k == j || ki1 == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k += 2) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 31 =====
```
 			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
 		}
 		// make sure the segment from i to j doesn't intersect any edges
-		for (int k = 0; k < s; k++) {
+		for (int k = 0; k >= s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
 			if (k == i || k == j || ki1 == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k >= s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 32 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k != i || k == j || ki1 == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k != i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 33 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || k != j || ki1 == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k != j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 34 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || k == j || ki1 != i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 != i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 35 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || k == j || ki1 == i || ki1 != j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 != j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 36 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || k == j || ki1 == j) { /* do nothing */ }
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == j) { /* do nothing */ }
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 37 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || k == j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 38 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || ki1 == i) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || ki1 == i) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 39 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 40 =====
```
 		// make sure the segment from i to j doesn't intersect any edges
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
-			if (k == i || k == j || ki1 == i || ki1 == j) continue;
+			if (k == j || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == j || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 41 =====
```
 		for (int k = 0; k < s; k++) {
 			int ki1 = k + 1 == s ? 0 : k + 1;
 			if (k == i || k == j || ki1 == i || ki1 == j) continue;
-			Vector2 k1 = polygon.get(k);
+			Vector2 k1 = polygon.get(0); // This will always reference the first vertex, ignoring the current index k.
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(0); // This will always reference the first vertex, ignoring the current index k.
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 42 =====
```
 			int ki1 = k + 1 == s ? 0 : k + 1;
 			if (k == i || k == j || ki1 == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
-			Vector2 k2 = polygon.get(ki1);
+			Vector2 k2 = polygon.get(0);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
 			if (in != null) return false;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(0);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 43 =====
```
 			int ki1 = k + 1 == s ? 0 : k + 1;
 			if (k == i || k == j || ki1 == i || ki1 == j) continue;
 			Vector2 k1 = polygon.get(k);
-			Vector2 k2 = polygon.get(ki1);
+			Vector2 k2 = polygon.get(i);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
 			if (in != null) return false;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(i);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 44 =====
```
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
 			
-			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
+			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k1);
 			if (in != null) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k1);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 45 =====
```
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
 			
-			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
+			Vector2 in = Segment.getSegmentIntersection(iv, k1, jv, k2);
 			if (in != null) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, k1, jv, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 46 =====
```
 			Vector2 k1 = polygon.get(k);
 			Vector2 k2 = polygon.get(ki1);
 			
-			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
+			Vector2 in = Segment.getSegmentIntersection(k1, iv, jv, k2);
 			if (in != null) return false;
 		}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(k1, iv, jv, k2);
			if (in != null) return false;
		}
		
		return true;
	}
```
===== 47 =====
```
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
-			if (in != null) return false;
+			if (in != null) continue;
 		}
 		
 		return true;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) continue;
		}
		
		return true;
	}
```
===== 48 =====
```
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
-			if (in != null) return false;
+			if (in != null) return true;
 		}
 		
 		return true;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return true;
		}
		
		return true;
	}
```
===== 49 =====
```
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
-			if (in != null) return false;
+			if (in != null) return true; // Incorrectly returns true instead of false
 		}
 		
 		return true;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return true; // Incorrectly returns true instead of false
		}
		
		return true;
	}
```
===== 50 =====
```
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
-			if (in != null) return false;
+			if (in == null) return false;
 		}
 		
 		return true;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in == null) return false;
		}
		
		return true;
	}
```
===== 51 =====
```
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
-			if (in != null) return false;
+			if (in == null) return false; // This line is commented out
 		}
 		
 		return true;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in == null) return false; // This line is commented out
		}
		
		return true;
	}
```
===== 52 =====
```
 			Vector2 k2 = polygon.get(ki1);
 			
 			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
-			if (in != null) return false;
+			if (in == null) return true;
 		}
 		
 		return true;
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in == null) return true;
		}
		
		return true;
	}
```
===== 53 =====
```
 			if (in != null) return false;
 		}
 		
-		return true;
+		return false;
 	}
```
```
	/**
	 * Returns true if the vertex at index i can see the vertex at index j.
	 * @param polygon the current polygon
	 * @param i the ith vertex
	 * @param j the jth vertex
	 * @return boolean
	 * @since 3.1.10
	 */
	private boolean isVisible(List<Vector2> polygon, int i, int j) {
		int s = polygon.size();
		Vector2 iv0, iv, iv1;
		Vector2 jv0, jv, jv1;
		
		iv0 = polygon.get(i == 0 ? s - 1 : i - 1);
		iv = polygon.get(i);
		iv1 = polygon.get(i + 1 == s ? 0 : i + 1);
		
		jv0 = polygon.get(j == 0 ? s - 1 : j - 1);
		jv = polygon.get(j);
		jv1 = polygon.get(j + 1 == s ? 0 : j + 1);
		
		// can i see j
		if (this.isReflex(iv0, iv, iv1)) {
			if (leftOn(iv, iv0, jv) && rightOn(iv, iv1, jv)) return false;
		} else {
			if (rightOn(iv, iv1, jv) || leftOn(iv, iv0, jv)) return false;
		}
		// can j see i
		if (this.isReflex(jv0, jv, jv1)) {
			if (leftOn(jv, jv0, iv) && rightOn(jv, jv1, iv)) return false;
		} else {
			if (rightOn(jv, jv1, iv) || leftOn(jv, jv0, iv)) return false;
		}
		// make sure the segment from i to j doesn't intersect any edges
		for (int k = 0; k < s; k++) {
			int ki1 = k + 1 == s ? 0 : k + 1;
			if (k == i || k == j || ki1 == i || ki1 == j) continue;
			Vector2 k1 = polygon.get(k);
			Vector2 k2 = polygon.get(ki1);
			
			Vector2 in = Segment.getSegmentIntersection(iv, jv, k1, k2);
			if (in != null) return false;
		}
		
		return false;
	}
```
