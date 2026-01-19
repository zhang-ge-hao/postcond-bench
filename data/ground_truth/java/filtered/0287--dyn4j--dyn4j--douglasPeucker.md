https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/DouglasPeucker.java#L124-L208
```
🈚️

It's hard
```
```
//@ ensures polyline.size() < 3 ==> \result.size() == polyline.size();
//@ ensures polyline.size() < 3 ==> java.util.stream.IntStream.range(0, polyline.size()).allMatch(i -> \result.get(i).equals(polyline.get(i).point));
//@ ensures polyline.size() >= 3 ==> \result.size() >= 2;
//@ ensures polyline.size() >= 1 ==> \result.get(0).equals(polyline.get(0).point);
//@ ensures polyline.size() >= 2 ==> \result.get(\result.size() - 1).equals(polyline.get(polyline.size() - 1).point);
//@ ensures polyline.size() >= 1 ==> java.util.stream.IntStream.range(0, \result.size()).allMatch(i -> polyline.stream().map(v -> v.point).anyMatch(p -> p.equals(\result.get(i))));
```
[1, 2, 3, 9, 10, 13, 14, 15, 16, 17, 19, 23, 25, 29, 30, 34, 36, 41, 44, 45, 46, 48]
===== 1 =====
```
 		List<Vector2> result = new ArrayList<Vector2>();
 		
 		// can't do anything with 1 or 2 points - we just have to keep them
-		if (size < 3) {
+		if (size != 2) {
 			for (int i = 0; i < size; i++) {
 				result.add(polyline.get(i).point);
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size != 2) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 2 =====
```
 		List<Vector2> result = new ArrayList<Vector2>();
 		
 		// can't do anything with 1 or 2 points - we just have to keep them
