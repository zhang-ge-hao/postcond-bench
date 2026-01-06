https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/AdaptiveDecimal.java#L550-L601
```
//@ ensures \result != null;
//@ ensures \old(result) == null ==> \result != \old(result);
//@ ensures \old(result) != null ==> \result == \old(result);
//@ ensures \result.size() == 4;
//@ ensures \result.capacity() >= 4;
```
```
return value - inner repository type


return value content

repository defined type
```
passed
```
//@ ensures \result != null;
//@ ensures \result.size() == 4;
//@ ensures \old(result) != null ==> \result == \old(result);
//@ ensures \result.get(0) == AdaptiveDecimal.getErrorComponentFromDifference(a0, b0, a0 - b0);
//@ ensures \result.get(1) == AdaptiveDecimal.getErrorComponentFromDifference(AdaptiveDecimal.getErrorComponentFromSum(a1, a0 - b0, a1 + (a0 - b0)), b1, AdaptiveDecimal.getErrorComponentFromSum(a1, a0 - b0, a1 + (a0 - b0)) - b1);
//@ ensures \result.get(2) == AdaptiveDecimal.getErrorComponentFromSum(a1 + (a0 - b0), AdaptiveDecimal.getErrorComponentFromSum(a1, a0 - b0, a1 + (a0 - b0)) - b1, (a1 + (a0 - b0)) + (AdaptiveDecimal.getErrorComponentFromSum(a1, a0 - b0, a1 + (a0 - b0)) - b1));
//@ ensures \result.get(3) == (a1 + (a0 - b0)) + (AdaptiveDecimal.getErrorComponentFromSum(a1, a0 - b0, a1 + (a0 - b0)) - b1);
```
===== 16: failed =====
```
 		x1 = AdaptiveDecimal.getErrorComponentFromDifference(imm1, b1, imm = imm1 - b1);
 		x2 = AdaptiveDecimal.getErrorComponentFromSum(imm2, imm, x3 = imm2 + imm);
 		
-		result.append(x0);
+		result.append(Double.NaN);
 		result.append(x1);
 		result.append(x2);
 		result.append(x3);
```
```
	/**
	 * Given two unrolled expansions (a0, a1) and (b0, b1) performs the difference
	 * (a0, a1) - (b0, b1) and stores the 4 component result in the given {@link AdaptiveDecimal} {@code result}.
	 * In the same way as with {@link AdaptiveDecimal#sum(AdaptiveDecimal, AdaptiveDecimal)} if {@code result} is null
	 * a new one is allocated, otherwise the existing is cleared and used.
	 * Does not perform zero elimination.
	 * This is also a helper method to allow fast computation of the cross product
	 * without the overhead of creating new {@link AdaptiveDecimal} and performing
	 * the generalized sum procedure.
	 * 
	 * @param a0 The first component of a
	 * @param a1 The second component of a
	 * @param b0 The first component of b
	 * @param b1 The second component of b
	 * @param result The {@link AdaptiveDecimal} in which the difference is stored or null to allocate a new one
	 * @return The result
	 */
	static AdaptiveDecimal fromDiff(double a0, double a1, double b0, double b1, AdaptiveDecimal result) {
		// the exact order of those operations is necessary for correct functionality 
		// This is a rewrite of the corresponding Two_Two_Diff macro in the original code
		
		// allocate a new instance of sufficient size if result is null or just clear
		if (result == null) {
			result = new AdaptiveDecimal(4);
		} else {
			result.clear();	
		}
		
		// x0-x1-x2-x3 store the resulting components with increasing magnitude
		double x0, x1, x2, x3;
		
		// variable to store immediate results for each pair of Diff/Sum
		double imm;
		
		// variables to store immediate results across the two pairs 
		double imm1, imm2;
		
		// Diff (a0, a1) - b0, result = (x0, imm1, imm2)
		x0 = AdaptiveDecimal.getErrorComponentFromDifference(a0, b0, imm = a0 - b0);
		imm1 = AdaptiveDecimal.getErrorComponentFromSum(a1, imm, imm2 = a1 + imm);
		
		// Diff (imm1, imm2) - b1, result = (x1, x2, x3)
		x1 = AdaptiveDecimal.getErrorComponentFromDifference(imm1, b1, imm = imm1 - b1);
		x2 = AdaptiveDecimal.getErrorComponentFromSum(imm2, imm, x3 = imm2 + imm);
		
		result.append(Double.NaN);
		result.append(x1);
		result.append(x2);
		result.append(x3);
		
		return result;
	}
```
