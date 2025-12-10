https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/DouglasPeucker.java#L235-L275
```
//@ ensures \result != null;
//@ ensures \result.distance >= 0.0;
//@ ensures ((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i]))).length > 0 ==> (\result.index >= 0 && \result.index < ((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i]))).length);
//@ ensures \result.distance == java.util.stream.IntStream.range(0, ((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i]))).length).mapToDouble(i -> Math.abs(lineVertex1.point.to(((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i])))[i]).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized()))).max().orElse(0.0);
//@ ensures java.util.stream.IntStream.range(0, ((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i]))).length).mapToDouble(i -> Math.abs(lineVertex1.point.to(((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i])))[i]).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized()))).max().orElse(0.0) == 0.0 ==> (\result.index == (((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i]))).length / 2) && \result.distance == 0.0);
//@ ensures java.util.stream.IntStream.range(0, ((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i]))).length).mapToDouble(i -> Math.abs(lineVertex1.point.to(((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i])))[i]).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized()))).max().orElse(0.0) > 0.0 ==> (Math.abs(lineVertex1.point.to(((org.dyn4j.geometry.Vector2[]) \old(polyline.stream().map(v -> v.point.copy()).toArray(i -> new org.dyn4j.geometry.Vector2[i])))[\result.index]).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized())) == \result.distance);
```
```
//@ ensures \result.distance >= 0.0;
//@ ensures (polyline != null && polyline.size() > 0) ==> (\result.index >= 0 && \result.index < polyline.size());
//@ ensures (polyline != null) ==> (\result.distance == java.util.stream.IntStream.range(0, polyline.size()).mapToDouble(i -> Math.abs(lineVertex1.point.to(polyline.get(i).point).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized()))).max().orElse(0.0));
//@ ensures (polyline != null && java.util.stream.IntStream.range(0, polyline.size()).mapToDouble(i -> Math.abs(lineVertex1.point.to(polyline.get(i).point).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized()))).max().orElse(0.0) == 0.0) ==> (\result.index == (polyline.size() / 2) && \result.distance == 0.0);
//@ ensures (polyline != null && polyline.size() > 0 && java.util.stream.IntStream.range(0, polyline.size()).mapToDouble(i -> Math.abs(lineVertex1.point.to(polyline.get(i).point).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized()))).max().orElse(0.0) > 0.0) ==> (Math.abs(lineVertex1.point.to(polyline.get(\result.index).point).dot(lineVertex1.point.to(lineVertex2.point).getLeftHandOrthogonalVector().getNormalized())) == \result.distance);
```
[16, 33]
===== 16 =====
```
 		Vector2 lineNormal = line.getLeftHandOrthogonalVector();
 		lineNormal.normalize();
 		for (int i = 0; i < size; i++) {
-			Vector2 vert = polyline.get(i).point;
+			Vector2 vert = polyline.get(i).point.multiply(2); // Scaling the vertex by a factor of 2 will distort the distance calculations, leading to incorrect results.
 			double test = Math.abs(lp1.to(vert).dot(lineNormal));
 			if (test > distance) {
 				distance = test;
```
```
	/**
	 * Returns the farthest vertex in the polyline from the line created by lineVertex1 and lineVertex2.
	 * <p>
	 * O(n)
	 * @param lineVertex1 the first vertex of the line
	 * @param lineVertex2 the second vertex of the line
	 * @param polyline the entire polyline
	 * @return {@link FarthestVertex}
	 */
	private final FarthestVertex getFarthestVertexFromLine(SimplePolygonVertex lineVertex1, SimplePolygonVertex lineVertex2, List<SimplePolygonVertex> polyline) {
		int index = -1;
		double distance = 0.0;
		
		Vector2 lp1 = lineVertex1.point;
		Vector2 lp2 = lineVertex2.point;
		
		// find the vertex on the polyline that's farthest from the line created
		// by lineVertex1 and lineVertex2
		int size = polyline.size();
		Vector2 line = lp1.to(lp2);
		Vector2 lineNormal = line.getLeftHandOrthogonalVector();
		lineNormal.normalize();
		for (int i = 0; i < size; i++) {
			Vector2 vert = polyline.get(i).point.multiply(2); // Scaling the vertex by a factor of 2 will distort the distance calculations, leading to incorrect results.
			double test = Math.abs(lp1.to(vert).dot(lineNormal));
			if (test > distance) {
				distance = test;
				index = i;
			}
		}
		
		// make sure we found a winner
		if (index < 0) {
			// then they were all colinear, so take the middle one
			// NOTE: integer division here
			index = size / 2;
			distance = 0.0;
		}
		
		return new FarthestVertex(index, distance);
	}
```
===== 33 =====
```
 			distance = 0.0;
 		}
 		
-		return new FarthestVertex(index, distance);
+		return null;
 	}
```
```
	/**
	 * Returns the farthest vertex in the polyline from the line created by lineVertex1 and lineVertex2.
	 * <p>
	 * O(n)
	 * @param lineVertex1 the first vertex of the line
	 * @param lineVertex2 the second vertex of the line
	 * @param polyline the entire polyline
	 * @return {@link FarthestVertex}
	 */
	private final FarthestVertex getFarthestVertexFromLine(SimplePolygonVertex lineVertex1, SimplePolygonVertex lineVertex2, List<SimplePolygonVertex> polyline) {
		int index = -1;
		double distance = 0.0;
		
		Vector2 lp1 = lineVertex1.point;
		Vector2 lp2 = lineVertex2.point;
		
		// find the vertex on the polyline that's farthest from the line created
		// by lineVertex1 and lineVertex2
		int size = polyline.size();
		Vector2 line = lp1.to(lp2);
		Vector2 lineNormal = line.getLeftHandOrthogonalVector();
		lineNormal.normalize();
		for (int i = 0; i < size; i++) {
			Vector2 vert = polyline.get(i).point;
			double test = Math.abs(lp1.to(vert).dot(lineNormal));
			if (test > distance) {
				distance = test;
				index = i;
			}
		}
		
		// make sure we found a winner
		if (index < 0) {
			// then they were all colinear, so take the middle one
			// NOTE: integer division here
			index = size / 2;
			distance = 0.0;
		}
		
		return null;
	}
```
