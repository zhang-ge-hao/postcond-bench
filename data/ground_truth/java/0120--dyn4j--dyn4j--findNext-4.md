https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/broadphase/DynamicAABBTree.java#L955-L985
```
//@ ensures \result ==> (this.nextPair.first != null && this.nextPair.second != null);
//@ ensures !\result ==> (!this.iterator.hasNext() && this.currentLeaf == null);
//@ ensures \result ==> (\old(this.iterator.hasNext()) || \old(this.currentLeaf) != null);
//@ ensures !\result ==> (this.nextPair.first == \old(this.nextPair.first) && this.nextPair.second == \old(this.nextPair.second));
```
```
//@ ensures \result ==> (this.nextPair.first != null && this.nextPair.second != null);
//@ ensures !\result ==> (!this.iterator.hasNext() && this.currentLeaf == null);
//@ ensures \result ==> (\old(this.iterator.hasNext()) || \old(this.currentLeaf) != null)
```
[3]
===== 3 =====
```
 				}
 			
 				// is there another collision with the current leaf?
-				if (this.findNextForCurrentLeaf()) {
+				if (this.findNextForCurrentLeaf() && this.currentLeaf != null) {
 					return true;
 				}
```
```
		/**
		 * Returns true if there's another pair to process and sets
		 * the nextPair field to that pair.
		 * @return boolean
		 */
		private boolean findNext() {
			// iterate through the list of AABBs to test the entire
			// broadphase against
			while (this.iterator.hasNext() || this.currentLeaf != null) {
				// if the current AABB is null, then grab a new one
				if (this.currentLeaf == null) {
					this.currentLeaf = this.iterator.next();
				}
				
				// if the current node in the broadphase is null
				// then we need to start at the root
				if (this.currentNode == null) {
					// start at the root node
					this.currentNode = DynamicAABBTree.this.root;
				}
			
				// is there another collision with the current leaf?
				if (this.findNextForCurrentLeaf() && this.currentLeaf != null) {
					return true;
				}
				
				// if not we need to move to the next leaf
			}
			
			return false;
		}
```
