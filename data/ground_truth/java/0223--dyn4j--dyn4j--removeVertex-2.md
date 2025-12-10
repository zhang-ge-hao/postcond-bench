https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/Visvalingam.java#L210-L263
```
//@ ensures ((AreaTrackedVertex)v.prev).next == (AreaTrackedVertex)v.next;
//@ ensures ((AreaTrackedVertex)v.next).prev == (AreaTrackedVertex)v.prev;
//@ ensures ((AreaTrackedVertex)v.prev).area == getTriangleArea(((AreaTrackedVertex)v.prev).prev.point, ((AreaTrackedVertex)v.prev).point, ((AreaTrackedVertex)v.next).point);
//@ ensures ((AreaTrackedVertex)v.next).area == getTriangleArea(((AreaTrackedVertex)v.prev).point, ((AreaTrackedVertex)v.next).point, ((AreaTrackedVertex)v.next).next.point);
//@ ensures ((AreaTrackedVertex)v.prev).nextSegment.point1 == ((AreaTrackedVertex)v.prev).point && ((AreaTrackedVertex)v.prev).nextSegment.point2 == ((AreaTrackedVertex)v.next).point && ((AreaTrackedVertex)v.next).prevSegment == ((AreaTrackedVertex)v.prev).nextSegment;
//@ ensures queue.contains((AreaTrackedVertex)v.prev) && queue.contains((AreaTrackedVertex)v.next);
//@ ensures queue.size() >= \old(queue.size());
//@ ensures queue.stream().noneMatch(u -> { AreaTrackedVertex a = (AreaTrackedVertex)u; return a.index == -1; });
//@ ensures queue.stream().noneMatch(u -> { AreaTrackedVertex a = (AreaTrackedVertex)u; return a.prevSegment == \old(((AreaTrackedVertex)v).prevSegment) || a.nextSegment == \old(((AreaTrackedVertex)v).prevSegment); });
//@ ensures queue.stream().noneMatch(u -> { AreaTrackedVertex a = (AreaTrackedVertex)u; return a.prevSegment == \old(((AreaTrackedVertex)v).nextSegment) || a.nextSegment == \old(((AreaTrackedVertex)v).nextSegment); });
//@ ensures java.util.stream.StreamSupport.stream(java.util.Spliterators.spliteratorUnknownSize(tree.getAABBDetectIterator(((SegmentTreeLeaf)\old(((AreaTrackedVertex)v).prevSegment)).aabb), 0), false).noneMatch(l -> l.index1 == ((AreaTrackedVertex)v).index || l.index2 == ((AreaTrackedVertex)v).index);
//@ ensures java.util.stream.StreamSupport.stream(java.util.Spliterators.spliteratorUnknownSize(tree.getAABBDetectIterator(((SegmentTreeLeaf)\old(((AreaTrackedVertex)v).nextSegment)).aabb), 0), false).noneMatch(l -> l.index1 == ((AreaTrackedVertex)v).index || l.index2 == ((AreaTrackedVertex)v).index);
//@ ensures \result == (((AreaTrackedVertex)v.prev) == ((AreaTrackedVertex)v.next));
```
```
//@ ensures ((AreaTrackedVertex)v.prev).next == (AreaTrackedVertex)v.next;
//@ ensures ((AreaTrackedVertex)v.next).prev == (AreaTrackedVertex)v.prev;
//@ ensures ((AreaTrackedVertex)v.prev).area == getTriangleArea(((AreaTrackedVertex)v.prev).prev.point, ((AreaTrackedVertex)v.prev).point, ((AreaTrackedVertex)v.next).point);
//@ ensures ((AreaTrackedVertex)v.next).area == getTriangleArea(((AreaTrackedVertex)v.prev).point, ((AreaTrackedVertex)v.next).point, ((AreaTrackedVertex)v.next).next.point);
//@ ensures ((AreaTrackedVertex)v.prev).nextSegment.point1 == ((AreaTrackedVertex)v.prev).point && ((AreaTrackedVertex)v.prev).nextSegment.point2 == ((AreaTrackedVertex)v.next).point && ((AreaTrackedVertex)v.next).prevSegment == ((AreaTrackedVertex)v.prev).nextSegment;
//@ ensures queue.contains((AreaTrackedVertex)v.prev) && queue.contains((AreaTrackedVertex)v.next);
//@ ensures queue.stream().noneMatch(u -> { AreaTrackedVertex a = (AreaTrackedVertex)u; return a.index == -1; });
//@ ensures queue.stream().noneMatch(u -> { AreaTrackedVertex a = (AreaTrackedVertex)u; return a.prevSegment == \old(((AreaTrackedVertex)v).prevSegment) || a.nextSegment == \old(((AreaTrackedVertex)v).prevSegment); });
//@ ensures queue.stream().noneMatch(u -> { AreaTrackedVertex a = (AreaTrackedVertex)u; return a.prevSegment == \old(((AreaTrackedVertex)v).nextSegment) || a.nextSegment == \old(((AreaTrackedVertex)v).nextSegment); });
//@ ensures \result == ( ((AreaTrackedVertex)v.prev) == ((AreaTrackedVertex)v.next) );
```
[9, 10, 11]
===== 9 =====
```
 		tprev.nextSegment = new SegmentTreeLeaf(v1, v2, tprev.index, tnext.index);
 		tnext.prevSegment = tprev.nextSegment;
 		// remove the two segments attached to the removed vertex
-		tree.remove(tprevSegment);
+		
 		tree.remove(tnextSegment);
 		// add the new segment to the segment tree
 		tree.add(tprev.nextSegment);
```
```
	/**
	 * Removes the given vertex from the queue and segment tree.
	 * @param v the vertex to remove
	 * @param queue the queue to remove the vertex from
	 * @param tree the segment tree to remove the vertex from
	 */
	private final boolean removeVertex(AreaTrackedVertex v, Queue<AreaTrackedVertex> queue, SegmentTree tree) {
		Vector2 v0 = null;
		Vector2 v1 = null;
		Vector2 v2 = null;
		
		AreaTrackedVertex tprev = (AreaTrackedVertex)v.prev;
		AreaTrackedVertex tnext = (AreaTrackedVertex)v.next;
		SegmentTreeLeaf tprevSegment = v.prevSegment;
		SegmentTreeLeaf tnextSegment = v.nextSegment;
		
		tprev.next = tnext;
		tnext.prev = tprev;
		
		// recompute the previous segment's triangular area
		v0 = tprev.prev.point;
		v1 = tprev.point;
		v2 = tnext.point;
		tprev.area = getTriangleArea(v0, v1, v2);

		// recompute the next segment's triangular area
		v0 = tprev.point;
		v1 = tnext.point;
		v2 = tnext.next.point;
		tnext.area = getTriangleArea(v0, v1, v2);
		
		// build a new segment with the given vertex removed
		v1 = tprev.point;
		v2 = tnext.point;
		
		// update the segment tree to account for the removed segments/vertex
		tprev.nextSegment = new SegmentTreeLeaf(v1, v2, tprev.index, tnext.index);
		tnext.prevSegment = tprev.nextSegment;
		// remove the two segments attached to the removed vertex
		
		tree.remove(tnextSegment);
		// add the new segment to the segment tree
		tree.add(tprev.nextSegment);
		
		// remove the adjacent vertices from the queue
		queue.remove(tprev);
		queue.remove(tnext);
		
		// add them back to the queue so they are sorted in the correct place
		queue.add(tprev);
		queue.add(tnext);
		
		return tprev == tnext;
	}
```
===== 10 =====
```
 		tnext.prevSegment = tprev.nextSegment;
 		// remove the two segments attached to the removed vertex
 		tree.remove(tprevSegment);
-		tree.remove(tnextSegment);
+		
 		// add the new segment to the segment tree
 		tree.add(tprev.nextSegment);
```
```
	/**
	 * Removes the given vertex from the queue and segment tree.
	 * @param v the vertex to remove
	 * @param queue the queue to remove the vertex from
	 * @param tree the segment tree to remove the vertex from
	 */
	private final boolean removeVertex(AreaTrackedVertex v, Queue<AreaTrackedVertex> queue, SegmentTree tree) {
		Vector2 v0 = null;
		Vector2 v1 = null;
		Vector2 v2 = null;
		
		AreaTrackedVertex tprev = (AreaTrackedVertex)v.prev;
		AreaTrackedVertex tnext = (AreaTrackedVertex)v.next;
		SegmentTreeLeaf tprevSegment = v.prevSegment;
		SegmentTreeLeaf tnextSegment = v.nextSegment;
		
		tprev.next = tnext;
		tnext.prev = tprev;
		
		// recompute the previous segment's triangular area
		v0 = tprev.prev.point;
		v1 = tprev.point;
		v2 = tnext.point;
		tprev.area = getTriangleArea(v0, v1, v2);

		// recompute the next segment's triangular area
		v0 = tprev.point;
		v1 = tnext.point;
		v2 = tnext.next.point;
		tnext.area = getTriangleArea(v0, v1, v2);
		
		// build a new segment with the given vertex removed
		v1 = tprev.point;
		v2 = tnext.point;
		
		// update the segment tree to account for the removed segments/vertex
		tprev.nextSegment = new SegmentTreeLeaf(v1, v2, tprev.index, tnext.index);
		tnext.prevSegment = tprev.nextSegment;
		// remove the two segments attached to the removed vertex
		tree.remove(tprevSegment);
		
		// add the new segment to the segment tree
		tree.add(tprev.nextSegment);
		
		// remove the adjacent vertices from the queue
		queue.remove(tprev);
		queue.remove(tnext);
		
		// add them back to the queue so they are sorted in the correct place
		queue.add(tprev);
		queue.add(tnext);
		
		return tprev == tnext;
	}
```
===== 11 =====
```
 		
 		// remove the adjacent vertices from the queue
 		queue.remove(tprev);
-		queue.remove(tnext);
+		queue.clear();
 		
 		// add them back to the queue so they are sorted in the correct place
 		queue.add(tprev);
```
```
	/**
	 * Removes the given vertex from the queue and segment tree.
	 * @param v the vertex to remove
	 * @param queue the queue to remove the vertex from
	 * @param tree the segment tree to remove the vertex from
	 */
	private final boolean removeVertex(AreaTrackedVertex v, Queue<AreaTrackedVertex> queue, SegmentTree tree) {
		Vector2 v0 = null;
		Vector2 v1 = null;
		Vector2 v2 = null;
		
		AreaTrackedVertex tprev = (AreaTrackedVertex)v.prev;
		AreaTrackedVertex tnext = (AreaTrackedVertex)v.next;
		SegmentTreeLeaf tprevSegment = v.prevSegment;
		SegmentTreeLeaf tnextSegment = v.nextSegment;
		
		tprev.next = tnext;
		tnext.prev = tprev;
		
		// recompute the previous segment's triangular area
		v0 = tprev.prev.point;
		v1 = tprev.point;
		v2 = tnext.point;
		tprev.area = getTriangleArea(v0, v1, v2);

		// recompute the next segment's triangular area
		v0 = tprev.point;
		v1 = tnext.point;
		v2 = tnext.next.point;
		tnext.area = getTriangleArea(v0, v1, v2);
		
		// build a new segment with the given vertex removed
		v1 = tprev.point;
		v2 = tnext.point;
		
		// update the segment tree to account for the removed segments/vertex
		tprev.nextSegment = new SegmentTreeLeaf(v1, v2, tprev.index, tnext.index);
		tnext.prevSegment = tprev.nextSegment;
		// remove the two segments attached to the removed vertex
		tree.remove(tprevSegment);
		tree.remove(tnextSegment);
		// add the new segment to the segment tree
		tree.add(tprev.nextSegment);
		
		// remove the adjacent vertices from the queue
		queue.remove(tprev);
		queue.clear();
		
		// add them back to the queue so they are sorted in the correct place
		queue.add(tprev);
		queue.add(tnext);
		
		return tprev == tnext;
	}
```
