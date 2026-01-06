https://github.com/yinlou/mltk/blob/f50c42986fdd016e7da38d5e381ed24d8fe87e41/./src/main/java/mltk/util/VectorUtils.java#L191-L212
```
// @ ensures (a != null && b != null && a.length == b.length && a.length > 1 && !java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == a[0]) && !java.util.stream.IntStream.range(0, b.length).allMatch(i -> b[i] == b[0])) ==> (\result >= -1.0 && \result <= 1.0);
// @ ensures (a != null && b != null && a.length == b.length && a.length > 1 && java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == b[i]) && !java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == a[0])) ==> (\result == 1.0);
// @ ensures (a != null && b != null && a.length == b.length && a.length > 1 && java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] - b[i] == (a[0] - b[0])) && !java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == a[0]) && !java.util.stream.IntStream.range(0, b.length).allMatch(i -> b[i] == b[0])) ==> (\result == 1.0);
// @ ensures (a != null && b != null && a.length == b.length && a.length > 1 && java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == -b[i]) && !java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == a[0]) && !java.util.stream.IntStream.range(0, b.length).allMatch(i -> b[i] == b[0])) ==> (\result == -1.0);
// @ ensures (a != null && b != null && a.length == b.length && a.length > 1 && java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] + b[i] == (a[0] + b[0])) && !java.util.stream.IntStream.range(0, a.length).allMatch(i -> a[i] == a[0]) && !java.util.stream.IntStream.range(0, b.length).allMatch(i -> b[i] == b[0])) ==> (\result == -1.0);
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
//@ ensures (StatUtils.sumSq(\old(a)) - \old(a.length) * StatUtils.mean(\old(a)) * StatUtils.mean(\old(a)) > 0 && StatUtils.sumSq(\old(b)) - \old(b.length) * StatUtils.mean(\old(b)) * StatUtils.mean(\old(b)) > 0) ==> \result == (VectorUtils.dotProduct(\old(a), \old(b)) - \old(a.length) * StatUtils.mean(\old(a)) * StatUtils.mean(\old(b))) / Math.sqrt((StatUtils.sumSq(\old(a)) - \old(a.length) * StatUtils.mean(\old(a)) * StatUtils.mean(\old(a))) * (StatUtils.sumSq(\old(b)) - \old(b.length) * StatUtils.mean(\old(b)) * StatUtils.mean(\old(b))));
```
===== 5: failed =====
```
 	 */
 	public static double correlation(double[] a, double[] b) {
 		double mean1 = StatUtils.mean(a);
-		double mean2 = StatUtils.mean(b);
+		double mean2 = 0; // Setting mean2 to zero, which will affect the correlation calculation
 		double x = 0;
 		double s1 = 0;
 		double s2 = 0;
```
```
	/**
	 * Returns the Pearson correlation coefficient between two vectors.
	 * 
	 * @param a the 1st vector.
	 * @param b the 2nd vector.
	 * @return the Pearson correlation coefficient between two vectors.
	 */
	public static double correlation(double[] a, double[] b) {
		double mean1 = StatUtils.mean(a);
		double mean2 = 0; // Setting mean2 to zero, which will affect the correlation calculation
		double x = 0;
		double s1 = 0;
		double s2 = 0;
		for (int i = 0; i < a.length; i++) {
			double d1 = (a[i] - mean1);
			double d2 = (b[i] - mean2);
			x += d1 * d2;
			s1 += d1 * d1;
			s2 += d2 * d2;
		}
		return x / Math.sqrt(s1 * s2);
	}
```
