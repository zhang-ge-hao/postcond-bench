https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/SegmentTree.java#L202-L262
```
// @ ensures (this.root == null) <==> (\old(this.root) == null || \old(node == this.root));
// @ ensures this.root == null || this.root.parent == null;
// @ ensures \old(this.root != null && node != this.root && node.parent != null && node.parent.parent == null) ==> (this.root == \old((node.parent.left == node ? node.parent.right : node.parent.left)) && this.root.parent == null);
// @ ensures \old(node != null) ==> node != null;
// @ ensures \old(node != null) ==> node.parent == \old(node.parent);
// @ ensures \old(node != null) ==> node.left == \old(node.left);
// @ ensures \old(node != null) ==> node.right == \old(node.right);
// @ ensures \old(node != null) ==> node.aabb == \old(node.aabb);
// @ ensures \old(node != null) ==> node.height == \old(node.height);
```
```
null pointer exception

=> java.lang.NullPointerException: Cannot read field "left" because "<parameter1>.parent" is null
```
failed
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