-		if (size < 3) {
+		if (size < 4) {
 			for (int i = 0; i < size; i++) {
 				result.add(polyline.get(i).point);
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 4) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 3 =====
```
 		List<Vector2> result = new ArrayList<Vector2>();
 		
 		// can't do anything with 1 or 2 points - we just have to keep them
-		if (size < 3) {
+		if (size <= 3) {
 			for (int i = 0; i < size; i++) {
 				result.add(polyline.get(i).point);
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size <= 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 9 =====
```
 		// can't do anything with 1 or 2 points - we just have to keep them
 		if (size < 3) {
 			for (int i = 0; i < size; i++) {
-				result.add(polyline.get(i).point);
+				result.add(polyline.get(i).point.add(new Vector2(1, 1))); // Adding an offset to the point, which alters its original position and can lead to incorrect results.
 			}
 			return result;
 		}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point.add(new Vector2(1, 1))); // Adding an offset to the point, which alters its original position and can lead to incorrect results.
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 10 =====
```
 		// can't do anything with 1 or 2 points - we just have to keep them
 		if (size < 3) {
 			for (int i = 0; i < size; i++) {
-				result.add(polyline.get(i).point);
+				result.add(polyline.get(i).point.multiply(2)); // Adding a scaled version of the point, which changes its position and leads to incorrect simplification.
 			}
 			return result;
 		}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point.multiply(2)); // Adding a scaled version of the point, which changes its position and leads to incorrect simplification.
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 13 =====
```
 		
 		// get the farthest vertex from the line created from the start to the end
 		// vertex on the polyline
-		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
+		FarthestVertex fv = this.getFarthestVertexFromLine(ev, sv, polyline); // Swapped parameters
 		
 		// check the farthest point's distance - if it's higher than the minimum
 		// distance epsilon, then we need to subdivide the polyline since we can't
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(ev, sv, polyline); // Swapped parameters
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 14 =====
```
 		// check the farthest point's distance - if it's higher than the minimum
 		// distance epsilon, then we need to subdivide the polyline since we can't
 		// reduce here (we might be able to reduce elsewhere)
-		if (fv.distance >= epsilon) {
+		if (fv.distance < epsilon) {
 			// sub-divide and run the algo on each half
 			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
 			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance < epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 15 =====
```
 		// check the farthest point's distance - if it's higher than the minimum
 		// distance epsilon, then we need to subdivide the polyline since we can't
 		// reduce here (we might be able to reduce elsewhere)
-		if (fv.distance >= epsilon) {
+		if (fv.distance <= epsilon) {
 			// sub-divide and run the algo on each half
 			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
 			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance <= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 16 =====
```
 		// check the farthest point's distance - if it's higher than the minimum
 		// distance epsilon, then we need to subdivide the polyline since we can't
 		// reduce here (we might be able to reduce elsewhere)
-		if (fv.distance >= epsilon) {
+		if (fv.distance == epsilon) {
 			// sub-divide and run the algo on each half
 			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
 			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance == epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 17 =====
```
 		// check the farthest point's distance - if it's higher than the minimum
 		// distance epsilon, then we need to subdivide the polyline since we can't
 		// reduce here (we might be able to reduce elsewhere)
-		if (fv.distance >= epsilon) {
+		if (fv.distance > epsilon) {
 			// sub-divide and run the algo on each half
 			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
 			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance > epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 19 =====
```
 		if (fv.distance >= epsilon) {
 			// sub-divide and run the algo on each half
 			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
-			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
+			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index + 1, size), tree);
 			
 			// recombine the reduced polylines
 			result.addAll(aReduced.subList(0, aReduced.size() - 1));
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index + 1, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 23 =====
```
 			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
 			
 			// recombine the reduced polylines
-			result.addAll(aReduced.subList(0, aReduced.size() - 1));
+			result.addAll(aReduced); // This adds all vertices from aReduced, potentially including the last vertex which should not be added.
 			result.addAll(bReduced);
 		} else {
 			// check for self-intersection
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced); // This adds all vertices from aReduced, potentially including the last vertex which should not be added.
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 25 =====
```
 			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
 			
 			// recombine the reduced polylines
-			result.addAll(aReduced.subList(0, aReduced.size() - 1));
+			result.addAll(aReduced.subList(0, aReduced.size())); // This adds all vertices from aReduced, including the last vertex, which should not be included.
 			result.addAll(bReduced);
 		} else {
 			// check for self-intersection
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size())); // This adds all vertices from aReduced, including the last vertex, which should not be included.
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 29 =====
```
 			
 			// recombine the reduced polylines
 			result.addAll(aReduced.subList(0, aReduced.size() - 1));
-			result.addAll(bReduced);
+			result.addAll(bReduced.subList(1, bReduced.size())); // Skips the first vertex of bReduced
 		} else {
 			// check for self-intersection
 			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced.subList(1, bReduced.size())); // Skips the first vertex of bReduced
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 30 =====
```
 				
 				// sub-divide and run the algo on each half
 				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
-				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
+				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index + 1, size), tree);
 				
 				// recombine the reduced polylines
 				result.addAll(aReduced.subList(0, aReduced.size() - 1));
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index + 1, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 34 =====
```
 				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
 				
 				// recombine the reduced polylines
-				result.addAll(aReduced.subList(0, aReduced.size() - 1));
+				result.addAll(aReduced); // Adds all vertices from aReduced, including the last one, which may cause incorrect simplification.
 				result.addAll(bReduced);
 				
 				return result;
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced); // Adds all vertices from aReduced, including the last one, which may cause incorrect simplification.
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 36 =====
```
 				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
 				
 				// recombine the reduced polylines
-				result.addAll(aReduced.subList(0, aReduced.size() - 1));
+				result.addAll(aReduced.subList(0, aReduced.size())); // Adds all vertices from aReduced, which is the same as adding all, leading to redundancy.
 				result.addAll(bReduced);
 				
 				return result;
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size())); // Adds all vertices from aReduced, which is the same as adding all, leading to redundancy.
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 41 =====
```
 				
 				// recombine the reduced polylines
 				result.addAll(aReduced.subList(0, aReduced.size() - 1));
-				result.addAll(bReduced);
+				result.addAll(bReduced.subList(1, bReduced.size())); // Skips the first vertex of the second reduced polyline
 				
 				return result;
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced.subList(1, bReduced.size())); // Skips the first vertex of the second reduced polyline
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 44 =====
```
 			// if there's no self-intersection, then we need to remove
 			// all segments from the segment tree in between these vertices
 			SimplePolygonVertex b = sv;
-			while (b != ev) {
+			while (b != sv) {
 				tree.remove(b.nextSegment);
 				b = b.next;
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != sv) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 45 =====
```
 			// if there's no self-intersection, then we need to remove
 			// all segments from the segment tree in between these vertices
 			SimplePolygonVertex b = sv;
-			while (b != ev) {
+			while (b == ev) {
 				tree.remove(b.nextSegment);
 				b = b.next;
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b == ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 46 =====
```
 			// all segments from the segment tree in between these vertices
 			SimplePolygonVertex b = sv;
 			while (b != ev) {
-				tree.remove(b.nextSegment);
+				
 				b = b.next;
 			}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point);
			result.add(ev.point);
		}
		
		return result;
	}
```
===== 48 =====
```
 			
 			// just use the start/end vertices
 			// as the result
-			result.add(sv.point);
+			result.add(sv.point); result.add(sv.point); // Duplicating the start vertex in the result
 			result.add(ev.point);
 		}
```
```
	/**
	 * Recursively sub-divide the given polyline performing the douglas Peucker algorithm.
	 * <p>
	 * O(mn) in worst case, O(n log m) in best case, where n is the number of vertices in the
	 * original polyline and m is the number of vertices in the reduced polyline.
	 * @param polyline
	 * @return List&lt;{@link Vector2}&gt;
	 */
	private final List<Vector2> douglasPeucker(List<SimplePolygonVertex> polyline, SegmentTree tree) {
		int size = polyline.size();
		List<Vector2> result = new ArrayList<Vector2>();
		
		// can't do anything with 1 or 2 points - we just have to keep them
		if (size < 3) {
			for (int i = 0; i < size; i++) {
				result.add(polyline.get(i).point);
			}
			return result;
		}
		
		// get the start/end vertices of the polyline
		SimplePolygonVertex sv = polyline.get(0);
		SimplePolygonVertex ev = polyline.get(size - 1);
		
		// get the farthest vertex from the line created from the start to the end
		// vertex on the polyline
		FarthestVertex fv = this.getFarthestVertexFromLine(sv, ev, polyline);
		
		// check the farthest point's distance - if it's higher than the minimum
		// distance epsilon, then we need to subdivide the polyline since we can't
		// reduce here (we might be able to reduce elsewhere)
		if (fv.distance >= epsilon) {
			// sub-divide and run the algo on each half
			List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
			List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
			
			// recombine the reduced polylines
			result.addAll(aReduced.subList(0, aReduced.size() - 1));
			result.addAll(bReduced);
		} else {
			// check for self-intersection
			if (this.isSelfIntersectionProduced(sv, ev, tree)) {
				// if removing all the points between v1 and v2 produces self-intersection
				// then we can either stop and all points between v1 and v2 to the result
				// or we can split the polyline by the farthest point and try to simplify
				// those sub-polylines
				
				// sub-divide and run the algo on each half
				List<Vector2> aReduced = this.douglasPeucker(polyline.subList(0, fv.index + 1), tree);
				List<Vector2> bReduced = this.douglasPeucker(polyline.subList(fv.index, size), tree);
				
				// recombine the reduced polylines
				result.addAll(aReduced.subList(0, aReduced.size() - 1));
				result.addAll(bReduced);
				
				return result;
			}
			
			// if there's no self-intersection, then we need to remove
			// all segments from the segment tree in between these vertices
			SimplePolygonVertex b = sv;
			while (b != ev) {
				tree.remove(b.nextSegment);
				b = b.next;
			}
			
			// remove all the vertices between sv/ev
			sv.next = ev;
			ev.prev = sv;
			
			// create a new segment between sv/ev
			sv.nextSegment = new SegmentTreeLeaf(sv.point, ev.point, sv.index, ev.index);
			ev.prevSegment = sv.nextSegment;
			
			// add the new segment to the segment tree
			tree.add(sv.nextSegment);
			
			// just use the start/end vertices
			// as the result
			result.add(sv.point); result.add(sv.point); // Duplicating the start vertex in the result
			result.add(ev.point);
		}
		
		return result;
	}
```
