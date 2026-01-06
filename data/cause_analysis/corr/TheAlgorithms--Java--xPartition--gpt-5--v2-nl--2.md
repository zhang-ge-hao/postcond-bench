https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/divideandconquer/ClosestPair.java#L77-L102
```
// @ ensures \result >= first && \result <= last;
// @ ensures a == \old(a);
// @ ensures java.util.stream.IntStream.range(0, first).allMatch(i -> a[i].x == \old(a[i].x) && a[i].y == \old(a[i].y));
// @ ensures java.util.stream.IntStream.range(last + 1, a.length).allMatch(i -> a[i].x == \old(a[i].x) && a[i].y == \old(a[i].y));
// @ ensures java.util.stream.IntStream.range(first, \result).allMatch(i -> a[i].x <= a[\result].x);
// @ ensures java.util.stream.IntStream.range(\result + 1, last + 1).allMatch(i -> a[i].x >= a[\result].x);
// @ ensures java.util.stream.IntStream.rangeClosed(first, last).anyMatch(i -> a[\result].x == \old(a[i].x) && a[\result].y == \old(a[i].y));
// @ ensures java.util.stream.IntStream.rangeClosed(first, last).allMatch(k -> java.util.stream.IntStream.rangeClosed(first, last).anyMatch(j -> a[k].x == \old(a[j].x) && a[k].y == \old(a[j].y));
// @ ensures java.util.stream.IntStream.rangeClosed(first, last).allMatch(j -> java.util.stream.IntStream.rangeClosed(first, last).anyMatch(k -> a[k].x == \old(a[j].x) && a[k].y == \old(a[j].y));
```
```
syntax error

error: ')' or ',' expected
```
compile_failure
```
//@ ensures \result >= first && \result <= last;
//@ ensures a[\result] == \old(a[last]);
//@ ensures java.util.stream.IntStream.range(first, \result).allMatch(k -> a[k].x <= a[\result].x);
//@ ensures java.util.stream.IntStream.range(\result + 1, last + 1).allMatch(k -> a[k].x > a[\result].x);
```
