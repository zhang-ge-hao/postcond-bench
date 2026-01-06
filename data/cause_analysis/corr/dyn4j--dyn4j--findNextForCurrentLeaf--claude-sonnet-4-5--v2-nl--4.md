https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/broadphase/DynamicAABBTree.java#L987-L1085
```
//@ ensures \result ==> nextPair != null;
//@ ensures \result ==> nextPair.getFirst() != null;
//@ ensures \result ==> nextPair.getSecond() != null;
//@ ensures \result ==> nextPair.getFirst() != nextPair.getSecond();
//@ ensures \result ==> currentLeaf != null;
//@ ensures \result ==> nextPair.getFirst() == currentLeaf.data || nextPair.getSecond() == currentLeaf.data;
```
```
hallucination on attribute

no `data` in `currentLeaf` object (`DynamicAABBTreeLeaf` class)
```
compile_failure
```
//@ ensures \result ==> this.nextPair.first == \old(this.currentLeaf.item);
//@ ensures \result ==> DynamicAABBTree.this.leaves.get(this.nextPair.first) != null && DynamicAABBTree.this.leaves.get(this.nextPair.second) != null;
//@ ensures \result ==> DynamicAABBTree.this.leaves.get(this.nextPair.second).aabb.overlaps(DynamicAABBTree.this.leaves.get(this.nextPair.first).aabb);
//@ ensures \result ==> DynamicAABBTree.this.broadphaseFilter.isAllowed(this.nextPair.second, this.nextPair.first);
//@ ensures \result ==> !\old(this.tested.containsKey(this.nextPair.second));
//@ ensures !\result ==> (\old(this.currentLeaf) != null ==> (this.tested.containsKey(\old(this.currentLeaf.item)) && this.currentLeaf == null && this.currentNode == null));
//@ ensures \old(this.currentNode == DynamicAABBTree.this.root && this.currentLeaf != null && DynamicAABBTree.this.leaves.values().stream().anyMatch(l -> l != null && l.aabb.overlaps(this.currentLeaf.aabb) && DynamicAABBTree.this.broadphaseFilter.isAllowed(l.item, this.currentLeaf.item) && !this.tested.containsKey(l.item))) ==> \result;

```
