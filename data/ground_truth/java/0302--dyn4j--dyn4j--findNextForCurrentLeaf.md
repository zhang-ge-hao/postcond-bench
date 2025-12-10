https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/collision/broadphase/DynamicAABBTree.java#L987-L1085
```
//@ ensures \result ==> this.nextPair.first == \old(this.currentLeaf.item);
//@ ensures \result ==> DynamicAABBTree.this.leaves.get(this.nextPair.first) != null && DynamicAABBTree.this.leaves.get(this.nextPair.second) != null;
//@ ensures \result ==> DynamicAABBTree.this.leaves.get(this.nextPair.second).aabb.overlaps(DynamicAABBTree.this.leaves.get(this.nextPair.first).aabb);
//@ ensures \result ==> DynamicAABBTree.this.broadphaseFilter.isAllowed(this.nextPair.second, this.nextPair.first);
//@ ensures \result ==> !\old(this.tested.containsKey(this.nextPair.second));
//@ ensures !\result ==> (\old(this.currentLeaf) != null ==> (this.tested.containsKey(\old(this.currentLeaf.item)) && this.currentLeaf == null && this.currentNode == null));
//@ ensures \old(this.currentNode == DynamicAABBTree.this.root && this.currentLeaf != null && DynamicAABBTree.this.leaves.values().stream().anyMatch(l -> l != null && l.aabb.overlaps(this.currentLeaf.aabb) && DynamicAABBTree.this.broadphaseFilter.isAllowed(l.item, this.currentLeaf.item) && !this.tested.containsKey(l.item))) ==> \result;
```
```
//@ ensures \result ==> this.nextPair.first == \old(this.currentLeaf.item);
//@ ensures \result ==> DynamicAABBTree.this.leaves.get(this.nextPair.first) != null && DynamicAABBTree.this.leaves.get(this.nextPair.second) != null;
//@ ensures \result ==> DynamicAABBTree.this.leaves.get(this.nextPair.second).aabb.overlaps(DynamicAABBTree.this.leaves.get(this.nextPair.first).aabb);
//@ ensures \result ==> DynamicAABBTree.this.broadphaseFilter.isAllowed(this.nextPair.second, this.nextPair.first);
//@ ensures \result ==> !\old(this.tested.containsKey(this.nextPair.second));
//@ ensures !\result ==> (\old(this.currentLeaf) != null ==> (this.tested.containsKey(\old(this.currentLeaf.item)) && this.currentLeaf == null && this.currentNode == null));
```
[0, 1, 2, 4, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19]
===== 0 =====
```
 			// perform a iterative, stack-less, traversal of the tree
 			while (test != null) {
 				// check if the current node overlaps the desired node
-				if (test.aabb.overlaps(node.aabb)) {
+				if (!test.aabb.overlaps(node.aabb)) {
 					// if they do overlap, then check the left child node
 					if (test.left != null) {
 						// if the left is not null, then check that subtree
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (!test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 1 =====
```
 			// perform a iterative, stack-less, traversal of the tree
 			while (test != null) {
 				// check if the current node overlaps the desired node
-				if (test.aabb.overlaps(node.aabb)) {
+				if (test.aabb.contains(node.aabb)) {
 					// if they do overlap, then check the left child node
 					if (test.left != null) {
 						// if the left is not null, then check that subtree
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.contains(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 2 =====
```
 			// perform a iterative, stack-less, traversal of the tree
 			while (test != null) {
 				// check if the current node overlaps the desired node
-				if (test.aabb.overlaps(node.aabb)) {
+				if (test.aabb.equals(node.aabb)) {
 					// if they do overlap, then check the left child node
 					if (test.left != null) {
 						// if the left is not null, then check that subtree
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.equals(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 4 =====
```
 			// perform a iterative, stack-less, traversal of the tree
 			while (test != null) {
 				// check if the current node overlaps the desired node
-				if (test.aabb.overlaps(node.aabb)) {
+				if (test.aabb.getPerimeter() < node.aabb.getPerimeter()) {
 					// if they do overlap, then check the left child node
 					if (test.left != null) {
 						// if the left is not null, then check that subtree
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.getPerimeter() < node.aabb.getPerimeter()) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 6 =====
```
 						// if both are null, then this is a leaf node
 						
 						// don't compare nodes among themselves
-						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
+						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, leaf.item)) {
 							// have we already tested this pair?
 							boolean tested = this.tested.containsKey(leaf.item);
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, leaf.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 7 =====
```
 						// don't compare nodes among themselves
 						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
 							// have we already tested this pair?
-							boolean tested = this.tested.containsKey(leaf.item);
+							boolean tested = this.tested.size() > 0;
 							
 							// check the tested flag to avoid duplicates and
 							// verify we aren't testing the same body against
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.size() > 0;
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 8 =====
```
 							// check the tested flag to avoid duplicates and
 							// verify we aren't testing the same body against
 							// itself
-							if (!tested) {
+							if (tested && !this.tested.containsKey(leaf.item)) {
 								// its a leaf so we have a collision
 								this.nextPair.first = node.item;
 								this.nextPair.second = leaf.item;
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (tested && !this.tested.containsKey(leaf.item)) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 10 =====
```
 							// check the tested flag to avoid duplicates and
 							// verify we aren't testing the same body against
 							// itself
-							if (!tested) {
+							if (this.tested.containsKey(node.item)) {
 								// its a leaf so we have a collision
 								this.nextPair.first = node.item;
 								this.nextPair.second = leaf.item;
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (this.tested.containsKey(node.item)) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 12 =====
```
 				// desired aabb, then we need to go back up the tree until we
 				// find the first left node who's right node is not null
 				boolean nextNodeFound = false;
-				while (test.parent != null) {
+				while (test.height > 0) {
 					// check if the current node the left child of its parent
 					if (test == test.parent.left) {
 						// it is, so check if the right node is non-null
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.height > 0) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 13 =====
```
 				// desired aabb, then we need to go back up the tree until we
 				// find the first left node who's right node is not null
 				boolean nextNodeFound = false;
-				while (test.parent != null) {
+				while (test.left != null) {
 					// check if the current node the left child of its parent
 					if (test == test.parent.left) {
 						// it is, so check if the right node is non-null
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.left != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 14 =====
```
 				// desired aabb, then we need to go back up the tree until we
 				// find the first left node who's right node is not null
 				boolean nextNodeFound = false;
-				while (test.parent != null) {
+				while (test.right != null) {
 					// check if the current node the left child of its parent
 					if (test == test.parent.left) {
 						// it is, so check if the right node is non-null
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.right != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 15 =====
```
 				boolean nextNodeFound = false;
 				while (test.parent != null) {
 					// check if the current node the left child of its parent
-					if (test == test.parent.left) {
+					if (test != test.parent.left) {
 						// it is, so check if the right node is non-null
 						// NOTE: not need since the tree is a complete tree (every node has two children)
 						//if (n.parent.right != null) {
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test != test.parent.left) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 16 =====
```
 				boolean nextNodeFound = false;
 				while (test.parent != null) {
 					// check if the current node the left child of its parent
-					if (test == test.parent.left) {
+					if (test == null) {
 						// it is, so check if the right node is non-null
 						// NOTE: not need since the tree is a complete tree (every node has two children)
 						//if (n.parent.right != null) {
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == null) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 17 =====
```
 				boolean nextNodeFound = false;
 				while (test.parent != null) {
 					// check if the current node the left child of its parent
-					if (test == test.parent.left) {
+					if (test == test.parent.right) {
 						// it is, so check if the right node is non-null
 						// NOTE: not need since the tree is a complete tree (every node has two children)
 						//if (n.parent.right != null) {
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test == test.parent.right) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 18 =====
```
 				boolean nextNodeFound = false;
 				while (test.parent != null) {
 					// check if the current node the left child of its parent
-					if (test == test.parent.left) {
+					if (test.parent == null) {
 						// it is, so check if the right node is non-null
 						// NOTE: not need since the tree is a complete tree (every node has two children)
 						//if (n.parent.right != null) {
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test.parent == null) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
===== 19 =====
```
 				boolean nextNodeFound = false;
 				while (test.parent != null) {
 					// check if the current node the left child of its parent
-					if (test == test.parent.left) {
+					if (test.parent.left == null) {
 						// it is, so check if the right node is non-null
 						// NOTE: not need since the tree is a complete tree (every node has two children)
 						//if (n.parent.right != null) {
```
```
		/**
		 * Conversion of the non-recursive detection method into a finite state machine.
		 * <p>
		 * This method returns true if there's a "next" collision and places the next collision
		 * result in storage to be reported in the call to the {@link #next()} method.
		 * @return boolean
		 */
		private boolean findNextForCurrentLeaf() {
			boolean foundCollision = false;
			
			// find the next collision pair (if there is one)
			DynamicAABBTreeLeaf<T> node = this.currentLeaf;
			DynamicAABBTreeNode test = this.currentNode;
			
			// perform a iterative, stack-less, traversal of the tree
			while (test != null) {
				// check if the current node overlaps the desired node
				if (test.aabb.overlaps(node.aabb)) {
					// if they do overlap, then check the left child node
					if (test.left != null) {
						// if the left is not null, then check that subtree
						test = test.left;
						continue;
					} else {
						@SuppressWarnings("unchecked")
						DynamicAABBTreeLeaf<T> leaf = (DynamicAABBTreeLeaf<T>)test;
						// if both are null, then this is a leaf node
						
						// don't compare nodes among themselves
						if (DynamicAABBTree.this.broadphaseFilter.isAllowed(leaf.item, node.item)) {
							// have we already tested this pair?
							boolean tested = this.tested.containsKey(leaf.item);
							
							// check the tested flag to avoid duplicates and
							// verify we aren't testing the same body against
							// itself
							if (!tested) {
								// its a leaf so we have a collision
								this.nextPair.first = node.item;
								this.nextPair.second = leaf.item;
								
								// we can't return here because we need to advance the detection
								// to the next node to test before we exit from this method
								foundCollision = true;
							}
							// if its a leaf node then we need to go back up the
							// tree and test nodes we haven't yet
						}
					}
				}
				
				// if the current node is a leaf node or doesnt overlap the
				// desired aabb, then we need to go back up the tree until we
				// find the first left node who's right node is not null
				boolean nextNodeFound = false;
				while (test.parent != null) {
					// check if the current node the left child of its parent
					if (test.parent.left == null) {
						// it is, so check if the right node is non-null
						// NOTE: not need since the tree is a complete tree (every node has two children)
						//if (n.parent.right != null) {
							// it isn't so the sibling node is the next node
							test = test.parent.right;
							nextNodeFound = true;
							break;
						//}
					}
					// if the current node isn't a left node or it is but its
					// sibling is null, go to the parent node
					test = test.parent;
				}
				
				// update the current node so we can pick up where we left off
				this.currentNode = test;
				
				// if we didn't find it then we are done
				if (!nextNodeFound) {
					// this indicates that we're done testing the currentLeaf against
					// the entire broadphase
					
					// make sure the leaf is marked as already tested
					this.tested.put(this.currentLeaf.item, true);
					
					// make sure the next call to hasNext gets the next AABB to test
					this.currentLeaf = null;
					
					// make sure the testing begins at the root node
					this.currentNode = null;
					break;
				}
				
				// if we found a collision then we need to stop
				if (foundCollision) {
					break;
				}
			}
			
			return foundCollision;
		}
```
