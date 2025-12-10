https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/decompose/DoubleEdgeList.java#L464-L561
```
//@ ensures this.vertices.size() == \old(this.vertices.size());
//@ ensures monotonePolygon.vertices.size() == \old(monotonePolygon.vertices.size());
//@ ensures (this.faces.size() - \old(this.faces.size())) == (monotonePolygon.vertices.size() > 2 ? (monotonePolygon.vertices.size() - 3) : 0);
//@ ensures (this.edges.size() - \old(this.edges.size())) == 2 * (this.faces.size() - \old(this.faces.size()));
//@ ensures this.faces.subList(\old(this.faces.size()), this.faces.size()).stream().allMatch(f -> f.getEdgeCount() == 3);
//@ ensures this.faces.subList(\old(this.faces.size()), this.faces.size()).stream().allMatch(f -> monotonePolygon.vertices.stream().anyMatch(mv -> mv.data == f.edge.origin) && monotonePolygon.vertices.stream().anyMatch(mv -> mv.data == f.edge.next.origin) && monotonePolygon.vertices.stream().anyMatch(mv -> mv.data == f.edge.next.next.origin));
//@ ensures this.edges.stream().skip(\old(this.edges.size())).filter(e -> this.edges.indexOf(e) % 2 == 0).allMatch(e -> monotonePolygon.vertices.stream().anyMatch(mv -> mv.data == e.origin) && monotonePolygon.vertices.stream().anyMatch(mv2 -> mv2.data == e.twin.origin));
//@ ensures this.edges.stream().skip(\old(this.edges.size())).filter(e -> this.edges.indexOf(e) % 2 == 0).allMatch(e -> monotonePolygon.vertices.stream().noneMatch(mv -> mv.data == e.origin && (mv.next.data == e.twin.origin || mv.previous.data == e.twin.origin)));
//@ ensures this.edges.stream().skip(\old(this.edges.size())).filter(e1 -> this.edges.indexOf(e1) % 2 == 0).allMatch(e1 -> this.edges.stream().skip(\old(this.edges.size())).filter(e2 -> this.edges.indexOf(e2) % 2 == 0).allMatch(e2 -> e1 == e2 || e1.origin == e2.origin || e1.origin == e2.twin.origin || e1.twin.origin == e2.origin || e1.twin.origin == e2.twin.origin || Segment.getSegmentIntersection(e1.origin.point, e1.twin.origin.point, e2.origin.point, e2.twin.origin.point) == null));
//@ ensures this.edges.stream().skip(\old(this.edges.size())).filter(e1 -> this.edges.indexOf(e1) % 2 == 0).allMatch(e1 -> monotonePolygon.vertices.stream().allMatch(mv -> e1.origin == mv.data || e1.origin == mv.next.data || e1.twin.origin == mv.data || e1.twin.origin == mv.next.data || Segment.getSegmentIntersection(e1.origin.point, e1.twin.origin.point, mv.data.point, mv.next.data.point) == null));
```
```
//@ ensures this.vertices.size() == \old(this.vertices.size());
//@ ensures monotonePolygon.vertices.size() == \old(monotonePolygon.vertices.size());
//@ ensures (this.faces.size() - \old(this.faces.size())) == (monotonePolygon.vertices.size() > 2 ? (monotonePolygon.vertices.size() - 3) : 0);
//@ ensures (this.edges.size() - \old(this.edges.size())) == 2 * (this.faces.size() - \old(this.faces.size()));
//@ ensures this.faces.subList(\old(this.faces.size()), this.faces.size()).stream().allMatch(f -> f.getEdgeCount() == 3);
```
[19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]
===== 19 =====
```
 			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
 				double cross = 0;
 				
-				int sSize = stack.size();
+				int sSize = 0; // Sets size to 0, causing the loop to never execute
 				while (sSize > 1) {
 					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = 0; // Sets size to 0, causing the loop to never execute
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 20 =====
```
 				double cross = 0;
 				
 				int sSize = stack.size();
