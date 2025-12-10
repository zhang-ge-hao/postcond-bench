https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/hull/LinkedVertexHull.java#L90-L189
```
//@ ensures \result != null;
//@ ensures \result.leftMost == left.leftMost;
//@ ensures \result.rightMost == right.rightMost;
//@ ensures \old(left.size) >= 1 && \old(right.size) >= 1 ==> \result.size >= 2;
//@ ensures \result.size >= 1 && \result.size <= \old(left.size + right.size);
//@ ensures java.util.Arrays.stream(\result.toArray()).allMatch(p -> java.util.Arrays.asList(\old(left.toArray())).contains(p) || java.util.Arrays.asList(\old(right.toArray())).contains(p));
//@ ensures (\result.size < 3) || java.util.stream.IntStream.range(0, \result.size).allMatch(i -> RobustGeometry.getLocation(\result.toArray()[(i+2) % \result.size], \result.toArray()[i], \result.toArray()[(i+1) % \result.size]) > 0);
```
```
//@ ensures \result.leftMost == left.leftMost;
//@ ensures \result.rightMost == right.rightMost;
//@ ensures \result.size >= 1;
//@ ensures java.util.Arrays.stream(\result.toArray()).allMatch(p -> java.util.Arrays.asList(\old(left.toArray())).contains(p) || java.util.Arrays.asList(\old(right.toArray())).contains(p));
//@ ensures (\result.size < 3) || java.util.stream.IntStream.range(0, \result.size).allMatch(i -> RobustGeometry.getLocation(\result.toArray()[(i+2) % \result.size], \result.toArray()[i], \result.toArray()[(i+1) % \result.size]) >= 0);
```
[1, 10, 11, 12]
===== 1 =====
```
 				limitRightU--;
 			}
 			
-			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) <= 0) {
+			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) < 0) {
 				lu = lu.prev;
 				limitLeftU--;
 			}
```
```
	/**
	 * Merges the two given convex {@link LinkedVertexHull}s into one convex {@link LinkedVertexHull}.
	 * <p>
	 * The left {@link LinkedVertexHull} should contain only points whose x coordinates are
	 * less than all the points in the right {@link LinkedVertexHull}.
	 * @param left the left convex {@link LinkedVertexHull}
	 * @param right the right convex {@link LinkedVertexHull}
	 * @return {@link LinkedVertexHull} the merged convex hull
	 */
	public static final LinkedVertexHull merge(LinkedVertexHull left, LinkedVertexHull right) {
		// This merge algorithm handles all cases, including point-point and point-segment without special cases.
		// It finds the upper and lower edges that connect the two hulls such that the resulting hull remains convex
		
		LinkedVertexHull hull = new LinkedVertexHull();
		hull.leftMost = left.leftMost;
		hull.rightMost = right.rightMost;
		
		LinkedVertex lu = left.rightMost;
		LinkedVertex ru = right.leftMost;
		
		// We don't use strict inequalities when checking the result of getLocation
		// so we can remove coincident points in the hull.
		// As a result we must limit the number of loops that go to the left or right
		// because else ru = ru.prev can loop over and never terminate
		// We can walk at most side.size - 1 before looping over
		int limitRightU = right.size - 1;
		int limitLeftU = left.size - 1;
		
		while (true) {
			LinkedVertex prevLu = lu;
			LinkedVertex prevRu = ru;
			
			while (limitRightU > 0 && RobustGeometry.getLocation(ru.next.point, lu.point, ru.point) <= 0) {
				ru = ru.next;
				limitRightU--;
			}
			
			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) < 0) {
				lu = lu.prev;
				limitLeftU--;
			}
			
			// If no progress is made there's nothing else to do
			if (lu == prevLu && ru == prevRu) {
				break;
			}
		}
		
		// Same as before, for the other side
		
		LinkedVertex ll = left.rightMost;
		LinkedVertex rl = right.leftMost;
		
		int limitRightL = right.size - 1;
		int limitLeftL = left.size - 1;
		
		while (true) {
			LinkedVertex prevLl = ll;
			LinkedVertex prevRl = rl;
			
			while (limitRightL > 0 && RobustGeometry.getLocation(rl.prev.point, ll.point, rl.point) >= 0) {
				rl = rl.prev;
				limitRightL--;
			}
			
			while (limitLeftL > 0 && RobustGeometry.getLocation(ll.next.point, ll.point, rl.point) >= 0) {
				ll = ll.next;
				limitLeftL--;
			}
			
			// If no progress is made there's nothing else to do
			if (ll == prevLl && rl == prevRl) {
				break;
			}
		}
		
		// link the hull
		lu.next = ru;
		ru.prev = lu;
		
		ll.prev = rl;
		rl.next = ll;
		
		// We could compute size with a closed-form type based on the four values
		// of limitLeft/Right/L/U but it is not straightforward and there is no observable
		// speed gain. So use a simple loop instead
		int size = 0;
		LinkedVertex v = lu;
		
		do {
			size ++;
			v = v.next;
		} while (v != lu);
		
		// set the size
		hull.size = size;
		
		// return the merged hull
		return hull;
	}
```
===== 10 =====
```
 		do {
 			size ++;
 			v = v.next;
-		} while (v != lu);
+		} while (size < 0);
 		
 		// set the size
 		hull.size = size;
```
```
	/**
	 * Merges the two given convex {@link LinkedVertexHull}s into one convex {@link LinkedVertexHull}.
	 * <p>
	 * The left {@link LinkedVertexHull} should contain only points whose x coordinates are
	 * less than all the points in the right {@link LinkedVertexHull}.
	 * @param left the left convex {@link LinkedVertexHull}
	 * @param right the right convex {@link LinkedVertexHull}
	 * @return {@link LinkedVertexHull} the merged convex hull
	 */
	public static final LinkedVertexHull merge(LinkedVertexHull left, LinkedVertexHull right) {
		// This merge algorithm handles all cases, including point-point and point-segment without special cases.
		// It finds the upper and lower edges that connect the two hulls such that the resulting hull remains convex
		
		LinkedVertexHull hull = new LinkedVertexHull();
		hull.leftMost = left.leftMost;
		hull.rightMost = right.rightMost;
		
		LinkedVertex lu = left.rightMost;
		LinkedVertex ru = right.leftMost;
		
		// We don't use strict inequalities when checking the result of getLocation
		// so we can remove coincident points in the hull.
		// As a result we must limit the number of loops that go to the left or right
		// because else ru = ru.prev can loop over and never terminate
		// We can walk at most side.size - 1 before looping over
		int limitRightU = right.size - 1;
		int limitLeftU = left.size - 1;
		
		while (true) {
			LinkedVertex prevLu = lu;
			LinkedVertex prevRu = ru;
			
			while (limitRightU > 0 && RobustGeometry.getLocation(ru.next.point, lu.point, ru.point) <= 0) {
				ru = ru.next;
				limitRightU--;
			}
			
			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) <= 0) {
				lu = lu.prev;
				limitLeftU--;
			}
			
			// If no progress is made there's nothing else to do
			if (lu == prevLu && ru == prevRu) {
				break;
			}
		}
		
		// Same as before, for the other side
		
		LinkedVertex ll = left.rightMost;
		LinkedVertex rl = right.leftMost;
		
		int limitRightL = right.size - 1;
		int limitLeftL = left.size - 1;
		
		while (true) {
			LinkedVertex prevLl = ll;
			LinkedVertex prevRl = rl;
			
			while (limitRightL > 0 && RobustGeometry.getLocation(rl.prev.point, ll.point, rl.point) >= 0) {
				rl = rl.prev;
				limitRightL--;
			}
			
			while (limitLeftL > 0 && RobustGeometry.getLocation(ll.next.point, ll.point, rl.point) >= 0) {
				ll = ll.next;
				limitLeftL--;
			}
			
			// If no progress is made there's nothing else to do
			if (ll == prevLl && rl == prevRl) {
				break;
			}
		}
		
		// link the hull
		lu.next = ru;
		ru.prev = lu;
		
		ll.prev = rl;
		rl.next = ll;
		
		// We could compute size with a closed-form type based on the four values
		// of limitLeft/Right/L/U but it is not straightforward and there is no observable
		// speed gain. So use a simple loop instead
		int size = 0;
		LinkedVertex v = lu;
		
		do {
			size ++;
			v = v.next;
		} while (size < 0);
		
		// set the size
		hull.size = size;
		
		// return the merged hull
		return hull;
	}
```
===== 11 =====
```
 		do {
 			size ++;
 			v = v.next;
-		} while (v != lu);
+		} while (size <= 0);
 		
 		// set the size
 		hull.size = size;
```
```
	/**
	 * Merges the two given convex {@link LinkedVertexHull}s into one convex {@link LinkedVertexHull}.
	 * <p>
	 * The left {@link LinkedVertexHull} should contain only points whose x coordinates are
	 * less than all the points in the right {@link LinkedVertexHull}.
	 * @param left the left convex {@link LinkedVertexHull}
	 * @param right the right convex {@link LinkedVertexHull}
	 * @return {@link LinkedVertexHull} the merged convex hull
	 */
	public static final LinkedVertexHull merge(LinkedVertexHull left, LinkedVertexHull right) {
		// This merge algorithm handles all cases, including point-point and point-segment without special cases.
		// It finds the upper and lower edges that connect the two hulls such that the resulting hull remains convex
		
		LinkedVertexHull hull = new LinkedVertexHull();
		hull.leftMost = left.leftMost;
		hull.rightMost = right.rightMost;
		
		LinkedVertex lu = left.rightMost;
		LinkedVertex ru = right.leftMost;
		
		// We don't use strict inequalities when checking the result of getLocation
		// so we can remove coincident points in the hull.
		// As a result we must limit the number of loops that go to the left or right
		// because else ru = ru.prev can loop over and never terminate
		// We can walk at most side.size - 1 before looping over
		int limitRightU = right.size - 1;
		int limitLeftU = left.size - 1;
		
		while (true) {
			LinkedVertex prevLu = lu;
			LinkedVertex prevRu = ru;
			
			while (limitRightU > 0 && RobustGeometry.getLocation(ru.next.point, lu.point, ru.point) <= 0) {
				ru = ru.next;
				limitRightU--;
			}
			
			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) <= 0) {
				lu = lu.prev;
				limitLeftU--;
			}
			
			// If no progress is made there's nothing else to do
			if (lu == prevLu && ru == prevRu) {
				break;
			}
		}
		
		// Same as before, for the other side
		
		LinkedVertex ll = left.rightMost;
		LinkedVertex rl = right.leftMost;
		
		int limitRightL = right.size - 1;
		int limitLeftL = left.size - 1;
		
		while (true) {
			LinkedVertex prevLl = ll;
			LinkedVertex prevRl = rl;
			
			while (limitRightL > 0 && RobustGeometry.getLocation(rl.prev.point, ll.point, rl.point) >= 0) {
				rl = rl.prev;
				limitRightL--;
			}
			
			while (limitLeftL > 0 && RobustGeometry.getLocation(ll.next.point, ll.point, rl.point) >= 0) {
				ll = ll.next;
				limitLeftL--;
			}
			
			// If no progress is made there's nothing else to do
			if (ll == prevLl && rl == prevRl) {
				break;
			}
		}
		
		// link the hull
		lu.next = ru;
		ru.prev = lu;
		
		ll.prev = rl;
		rl.next = ll;
		
		// We could compute size with a closed-form type based on the four values
		// of limitLeft/Right/L/U but it is not straightforward and there is no observable
		// speed gain. So use a simple loop instead
		int size = 0;
		LinkedVertex v = lu;
		
		do {
			size ++;
			v = v.next;
		} while (size <= 0);
		
		// set the size
		hull.size = size;
		
		// return the merged hull
		return hull;
	}
```
===== 12 =====
```
 		do {
 			size ++;
 			v = v.next;
-		} while (v != lu);
+		} while (v == lu);
 		
 		// set the size
 		hull.size = size;
```
```
	/**
	 * Merges the two given convex {@link LinkedVertexHull}s into one convex {@link LinkedVertexHull}.
	 * <p>
	 * The left {@link LinkedVertexHull} should contain only points whose x coordinates are
	 * less than all the points in the right {@link LinkedVertexHull}.
	 * @param left the left convex {@link LinkedVertexHull}
	 * @param right the right convex {@link LinkedVertexHull}
	 * @return {@link LinkedVertexHull} the merged convex hull
	 */
	public static final LinkedVertexHull merge(LinkedVertexHull left, LinkedVertexHull right) {
		// This merge algorithm handles all cases, including point-point and point-segment without special cases.
		// It finds the upper and lower edges that connect the two hulls such that the resulting hull remains convex
		
		LinkedVertexHull hull = new LinkedVertexHull();
		hull.leftMost = left.leftMost;
		hull.rightMost = right.rightMost;
		
		LinkedVertex lu = left.rightMost;
		LinkedVertex ru = right.leftMost;
		
		// We don't use strict inequalities when checking the result of getLocation
		// so we can remove coincident points in the hull.
		// As a result we must limit the number of loops that go to the left or right
		// because else ru = ru.prev can loop over and never terminate
		// We can walk at most side.size - 1 before looping over
		int limitRightU = right.size - 1;
		int limitLeftU = left.size - 1;
		
		while (true) {
			LinkedVertex prevLu = lu;
			LinkedVertex prevRu = ru;
			
			while (limitRightU > 0 && RobustGeometry.getLocation(ru.next.point, lu.point, ru.point) <= 0) {
				ru = ru.next;
				limitRightU--;
			}
			
			while (limitLeftU > 0 && RobustGeometry.getLocation(lu.prev.point, lu.point, ru.point) <= 0) {
				lu = lu.prev;
				limitLeftU--;
			}
			
			// If no progress is made there's nothing else to do
			if (lu == prevLu && ru == prevRu) {
				break;
			}
		}
		
		// Same as before, for the other side
		
		LinkedVertex ll = left.rightMost;
		LinkedVertex rl = right.leftMost;
		
		int limitRightL = right.size - 1;
		int limitLeftL = left.size - 1;
		
		while (true) {
			LinkedVertex prevLl = ll;
			LinkedVertex prevRl = rl;
			
			while (limitRightL > 0 && RobustGeometry.getLocation(rl.prev.point, ll.point, rl.point) >= 0) {
				rl = rl.prev;
				limitRightL--;
			}
			
			while (limitLeftL > 0 && RobustGeometry.getLocation(ll.next.point, ll.point, rl.point) >= 0) {
				ll = ll.next;
				limitLeftL--;
			}
			
			// If no progress is made there's nothing else to do
			if (ll == prevLl && rl == prevRl) {
				break;
			}
		}
		
		// link the hull
		lu.next = ru;
		ru.prev = lu;
		
		ll.prev = rl;
		rl.next = ll;
		
		// We could compute size with a closed-form type based on the four values
		// of limitLeft/Right/L/U but it is not straightforward and there is no observable
		// speed gain. So use a simple loop instead
		int size = 0;
		LinkedVertex v = lu;
		
		do {
			size ++;
			v = v.next;
		} while (v == lu);
		
		// set the size
		hull.size = size;
		
		// return the merged hull
		return hull;
	}
```
