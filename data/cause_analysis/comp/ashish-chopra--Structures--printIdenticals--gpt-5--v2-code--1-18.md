https://github.com/ashish-chopra/Structures/blob/ce0a8f131568368bec3110f4ffddcb74d0b9ca0f/./src/main/java/com/applications/Identicals.java#L28-L52
```
// @ ensures \result != null;
// @ ensures first == \old(first) && second == \old(second);
// @ ensures java.util.Arrays.equals(first, \old(first)) && java.util.Arrays.equals(second, \old(second));
// @ ensures \result.startsWith("[") && \result.endsWith("]");
// @ ensures \result.length() >= 2;
// @ ensures (\result.length() > 2) ==> (\result.charAt(\result.length()-2) == ',');
// @ ensures \result.chars().filter(c -> c == ',').count() == java.util.Arrays.stream(\result.substring(1, \result.length()-1).split(",")).filter(s -> !s.isEmpty()).count();
// @ ensures (!java.util.Arrays.stream(\old(first)).anyMatch(a -> java.util.Arrays.stream(\old(second)).anyMatch(b -> b == a))) ==> \result.equals("[]");
// @ ensures !\result.equals("[]") ==> java.util.Arrays.stream(\old(first)).anyMatch(a -> java.util.Arrays.stream(\old(second)).anyMatch(b -> b == a));
// @ ensures java.util.Arrays.stream(\result.substring(1, \result.length()-1).split(",")).filter(s -> !s.isEmpty()).count() <= Math.min(first.length, second.length);
// @ ensures java.util.Arrays.stream(\result.substring(1, \result.length()-1).split(",")).filter(s -> !s.isEmpty()).mapToInt(Integer::parseInt).allMatch(x -> java.util.Arrays.stream(\old(first)).anyMatch(a -> a == x) && java.util.Arrays.stream(\old(second)).anyMatch(b -> b == x));
// @ ensures java.util.Arrays.stream(\result.substring(1, \result.length()-1).split(",")).filter(s -> !s.isEmpty()).mapToInt(Integer::parseInt).allMatch(x -> java.util.Arrays.stream(\result.substring(1, \result.length()-1).split(",")).filter(t -> !t.isEmpty()).mapToInt(Integer::parseInt).filter(y -> y == x).count() <= Math.min(java.util.Arrays.stream(\old(first)).filter(a -> a == x).count(), java.util.Arrays.stream(\old(second)).filter(b -> b == x).count()));
```
```
return value - primitive-like/scalar types

return value content

primitive-like/scalar types
```
passed
```
//@ ensures \result != null;
//@ ensures \result.equals("[" + java.util.stream.IntStream.range(0, first.length).filter(i -> java.util.stream.IntStream.range(0, i).noneMatch(k -> first[k] == first[i])).mapToObj(i -> { int v = first[i]; int c1 = (int) java.util.stream.IntStream.range(0, first.length).filter(k -> first[k] == v).count(); int c2 = (int) java.util.stream.IntStream.range(0, second.length).filter(k -> second[k] == v).count(); return java.util.stream.IntStream.range(0, Math.min(c1, c2)).mapToObj(x -> String.valueOf(v) + ",").collect(java.util.stream.Collectors.joining("")); }).collect(java.util.stream.Collectors.joining("")) + "]");
```
===== 18: failed =====
```
 			if (result == 0) {
 				list += first[i] + ",";
 				i++; j++;
-			} else if (result == -1) 
+			} else if (result == 1)
 				j++;
 			else 
 				i++;
```
```
	/**
	 * returns the identical numbers found in
	 * both the sorted array of N integers in running
	 * time of T(N) ~ N for worst case.
	 * 
	 */
	public String printIdenticals() { 
		// instead of printing, we return the list 
		// to compare with expected values
		String list = "[";	
		int i = 0, j = 0;
		while (i < first.length && j < second.length) {
			int result = compare(first[i], second[j]);
			if (result == 0) {
				list += first[i] + ",";
				i++; j++;
			} else if (result == 1)
				j++;
			else 
				i++;
		}
		list +=  "]";
		System.out.println(list);
		return list;
	}
```
