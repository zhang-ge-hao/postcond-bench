https://github.com/dyn4j/dyn4j/blob/1a3a5872dca5bc65fd9a2376100e33bed5d3cde6/./src/main/java/org/dyn4j/world/ConstraintGraph.java#L118-L144
```
//@ ensures contactConstraint.getBody1() != null ==> this.graph.get(contactConstraint.getBody1()) != null;
//@ ensures contactConstraint.getBody2() != null ==> this.graph.get(contactConstraint.getBody2()) != null;
//@ ensures contactConstraint.getBody1() != null ==> (this.graph.get(contactConstraint.getBody1()) != null ==> this.graph.get(contactConstraint.getBody1()).getBody() == contactConstraint.getBody1());
//@ ensures contactConstraint.getBody2() != null ==> (this.graph.get(contactConstraint.getBody2()) != null ==> this.graph.get(contactConstraint.getBody2()).getBody() == contactConstraint.getBody2());
//@ ensures contactConstraint.getBody1() != null ==> (this.graph.get(contactConstraint.getBody1()) != null ==> this.graph.get(contactConstraint.getBody1()).getContactConstraints().contains(contactConstraint));
//@ ensures contactConstraint.getBody2() != null ==> (this.graph.get(contactConstraint.getBody2()) != null ==> this.graph.get(contactConstraint.getBody2()).getContactConstraints().contains(contactConstraint));
//@ ensures contactConstraint.getBody1() != null && \old(this.graph.get(contactConstraint.getBody1())) != null ==> \old(this.graph.get(contactConstraint.getBody1())) == this.graph.get(contactConstraint.getBody1());
//@ ensures contactConstraint.getBody2() != null && \old(this.graph.get(contactConstraint.getBody2())) != null ==> \old(this.graph.get(contactConstraint.getBody2())) == this.graph.get(contactConstraint.getBody2());
//@ ensures contactConstraint.getBody1() != null && contactConstraint.getBody2() != null && contactConstraint.getBody1() != contactConstraint.getBody2() ==> this.graph.get(contactConstraint.getBody1()) != this.graph.get(contactConstraint.getBody2());
//@ ensures contactConstraint.getBody1() != null ==> this.graph.get(contactConstraint.getBody1()).getContactConstraints().stream().distinct().count() == this.graph.get(contactConstraint.getBody1()).getContactConstraints().size();
//@ ensures contactConstraint.getBody2() != null ==> this.graph.get(contactConstraint.getBody2()).getContactConstraints().stream().distinct().count() == this.graph.get(contactConstraint.getBody2()).getContactConstraints().size();
```
```
//@ ensures contactConstraint.getBody1() != null ==> this.graph.get(contactConstraint.getBody1()) != null;
//@ ensures contactConstraint.getBody2() != null ==> this.graph.get(contactConstraint.getBody2()) != null;
//@ ensures contactConstraint.getBody1() != null ==> (this.graph.get(contactConstraint.getBody1()) != null ==> this.graph.get(contactConstraint.getBody1()).getBody() == contactConstraint.getBody1());
//@ ensures contactConstraint.getBody2() != null ==> (this.graph.get(contactConstraint.getBody2()) != null ==> this.graph.get(contactConstraint.getBody2()).getBody() == contactConstraint.getBody2());
//@ ensures contactConstraint.getBody1() != null ==> (this.graph.get(contactConstraint.getBody1()) != null ==> this.graph.get(contactConstraint.getBody1()).getContactConstraints().contains(contactConstraint));
//@ ensures contactConstraint.getBody2() != null ==> (this.graph.get(contactConstraint.getBody2()) != null ==> this.graph.get(contactConstraint.getBody2()).getContactConstraints().contains(contactConstraint));
//@ ensures contactConstraint.getBody1() != null && \old(this.graph.get(contactConstraint.getBody1())) != null ==> \old(this.graph.get(contactConstraint.getBody1())) == this.graph.get(contactConstraint.getBody1());
//@ ensures contactConstraint.getBody2() != null && \old(this.graph.get(contactConstraint.getBody2())) != null ==> \old(this.graph.get(contactConstraint.getBody2())) == this.graph.get(contactConstraint.getBody2());
//@ ensures contactConstraint.getBody1() != null && contactConstraint.getBody2() != null && contactConstraint.getBody1() != contactConstraint.getBody2() ==> this.graph.get(contactConstraint.getBody1()) != this.graph.get(contactConstraint.getBody2());
```
[23]
===== 23 =====
```
 			this.graph.put(body2, node2);
 		}
 		
-		node1.contactConstraints.add(contactConstraint);
+		node1.contactConstraints.add(contactConstraint); node2.contactConstraints.add(contactConstraint);
 		node2.contactConstraints.add(contactConstraint);
 	}
```
```
	/**
	 * Adds an interaction graph edge for the given {@link ContactConstraint}.
	 * @param contactConstraint the contact constraint
	 */
	public void addContactConstraint(ContactConstraint<T> contactConstraint) {
		T body1 = contactConstraint.getBody1();
		T body2 = contactConstraint.getBody2();
		
		ConstraintGraphNode<T> node1 = this.graph.get(body1);
		ConstraintGraphNode<T> node2 = this.graph.get(body2);
		
		// NOTE: node1/node2 shouldn't ever be null since
		// the we shouldn't generate a contact constraint
		// for bodies that don't already exist in the world
		// but it's here just in case
		if (node1 == null) {
			node1 = new ConstraintGraphNode<T>(body1);
			this.graph.put(body1, node1);
		}
		if (node2 == null) {
			node2 = new ConstraintGraphNode<T>(body2);
			this.graph.put(body2, node2);
		}
		
		node1.contactConstraints.add(contactConstraint); node2.contactConstraints.add(contactConstraint);
		node2.contactConstraints.add(contactConstraint);
	}
```
