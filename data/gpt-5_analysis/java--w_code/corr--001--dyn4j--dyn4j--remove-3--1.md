https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/SegmentTree.java#L202-L262
```
// @ ensures \old(this.root) != null ==> ((this.root == null) <==> (node == \old(this.root)));
// @ ensures \old(this.root) == null ==> this.root == null;
// @ ensures this.root == null || this.root.parent == null;
// @ ensures \old(this.root) != null && \old(node.parent) != null && \old(node.parent.parent) == null && node != \old(this.root) ==> (this.root == ((\old((node.parent).left) == node) ? \old((node.parent).right) : \old((node.parent).left)));
// @ ensures \old(this.root) != null && \old(node.parent) != null && \old(node.parent.parent) != null ==> (((\old((node.parent.parent).left) == \old(node.parent)) ==> ((\old(node.parent.parent)).left == ((\old((node.parent).left) == node) ? \old((node.parent).right) : \old((node.parent).left))))) && ((\old((node.parent.parent).right) == \old(node.parent)) ==> ((\old(node.parent.parent)).right == ((\old((node.parent).left) == node) ? \old((node.parent).right) : \old((node.parent).left))))) && (((\old((node.parent).left) == node) ? \old((node.parent).right) : \old((node.parent).left)).parent == (\old(node.parent.parent))));
```
```
Syntax error.

SyntaxError: ')' mismatch.
```
compile_failure
```
//@ ensures \old(this.root) == null ==> this.root == null;
//@ ensures \old(this.root) != null && node == \old(this.root) ==> this.root == null;
//@ ensures \old(this.root) != null && node != \old(this.root) ==> this.root != null;
//@ ensures node != null ==> this.root != node;
//@ ensures \old(this.root != null && this.root.left == node) ==> this.root == \old(this.root == null ? null : this.root.right);
//@ ensures \old(this.root != null && this.root.right == node) ==> this.root == \old(this.root == null ? null : this.root.left);
//@ ensures this.root == null || this.root.parent == null;
//@ ensures this.root == null || this.root.left == null || this.root.right == null || this.root.aabb.getMinX() == Math.min(this.root.left.aabb.getMinX(), this.root.right.aabb.getMinX());
//@ ensures this.root == null || this.root.left == null || this.root.right == null || this.root.aabb.getMinY() == Math.min(this.root.left.aabb.getMinY(), this.root.right.aabb.getMinY());
//@ ensures this.root == null || this.root.left == null || this.root.right == null || this.root.aabb.getMaxX() == Math.max(this.root.left.aabb.getMaxX(), this.root.right.aabb.getMaxX());
//@ ensures this.root == null || this.root.left == null || this.root.right == null || this.root.aabb.getMaxY() == Math.max(this.root.left.aabb.getMaxY(), this.root.right.aabb.getMaxY());

```
