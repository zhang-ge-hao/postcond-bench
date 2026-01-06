https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/Bayazit.java#L404-L449
```
//@ ensures polygon.size() == \old(polygon.size());
//@ ensures polygon.equals(\old(polygon));
//@ ensures \result ==> !polygon.stream().anyMatch(v -> v == null);
//@ ensures i == \old(i) && j == \old(j);
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
//@ ensures \result == (( (isReflex(polygon.get(i == 0 ? polygon.size() - 1 : i - 1), polygon.get(i), polygon.get(i + 1 == polygon.size() ? 0 : i + 1)) ? !(leftOn(polygon.get(i), polygon.get(i == 0 ? polygon.size() - 1 : i - 1), polygon.get(j)) && rightOn(polygon.get(i), polygon.get(i + 1 == polygon.size() ? 0 : i + 1), polygon.get(j))) : !(rightOn(polygon.get(i), polygon.get(i + 1 == polygon.size() ? 0 : i + 1), polygon.get(j)) || leftOn(polygon.get(i), polygon.get(i == 0 ? polygon.size() - 1 : i - 1), polygon.get(j)))) && (isReflex(polygon.get(j == 0 ? polygon.size() - 1 : j - 1), polygon.get(j), polygon.get(j + 1 == polygon.size() ? 0 : j + 1)) ? !(leftOn(polygon.get(j), polygon.get(j == 0 ? polygon.size() - 1 : j - 1), polygon.get(i)) && rightOn(polygon.get(j), polygon.get(j + 1 == polygon.size() ? 0 : j + 1), polygon.get(i))) : !(rightOn(polygon.get(j), polygon.get(j + 1 == polygon.size() ? 0 : j + 1), polygon.get(i)) || leftOn(polygon.get(j), polygon.get(j == 0 ? polygon.size() - 1 : j - 1), polygon.get(i)))) && java.util.stream.IntStream.range(0, polygon.size()).allMatch(k -> (k == i || k == j || ((k + 1 == polygon.size() ? 0 : k + 1) == i) || ((k + 1 == polygon.size() ? 0 : k + 1) == j)) || Segment.getSegmentIntersection(polygon.get(i), polygon.get(j), polygon.get(k), polygon.get(k + 1 == polygon.size() ? 0 : k + 1)) == null)));

```
===== 0: failed =====
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
