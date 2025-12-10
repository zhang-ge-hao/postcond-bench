https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/BinarySearchTreeIterator.java#L118-L140
```
//@ ensures (from != null) ==> this.stack.stream().allMatch(n -> from.compareTo(n.comparable) <= 0);
//@ ensures this.stack.stream().distinct().count() == this.stack.size();
//@ ensures (from != null && this.root != null && from.compareTo(this.root.comparable) <= 0) ==> this.stack.contains(this.root);
//@ ensures !this.stack.isEmpty() ==> this.stack.stream().allMatch(n -> this.stack.peek().comparable.compareTo(n.comparable) <= 0);
//@ ensures from != null && this.root != null && \old(this.stack.isEmpty()) && from.compareTo(this.root.comparable) == 0 ==> this.stack.size() == \old(this.stack.size()) + 1 && this.stack.peek() == this.root;
//@ ensures from != null && this.root != null && this.root.left != null && \old(this.stack.isEmpty()) && from.compareTo(this.root.comparable) < 0 && from.compareTo(this.root.left.comparable) < 0 ==> this.stack.contains(this.root.left);
//@ ensures from != null && this.root != null && !this.stack.isEmpty() && from.compareTo(this.root.comparable) < 0 && from.compareTo(this.stack.peek().comparable) < 0 ==> this.stack.size() >= 2;
//@ ensures from != null && this.root != null && this.root.left != null && this.root.left.right != null && \old(this.stack.isEmpty()) && from.compareTo(this.root.left.right.comparable) == 0 ==> !this.stack.isEmpty() && this.stack.peek() == this.root.left.right;
```
```
//@ ensures (from != null) ==> this.stack.stream().allMatch(n -> from.compareTo(n.comparable) <= 0);
//@ ensures this.stack.stream().distinct().count() == this.stack.size();
//@ ensures (from != null && this.root != null && from.compareTo(this.root.comparable) <= 0) ==> this.stack.contains(this.root);
//@ ensures !this.stack.isEmpty() ==> this.stack.stream().allMatch(n -> this.stack.peek().comparable.compareTo(n.comparable) <= 0)
```
[0, 3, 7, 15, 16, 19]
===== 0 =====
```
 	 */
 	protected void pushLeftFrom(E from) {
 		BinarySearchTreeNode<E> node = this.root;
-		while (node != null) {
+		while (node != null && node.left != null) {
 			int cmp = from.compareTo(node.comparable);
 			if (cmp < 0) {
 				// go left
```
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null && node.left != null) {
			int cmp = from.compareTo(node.comparable);
			if (cmp < 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp > 0) {
				// go right
				node = node.right;
			} else {
				this.stack.push(node);
				break;
			}
		}
	}
```
===== 3 =====
```
 	protected void pushLeftFrom(E from) {
 		BinarySearchTreeNode<E> node = this.root;
 		while (node != null) {
-			int cmp = from.compareTo(node.comparable);
+			int cmp = from.compareTo(node.comparable) + 1; // introduces an off-by-one error
 			if (cmp < 0) {
 				// go left
 				this.stack.push(node);
```
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null) {
			int cmp = from.compareTo(node.comparable) + 1; // introduces an off-by-one error
			if (cmp < 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp > 0) {
				// go right
				node = node.right;
			} else {
				this.stack.push(node);
				break;
			}
		}
	}
```
===== 7 =====
```
 		BinarySearchTreeNode<E> node = this.root;
 		while (node != null) {
 			int cmp = from.compareTo(node.comparable);
-			if (cmp < 0) {
+			if (cmp == 0) {
 				// go left
 				this.stack.push(node);
 				node = node.left;
```
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null) {
			int cmp = from.compareTo(node.comparable);
			if (cmp == 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp > 0) {
				// go right
				node = node.right;
			} else {
				this.stack.push(node);
				break;
			}
		}
	}
```
===== 15 =====
```
 				// go left
 				this.stack.push(node);
 				node = node.left;
-			} else if (cmp > 0) {
+			} else if (cmp >= 0) {
 				// go right
 				node = node.right;
 			} else {
```
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null) {
			int cmp = from.compareTo(node.comparable);
			if (cmp < 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp >= 0) {
				// go right
				node = node.right;
			} else {
				this.stack.push(node);
				break;
			}
		}
	}
```
===== 16 =====
```
 				// go right
 				node = node.right;
 			} else {
-				this.stack.push(node);
+				
 				break;
 			}
 		}
```
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null) {
			int cmp = from.compareTo(node.comparable);
			if (cmp < 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp > 0) {
				// go right
				node = node.right;
			} else {
				
				break;
			}
		}
	}
```
===== 19 =====
```
 				// go right
 				node = node.right;
 			} else {
-				this.stack.push(node);
+				this.stack.push(node.right);
 				break;
 			}
 		}
```
```
	/**
	 * Pushes the required nodes onto the stack to begin iterating
	 * nodes in order starting from the given value.
	 * @param from the value to start iterating from
	 * @since 3.2.3
	 */
	protected void pushLeftFrom(E from) {
		BinarySearchTreeNode<E> node = this.root;
		while (node != null) {
			int cmp = from.compareTo(node.comparable);
			if (cmp < 0) {
				// go left
				this.stack.push(node);
				node = node.left;
			} else if (cmp > 0) {
				// go right
				node = node.right;
			} else {
				this.stack.push(node.right);
				break;
			}
		}
	}
```
