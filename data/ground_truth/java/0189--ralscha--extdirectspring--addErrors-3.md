https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/bean/ExtDirectFormPostResult.java#L183-L209
```
//@ ensures this.result.get(SUCCESS_PROPERTY) == Boolean.FALSE;
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map;
//@ ensures \old(this.result.get(ERRORS_PROPERTY)) != null ==> this.result.get(ERRORS_PROPERTY) == \old(this.result.get(ERRORS_PROPERTY));
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map ==> ((java.util.Map)this.result.get(ERRORS_PROPERTY)).containsKey(field);
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map ==> ((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field) instanceof java.util.List;
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map && ((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field) instanceof java.util.List ==> ((java.util.List)((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field)).containsAll(errors);
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map && ((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field) instanceof java.util.List ==> ((java.util.List)((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field)).size() >= errors.size();
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map && ((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field) instanceof java.util.List ==> ((java.util.List)((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field)).size() >= \old(((this.result.get(ERRORS_PROPERTY) instanceof java.util.Map && ((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field) instanceof java.util.List) ? ((java.util.List)((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field)).size() : 0)) + errors.size();
```
```
//@ ensures this.result.get(SUCCESS_PROPERTY) == Boolean.FALSE;
//@ ensures this.result.get(ERRORS_PROPERTY) instanceof java.util.Map;
//@ ensures ((java.util.Map)this.result.get(ERRORS_PROPERTY)).containsKey(field);
//@ ensures ((java.util.List)((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field)).containsAll(errors);
//@ ensures ((java.util.List)((java.util.Map)this.result.get(ERRORS_PROPERTY)).get(field)).size() >= errors.size();
```
[0, 1, 2, 9, 12]
===== 0 =====
```
 		Assert.notNull(errors, "field must not be null");
 
 		// do not overwrite existing errors
-		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY);
+		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY + "1");
 		if (errorMap == null) {
 			errorMap = new HashMap<>();
 			addResultProperty(ERRORS_PROPERTY, errorMap);
```
```
	/**
	 * Adds multiple error messages to a specific field. Does not overwrite already
	 * existing errors.
	 * @param field the name of the field
	 * @param errors a collection of error messages
	 */
	@SuppressWarnings("unchecked")
	public void addErrors(String field, List<String> errors) {
		Assert.notNull(field, "field must not be null");
		Assert.notNull(errors, "field must not be null");

		// do not overwrite existing errors
		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY + "1");
		if (errorMap == null) {
			errorMap = new HashMap<>();
			addResultProperty(ERRORS_PROPERTY, errorMap);
		}

		List<String> fieldErrors = errorMap.get(field);
		if (fieldErrors == null) {
			fieldErrors = new ArrayList<>();
			errorMap.put(field, fieldErrors);
		}
		fieldErrors.addAll(errors);

		addResultProperty(SUCCESS_PROPERTY, Boolean.FALSE);
	}
```
===== 1 =====
```
 		Assert.notNull(errors, "field must not be null");
 
 		// do not overwrite existing errors
-		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY);
+		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY + "s");
 		if (errorMap == null) {
 			errorMap = new HashMap<>();
 			addResultProperty(ERRORS_PROPERTY, errorMap);
```
```
	/**
	 * Adds multiple error messages to a specific field. Does not overwrite already
	 * existing errors.
	 * @param field the name of the field
	 * @param errors a collection of error messages
	 */
	@SuppressWarnings("unchecked")
	public void addErrors(String field, List<String> errors) {
		Assert.notNull(field, "field must not be null");
		Assert.notNull(errors, "field must not be null");

		// do not overwrite existing errors
		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY + "s");
		if (errorMap == null) {
			errorMap = new HashMap<>();
			addResultProperty(ERRORS_PROPERTY, errorMap);
		}

		List<String> fieldErrors = errorMap.get(field);
		if (fieldErrors == null) {
			fieldErrors = new ArrayList<>();
			errorMap.put(field, fieldErrors);
		}
		fieldErrors.addAll(errors);

		addResultProperty(SUCCESS_PROPERTY, Boolean.FALSE);
	}
```
===== 2 =====
```
 		Assert.notNull(errors, "field must not be null");
 
 		// do not overwrite existing errors
-		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY);
+		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(null);
 		if (errorMap == null) {
 			errorMap = new HashMap<>();
 			addResultProperty(ERRORS_PROPERTY, errorMap);
```
```
	/**
	 * Adds multiple error messages to a specific field. Does not overwrite already
	 * existing errors.
	 * @param field the name of the field
	 * @param errors a collection of error messages
	 */
	@SuppressWarnings("unchecked")
	public void addErrors(String field, List<String> errors) {
		Assert.notNull(field, "field must not be null");
		Assert.notNull(errors, "field must not be null");

		// do not overwrite existing errors
		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(null);
		if (errorMap == null) {
			errorMap = new HashMap<>();
			addResultProperty(ERRORS_PROPERTY, errorMap);
		}

		List<String> fieldErrors = errorMap.get(field);
		if (fieldErrors == null) {
			fieldErrors = new ArrayList<>();
			errorMap.put(field, fieldErrors);
		}
		fieldErrors.addAll(errors);

		addResultProperty(SUCCESS_PROPERTY, Boolean.FALSE);
	}
```
===== 9 =====
```
 			addResultProperty(ERRORS_PROPERTY, errorMap);
 		}
 
-		List<String> fieldErrors = errorMap.get(field);
+		List<String> fieldErrors = null; // This will cause a NullPointerException when trying to add errors.
 		if (fieldErrors == null) {
 			fieldErrors = new ArrayList<>();
 			errorMap.put(field, fieldErrors);
```
```
	/**
	 * Adds multiple error messages to a specific field. Does not overwrite already
	 * existing errors.
	 * @param field the name of the field
	 * @param errors a collection of error messages
	 */
	@SuppressWarnings("unchecked")
	public void addErrors(String field, List<String> errors) {
		Assert.notNull(field, "field must not be null");
		Assert.notNull(errors, "field must not be null");

		// do not overwrite existing errors
		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY);
		if (errorMap == null) {
			errorMap = new HashMap<>();
			addResultProperty(ERRORS_PROPERTY, errorMap);
		}

		List<String> fieldErrors = null; // This will cause a NullPointerException when trying to add errors.
		if (fieldErrors == null) {
			fieldErrors = new ArrayList<>();
			errorMap.put(field, fieldErrors);
		}
		fieldErrors.addAll(errors);

		addResultProperty(SUCCESS_PROPERTY, Boolean.FALSE);
	}
```
===== 12 =====
```
 		List<String> fieldErrors = errorMap.get(field);
 		if (fieldErrors == null) {
 			fieldErrors = new ArrayList<>();
-			errorMap.put(field, fieldErrors);
+			errorMap.put(field, null);
 		}
 		fieldErrors.addAll(errors);
```
```
	/**
	 * Adds multiple error messages to a specific field. Does not overwrite already
	 * existing errors.
	 * @param field the name of the field
	 * @param errors a collection of error messages
	 */
	@SuppressWarnings("unchecked")
	public void addErrors(String field, List<String> errors) {
		Assert.notNull(field, "field must not be null");
		Assert.notNull(errors, "field must not be null");

		// do not overwrite existing errors
		Map<String, List<String>> errorMap = (Map<String, List<String>>) this.result.get(ERRORS_PROPERTY);
		if (errorMap == null) {
			errorMap = new HashMap<>();
			addResultProperty(ERRORS_PROPERTY, errorMap);
		}

		List<String> fieldErrors = errorMap.get(field);
		if (fieldErrors == null) {
			fieldErrors = new ArrayList<>();
			errorMap.put(field, null);
		}
		fieldErrors.addAll(errors);

		addResultProperty(SUCCESS_PROPERTY, Boolean.FALSE);
	}
```
