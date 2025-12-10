https://github.com/tzaeschke/zoodb/blob/311c96bc6f9413762c54b4638c85a60558707aab/./src/org/zoodb/internal/server/DiskAccessOneFile.java#L167-L189
```
//@ ensures \result != null;
//@ ensures !\result.isEmpty();
//@ ensures \result.stream().allMatch(def -> def != null);
//@ ensures \result.size() >= 2;
//@ ensures (int)\result.stream().distinct().count() == \result.size();
//@ ensures \result.stream().allMatch(def -> schemaIndex.getSchema(def) != null);
//@ ensures txContext.getSchemaTxId() == schemaIndex.getTxIdOfLastWrite();
//@ ensures txContext.getSchemaIndexTxId() == schemaIndex.getTxIdOfLastWriteThatRequiresRefresh();
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
 	@Override
 	public Collection<ZooClassDef> readSchemaAll() {
 		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
-		if (all.isEmpty()) {
+		if (!all.isEmpty()) {
 			//new database, need to initialize!
 			
 			//This is the root schema
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (!all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 1 =====
```
 	@Override
 	public Collection<ZooClassDef> readSchemaAll() {
 		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
-		if (all.isEmpty()) {
+		if (all.size() == 1) {
 			//new database, need to initialize!
 			
 			//This is the root schema
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.size() == 1) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 2 =====
```
 	@Override
 	public Collection<ZooClassDef> readSchemaAll() {
 		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
-		if (all.isEmpty()) {
+		if (all.size() > 0) {
 			//new database, need to initialize!
 			
 			//This is the root schema
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.size() > 0) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 3 =====
```
 			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
 			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
 			schemaIndex.defineSchema(zpcDef);
-			schemaIndex.defineSchema(meta);
+			
 
 			all = new ArrayList<>();
 			all.add(zpcDef);
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 4 =====
```
 			schemaIndex.defineSchema(meta);
 
 			all = new ArrayList<>();
-			all.add(zpcDef);
+			
 			all.add(meta);
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 5 =====
```
 			schemaIndex.defineSchema(meta);
 
 			all = new ArrayList<>();
-			all.add(zpcDef);
+			all.add(meta);
 			all.add(meta);
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(meta);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 6 =====
```
 			schemaIndex.defineSchema(meta);
 
 			all = new ArrayList<>();
-			all.add(zpcDef);
+			all.add(null);
 			all.add(meta);
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(null);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 7 =====
```
 
 			all = new ArrayList<>();
 			all.add(zpcDef);
-			all.add(meta);
+			
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
 		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 8 =====
```
 
 			all = new ArrayList<>();
 			all.add(zpcDef);
-			all.add(meta);
+			all.add(null); // Adding a null value, which may lead to NullPointerExceptions later
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
 		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(null); // Adding a null value, which may lead to NullPointerExceptions later
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 9 =====
```
 
 			all = new ArrayList<>();
 			all.add(zpcDef);
-			all.add(meta);
+			all.add(zpcDef); // Adding a duplicate schema definition instead of the meta definition
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
 		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(zpcDef); // Adding a duplicate schema definition instead of the meta definition
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 10 =====
```
 
 			all = new ArrayList<>();
 			all.add(zpcDef);
-			all.add(meta);
+			all.add(zpcDef); // Adding the wrong schema definition instead of the meta definition
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
 		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(zpcDef); // Adding the wrong schema definition instead of the meta definition
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return all;
	}
```
===== 11 =====
```
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
 		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
-		return all;
+		return java.util.Collections.emptyList();
 	}
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return java.util.Collections.emptyList();
	}
```
===== 12 =====
```
 		}
 		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
 		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
-		return all;
+		return null;
 	}
```
```
	/**
	 * @return List of all schemata in the database. These are loaded when the database is opened.
	 */
	@Override
	public Collection<ZooClassDef> readSchemaAll() {
		Collection<ZooClassDef> all = schemaIndex.readSchemaAll(this, node);
		if (all.isEmpty()) {
			//new database, need to initialize!
			
			//This is the root schema
			ZooClassDef zpcDef = ZooClassDef.bootstrapZooPCImpl(); 
			ZooClassDef meta = ZooClassDef.bootstrapZooClassDef(); 
			schemaIndex.defineSchema(zpcDef);
			schemaIndex.defineSchema(meta);

			all = new ArrayList<>();
			all.add(zpcDef);
			all.add(meta);
		}
		txContext.setSchemaTxId(schemaIndex.getTxIdOfLastWrite());
		txContext.setSchemaIndexTxId(schemaIndex.getTxIdOfLastWriteThatRequiresRefresh());
		return null;
	}
```
