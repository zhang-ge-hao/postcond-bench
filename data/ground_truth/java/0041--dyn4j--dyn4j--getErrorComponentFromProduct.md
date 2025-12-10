https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AdaptiveDecimal.java#L656-L686
```
//@ ensures \result == ((a - ((RobustGeometry.SPLITTER * a) - ((RobustGeometry.SPLITTER * a) - a))) * (b - ((RobustGeometry.SPLITTER * b) - ((RobustGeometry.SPLITTER * b) - b))) - (((product - (((RobustGeometry.SPLITTER * a) - ((RobustGeometry.SPLITTER * a) - a)) * ((RobustGeometry.SPLITTER * b) - ((RobustGeometry.SPLITTER * b) - b)))) - ((a - ((RobustGeometry.SPLITTER * a) - ((RobustGeometry.SPLITTER * a) - a))) * ((RobustGeometry.SPLITTER * b) - ((RobustGeometry.SPLITTER * b) - b)))) - (((RobustGeometry.SPLITTER * a) - ((RobustGeometry.SPLITTER * a) - a)) * (b - ((RobustGeometry.SPLITTER * b) - ((RobustGeometry.SPLITTER * b) - b))))));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
===== 0 =====
```
 		// the exact order of those operations is necessary for correct functionality 
 		
 		// split a in two parts
-		double ac = RobustGeometry.SPLITTER * a;
+		double ac = RobustGeometry.SPLITTER / a;
 		double abig = ac - a;
 		double ahi = ac - abig;
 		double alo = a - ahi;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER / a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 1 =====
```
 		
 		// split a in two parts
 		double ac = RobustGeometry.SPLITTER * a;
-		double abig = ac - a;
+		double abig = ac + a;
 		double ahi = ac - abig;
 		double alo = a - ahi;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac + a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 2 =====
```
 		// split a in two parts
 		double ac = RobustGeometry.SPLITTER * a;
 		double abig = ac - a;
-		double ahi = ac - abig;
+		double ahi = ac + abig;
 		double alo = a - ahi;
 		
 		// split b in two parts
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac + abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 3 =====
```
 		double ac = RobustGeometry.SPLITTER * a;
 		double abig = ac - a;
 		double ahi = ac - abig;
-		double alo = a - ahi;
+		double alo = a + ahi;
 		
 		// split b in two parts
 		double bc = RobustGeometry.SPLITTER * b;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a + ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 4 =====
```
 		double alo = a - ahi;
 		
 		// split b in two parts
-		double bc = RobustGeometry.SPLITTER * b;
+		double bc = RobustGeometry.SPLITTER / b;
 		double bbig = bc - b;
 		double bhi = bc - bbig;
 		double blo = b - bhi;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER / b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 5 =====
```
 		
 		// split b in two parts
 		double bc = RobustGeometry.SPLITTER * b;
-		double bbig = bc - b;
+		double bbig = bc + b;
 		double bhi = bc - bbig;
 		double blo = b - bhi;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc + b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 6 =====
```
 		// split b in two parts
 		double bc = RobustGeometry.SPLITTER * b;
 		double bbig = bc - b;
-		double bhi = bc - bbig;
+		double bhi = bc + bbig;
 		double blo = b - bhi;
 		
 		double error1 = product - (ahi * bhi);
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc + bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 7 =====
```
 		double bc = RobustGeometry.SPLITTER * b;
 		double bbig = bc - b;
 		double bhi = bc - bbig;
-		double blo = b - bhi;
+		double blo = b + bhi;
 		
 		double error1 = product - (ahi * bhi);
 		double error2 = error1 - (alo * bhi);
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b + bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 8 =====
```
 		double bhi = bc - bbig;
 		double blo = b - bhi;
 		
-		double error1 = product - (ahi * bhi);
+		double error1 = product + (ahi * bhi);
 		double error2 = error1 - (alo * bhi);
 		double error3 = error2 - (ahi * blo);
 		double error = alo * blo - error3;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product + (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 9 =====
```
 		double bhi = bc - bbig;
 		double blo = b - bhi;
 		
-		double error1 = product - (ahi * bhi);
+		double error1 = product - (ahi / bhi);
 		double error2 = error1 - (alo * bhi);
 		double error3 = error2 - (ahi * blo);
 		double error = alo * blo - error3;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi / bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 10 =====
```
 		double blo = b - bhi;
 		
 		double error1 = product - (ahi * bhi);
-		double error2 = error1 - (alo * bhi);
+		double error2 = error1 + (alo * bhi);
 		double error3 = error2 - (ahi * blo);
 		double error = alo * blo - error3;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 + (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 11 =====
```
 		double blo = b - bhi;
 		
 		double error1 = product - (ahi * bhi);
-		double error2 = error1 - (alo * bhi);
+		double error2 = error1 - (alo / bhi);
 		double error3 = error2 - (ahi * blo);
 		double error = alo * blo - error3;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo / bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 12 =====
```
 		
 		double error1 = product - (ahi * bhi);
 		double error2 = error1 - (alo * bhi);
-		double error3 = error2 - (ahi * blo);
+		double error3 = error2 + (ahi * blo);
 		double error = alo * blo - error3;
 		
 		return error;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 + (ahi * blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 13 =====
```
 		
 		double error1 = product - (ahi * bhi);
 		double error2 = error1 - (alo * bhi);
-		double error3 = error2 - (ahi * blo);
+		double error3 = error2 - (ahi / blo);
 		double error = alo * blo - error3;
 		
 		return error;
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi / blo);
		double error = alo * blo - error3;
		
		return error;
	}
```
===== 14 =====
```
 		double error1 = product - (ahi * bhi);
 		double error2 = error1 - (alo * bhi);
 		double error3 = error2 - (ahi * blo);
-		double error = alo * blo - error3;
+		double error = alo * blo + error3;
 		
 		return error;
 	}
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo + error3;
		
		return error;
	}
```
===== 15 =====
```
 		double error1 = product - (ahi * bhi);
 		double error2 = error1 - (alo * bhi);
 		double error3 = error2 - (ahi * blo);
-		double error = alo * blo - error3;
+		double error = alo / blo - error3;
 		
 		return error;
 	}
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo / blo - error3;
		
		return error;
	}
```
===== 16 =====
```
 		double error3 = error2 - (ahi * blo);
 		double error = alo * blo - error3;
 		
-		return error;
+		return 0;
 	}
```
```
	/**
	 * Given two values a, b and their product = fl(a * b) calculates the value error for which
	 * fl(a) * fl(b) = fl(a * b) + fl(error).
	 * 
	 * @param a The first value
	 * @param b The second value
	 * @param product Their product, must always be product = fl(a * b)
	 * @return The error described above
	 */
	public static double getErrorComponentFromProduct(double a, double b, double product) {
		// the exact order of those operations is necessary for correct functionality 
		
		// split a in two parts
		double ac = RobustGeometry.SPLITTER * a;
		double abig = ac - a;
		double ahi = ac - abig;
		double alo = a - ahi;
		
		// split b in two parts
		double bc = RobustGeometry.SPLITTER * b;
		double bbig = bc - b;
		double bhi = bc - bbig;
		double blo = b - bhi;
		
		double error1 = product - (ahi * bhi);
		double error2 = error1 - (alo * bhi);
		double error3 = error2 - (ahi * blo);
		double error = alo * blo - error3;
		
		return 0;
	}
```
