https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/geometry/simplify/SegmentTree.java#L202-L262
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
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
 	private void remove(SegmentTreeNode node) {
 		// check for an empty tree
 		// should never happen based on current usage
-		if (this.root == null) return;
+		if (node.isLeaf()) return;
 		// check the root node
 		if (node == this.root) {
 			// set the root to null
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (node.isLeaf()) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 1 =====
```
 	private void remove(SegmentTreeNode node) {
 		// check for an empty tree
 		// should never happen based on current usage
-		if (this.root == null) return;
+		if (this.root != null) return;
 		// check the root node
 		if (node == this.root) {
 			// set the root to null
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root != null) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 2 =====
```
 		// should never happen based on current usage
 		if (this.root == null) return;
 		// check the root node
-		if (node == this.root) {
+		if (node.height < 2) {
 			// set the root to null
 			this.root = null;
 			// return from the remove method
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node.height < 2) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 3 =====
```
 		// should never happen based on current usage
 		if (this.root == null) return;
 		// check the root node
-		if (node == this.root) {
+		if (node.left == null) {
 			// set the root to null
 			this.root = null;
 			// return from the remove method
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node.left == null) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 4 =====
```
 		SegmentTreeNode parent = node.parent;
 		SegmentTreeNode grandparent = parent.parent;
 		SegmentTreeNode other;
-		if (parent.left == node) {
+		if (parent.right == node) {
 			other = parent.right;
 		} else {
 			other = parent.left;
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.right == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 5 =====
```
 				
 				// neither node should be null
 				n.height = 1 + Math.max(left.height, right.height);
-				n.aabb.union(left.aabb, right.aabb);
+				n.aabb.union(left.aabb, left.aabb);
 				
 				n = n.parent;
 			}
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, left.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 6 =====
```
 				
 				// neither node should be null
 				n.height = 1 + Math.max(left.height, right.height);
-				n.aabb.union(left.aabb, right.aabb);
+				n.aabb.union(left.aabb, new AABB(1, 1, 1, 1));
 				
 				n = n.parent;
 			}
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(left.aabb, new AABB(1, 1, 1, 1));
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
===== 7 =====
```
 				
 				// neither node should be null
 				n.height = 1 + Math.max(left.height, right.height);
-				n.aabb.union(left.aabb, right.aabb);
+				n.aabb.union(right.aabb, right.aabb);
 				
 				n = n.parent;
 			}
```
```
	/**
	 * Internal method to remove a node from the tree.
	 * @param node the node to remove
	 */
	private void remove(SegmentTreeNode node) {
		// check for an empty tree
		// should never happen based on current usage
		if (this.root == null) return;
		// check the root node
		if (node == this.root) {
			// set the root to null
			this.root = null;
			// return from the remove method
			return;
		}
		
		// get the node's parent, grandparent, and sibling
		SegmentTreeNode parent = node.parent;
		SegmentTreeNode grandparent = parent.parent;
		SegmentTreeNode other;
		if (parent.left == node) {
			other = parent.right;
		} else {
			other = parent.left;
		}
		
		// check if the grandparent is null
		// indicating that the parent is the root
		if (grandparent != null) {
			// remove the node by overwriting the parent node
			// reference in the grandparent with the sibling
			if (grandparent.left == parent) {
				grandparent.left = other;
			} else {
				grandparent.right = other;
			}
			// set the siblings parent to the grandparent
			other.parent = grandparent;
			
			// finally rebalance the tree
			SegmentTreeNode n = grandparent;
			while (n != null) {
				// balance the current subtree
				n = balance(n);
				
				SegmentTreeNode left = n.left;
				SegmentTreeNode right = n.right;
				
				// neither node should be null
				n.height = 1 + Math.max(left.height, right.height);
				n.aabb.union(right.aabb, right.aabb);
				
				n = n.parent;
			}
		} else {
			// the parent is the root so set the root to the sibling
			this.root = other;
			// set the siblings parent to null
			other.parent = null;
		}
	}
```
