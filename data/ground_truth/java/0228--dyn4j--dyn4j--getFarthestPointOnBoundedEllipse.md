https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/Ellipse.java#L435-L496
```
//@ ensures \result != null;
//@ ensures \result.x >= xmin - 1.0e-9 && \result.x <= xmax + 1.0e-9;
//@ ensures \result.y >= -1.0e-9;
//@ ensures Math.abs(((\result.x * \result.x) / (a * a) + (\result.y * \result.y) / (b * b)) - 1.0) <= 1.0e-8;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - xmin) * (point.x - xmin) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmin * xmin))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmin * xmin)))))) - 1.0e-9;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - xmax) * (point.x - xmax) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmax * xmax))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmax * xmax)))))) - 1.0e-9;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - ((xmin + xmax) * 0.5)) * (point.x - ((xmin + xmax) * 0.5)) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (((xmin + xmax) * 0.5) * ((xmin + xmax) * 0.5)))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (((xmin + xmax) * 0.5) * ((xmin + xmax) * 0.5))))))) - 1.0e-9;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - ((2.0 * xmin + xmax) / 3.0)) * (point.x - ((2.0 * xmin + xmax) / 3.0)) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (((2.0 * xmin + xmax) / 3.0) * ((2.0 * xmin + xmax) / 3.0)))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (((2.0 * xmin + xmax) / 3.0) * ((2.0 * xmin + xmax) / 3.0))))))) - 1.0e-9;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - ((xmin + 2.0 * xmax) / 3.0)) * (point.x - ((xmin + 2.0 * xmax) / 3.0)) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (((xmin + 2.0 * xmax) / 3.0) * ((xmin + 2.0 * xmax) / 3.0)))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (((xmin + 2.0 * xmax) / 3.0) * ((xmin + 2.0 * xmax) / 3.0))))))) - 1.0e-9;
//@ ensures \result.x <= xmin + 1.0e-6 || \result.x >= xmax - 1.0e-6 || Math.abs(-2.0 * (point.x - \result.x) + 2.0 * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (\result.x * \result.x))))) * ((b / a) * \result.x / Math.sqrt(Math.max(0.0, (a * a) - (\result.x * \result.x))))) <= 2.0e-2;
```
```
//@ ensures \result != null;
//@ ensures \result.x >= xmin - 1e-9 && \result.x <= xmax + 1e-9;
//@ ensures \result.y >= -1e-9;
//@ ensures Math.abs(((\result.x * \result.x) / (a * a) + (\result.y * \result.y) / (b * b)) - 1.0) <= 1e-9;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - xmin) * (point.x - xmin) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmin * xmin))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmin * xmin)))))) - 1e-9;
//@ ensures ((point.x - \result.x) * (point.x - \result.x) + (point.y - \result.y) * (point.y - \result.y)) >= ((point.x - xmax) * (point.x - xmax) + (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmax * xmax))))) * (point.y - ((b / a) * Math.sqrt(Math.max(0.0, (a * a) - (xmax * xmax)))))) - 1e-9;
```
[9, 13, 15, 27, 28, 31, 32, 33]
===== 9 =====
```
 		// compute the golden ratio test points
 		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
 		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
-		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
+		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2 - 1.0, q, p);
 		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
 
 		// our bracket is now: [x0, x2, x3, x1]
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2 - 1.0, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
			}
		}
			
		return p;
	}
```
===== 13 =====
```
 
 		// our bracket is now: [x0, x2, x3, x1]
 		// iteratively reduce the bracket
-		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
+		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i += 3) {
 			if (fx2 < fx3) {
 				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
 					break;
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i += 3) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
			}
		}
			
		return p;
	}
```
===== 15 =====
```
 		// our bracket is now: [x0, x2, x3, x1]
 		// iteratively reduce the bracket
 		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
-			if (fx2 < fx3) {
+			if (fx2 != fx3) {
 				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
 					break;
 				}
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 != fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
			}
		}
			
		return p;
	}
```
===== 27 =====
```
 				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
 				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
 			} else {
-				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
+				if (Math.abs(x3 - x0) > FARTHEST_POINT_EPSILON) {
 					break;
 				}
 				x1 = x3;
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) > FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
			}
		}
			
		return p;
	}
```
===== 28 =====
```
 				x1 = x3;
 				x3 = x2;
 				fx3 = fx2;
-				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
+				x2 = x1 + (x1 - x0) * INV_GOLDEN_RATIO;
 				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
 			}
 		}
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
			}
		}
			
		return p;
	}
```
===== 31 =====
```
 				x3 = x2;
 				fx3 = fx2;
 				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
-				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
+				fx2 = Ellipse.getSquaredDistance(aa, ba, x2 + 1, q, p);
 			}
 		}
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2 + 1, q, p);
			}
		}
			
		return p;
	}
```
===== 32 =====
```
 				x3 = x2;
 				fx3 = fx2;
 				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
-				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
+				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, new Vector2(px + 1, py), p);
 			}
 		}
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, new Vector2(px + 1, py), p);
			}
		}
			
		return p;
	}
```
===== 33 =====
```
 				x3 = x2;
 				fx3 = fx2;
 				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
-				fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
+				fx2 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
 			}
 		}
```
```
	/**
	 * Performs a golden section search of the ellipse bounded between the interval [xmin, xmax] for the farthest
	 * point from the given point.
	 * <p>
	 * This method assumes that this ellipse is centered on the origin and 
	 * has it's semi-major axis aligned with the x-axis and its semi-minor 
	 * axis aligned with the y-axis.
	 * @param xmin the minimum x value
	 * @param xmax the maximum x value
	 * @param a the half width of the ellipse
	 * @param b the half height of the ellipse
	 * @param point the query point
	 * @return {@link Vector2}
	 * @since 3.4.0
	 */
	static final Vector2 getFarthestPointOnBoundedEllipse(double xmin, double xmax, double a, double b, Vector2 point) 
	{
		double px = point.x;
		double py = point.y;
		
		// our bracketing bounds will be [x0, x1]
		double x0 = xmin;
		double x1 = xmax;

		final Vector2 q = new Vector2(px, py);
		final Vector2 p = new Vector2();
		
		final double aa = a * a;
		final double ba = b / a;

		// compute the golden ratio test points
		double x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
		double x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
		double fx2 = Ellipse.getSquaredDistance(aa, ba, x2, q, p);
		double fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);

		// our bracket is now: [x0, x2, x3, x1]
		// iteratively reduce the bracket
		for (int i = 0; i < FARTHEST_POINT_MAX_ITERATIONS; i++) {
			if (fx2 < fx3) {
				if (Math.abs(x1 - x2) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x0 = x2;
				x2 = x3;
				fx2 = fx3;
				x3 = x0 + (x1 - x0) * INV_GOLDEN_RATIO;
				fx3 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			} else {
				if (Math.abs(x3 - x0) <= FARTHEST_POINT_EPSILON) {
					break;
				}
				x1 = x3;
				x3 = x2;
				fx3 = fx2;
				x2 = x1 - (x1 - x0) * INV_GOLDEN_RATIO;
				fx2 = Ellipse.getSquaredDistance(aa, ba, x3, q, p);
			}
		}
			
		return p;
	}
```
