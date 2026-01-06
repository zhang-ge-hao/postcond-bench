https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/datastructures/lists/CursorLinkedList.java#L116-L126
```
// @ ensures (index >= 0 && index < \old(count)) ==> count == \old(count) - 1;
// @ ensures (index < 0 || index >= \old(count)) ==> count == \old(count);
// @ ensures (index < 0 || index >= \old(count)) ==> head == \old(head);
// @ ensures (index < 0 || index >= \old(count)) ==> java.util.stream.IntStream.range(0, count).allMatch(i -> java.util.Objects.equals(get(i), \old(get(i))));
// @ ensures (index >= 0 && index < \old(count)) ==> java.util.stream.IntStream.range(0, index).allMatch(i -> java.util.Objects.equals(get(i), \old(get(i))));
// @ ensures (index >= 0 && index < \old(count)) ==> java.util.stream.IntStream.range(index, count).allMatch(i -> java.util.Objects.equals(get(i), \old(get(i + 1))));
```
```
limited spec

.allMatch(i -> java.util.Objects.equals(get(i), \old(get(i))))
```
compile_failure
```
//@ ensures index >= 0 && index < \old(count) ==> count == \old(count) - 1;
//@ ensures index < 0 || index >= \old(count) ==> count == \old(count);
//@ ensures index >= 0 && index < \old(count) ==> indexOf(\old(get(index))) == -1;
//@ ensures index > 0 && index < \old(count) ==> get(0) == \old(get(0));
//@ ensures index >= 0 && index < \old(count) - 1 ==> get(index) == \old(get(index + 1));
//@ ensures \old(count) > 0 && index == \old(count) - 1 ==> get(index) == null
```
