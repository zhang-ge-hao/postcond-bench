https://github.com/j256/ormlite-android/blob/71373ea30e61b233676b15a335f2a55b3271a7ae/./src/main/java/com/j256/ormlite/android/apptools/OrmLiteConfigUtil.java#L229-L255
```
🈚️

Iterator (OutputStream)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
 	 */
 	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
 			throws SQLException, IOException {
-		if (sortClasses) {
+		if (classes.length > 0) {
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (classes.length > 0) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 1 =====
```
 	 */
 	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
 			throws SQLException, IOException {
-		if (sortClasses) {
+		if (sortClasses && classes.length == 0) {
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses && classes.length == 0) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 2 =====
```
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
-			Arrays.sort(sortedClasses, classComparator);
+			
 			classes = sortedClasses;
 		}
 		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 3 =====
```
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
-			Arrays.sort(sortedClasses, classComparator);
+			Arrays.sort(sortedClasses, (c1, c2) -> 0); // Always returns 0, resulting in no sorting
 			classes = sortedClasses;
 		}
 		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, (c1, c2) -> 0); // Always returns 0, resulting in no sorting
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 4 =====
```
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
-			Arrays.sort(sortedClasses, classComparator);
+			Arrays.sort(sortedClasses, (c1, c2) -> Integer.compare(c1.hashCode(), c2.hashCode())); // Sorts by hash code, which is not a reliable ordering
 			classes = sortedClasses;
 		}
 		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, (c1, c2) -> Integer.compare(c1.hashCode(), c2.hashCode())); // Sorts by hash code, which is not a reliable ordering
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 5 =====
```
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
-			Arrays.sort(sortedClasses, classComparator);
+			Arrays.sort(sortedClasses, (c1, c2) -> c1.getName().length() - c2.getName().length());
 			classes = sortedClasses;
 		}
 		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, (c1, c2) -> c1.getName().length() - c2.getName().length());
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 6 =====
```
 			// sort our class list to make the output more deterministic
 			Class<?>[] sortedClasses = new Class<?>[classes.length];
 			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
-			Arrays.sort(sortedClasses, classComparator);
+			Arrays.sort(sortedClasses, (c1, c2) -> c2.getName().compareTo(c1.getName()));
 			classes = sortedClasses;
 		}
 		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, (c1, c2) -> c2.getName().compareTo(c1.getName()));
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 7 =====
```
 		try {
 			writeHeader(writer);
 			for (Class<?> clazz : classes) {
-				writeConfigForTable(writer, clazz, sortClasses);
+				
 			}
 			// NOTE: done is here because this is public
 			System.out.println("Done.");
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.close();
		}
	}
```
===== 8 =====
```
 			// NOTE: done is here because this is public
 			System.out.println("Done.");
 		} finally {
-			writer.close();
+			
 		}
 	}
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			
		}
	}
```
===== 9 =====
```
 			// NOTE: done is here because this is public
 			System.out.println("Done.");
 		} finally {
-			writer.close();
+			writer = null; // Nullifying the writer reference
 		}
 	}
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer = null; // Nullifying the writer reference
		}
	}
```
===== 10 =====
```
 			// NOTE: done is here because this is public
 			System.out.println("Done.");
 		} finally {
-			writer.close();
+			writer.append("Finished writing."); // Appending a message instead of closing
 		}
 	}
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.append("Finished writing."); // Appending a message instead of closing
		}
	}
```
===== 11 =====
```
 			// NOTE: done is here because this is public
 			System.out.println("Done.");
 		} finally {
-			writer.close();
+			writer.write(""); // Writing an empty string instead of closing the writer
 		}
 	}
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.write(""); // Writing an empty string instead of closing the writer
		}
	}
```
===== 12 =====
```
 			// NOTE: done is here because this is public
 			System.out.println("Done.");
 		} finally {
-			writer.close();
+			writer.write("Done."); // Writing a message instead of closing the writer
 		}
 	}
```
```
	/**
	 * Write a configuration file to an output stream with the configuration for classes.
	 * 
	 * @param sortClasses
	 *            Set to true to sort the classes and fields by name before the file is generated.
	 */
	public static void writeConfigFile(OutputStream outputStream, Class<?>[] classes, boolean sortClasses)
			throws SQLException, IOException {
		if (sortClasses) {
			// sort our class list to make the output more deterministic
			Class<?>[] sortedClasses = new Class<?>[classes.length];
			System.arraycopy(classes, 0, sortedClasses, 0, classes.length);
			Arrays.sort(sortedClasses, classComparator);
			classes = sortedClasses;
		}
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream), 4096);
		try {
			writeHeader(writer);
			for (Class<?> clazz : classes) {
				writeConfigForTable(writer, clazz, sortClasses);
			}
			// NOTE: done is here because this is public
			System.out.println("Done.");
		} finally {
			writer.write("Done."); // Writing a message instead of closing the writer
		}
	}
```
