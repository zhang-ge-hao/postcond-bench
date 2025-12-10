https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/DoubleEdgeList.java#L685-L743
```
//@ ensures this.vertices.size() == \old(this.vertices.size());
//@ ensures this.edges.size() <= \old(this.edges.size());
//@ ensures this.faces.size() <= \old(this.faces.size());
//@ ensures java.util.stream.IntStream.range(\old(this.vertices.size()) * 2, this.edges.size()).allMatch(j -> this.isReflex(this.edges.get(j).getPrevious().origin, this.edges.get(j).origin, this.edges.get(j).twin.next.next.origin) || this.isReflex(this.edges.get(j).twin.getPrevious().origin, this.edges.get(j).twin.origin, this.edges.get(j).next.next.origin));
//@ ensures this.edges.stream().filter(e -> e != null && e.face != null).allMatch(e -> !this.isReflex(e.getPrevious().origin, e.origin, e.next.origin));
```
```
//@ ensures java.util.stream.IntStream.range(\old(this.vertices.size())*2, this.edges.size()).allMatch(j -> this.isReflex(this.edges.get(j).getPrevious().origin, this.edges.get(j).origin, this.edges.get(j).twin.next.next.origin) || this.isReflex(this.edges.get(j).twin.getPrevious().origin, this.edges.get(j).twin.origin, this.edges.get(j).next.next.origin));
```
[0, 1, 2, 3, 6, 8, 9, 10, 11, 12, 14]
===== 0 =====
```
 			
 			// test the first end point
 			DoubleEdgeListVertex v1 = e.origin;
-			DoubleEdgeListVertex v0 = e.getPrevious().origin;
+			DoubleEdgeListVertex v0 = e.getPrevious().twin.origin; // Incorrectly uses the twin of the previous edge's origin instead of the previous edge's origin.
 			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().twin.origin; // Incorrectly uses the twin of the previous edge's origin instead of the previous edge's origin.
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 1 =====
```
 			
 			// test the first end point
 			DoubleEdgeListVertex v1 = e.origin;
-			DoubleEdgeListVertex v0 = e.getPrevious().origin;
+			DoubleEdgeListVertex v0 = e.next.origin; // Incorrectly uses the next edge's origin instead of the previous edge's origin.
 			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.next.origin; // Incorrectly uses the next edge's origin instead of the previous edge's origin.
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 2 =====
```
 			
 			// test the first end point
 			DoubleEdgeListVertex v1 = e.origin;
-			DoubleEdgeListVertex v0 = e.getPrevious().origin;
+			DoubleEdgeListVertex v0 = e.origin; // Incorrectly uses the origin of the current edge instead of the previous edge.
 			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.origin; // Incorrectly uses the origin of the current edge instead of the previous edge.
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 3 =====
```
 			
 			// test the first end point
 			DoubleEdgeListVertex v1 = e.origin;
-			DoubleEdgeListVertex v0 = e.getPrevious().origin;
+			DoubleEdgeListVertex v0 = e.twin.origin; // Incorrectly uses the twin's origin instead of the previous edge's origin.
 			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.twin.origin; // Incorrectly uses the twin's origin instead of the previous edge's origin.
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 6 =====
```
 			
 			// check if removing this half edge creates a reflex vertex at the
 			// origin vertex of this half edge
-			if (isReflex(v0, v1, v2)) {
+			if (isReflex(v0, v1, v2) && false) {
 				// if it did, then we cannot remove this edge
 				// so skip the next one and continue
 				i+=2;
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2) && false) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 8 =====
```
 			
 			// test the other end point
 			v1 = e.twin.origin;
-			v0 = e.twin.getPrevious().origin;
+			v0 = e.getPrevious().twin.origin; // Incorrectly uses the twin of the previous edge's origin
 			v2 = e.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.getPrevious().twin.origin; // Incorrectly uses the twin of the previous edge's origin
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 9 =====
```
 			
 			// test the other end point
 			v1 = e.twin.origin;
-			v0 = e.twin.getPrevious().origin;
+			v0 = e.next.origin; // Incorrectly uses the next edge's origin instead of the previous edge
 			v2 = e.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.next.origin; // Incorrectly uses the next edge's origin instead of the previous edge
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 10 =====
```
 			
 			// test the other end point
 			v1 = e.twin.origin;
-			v0 = e.twin.getPrevious().origin;
+			v0 = e.origin; // Incorrectly uses the origin of the current edge instead of the previous edge
 			v2 = e.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.origin; // Incorrectly uses the origin of the current edge instead of the previous edge
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 11 =====
```
 			
 			// test the other end point
 			v1 = e.twin.origin;
-			v0 = e.twin.getPrevious().origin;
+			v0 = e.twin.next.origin; // Incorrectly uses the origin of the next edge of the twin instead of the previous edge
 			v2 = e.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.next.origin; // Incorrectly uses the origin of the next edge of the twin instead of the previous edge
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 12 =====
```
 			
 			// test the other end point
 			v1 = e.twin.origin;
-			v0 = e.twin.getPrevious().origin;
+			v0 = e.twin.origin; // Incorrectly uses the origin of the twin edge instead of the previous edge
 			v2 = e.next.next.origin;
 			
 			// check if removing this half edge creates a reflex vertex at the
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.origin; // Incorrectly uses the origin of the twin edge instead of the previous edge
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
===== 14 =====
```
 			
 			// check if removing this half edge creates a reflex vertex at the
 			// origin of this half edge's twin
-			if (isReflex(v0, v1, v2)) {
+			if (isReflex(v0, v1, v2) && v0 == v2) {
 				// if it did, then we cannot remove this edge
 				// so skip the next one and continue
 				i+=2;
```
```
	/**
	 * Performs the Hertel-Mehlhorn algorithm on the given DCEL assuming that
	 * it is a valid triangulation.
	 * <p>
	 * This method will remove unnecessary diagonals and remove faces that get merged
	 * leaving a convex decomposition.
	 * <p>
	 * This method is guaranteed to produce a convex decomposition with no more than
	 * 4 times the minimum number of convex pieces.
	 */
	public void hertelMehlhorn() {
		// loop over all the edges and see which we can remove
		int vSize = this.vertices.size();
		
		// This method will remove any unnecessary diagonals (those that do not
		// form reflex vertices when removed).  This method is O(n) where n is the
		// number of diagonals added to the original DCEL.  We can start processing
		// diagonals after all the initial diagonals (the initial diagonals are the
		// edges of the original polygon).  We can also skip every other half edge
		// since each edge is stored with its twin in the next index.
		
		int i = vSize * 2;
		while (i < this.edges.size()) {
			
			// see if removing this edge creates a reflex vertex at the end points
			DoubleEdgeListHalfEdge e = this.edges.get(i);
			
			// test the first end point
			DoubleEdgeListVertex v1 = e.origin;
			DoubleEdgeListVertex v0 = e.getPrevious().origin;
			DoubleEdgeListVertex v2 = e.twin.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin vertex of this half edge
			if (isReflex(v0, v1, v2)) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// test the other end point
			v1 = e.twin.origin;
			v0 = e.twin.getPrevious().origin;
			v2 = e.next.next.origin;
			
			// check if removing this half edge creates a reflex vertex at the
			// origin of this half edge's twin
			if (isReflex(v0, v1, v2) && v0 == v2) {
				// if it did, then we cannot remove this edge
				// so skip the next one and continue
				i+=2;
				continue;
			}
			
			// otherwise we can remove this edge
			this.removeHalfEdges(i, e);
		}
	}
```
