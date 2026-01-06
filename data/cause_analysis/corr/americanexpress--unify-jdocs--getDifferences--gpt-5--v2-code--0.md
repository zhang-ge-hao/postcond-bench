https://github.com/americanexpress/unify-jdocs/blob/325af27be93ae4a1df784cf683cdff61e1bb7ac3/./src/main/java/com/americanexpress/unify/jdocs/JDocument.java#L3491-L3538
```
// @ ensures \result != null;
// @ ensures \result.stream().noneMatch(e -> e == null);
// @ ensures onlyDifferences ==> \result.stream().allMatch(di -> di.getDiffResult() != PathDiffResult.EQUAL);
// @ ensures !onlyDifferences ==> (\result.size() == (int)\old(java.util.stream.Stream.concat(this.flattenWithValues().stream().map(pv -> pv.getPath()), right.flattenWithValues().stream().map(pv -> pv.getPath())).distinct().count()));
// @ ensures onlyDifferences ==> (\result.size() == (int)\old(
// @   this.flattenWithValues().stream()
// @     .filter(lp -> right.flattenWithValues().stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && !java.util.Objects.equals(lp.getValue(), rp.getValue())))
// @     .count()
// @   + this.flattenWithValues().stream()
// @     .filter(lp -> lp.getValue() != null && right.flattenWithValues().stream().noneMatch(rp -> rp.getPath().equals(lp.getPath())))
// @     .count()
// @   + right.flattenWithValues().stream()
// @     .filter(rp -> rp.getValue() != null && this.flattenWithValues().stream().noneMatch(lp -> lp.getPath().equals(rp.getPath())))
// @     .count()
// @ ));
// @ ensures !onlyDifferences ==> (\result.stream().filter(di -> di.getDiffResult() == PathDiffResult.EQUAL).count()
// @   == \old(java.util.stream.Stream.concat(this.flattenWithValues().stream().map(pv -> pv.getPath()), right.flattenWithValues().stream().map(pv -> pv.getPath())).distinct().count())
// @      - \old(
// @          this.flattenWithValues().stream()
// @            .filter(lp -> right.flattenWithValues().stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && !java.util.Objects.equals(lp.getValue(), rp.getValue())))
// @            .count()
// @          + this.flattenWithValues().stream()
// @            .filter(lp -> lp.getValue() != null && right.flattenWithValues().stream().noneMatch(rp -> rp.getPath().equals(lp.getPath())))
// @            .count()
// @          + right.flattenWithValues().stream()
// @            .filter(rp -> rp.getValue() != null && this.flattenWithValues().stream().noneMatch(lp -> lp.getPath().equals(rp.getPath())))
// @            .count()
// @        )
// @ );
```
```
limited spec

```
compile_failure
```
//@ ensures \result != null;
//@ ensures \result.stream().allMatch(di -> di != null);
//@ ensures \result.stream().allMatch(di -> di.getDiffResult() != null);
//@ ensures \result.stream().noneMatch(di -> di.getLeft() == null && di.getRight() == null);
//@ ensures \result.stream().filter(di -> di.getLeft() != null).allMatch(di -> \old(flattenWithValues()).stream().anyMatch(lp -> lp.getPath().equals(di.getLeft().getPath())));
//@ ensures \result.stream().filter(di -> di.getRight() != null).allMatch(di -> \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(di.getRight().getPath())));
//@ ensures \result.stream().filter(di -> di.getLeft() != null && di.getRight() == null).allMatch(di -> \old(right.flattenWithValues()).stream().noneMatch(rp -> rp.getPath().equals(di.getLeft().getPath())));
//@ ensures \result.stream().filter(di -> di.getLeft() == null && di.getRight() != null).allMatch(di -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(di.getRight().getPath())));
//@ ensures !onlyDifferences ==> (\old(flattenWithValues()).stream().allMatch(lp -> \result.stream().filter(di -> di.getLeft() != null).anyMatch(di -> di.getLeft().getPath().equals(lp.getPath()) && ((lp.getValue() == null && di.getLeft().getValue() == null) || (lp.getValue() != null && di.getLeft().getValue() != null && lp.getValue().equals(di.getLeft().getValue()))))));
//@ ensures !onlyDifferences ==> (\old(right.flattenWithValues()).stream().filter(rp -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).allMatch(rp -> \result.stream().anyMatch(di -> di.getLeft() == null && di.getRight() != null && di.getRight().getPath().equals(rp.getPath()) && ((rp.getValue() == null && di.getRight().getValue() == null) || (rp.getValue() != null && di.getRight().getValue() != null && rp.getValue().equals(di.getRight().getValue()))))));
//@ ensures !onlyDifferences ==> ((long)\result.size() == (long)\old(flattenWithValues()).size() + \old(right.flattenWithValues()).stream().filter(rp -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).count());
//@ ensures onlyDifferences ==> (\result.stream().noneMatch(di -> di.getDiffResult() == PathDiffResult.EQUAL));
//@ ensures onlyDifferences ==> (\old(flattenWithValues()).stream().filter(lp -> \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && ((lp.getValue() == null && rp.getValue() == null) || (lp.getValue() != null && rp.getValue() != null && lp.getValue().equals(rp.getValue()))))).allMatch(lp -> \result.stream().noneMatch(di -> (di.getLeft() != null && di.getLeft().getPath().equals(lp.getPath())) || (di.getRight() != null && di.getRight().getPath().equals(lp.getPath())))));
//@ ensures onlyDifferences ==> (\old(flattenWithValues()).stream().filter(lp -> (lp.getValue() != null && \old(right.flattenWithValues()).stream().noneMatch(rp -> rp.getPath().equals(lp.getPath()))) || \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && !(((lp.getValue() == null) && (rp.getValue() == null)) || (lp.getValue() != null && rp.getValue() != null && lp.getValue().equals(rp.getValue()))))).allMatch(lp -> \result.stream().filter(di -> di.getLeft() != null).anyMatch(di -> di.getLeft().getPath().equals(lp.getPath()) && ((lp.getValue() == null && di.getLeft().getValue() == null) || (lp.getValue() != null && di.getLeft().getValue() != null && lp.getValue().equals(di.getLeft().getValue()))))));
//@ ensures onlyDifferences ==> (\old(right.flattenWithValues()).stream().filter(rp -> rp.getValue() != null && \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).allMatch(rp -> \result.stream().anyMatch(di -> di.getLeft() == null && di.getRight() != null && di.getRight().getPath().equals(rp.getPath()) && ((rp.getValue() == null && di.getRight().getValue() == null) || (rp.getValue() != null && di.getRight().getValue() != null && rp.getValue().equals(di.getRight().getValue()))))));
//@ ensures onlyDifferences ==> ((long)\result.size() == \old(flattenWithValues()).stream().filter(lp -> (lp.getValue() != null && \old(right.flattenWithValues()).stream().noneMatch(rp -> rp.getPath().equals(lp.getPath()))) || \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && !(((lp.getValue() == null) && (rp.getValue() == null)) || (lp.getValue() != null && rp.getValue() != null && lp.getValue().equals(rp.getValue()))))).count() + \old(right.flattenWithValues()).stream().filter(rp -> rp.getValue() != null && \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).count());

```
