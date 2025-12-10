https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/AbstractSimplifier.java#L165-L232
```
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) <= Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) <= Epsilon.E) ==> (\result <==> (Math.max(Math.min(a1.dot(a1.to(a2)), a2.dot(a1.to(a2))), Math.min(b1.dot(a1.to(a2)), b2.dot(a1.to(a2)))) <= Math.min(Math.max(a1.dot(a1.to(a2)), a2.dot(a1.to(a2))), Math.max(b1.dot(a1.to(a2)), b2.dot(a1.to(a2))))));
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) <= Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E) ==> !\result;
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) <= Epsilon.E) ==> !\result;
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E && \result) ==> (((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2)))) > 0.0 && ((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2)))) < 1.0);
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E && \result) ==> ((((b1.to(b2).product((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))))).add(b1)).difference(a1).dot(a1.to(a2))) / a1.to(a2).dot(a1.to(a2)) > 0.0 && (((b1.to(b2).product((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))))).add(b1)).difference(a1).dot(a1.to(a2))) / a1.to(a2).dot(a1.to(a2)) < 1.0);
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E && ((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))) > 0.0) && ((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))) < 1.0) && ((((b1.to(b2).product((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))))).add(b1)).difference(a1).dot(a1.to(a2))) / a1.to(a2).dot(a1.to(a2)) > 0.0) && ((((b1.to(b2).product((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))))).add(b1)).difference(a1).dot(a1.to(a2))) / a1.to(a2).dot(a1.to(a2)) < 1.0)) ==> \result;
```
```
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) <= Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) <= Epsilon.E) ==> (\result <==> (Math.max(Math.min(a1.dot(a1.to(a2)), a2.dot(a1.to(a2))), Math.min(b1.dot(a1.to(a2)), b2.dot(a1.to(a2)))) <= Math.min(Math.max(a1.dot(a1.to(a2)), a2.dot(a1.to(a2))), Math.max(b1.dot(a1.to(a2)), b2.dot(a1.to(a2))))));
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) <= Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E) ==> !\result;
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) <= Epsilon.E) ==> !\result;
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E && \result) ==> (((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2)))) > 0.0 && ((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2)))) < 1.0);
//@ ensures (Math.abs(b1.to(b2).cross(a1.to(a2))) > Epsilon.E && Math.abs(a1.difference(b1).cross(a1.to(a2))) > Epsilon.E && \result) ==> ((((b1.to(b2).product((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))))).add(b1)).difference(a1).dot(a1.to(a2))) / a1.to(a2).dot(a1.to(a2)) > 0.0 && (((b1.to(b2).product((a1.difference(b1).cross(a1.to(a2))) / (b1.to(b2).cross(a1.to(a2))))).add(b1)).difference(a1).dot(a1.to(a2))) / a1.to(a2).dot(a1.to(a2)) < 1.0);
```
[30, 31, 41, 48, 53, 59]
===== 30 =====
```
 		}
 		
 		// if just the top is zero, then there's no intersection
-		if (Math.abs(ambxA) <= Epsilon.E) {
+		if (Math.abs(ambxA) > Epsilon.E) {
 			return false;
 		}
```
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) > Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = B.product(tb).add(b1);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A);
		if (ta <= 0.0 || ta >= 1.0) {
			// no intersection
			return false;
		}
		
		return true;
	}
```
===== 31 =====
```
 		}
 		
 		// if just the top is zero, then there's no intersection
-		if (Math.abs(ambxA) <= Epsilon.E) {
+		if (Math.abs(ambxA) >= Epsilon.E) {
 			return false;
 		}
```
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) >= Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = B.product(tb).add(b1);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A);
		if (ta <= 0.0 || ta >= 1.0) {
			// no intersection
			return false;
		}
		
		return true;
	}
```
===== 41 =====
```
 		}
 		
 		// compute the intersection point
-		Vector2 ip = B.product(tb).add(b1);
+		Vector2 ip = A.product(tb).add(a2);
 		
 		// since both are segments we need to verify that
 		// ta is also valid.
```
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) <= Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = A.product(tb).add(a2);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A);
		if (ta <= 0.0 || ta >= 1.0) {
			// no intersection
			return false;
		}
		
		return true;
	}
```
===== 48 =====
```
 		// since both are segments we need to verify that
 		// ta is also valid.
 		// compute ta
-		double ta = ip.difference(a1).dot(A) / A.dot(A);
+		double ta = ip.difference(a1).dot(A) / A.dot(A) * 2;
 		if (ta <= 0.0 || ta >= 1.0) {
 			// no intersection
 			return false;
```
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) <= Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = B.product(tb).add(b1);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A) * 2;
		if (ta <= 0.0 || ta >= 1.0) {
			// no intersection
			return false;
		}
		
		return true;
	}
```
===== 53 =====
```
 		// ta is also valid.
 		// compute ta
 		double ta = ip.difference(a1).dot(A) / A.dot(A);
-		if (ta <= 0.0 || ta >= 1.0) {
+		if (ta < 0.0 || ta > 0.5) {
 			// no intersection
 			return false;
 		}
```
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) <= Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = B.product(tb).add(b1);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A);
		if (ta < 0.0 || ta > 0.5) {
			// no intersection
			return false;
		}
		
		return true;
	}
```
===== 59 =====
```
 			return false;
 		}
 		
-		return true;
+		return false;
 	}
```
```
	/**
	 * Returns true if the given segments intersect each other.
	 * @param a1 the first point of the first segment
	 * @param a2 the second point of the first segment
	 * @param b1 the first point of the second segment
	 * @param b2 the second point of the second segment
	 * @return boolean
	 */
	protected final boolean intersects(Vector2 a1, Vector2 a2, Vector2 b1, Vector2 b2) {
		Vector2 A = a1.to(a2);
		Vector2 B = b1.to(b2);

		// compute the bottom
		double BxA = B.cross(A);
		// compute the top
		double ambxA = a1.difference(b1).cross(A);
		
		// if the bottom is zero, then the segments are either parallel or coincident
		if (Math.abs(BxA) <= Epsilon.E) {
			// if the top is zero, then the segments are coincident
			if (Math.abs(ambxA) <= Epsilon.E) {
				// project the segment points onto the segment vector (which
				// is the same for A and B since they are coincident)
				A.normalize();
				double ad1 = a1.dot(A);
				double ad2 = a2.dot(A);
				double bd1 = b1.dot(A);
				double bd2 = b2.dot(A);
				
				// then compare their location on the number line for intersection
				Interval ia = new Interval(ad1, ad2);
				Interval ib = new Interval(bd1 < bd2 ? bd1 : bd2, bd1 > bd2 ? bd1 : bd2);
				
				if (ia.overlaps(ib)) {
					return true;
				}
			}
			
			// otherwise they are parallel
			return false;
		}
		
		// if just the top is zero, then there's no intersection
		if (Math.abs(ambxA) <= Epsilon.E) {
			return false;
		}
		
		// compute tb
		double tb = ambxA / BxA;
		if (tb <= 0.0 || tb >= 1.0) {
			// no intersection
			return false;
		}
		
		// compute the intersection point
		Vector2 ip = B.product(tb).add(b1);
		
		// since both are segments we need to verify that
		// ta is also valid.
		// compute ta
		double ta = ip.difference(a1).dot(A) / A.dot(A);
		if (ta <= 0.0 || ta >= 1.0) {
			// no intersection
			return false;
		}
		
		return false;
	}
```