-				while (sSize > 1) {
+				while (sSize != 2) {
 					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize != 2) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 21 =====
```
 				double cross = 0;
 				
 				int sSize = stack.size();
-				while (sSize > 1) {
+				while (sSize < 1) {
 					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize < 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 22 =====
```
 				double cross = 0;
 				
 				int sSize = stack.size();
-				while (sSize > 1) {
+				while (sSize <= 1) {
 					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize <= 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 23 =====
```
 				double cross = 0;
 				
 				int sSize = stack.size();
-				while (sSize > 1) {
+				while (sSize > 2) {
 					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 2) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 24 =====
```
 				
 				int sSize = stack.size();
 				while (sSize > 1) {
-					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
+					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(0);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
 					
 					Vector2 p1 = v.data.point;
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(0);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 25 =====
```
 				
 				int sSize = stack.size();
 				while (sSize > 1) {
-					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
+					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1).next;
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
 					
 					Vector2 p1 = v.data.point;
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1).next;
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 26 =====
```
 				
 				int sSize = stack.size();
 				while (sSize > 1) {
-					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
+					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 2);
 					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
 					
 					Vector2 p1 = v.data.point;
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 2);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 27 =====
```
 				int sSize = stack.size();
 				while (sSize > 1) {
 					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
-					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
+					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 1); // This gets the top element instead of the second to last
 					
 					Vector2 p1 = v.data.point;
 					Vector2 p2 = vt.data.point;
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 1); // This gets the top element instead of the second to last
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 28 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType != MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType != MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 29 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType != MonotoneChainType.LEFT) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType != MonotoneChainType.LEFT) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 30 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 31 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType == MonotoneChainType.LEFT && v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT && v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 32 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType == MonotoneChainType.LEFT || v.chainType != MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType != MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 33 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.RIGHT) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.RIGHT) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 34 =====
```
 					Vector2 p3 = vt1.data.point;
 					
 					// what chain is the current vertex on
-					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
+					if (v.chainType == MonotoneChainType.RIGHT) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.RIGHT) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 35 =====
```
 					
 					// what chain is the current vertex on
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
-						Vector2 v1 = p2.to(p3);
+						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 36 =====
```
 					
 					// what chain is the current vertex on
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
-						Vector2 v1 = p2.to(p3);
+						Vector2 v1 = p2.to(p1);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p1);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 37 =====
```
 					
 					// what chain is the current vertex on
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
-						Vector2 v1 = p2.to(p3);
+						Vector2 v1 = p2.to(p2);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p2);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 38 =====
```
 					
 					// what chain is the current vertex on
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
-						Vector2 v1 = p2.to(p3);
+						Vector2 v1 = p3.to(p2);
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p3.to(p2);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 39 =====
```
 					// what chain is the current vertex on
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
-						Vector2 v2 = p2.to(p1);
+						Vector2 v2 = p1.to(p1);
 						cross = v1.cross(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p1.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 40 =====
```
 					// what chain is the current vertex on
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
-						Vector2 v2 = p2.to(p1);
+						Vector2 v2 = p1.to(p2);
 						cross = v1.cross(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p1.to(p2);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 41 =====
```
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
-						cross = v1.cross(v2);
+						cross = v1.cross(v2) * -1;
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2) * -1;
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 42 =====
```
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
-						cross = v1.cross(v2);
+						cross = v1.cross(v2) + 1;
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2) + 1;
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 43 =====
```
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
-						cross = v1.cross(v2);
+						cross = v1.cross(v2) + v2.cross(v1);
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2) + v2.cross(v1);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 44 =====
```
 					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
 						Vector2 v1 = p2.to(p3);
 						Vector2 v2 = p2.to(p1);
-						cross = v1.cross(v2);
+						cross = v1.dot(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.dot(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 45 =====
```
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
-						Vector2 v1 = p1.to(p2);
+						Vector2 v1 = p1.to(p1);
 						Vector2 v2 = p3.to(p2);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p1);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 46 =====
```
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
-						Vector2 v1 = p1.to(p2);
+						Vector2 v1 = p2.to(p1);
 						Vector2 v2 = p3.to(p2);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p2.to(p1);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 47 =====
```
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
-						Vector2 v1 = p1.to(p2);
+						Vector2 v1 = p2.to(p2);
 						Vector2 v2 = p3.to(p2);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p2.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 48 =====
```
 						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					} else {
-						Vector2 v1 = p1.to(p2);
+						Vector2 v1 = p3.to(p1);
 						Vector2 v2 = p3.to(p2);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p3.to(p1);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 49 =====
```
 						cross = v1.cross(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
-						Vector2 v2 = p3.to(p2);
+						Vector2 v2 = p1.to(p2);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p1.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 50 =====
```
 						cross = v1.cross(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
-						Vector2 v2 = p3.to(p2);
+						Vector2 v2 = p1.to(p3);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p1.to(p3);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 51 =====
```
 						cross = v1.cross(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
-						Vector2 v2 = p3.to(p2);
+						Vector2 v2 = p2.to(p1);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 52 =====
```
 						cross = v1.cross(v2);
 					} else {
 						Vector2 v1 = p1.to(p2);
-						Vector2 v2 = p3.to(p2);
+						Vector2 v2 = p2.to(p3);
 						cross = v1.cross(v2);
 					}
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p2.to(p3);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 53 =====
```
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
-						cross = v1.cross(v2);
+						cross = -v1.cross(v2);
 					}
 					
 					// make sure the angle is less than pi before we create
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = -v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 54 =====
```
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
-						cross = v1.cross(v2);
+						cross = v1.cross(v1);
 					}
 					
 					// make sure the angle is less than pi before we create
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v1);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 55 =====
```
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
-						cross = v1.cross(v2);
+						cross = v1.dot(v2);
 					}
 					
 					// make sure the angle is less than pi before we create
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.dot(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 56 =====
```
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
-						cross = v1.cross(v2);
+						cross = v2.cross(v1);
 					}
 					
 					// make sure the angle is less than pi before we create
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v2.cross(v1);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 57 =====
```
 					} else {
 						Vector2 v1 = p1.to(p2);
 						Vector2 v2 = p3.to(p2);
-						cross = v1.cross(v2);
+						cross = v2.cross(v2);
 					}
 					
 					// make sure the angle is less than pi before we create
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v2.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 58 =====
```
 					
 					// make sure the angle is less than pi before we create
 					// a triangle from the points
