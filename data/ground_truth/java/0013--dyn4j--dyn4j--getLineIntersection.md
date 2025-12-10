https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Segment.java#L344-L395
```
//@ ensures (\result == null) <==> (Math.abs(((bp2.x - bp1.x) * (ap2.y - ap1.y) - (bp2.y - bp1.y) * (ap2.x - ap1.x))) <= Epsilon.E || Math.abs(((ap1.x - bp1.x) * (ap2.y - ap1.y) - (ap1.y - bp1.y) * (ap2.x - ap1.x))) <= Epsilon.E);
//@ ensures \result != null ==> Math.abs(((bp2.x - bp1.x) * (ap2.y - ap1.y) - (bp2.y - bp1.y) * (ap2.x - ap1.x))) > Epsilon.E && Math.abs(((ap1.x - bp1.x) * (ap2.y - ap1.y) - (ap1.y - bp1.y) * (ap2.x - ap1.x))) > Epsilon.E;
//@ ensures \result != null ==> Math.abs((\result.x - ap1.x) * (ap2.y - ap1.y) - (\result.y - ap1.y) * (ap2.x - ap1.x)) <= Epsilon.E;
//@ ensures \result != null ==> Math.abs((\result.x - bp1.x) * (bp2.y - bp1.y) - (\result.y - bp1.y) * (bp2.x - bp1.x)) <= Epsilon.E;
//@ ensures \result != null ==> Math.abs(\result.x - (bp1.x + (bp2.x - bp1.x) * (((ap1.x - bp1.x) * (ap2.y - ap1.y) - (ap1.y - bp1.y) * (ap2.x - ap1.x)) / (((bp2.x - bp1.x) * (ap2.y - ap1.y)) - ((bp2.y - bp1.y) * (ap2.x - ap1.x)))))) <= Epsilon.E;
//@ ensures \result != null ==> Math.abs(\result.y - (bp1.y + (bp2.y - bp1.y) * (((ap1.x - bp1.x) * (ap2.y - ap1.y) - (ap1.y - bp1.y) * (ap2.x - ap1.x)) / (((bp2.x - bp1.x) * (ap2.y - ap1.y)) - ((bp2.y - bp1.y) * (ap2.x - ap1.x)))))) <= Epsilon.E;
```
```
//@ ensures (\result == null) <==> (Math.abs(bp1.to(bp2).cross(ap1.to(ap2))) <= Epsilon.E || Math.abs(ap1.difference(bp1).cross(ap1.to(ap2))) <= Epsilon.E);
//@ ensures \result != null ==> Math.abs(bp1.to(bp2).cross(ap1.to(ap2))) > Epsilon.E && Math.abs(ap1.difference(bp1).cross(ap1.to(ap2))) > Epsilon.E;
//@ ensures \result != null ==> (\result.equals(bp1.add(bp1.to(bp2).product((ap1.difference(bp1).cross(ap1.to(ap2))) / (bp1.to(bp2).cross(ap1.to(ap2)))))));
//@ ensures \result != null ==> Math.abs(\result.difference(ap1).cross(ap1.to(ap2))) <= Epsilon.E && Math.abs(\result.difference(bp1).cross(bp1.to(bp2))) <= Epsilon.E;
```
[26]
===== 26 =====
```
 		// compute tb
 		double tb = ambxA / BxA;
 		// compute the intersection point
-		return B.product(tb).add(bp1);
+		return bp1; // Returns the first point instead of calculating the intersection point
 	}
```
```
	/**
	 * Returns the intersection point of the two lines or null if they are parallel or coincident.
	 * <p>
	 * If we let:
	 * <p style="white-space: pre;"> A = A<sub>p2</sub> - A<sub>p1</sub>
	 * B = B<sub>p2</sub> - B<sub>p1</sub></p>
	 * we can create two parametric equations:
	 * <p style="white-space: pre;"> Q = A<sub>p1</sub> + t<sub>a</sub>A
	 * Q = B<sub>p1</sub> + t<sub>b</sub>B</p>
	 * Where Q is the intersection point:
	 * <p style="white-space: pre;"> A<sub>p1</sub> + t<sub>a</sub>A = B<sub>p1</sub> + t<sub>b</sub>B</p>
	 * We can solve for t<sub>b</sub> by applying the cross product with A on both sides:
	 * <p style="white-space: pre;"> (A<sub>p1</sub> + t<sub>a</sub>A) x A = (B<sub>p1</sub> + t<sub>b</sub>B) x A
	 * A<sub>p1</sub> x A = B<sub>p1</sub> x A + t<sub>b</sub>B x A
	 * (A<sub>p1</sub> - B<sub>p1</sub>) x A = t<sub>b</sub>B x A
	 * t<sub>b</sub> = ((A<sub>p1</sub> - B<sub>p1</sub>) x A) / (B x A)</p>
	 * If B x A == 0 then the lines are parallel.  If both the top and bottom are zero 
	 * then the lines are coincident.
	 * <p>
	 * If the lines are parallel or coincident, null is returned.
	 * @param ap1 the first point of the first line
	 * @param ap2 the second point of the first line
	 * @param bp1 the first point of the second line
	 * @param bp2 the second point of the second line
	 * @return Vector2 the intersection point; null if the lines are parallel or coincident
	 * @see #getSegmentIntersection(Vector2, Vector2, Vector2, Vector2)
	 * @throws NullPointerException if ap1, ap2, bp1 or bp2 is null
	 * @since 3.1.1
	 */
	public static final Vector2 getLineIntersection(Vector2 ap1, Vector2 ap2, Vector2 bp1, Vector2 bp2) {
		Vector2 A = ap1.to(ap2);
		Vector2 B = bp1.to(bp2);
		
		// compute the bottom
		double BxA = B.cross(A);
		if (Math.abs(BxA) <= Epsilon.E) {
			// the lines are parallel and don't intersect
			return null;
		}
		
		// compute the top
		double ambxA = ap1.difference(bp1).cross(A);
		if (Math.abs(ambxA) <= Epsilon.E) {
			// the lines are coincident
			return null;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		// compute the intersection point
		return bp1; // Returns the first point instead of calculating the intersection point
	}
```
