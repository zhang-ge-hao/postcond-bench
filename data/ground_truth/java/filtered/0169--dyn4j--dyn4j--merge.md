https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/SweepLine.java#L209-L241
```
🈚️

It's hard.

//@ ensures sweepstate.referenceY.value == vertex.point.y;
//@ ensures sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest != null;
//@ ensures sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest.helper == vertex;
//@ ensures \old(vertex.right.helper.type == SweepLineVertexType.MERGE) ==> (sweepstate.dcel.edges.size() >= \old(sweepstate.dcel.edges.size()) + 2);
//@ ensures \old(sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest.helper.type == SweepLineVertexType.MERGE) ==> (sweepstate.dcel.edges.size() >= \old(sweepstate.dcel.edges.size()) + 2);
//@ ensures (\old(sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest) == sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest && \old(sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest.helper.type == SweepLineVertexType.MERGE)) ==> (sweepstate.dcel.edges.size() >= \old(sweepstate.dcel.edges.size()) + 2);
```
```
//@ ensures sweepstate.referenceY.value == vertex.point.y;
//@ ensures sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest != null;
//@ ensures sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest.helper == vertex;
//@ ensures \old(vertex.right.helper.type == SweepLineVertexType.MERGE) ==> (sweepstate.dcel.edges.size() >= \old(sweepstate.dcel.edges.size()) + 2);
//@ ensures \old(sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest.helper.type == SweepLineVertexType.MERGE) ==> (sweepstate.dcel.edges.size() >= \old(sweepstate.dcel.edges.size()) + 2);
```
[3, 4, 5, 6, 7, 8]
===== 3 =====
```
 		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
 		
 		// is the edge's helper a merge vertex
-		if (ej.helper.type == SweepLineVertexType.MERGE) {
+		if (ej.helper.type != SweepLineVertexType.MERGE) {
 			// connect v to ej.helper
 			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
 		}
```
```
	/**
	 * Handles a {@link SweepLineVertexType#MERGE} event.
	 * @param vertex the vertex
	 * @param sweepstate the current state of the SweepLine algorithm
	 */
	final void merge(SweepLineVertex vertex, SweepLineState sweepstate) {
		// get the previous edge
		SweepLineEdge eiPrev = vertex.right;
		// check if its helper is a merge vertex
		if (eiPrev.helper.type == SweepLineVertexType.MERGE) {
			// connect v to v.right.helper
			sweepstate.dcel.addHalfEdges(vertex.index, eiPrev.helper.index);
		}
		// set the reference y to the current vertex's y
		sweepstate.referenceY.value = vertex.point.y;
		// remove the previous edge since the sweep 
		// line no longer intersects with it
		sweepstate.tree.remove(eiPrev);
		// find the edge closest to the given vertex
		SweepLineEdge ej = sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest;
		
		// this indicates that there's self intersection or holes
		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
		
		// is the edge's helper a merge vertex
		if (ej.helper.type != SweepLineVertexType.MERGE) {
			// connect v to ej.helper
			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
		}
		
		// set the closest edge's helper to this vertex
		ej.helper = vertex;
	}
```
===== 4 =====
```
 		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
 		
 		// is the edge's helper a merge vertex
-		if (ej.helper.type == SweepLineVertexType.MERGE) {
+		if (ej.helper.type == SweepLineVertexType.END) {
 			// connect v to ej.helper
 			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
 		}
```
```
	/**
	 * Handles a {@link SweepLineVertexType#MERGE} event.
	 * @param vertex the vertex
	 * @param sweepstate the current state of the SweepLine algorithm
	 */
	final void merge(SweepLineVertex vertex, SweepLineState sweepstate) {
		// get the previous edge
		SweepLineEdge eiPrev = vertex.right;
		// check if its helper is a merge vertex
		if (eiPrev.helper.type == SweepLineVertexType.MERGE) {
			// connect v to v.right.helper
			sweepstate.dcel.addHalfEdges(vertex.index, eiPrev.helper.index);
		}
		// set the reference y to the current vertex's y
		sweepstate.referenceY.value = vertex.point.y;
		// remove the previous edge since the sweep 
		// line no longer intersects with it
		sweepstate.tree.remove(eiPrev);
		// find the edge closest to the given vertex
		SweepLineEdge ej = sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest;
		
		// this indicates that there's self intersection or holes
		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
		
		// is the edge's helper a merge vertex
		if (ej.helper.type == SweepLineVertexType.END) {
			// connect v to ej.helper
			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
		}
		
		// set the closest edge's helper to this vertex
		ej.helper = vertex;
	}
```
===== 5 =====
```
 		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
 		
 		// is the edge's helper a merge vertex
-		if (ej.helper.type == SweepLineVertexType.MERGE) {
+		if (ej.helper.type == SweepLineVertexType.REGULAR) {
 			// connect v to ej.helper
 			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
 		}
```
```
	/**
	 * Handles a {@link SweepLineVertexType#MERGE} event.
	 * @param vertex the vertex
	 * @param sweepstate the current state of the SweepLine algorithm
	 */
	final void merge(SweepLineVertex vertex, SweepLineState sweepstate) {
		// get the previous edge
		SweepLineEdge eiPrev = vertex.right;
		// check if its helper is a merge vertex
		if (eiPrev.helper.type == SweepLineVertexType.MERGE) {
			// connect v to v.right.helper
			sweepstate.dcel.addHalfEdges(vertex.index, eiPrev.helper.index);
		}
		// set the reference y to the current vertex's y
		sweepstate.referenceY.value = vertex.point.y;
		// remove the previous edge since the sweep 
		// line no longer intersects with it
		sweepstate.tree.remove(eiPrev);
		// find the edge closest to the given vertex
		SweepLineEdge ej = sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest;
		
		// this indicates that there's self intersection or holes
		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
		
		// is the edge's helper a merge vertex
		if (ej.helper.type == SweepLineVertexType.REGULAR) {
			// connect v to ej.helper
			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
		}
		
		// set the closest edge's helper to this vertex
		ej.helper = vertex;
	}
```
===== 6 =====
```
 		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
 		
 		// is the edge's helper a merge vertex
-		if (ej.helper.type == SweepLineVertexType.MERGE) {
+		if (ej.helper.type == SweepLineVertexType.START) {
 			// connect v to ej.helper
 			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
 		}
```
```
	/**
	 * Handles a {@link SweepLineVertexType#MERGE} event.
	 * @param vertex the vertex
	 * @param sweepstate the current state of the SweepLine algorithm
	 */
	final void merge(SweepLineVertex vertex, SweepLineState sweepstate) {
		// get the previous edge
		SweepLineEdge eiPrev = vertex.right;
		// check if its helper is a merge vertex
		if (eiPrev.helper.type == SweepLineVertexType.MERGE) {
			// connect v to v.right.helper
			sweepstate.dcel.addHalfEdges(vertex.index, eiPrev.helper.index);
		}
		// set the reference y to the current vertex's y
		sweepstate.referenceY.value = vertex.point.y;
		// remove the previous edge since the sweep 
		// line no longer intersects with it
		sweepstate.tree.remove(eiPrev);
		// find the edge closest to the given vertex
		SweepLineEdge ej = sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest;
		
		// this indicates that there's self intersection or holes
		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
		
		// is the edge's helper a merge vertex
		if (ej.helper.type == SweepLineVertexType.START) {
			// connect v to ej.helper
			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
		}
		
		// set the closest edge's helper to this vertex
		ej.helper = vertex;
	}
```
===== 7 =====
```
 		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
 		
 		// is the edge's helper a merge vertex
-		if (ej.helper.type == SweepLineVertexType.MERGE) {
+		if (ej.helper.type == null) {
 			// connect v to ej.helper
 			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
 		}
```
```
	/**
	 * Handles a {@link SweepLineVertexType#MERGE} event.
	 * @param vertex the vertex
	 * @param sweepstate the current state of the SweepLine algorithm
	 */
	final void merge(SweepLineVertex vertex, SweepLineState sweepstate) {
		// get the previous edge
		SweepLineEdge eiPrev = vertex.right;
		// check if its helper is a merge vertex
		if (eiPrev.helper.type == SweepLineVertexType.MERGE) {
			// connect v to v.right.helper
			sweepstate.dcel.addHalfEdges(vertex.index, eiPrev.helper.index);
		}
		// set the reference y to the current vertex's y
		sweepstate.referenceY.value = vertex.point.y;
		// remove the previous edge since the sweep 
		// line no longer intersects with it
		sweepstate.tree.remove(eiPrev);
		// find the edge closest to the given vertex
		SweepLineEdge ej = sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest;
		
		// this indicates that there's self intersection or holes
		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
		
		// is the edge's helper a merge vertex
		if (ej.helper.type == null) {
			// connect v to ej.helper
			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
		}
		
		// set the closest edge's helper to this vertex
		ej.helper = vertex;
	}
```
===== 8 =====
```
 		// is the edge's helper a merge vertex
 		if (ej.helper.type == SweepLineVertexType.MERGE) {
 			// connect v to ej.helper
-			sweepstate.dcel.addHalfEdges(vertex.index, ej.helper.index);
+			
 		}
 		
 		// set the closest edge's helper to this vertex
```
```
	/**
	 * Handles a {@link SweepLineVertexType#MERGE} event.
	 * @param vertex the vertex
	 * @param sweepstate the current state of the SweepLine algorithm
	 */
	final void merge(SweepLineVertex vertex, SweepLineState sweepstate) {
		// get the previous edge
		SweepLineEdge eiPrev = vertex.right;
		// check if its helper is a merge vertex
		if (eiPrev.helper.type == SweepLineVertexType.MERGE) {
			// connect v to v.right.helper
			sweepstate.dcel.addHalfEdges(vertex.index, eiPrev.helper.index);
		}
		// set the reference y to the current vertex's y
		sweepstate.referenceY.value = vertex.point.y;
		// remove the previous edge since the sweep 
		// line no longer intersects with it
		sweepstate.tree.remove(eiPrev);
		// find the edge closest to the given vertex
		SweepLineEdge ej = sweepstate.tree.search(new ClosestEdgeToVertexSearchCriteria(vertex)).closest;
		
		// this indicates that there's self intersection or holes
		if (ej == null) throw new IllegalArgumentException("The input must be a simple polygon");
		
		// is the edge's helper a merge vertex
		if (ej.helper.type == SweepLineVertexType.MERGE) {
			// connect v to ej.helper
			
		}
		
		// set the closest edge's helper to this vertex
		ej.helper = vertex;
	}
```