-					if (cross < -Epsilon.E) {
+					if (cross < 0) {
 						// add the half edges
 						this.addHalfEdges(v.data, vt1.data);
 						// remove the top element
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < 0) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 59 =====
```
 					
 					// make sure the angle is less than pi before we create
 					// a triangle from the points
-					if (cross < -Epsilon.E) {
+					if (cross < Epsilon.E) {
 						// add the half edges
 						this.addHalfEdges(v.data, vt1.data);
 						// remove the top element
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross < Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 60 =====
```
 					
 					// make sure the angle is less than pi before we create
 					// a triangle from the points
-					if (cross < -Epsilon.E) {
+					if (cross <= 0) {
 						// add the half edges
 						this.addHalfEdges(v.data, vt1.data);
 						// remove the top element
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross <= 0) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 61 =====
```
 					
 					// make sure the angle is less than pi before we create
 					// a triangle from the points
-					if (cross < -Epsilon.E) {
+					if (cross > -Epsilon.E) {
 						// add the half edges
 						this.addHalfEdges(v.data, vt1.data);
 						// remove the top element
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross > -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 62 =====
```
 					
 					// make sure the angle is less than pi before we create
 					// a triangle from the points
-					if (cross < -Epsilon.E) {
+					if (cross > 0) {
 						// add the half edges
 						this.addHalfEdges(v.data, vt1.data);
 						// remove the top element
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross > 0) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
===== 63 =====
```
 					
 					// make sure the angle is less than pi before we create
 					// a triangle from the points
-					if (cross < -Epsilon.E) {
+					if (cross >= -Epsilon.E) {
 						// add the half edges
 						this.addHalfEdges(v.data, vt1.data);
 						// remove the top element
```
```
	/**
	 * Triangulates the given y-monotone polygon adding the new diagonals to this DCEL.
	 * @param monotonePolygon the monotone polygon (x or y) to triangulate
	 */
	final void triangulateYMonotonePolygon(MonotonePolygon<DoubleEdgeListVertex> monotonePolygon) {
		// create a stack to support triangulation
		List<MonotoneVertex<DoubleEdgeListVertex>> stack = new ArrayList<MonotoneVertex<DoubleEdgeListVertex>>();
		
		// get the sorted monotone vertices
		List<MonotoneVertex<DoubleEdgeListVertex>> vertices = monotonePolygon.vertices;
		
		// a monotone polygon can be triangulated in O(n) time
		
		// push the first two onto the stack
		// push
		stack.add(vertices.get(0));
		stack.add(vertices.get(1));
		
		int i = 2;
		while (!stack.isEmpty()) {
			// get the next vertex in the sorted list
			MonotoneVertex<DoubleEdgeListVertex> v = vertices.get(i);
			
			// get the bottom and top elements of the stack
			MonotoneVertex<DoubleEdgeListVertex> vBot = stack.get(0);
			MonotoneVertex<DoubleEdgeListVertex> vTop = stack.get(stack.size() - 1);
			
			// is the current vertex adjacent to the bottom element
			// but not to the top element?
			if (v.isAdjacent(vBot) && !v.isAdjacent(vTop)) {
				// create the triangles and pop all the points
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// clear the bottom point
				stack.clear();
				
				// push the remaining edge
				stack.add(vTop);
				stack.add(v);
			} else if (v.isAdjacent(vTop) && !v.isAdjacent(vBot)) {
				double cross = 0;
				
				int sSize = stack.size();
				while (sSize > 1) {
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.get(sSize - 1);
					MonotoneVertex<DoubleEdgeListVertex> vt1 = stack.get(sSize - 2);
					
					Vector2 p1 = v.data.point;
					Vector2 p2 = vt.data.point;
					Vector2 p3 = vt1.data.point;
					
					// what chain is the current vertex on
					if (v.chainType == MonotoneChainType.LEFT || v.chainType == MonotoneChainType.BOTTOM) {
						Vector2 v1 = p2.to(p3);
						Vector2 v2 = p2.to(p1);
						cross = v1.cross(v2);
					} else {
						Vector2 v1 = p1.to(p2);
						Vector2 v2 = p3.to(p2);
						cross = v1.cross(v2);
					}
					
					// make sure the angle is less than pi before we create
					// a triangle from the points
					if (cross >= -Epsilon.E) {
						// add the half edges
						this.addHalfEdges(v.data, vt1.data);
						// remove the top element
						// pop
						stack.remove(sSize - 1);
						sSize--;
					} else {
						// once we find an angle that is greater than pi then
						// we can quit and move to the next vertex in the sorted list
						break;
					}
				}
				stack.add(v);
			} else if (v.isAdjacent(vTop) && v.isAdjacent(vBot)) {
				// create the triangles and pop all the points
				// pop
				stack.remove(stack.size() - 1);
				while (stack.size() > 1) {
					// pop
					MonotoneVertex<DoubleEdgeListVertex> vt = stack.remove(stack.size() - 1);
					// create diagonal
					this.addHalfEdges(v.data, vt.data);
				}
				// we are done
				break;
			}
			i++;
		}
	}
```
