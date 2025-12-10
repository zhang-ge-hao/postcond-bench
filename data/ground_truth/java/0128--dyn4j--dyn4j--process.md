https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/narrowphase/LinkPostProcessor.java#L60-L154
```
//@ ensures (link.getPoint0() == null && link.getPoint3() == null) ==> (penetration.getNormal().x == \old(penetration.getNormal().x) && penetration.getNormal().y == \old(penetration.getNormal().y) && penetration.getDepth() == \old(penetration.getDepth()));
//@ ensures !(link.getPoint0() == null && link.getPoint3() == null) ==> ((penetration.getNormal().x == \old(penetration.getNormal().x) && penetration.getNormal().y == \old(penetration.getNormal().y) && penetration.getDepth() == \old(penetration.getDepth())) || (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0) || (penetration.getNormal().x == link.getEdgeVector().getLeftHandOrthogonalVector().x && penetration.getNormal().y == link.getEdgeVector().getLeftHandOrthogonalVector().y && penetration.getDepth() == \old(penetration.getDepth())));
//@ ensures (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0) ==> (((link.getPoint0() != null) && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) <= 0.0 && (link.getPreviousEdgeVector().x * link.getEdgeVector().y - link.getPreviousEdgeVector().y * link.getEdgeVector().x) > 0.0 && (\old(penetration.getNormal().x) * link.getPreviousEdgeVector().getLeftHandOrthogonalVector().y - \old(penetration.getNormal().y) * link.getPreviousEdgeVector().getLeftHandOrthogonalVector().x) > 0.0) || ((link.getPoint0() != null) && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) <= 0.0 && (link.getPreviousEdgeVector().x * link.getEdgeVector().y - link.getPreviousEdgeVector().y * link.getEdgeVector().x) <= 0.0 && (\old(penetration.getNormal().x) * link.getEdgeVector().getLeftHandOrthogonalVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().getLeftHandOrthogonalVector().y) < 0.0) || ((link.getPoint3() != null) && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) > 0.0 && (link.getEdgeVector().x * link.getNextEdgeVector().y - link.getEdgeVector().y * link.getNextEdgeVector().x) > 0.0 && (link.getNextEdgeVector().getLeftHandOrthogonalVector().x * \old(penetration.getNormal().y) - link.getNextEdgeVector().getLeftHandOrthogonalVector().y * \old(penetration.getNormal().x)) > 0.0) || ((link.getPoint3() != null) && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) > 0.0 && (link.getEdgeVector().x * link.getNextEdgeVector().y - link.getEdgeVector().y * link.getNextEdgeVector().x) <= 0.0 && (\old(penetration.getNormal().x) * link.getEdgeVector().getLeftHandOrthogonalVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().getLeftHandOrthogonalVector().y) < 0.0));
//@ ensures (link.getPoint0() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) <= 0.0 && (link.getPreviousEdgeVector().x * link.getEdgeVector().y - link.getPreviousEdgeVector().y * link.getEdgeVector().x) > 0.0 && (\old(penetration.getNormal().x) * link.getPreviousEdgeVector().getLeftHandOrthogonalVector().y - \old(penetration.getNormal().y) * link.getPreviousEdgeVector().getLeftHandOrthogonalVector().x) <= 0.0) ==> (penetration.getNormal().x == \old(penetration.getNormal().x) && penetration.getNormal().y == \old(penetration.getNormal().y) && penetration.getDepth() == \old(penetration.getDepth()));
//@ ensures (link.getPoint3() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) > 0.0 && (link.getEdgeVector().x * link.getNextEdgeVector().y - link.getEdgeVector().y * link.getNextEdgeVector().x) > 0.0 && (link.getNextEdgeVector().getLeftHandOrthogonalVector().x * \old(penetration.getNormal().y) - link.getNextEdgeVector().getLeftHandOrthogonalVector().y * \old(penetration.getNormal().x)) <= 0.0) ==> (penetration.getNormal().x == \old(penetration.getNormal().x) && penetration.getNormal().y == \old(penetration.getNormal().y) && penetration.getDepth() == \old(penetration.getDepth()));
//@ ensures (link.getPoint0() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) <= 0.0 && (link.getPreviousEdgeVector().x * link.getEdgeVector().y - link.getPreviousEdgeVector().y * link.getEdgeVector().x) <= 0.0 && (\old(penetration.getNormal().x) * link.getEdgeVector().getLeftHandOrthogonalVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().getLeftHandOrthogonalVector().y) >= 0.0) ==> (penetration.getNormal().x == link.getEdgeVector().getLeftHandOrthogonalVector().x && penetration.getNormal().y == link.getEdgeVector().getLeftHandOrthogonalVector().y && penetration.getDepth() == \old(penetration.getDepth()));
//@ ensures (link.getPoint3() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) > 0.0 && (link.getEdgeVector().x * link.getNextEdgeVector().y - link.getEdgeVector().y * link.getNextEdgeVector().x) <= 0.0 && (\old(penetration.getNormal().x) * link.getEdgeVector().getLeftHandOrthogonalVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().getLeftHandOrthogonalVector().y) >= 0.0) ==> (penetration.getNormal().x == link.getEdgeVector().getLeftHandOrthogonalVector().x && penetration.getNormal().y == link.getEdgeVector().getLeftHandOrthogonalVector().y && penetration.getDepth() == \old(penetration.getDepth()));
//@ ensures (link.getPoint0() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) <= 0.0 && (link.getPreviousEdgeVector().x * link.getEdgeVector().y - link.getPreviousEdgeVector().y * link.getEdgeVector().x) > 0.0 && (\old(penetration.getNormal().x) * link.getPreviousEdgeVector().getLeftHandOrthogonalVector().y - \old(penetration.getNormal().y) * link.getPreviousEdgeVector().getLeftHandOrthogonalVector().x) > 0.0) ==> (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0);
//@ ensures (link.getPoint0() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) <= 0.0 && (link.getPreviousEdgeVector().x * link.getEdgeVector().y - link.getPreviousEdgeVector().y * link.getEdgeVector().x) <= 0.0 && (\old(penetration.getNormal().x) * link.getEdgeVector().getLeftHandOrthogonalVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().getLeftHandOrthogonalVector().y) < 0.0) ==> (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0);
//@ ensures (link.getPoint3() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) > 0.0 && (link.getEdgeVector().x * link.getNextEdgeVector().y - link.getEdgeVector().y * link.getNextEdgeVector().x) > 0.0 && (link.getNextEdgeVector().getLeftHandOrthogonalVector().x * \old(penetration.getNormal().y) - link.getNextEdgeVector().getLeftHandOrthogonalVector().y * \old(penetration.getNormal().x)) > 0.0) ==> (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0);
//@ ensures (link.getPoint3() != null && (\old(penetration.getNormal().x) * link.getEdgeVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().y) > 0.0 && (link.getEdgeVector().x * link.getNextEdgeVector().y - link.getEdgeVector().y * link.getNextEdgeVector().x) <= 0.0 && (\old(penetration.getNormal().x) * link.getEdgeVector().getLeftHandOrthogonalVector().x + \old(penetration.getNormal().y) * link.getEdgeVector().getLeftHandOrthogonalVector().y) < 0.0) ==> (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0);
```
```
//@ ensures (link.getPoint0() == null && link.getPoint3() == null) ==> (penetration.getNormal().x == \old(penetration.getNormal().x) && penetration.getNormal().y == \old(penetration.getNormal().y) && penetration.getDepth() == \old(penetration.getDepth()));
//@ ensures !(link.getPoint0() == null && link.getPoint3() == null) ==> ((penetration.getNormal().x == \old(penetration.getNormal().x) && penetration.getNormal().y == \old(penetration.getNormal().y) && penetration.getDepth() == \old(penetration.getDepth())) || (penetration.getNormal().x == 0.0 && penetration.getNormal().y == 0.0 && penetration.getDepth() == 0.0) || (penetration.getNormal().x == link.getEdgeVector().getLeftHandOrthogonalVector().x && penetration.getNormal().y == link.getEdgeVector().getLeftHandOrthogonalVector().y && penetration.getDepth() == \old(penetration.getDepth())));
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 57, 58, 59, 60, 61, 62, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 97, 98, 99, 100, 101, 102]
===== 0 =====
```
 	 * @param penetration the narrow-phase collision information
 	 */
 	public void process(Link link, Penetration penetration) {
-		Vector2 prev = link.getPoint0();
+		Vector2 prev = null; // intentionally setting to null
 		Vector2 next = link.getPoint3();
 		
 		if (prev == null && next == null) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = null; // intentionally setting to null
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 1 =====
```
 	 */
 	public void process(Link link, Penetration penetration) {
 		Vector2 prev = link.getPoint0();
-		Vector2 next = link.getPoint3();
+		Vector2 next = null; // Sets next to null, which will lead to unexpected behavior
 		
 		if (prev == null && next == null) {
 			// if there's no connectivity info, then take
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = null; // Sets next to null, which will lead to unexpected behavior
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 2 =====
```
 		Vector2 prev = link.getPoint0();
 		Vector2 next = link.getPoint3();
 		
-		if (prev == null && next == null) {
+		if (next == null) {
 			// if there's no connectivity info, then take
 			// what the narrowphase gave us
 			return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 3 =====
```
 		Vector2 prev = link.getPoint0();
 		Vector2 next = link.getPoint3();
 		
-		if (prev == null && next == null) {
+		if (prev != null && next != null) {
 			// if there's no connectivity info, then take
 			// what the narrowphase gave us
 			return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev != null && next != null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 4 =====
```
 		Vector2 prev = link.getPoint0();
 		Vector2 next = link.getPoint3();
 		
-		if (prev == null && next == null) {
+		if (prev != null && next == null) {
 			// if there's no connectivity info, then take
 			// what the narrowphase gave us
 			return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev != null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 5 =====
```
 		Vector2 prev = link.getPoint0();
 		Vector2 next = link.getPoint3();
 		
-		if (prev == null && next == null) {
+		if (prev == null && next != null) {
 			// if there's no connectivity info, then take
 			// what the narrowphase gave us
 			return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next != null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 6 =====
```
 		Vector2 prev = link.getPoint0();
 		Vector2 next = link.getPoint3();
 		
-		if (prev == null && next == null) {
+		if (prev == null || next == null) {
 			// if there's no connectivity info, then take
 			// what the narrowphase gave us
 			return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null || next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 7 =====
```
 		Vector2 prev = link.getPoint0();
 		Vector2 next = link.getPoint3();
 		
-		if (prev == null && next == null) {
+		if (prev == null) {
 			// if there's no connectivity info, then take
 			// what the narrowphase gave us
 			return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 8 =====
```
 			return;
 		}
 		
-		Vector2 normal = penetration.getNormal().copy();
+		Vector2 normal = new Vector2(0, 0); // Initializes normal to a zero vector, which is incorrect.
 		Vector2 edge = link.getEdgeVector();
 		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = new Vector2(0, 0); // Initializes normal to a zero vector, which is incorrect.
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 9 =====
```
 			return;
 		}
 		
-		Vector2 normal = penetration.getNormal().copy();
+		Vector2 normal = penetration.getNormal().copy().add(new Vector2(1, 1)); // Modifies the normal by adding an arbitrary vector, introducing a defect.
 		Vector2 edge = link.getEdgeVector();
 		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy().add(new Vector2(1, 1)); // Modifies the normal by adding an arbitrary vector, introducing a defect.
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 15 =====
```
 		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
 		
 		// what "side" is the normal pointing towards?
-		double side = normal.dot(edge);
+		double side = normal.cross(edge);
 		
 		// check if the normal is pointing behind the edge normal
 		double back = normal.dot(edgeNormal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.cross(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 16 =====
```
 		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
 		
 		// what "side" is the normal pointing towards?
-		double side = normal.dot(edge);
+		double side = normal.dot(edgeNormal);
 		
 		// check if the normal is pointing behind the edge normal
 		double back = normal.dot(edgeNormal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edgeNormal);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 17 =====
```
 		double side = normal.dot(edge);
 		
 		// check if the normal is pointing behind the edge normal
-		double back = normal.dot(edgeNormal);
+		double back = edgeNormal.dot(edge);
 		
 		if (side <= 0) {
 			// test against the previous edge normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = edgeNormal.dot(edge);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 18 =====
```
 		double side = normal.dot(edge);
 		
 		// check if the normal is pointing behind the edge normal
-		double back = normal.dot(edgeNormal);
+		double back = normal.cross(edgeNormal);
 		
 		if (side <= 0) {
 			// test against the previous edge normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.cross(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 19 =====
```
 		double side = normal.dot(edge);
 		
 		// check if the normal is pointing behind the edge normal
-		double back = normal.dot(edgeNormal);
+		double back = normal.dot(edge);
 		
 		if (side <= 0) {
 			// test against the previous edge normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edge);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 20 =====
```
 		// check if the normal is pointing behind the edge normal
 		double back = normal.dot(edgeNormal);
 		
-		if (side <= 0) {
+		if (side != 0) {
 			// test against the previous edge normal
 			if (prev == null) {
 				// if previous is null, then do normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side != 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 21 =====
```
 		// check if the normal is pointing behind the edge normal
 		double back = normal.dot(edgeNormal);
 		
-		if (side <= 0) {
+		if (side == 0) {
 			// test against the previous edge normal
 			if (prev == null) {
 				// if previous is null, then do normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side == 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 22 =====
```
 		// check if the normal is pointing behind the edge normal
 		double back = normal.dot(edgeNormal);
 		
-		if (side <= 0) {
+		if (side > 0) {
 			// test against the previous edge normal
 			if (prev == null) {
 				// if previous is null, then do normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side > 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 23 =====
```
 		// check if the normal is pointing behind the edge normal
 		double back = normal.dot(edgeNormal);
 		
-		if (side <= 0) {
+		if (side >= 0) {
 			// test against the previous edge normal
 			if (prev == null) {
 				// if previous is null, then do normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side >= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 24 =====
```
 		
 		if (side <= 0) {
 			// test against the previous edge normal
-			if (prev == null) {
+			if (prev == null || next == null) {
 				// if previous is null, then do normal 
 				// two-sided segment behavior
 				return;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null || next == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 25 =====
```
 				return;
 			}
 			
-			Vector2 prevEdge = link.getPreviousEdgeVector();
+			Vector2 prevEdge = link.getEdgeVector(); // Incorrectly uses the current edge instead of the previous edge
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getEdgeVector(); // Incorrectly uses the current edge instead of the previous edge
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 28 =====
```
 				return;
 			}
 			
-			Vector2 prevEdge = link.getPreviousEdgeVector();
+			Vector2 prevEdge = new Vector2(0, 0); // Initializes prevEdge to a zero vector, which is not valid
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = new Vector2(0, 0); // Initializes prevEdge to a zero vector, which is not valid
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 29 =====
```
 			}
 			
 			Vector2 prevEdge = link.getPreviousEdgeVector();
-			prevEdge.normalize();
+			prevEdge = new Vector2(0, 0); // This replaces prevEdge with a new zero vector, losing the original edge information.
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge = new Vector2(0, 0); // This replaces prevEdge with a new zero vector, losing the original edge information.
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 30 =====
```
 			}
 			
 			Vector2 prevEdge = link.getPreviousEdgeVector();
-			prevEdge.normalize();
+			prevEdge.rotate(Math.PI / 2); // This rotates the previous edge by 90 degrees, potentially leading to incorrect normal calculations.
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.rotate(Math.PI / 2); // This rotates the previous edge by 90 degrees, potentially leading to incorrect normal calculations.
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 31 =====
```
 			}
 			
 			Vector2 prevEdge = link.getPreviousEdgeVector();
-			prevEdge.normalize();
+			prevEdge.set(1.0, 1.0); // This sets the previous edge to a fixed vector, ignoring its actual direction.
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.set(1.0, 1.0); // This sets the previous edge to a fixed vector, ignoring its actual direction.
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 32 =====
```
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
-			boolean isConvex = prevEdge.cross(edge) > 0;
+			boolean isConvex = prevEdge.cross(edge) < 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) < 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 33 =====
```
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
-			boolean isConvex = prevEdge.cross(edge) > 0;
+			boolean isConvex = prevEdge.cross(edge) <= 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) <= 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 34 =====
```
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
-			boolean isConvex = prevEdge.cross(edge) > 0;
+			boolean isConvex = prevEdge.cross(edge) == 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) == 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 35 =====
```
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
-			boolean isConvex = prevEdge.cross(edge) > 0;
+			boolean isConvex = prevEdge.dot(edge) < 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.dot(edge) < 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 36 =====
```
 			prevEdge.normalize();
 			
 			// does the previous edge and this edge form a convex feature?
-			boolean isConvex = prevEdge.cross(edge) > 0;
+			boolean isConvex = prevEdge.dot(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.dot(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 37 =====
```
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
-			if (isConvex) {
+			if (!isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (!isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 38 =====
```
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
-			if (isConvex) {
+			if (back >= 0.0) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (back >= 0.0) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 39 =====
```
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
-			if (isConvex) {
+			if (prevEdge.cross(edge) <= 0) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (prevEdge.cross(edge) <= 0) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 40 =====
```
 			
 			// does the previous edge and this edge form a convex feature?
 			boolean isConvex = prevEdge.cross(edge) > 0;
-			if (isConvex) {
+			if (side > 0) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (side > 0) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 41 =====
```
 			boolean isConvex = prevEdge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
+				double region = normal.cross(edgeNormal);
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(edgeNormal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 42 =====
```
 			boolean isConvex = prevEdge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
+				double region = normal.cross(prevEdge);
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 43 =====
```
 			boolean isConvex = prevEdge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
+				double region = normal.dot(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.dot(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 44 =====
```
 			boolean isConvex = prevEdge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
+				double region = prevEdge.cross(normal);
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = prevEdge.cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 45 =====
```
 			boolean isConvex = prevEdge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
+				double region = prevEdge.getLeftHandOrthogonalVector().dot(normal);
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = prevEdge.getLeftHandOrthogonalVector().dot(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 46 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
-				if (region > 0.0) {
+				if (region != 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region != 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 47 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
-				if (region > 0.0) {
+				if (region < 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region < 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 48 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
-				if (region > 0.0) {
+				if (region <= 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region <= 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 49 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
-				if (region > 0.0) {
+				if (region == 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region == 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 50 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
-				if (region > 0.0) {
+				if (region >= 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region >= 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 51 =====
```
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
 					// else skip
-					penetration.clear();
+					
 				}
 				
 				// it's allowed as is
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 53 =====
```
 				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
 					// else skip
-					penetration.clear();
+					penetration.depth = Math.abs(penetration.depth); // Incorrectly ensuring depth is positive
 				}
 				
 				// it's allowed as is
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.depth = Math.abs(penetration.depth); // Incorrectly ensuring depth is positive
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 57 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (back <= 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back <= 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 58 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (back > 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back > 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 59 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (back >= 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back >= 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 60 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (side < 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (side < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 61 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (side == 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (side == 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 62 =====
```
 				// it's allowed as is
 			} else if (back < 0.0) {
 				// else skip
-				penetration.clear();
+				
 			} else {
 				// the previous edge and this edge form a concave feature
 				// for this case, it's always the edge normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 65 =====
```
 				// it's allowed as is
 			} else if (back < 0.0) {
 				// else skip
-				penetration.clear();
+				penetration.normal.x = -penetration.normal.x; penetration.normal.y = -penetration.normal.y; // Incorrectly negating the normal
 			} else {
 				// the previous edge and this edge form a concave feature
 				// for this case, it's always the edge normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.normal.x = -penetration.normal.x; penetration.normal.y = -penetration.normal.y; // Incorrectly negating the normal
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 67 =====
```
 				return;
 			}
 			
-			Vector2 nextEdge = link.getNextEdgeVector();
+			Vector2 nextEdge = link.getEdgeVector(); // Uses the same edge vector instead of the next edge vector
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getEdgeVector(); // Uses the same edge vector instead of the next edge vector
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 68 =====
```
 				return;
 			}
 			
-			Vector2 nextEdge = link.getNextEdgeVector();
+			Vector2 nextEdge = new Vector2(0, 0); // Initializes nextEdge to a zero vector, which is not valid
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = new Vector2(0, 0); // Initializes nextEdge to a zero vector, which is not valid
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 69 =====
```
 			}
 			
 			Vector2 nextEdge = link.getNextEdgeVector();
-			nextEdge.normalize();
+			nextEdge.add(new Vector2(1, 1)); // Adds an arbitrary vector to nextEdge, distorting its direction.
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.add(new Vector2(1, 1)); // Adds an arbitrary vector to nextEdge, distorting its direction.
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 70 =====
```
 			}
 			
 			Vector2 nextEdge = link.getNextEdgeVector();
-			nextEdge.normalize();
+			nextEdge.set(-nextEdge.x, -nextEdge.y); // Negates the nextEdge, which could lead to incorrect normal direction.
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.set(-nextEdge.x, -nextEdge.y); // Negates the nextEdge, which could lead to incorrect normal direction.
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 71 =====
```
 			}
 			
 			Vector2 nextEdge = link.getNextEdgeVector();
-			nextEdge.normalize();
+			nextEdge.set(0, 0); // Sets the nextEdge to a zero vector, causing incorrect normal calculations.
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.set(0, 0); // Sets the nextEdge to a zero vector, causing incorrect normal calculations.
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 72 =====
```
 			}
 			
 			Vector2 nextEdge = link.getNextEdgeVector();
-			nextEdge.normalize();
+			nextEdge.set(nextEdge.x, 0); // Sets the y-component of nextEdge to 0, potentially leading to an invalid normal.
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.set(nextEdge.x, 0); // Sets the y-component of nextEdge to 0, potentially leading to an invalid normal.
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 73 =====
```
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
-			boolean isConvex = edge.cross(nextEdge) > 0;
+			boolean isConvex = edge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 74 =====
```
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
-			boolean isConvex = edge.cross(nextEdge) > 0;
+			boolean isConvex = edge.cross(nextEdge) < 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) < 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 75 =====
```
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
-			boolean isConvex = edge.cross(nextEdge) > 0;
+			boolean isConvex = edge.cross(nextEdge) <= 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) <= 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 76 =====
```
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
-			boolean isConvex = edge.cross(nextEdge) > 0;
+			boolean isConvex = nextEdge.cross(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = nextEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 77 =====
```
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
-			boolean isConvex = edge.cross(nextEdge) > 0;
+			boolean isConvex = nextEdge.cross(nextEdge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = nextEdge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 78 =====
```
 			nextEdge.normalize();
 			
 			// does this edge and the next edge form a convex feature?
-			boolean isConvex = edge.cross(nextEdge) > 0;
+			boolean isConvex = nextEdge.dot(edge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = nextEdge.dot(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 79 =====
```
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
-			if (isConvex) {
+			if (!isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (!isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 80 =====
```
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
-			if (isConvex) {
+			if (back >= 0.0) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (back >= 0.0) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 81 =====
```
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
-			if (isConvex) {
+			if (normal.dot(edgeNormal) < 0) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (normal.dot(edgeNormal) < 0) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 82 =====
```
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
-			if (isConvex) {
+			if (penetration.getDepth() > 0) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (penetration.getDepth() > 0) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 83 =====
```
 			
 			// does this edge and the next edge form a convex feature?
 			boolean isConvex = edge.cross(nextEdge) > 0;
-			if (isConvex) {
+			if (side > 0) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
 				if (region > 0.0) {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (side > 0) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 84 =====
```
 			boolean isConvex = edge.cross(nextEdge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
+				double region = nextEdge.cross(normal);
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 85 =====
```
 			boolean isConvex = edge.cross(nextEdge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
+				double region = nextEdge.getLeftHandOrthogonalVector().dot(normal);
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().dot(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 86 =====
```
 			boolean isConvex = edge.cross(nextEdge) > 0;
 			if (isConvex) {
 				// check if the normal is outside the allowable range
-				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
+				double region = normal.cross(nextEdge.getLeftHandOrthogonalVector());
 				if (region > 0.0) {
 					// else skip
 					penetration.clear();
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(nextEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 87 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
-				if (region > 0.0) {
+				if (region < 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region < 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 88 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
-				if (region > 0.0) {
+				if (region <= 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region <= 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 89 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
-				if (region > 0.0) {
+				if (region == 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region == 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 90 =====
```
 			if (isConvex) {
 				// check if the normal is outside the allowable range
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
-				if (region > 0.0) {
+				if (region >= 0.0) {
 					// else skip
 					penetration.clear();
 				}
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region >= 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 91 =====
```
 				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
 				if (region > 0.0) {
 					// else skip
-					penetration.clear();
+					
 				}
 				
 				// it's allowed as is
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 97 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (back <= 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back <= 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 98 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (back > 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back > 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 99 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (back >= 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back >= 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 100 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (side < 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (side < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 101 =====
```
 				}
 				
 				// it's allowed as is
-			} else if (back < 0.0) {
+			} else if (side == 0.0) {
 				// else skip
 				penetration.clear();
 			} else {
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (side == 0.0) {
				// else skip
				penetration.clear();
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
===== 102 =====
```
 				// it's allowed as is
 			} else if (back < 0.0) {
 				// else skip
-				penetration.clear();
+				
 			} else {
 				// this edge and the next edge form a concave feature
 				// for this case, it's always the edge normal
```
```
	/**
	 * Attempts to use the connectivity information to determine if the normal found in the narrow-phase is valid.
	 * If not, the normal is modified to within the valid range of normals based on the connectivity and the collision
	 * depth is adjusted.
	 * @param link the link
	 * @param penetration the narrow-phase collision information
	 */
	public void process(Link link, Penetration penetration) {
		Vector2 prev = link.getPoint0();
		Vector2 next = link.getPoint3();
		
		if (prev == null && next == null) {
			// if there's no connectivity info, then take
			// what the narrowphase gave us
			return;
		}
		
		Vector2 normal = penetration.getNormal().copy();
		Vector2 edge = link.getEdgeVector();
		Vector2 edgeNormal = edge.getLeftHandOrthogonalVector();
		
		// what "side" is the normal pointing towards?
		double side = normal.dot(edge);
		
		// check if the normal is pointing behind the edge normal
		double back = normal.dot(edgeNormal);
		
		if (side <= 0) {
			// test against the previous edge normal
			if (prev == null) {
				// if previous is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 prevEdge = link.getPreviousEdgeVector();
			prevEdge.normalize();
			
			// does the previous edge and this edge form a convex feature?
			boolean isConvex = prevEdge.cross(edge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = normal.cross(prevEdge.getLeftHandOrthogonalVector());
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				penetration.clear();
			} else {
				// the previous edge and this edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		} else {
			// test against the next edge normal
			if (next == null) {
				// if next is null, then do normal 
				// two-sided segment behavior
				return;
			}
			
			Vector2 nextEdge = link.getNextEdgeVector();
			nextEdge.normalize();
			
			// does this edge and the next edge form a convex feature?
			boolean isConvex = edge.cross(nextEdge) > 0;
			if (isConvex) {
				// check if the normal is outside the allowable range
				double region = nextEdge.getLeftHandOrthogonalVector().cross(normal);
				if (region > 0.0) {
					// else skip
					penetration.clear();
				}
				
				// it's allowed as is
			} else if (back < 0.0) {
				// else skip
				
			} else {
				// this edge and the next edge form a concave feature
				// for this case, it's always the edge normal
				Vector2 norm = edgeNormal;
				penetration.normal.x = norm.x;
				penetration.normal.y = norm.y;
			}
		}
		
		return;
	}
```
