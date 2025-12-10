https://github.com/jcbvm/i18n-editor/blob/2c8b7b5afbf2a8963cad9400bf0954340a0accd3/./src/main/java/com/jvms/i18neditor/util/ResourceKeys.java#L127-L145
```
//@ ensures \result != null;
//@ ensures (key == null || key.isEmpty()) ==> "".equals(\result);
//@ ensures key != null && !key.isEmpty() && (parentKey == null || parentKey.isEmpty()) ==> key.equals(\result);
//@ ensures key != null && !key.isEmpty() && parentKey != null && !parentKey.isEmpty() && key.indexOf(parentKey + ".") == -1 ==> "".equals(\result);
//@ ensures key != null && !key.isEmpty() && parentKey != null && !parentKey.isEmpty() && key.indexOf(parentKey + ".") != -1 ==> (key.substring(0, key.indexOf(parentKey + ".")) + key.substring(key.indexOf(parentKey + ".") + (parentKey + ".").length())).equals(\result);
```
```
//@ ensures key == null || key.isEmpty() ==> \result.equals("");
//@ ensures !(key == null || key.isEmpty()) && (parentKey == null || parentKey.isEmpty()) ==> \result.equals(key);
//@ ensures !(key == null || key.isEmpty()) && !(parentKey == null || parentKey.isEmpty()) && key.indexOf(parentKey + ".") == -1 ==> \result.equals("");
//@ ensures !(key == null || key.isEmpty()) && !(parentKey == null || parentKey.isEmpty()) && key.indexOf(parentKey + ".") != -1 ==> \result.equals(key.substring(0, key.indexOf(parentKey + ".")) + key.substring(key.indexOf(parentKey + ".") + (parentKey + ".").length()));
//@ ensures \result != null
```
[1, 2, 11, 17]
===== 1 =====
```
 	 * @return 	the part of the given key which is a child of the given parent key.
 	 */
 	public static String childKey(String key, String parentKey) {
-		if (key == null || key.isEmpty()) return "";
+		if (key == null || key.isEmpty()) return null;
 		if (parentKey == null || parentKey.isEmpty()) return key;
 		String result = key.replaceFirst(parentKey + "\\.", "");
 		if (result.equals(key)) return "";
```
```
	/**
	 * Retrieve the part of the given key which is a child part of the given parent key.
	 * A key is a child of another key if it has the same parts at the beginning as the other key.
	 * This function will only return the child parts, so without the beginning parent parts.
	 * 
	 * <p>If the resulting key is the same as the given key, the key is considered not to be a child 
	 * of the given parent key, so an empty key will be returned.</p>
	 * 
	 * @param 	key the original key.
	 * @param 	parentKey a possible parent key of the original key.
	 * @return 	the part of the given key which is a child of the given parent key.
	 */
	public static String childKey(String key, String parentKey) {
		if (key == null || key.isEmpty()) return null;
		if (parentKey == null || parentKey.isEmpty()) return key;
		String result = key.replaceFirst(parentKey + "\\.", "");
		if (result.equals(key)) return "";
		return result;
	}
```
===== 2 =====
```
 	 * @return 	the part of the given key which is a child of the given parent key.
 	 */
 	public static String childKey(String key, String parentKey) {
-		if (key == null || key.isEmpty()) return "";
+		if (key.length() == 0) return null;
 		if (parentKey == null || parentKey.isEmpty()) return key;
 		String result = key.replaceFirst(parentKey + "\\.", "");
 		if (result.equals(key)) return "";
```
```
	/**
	 * Retrieve the part of the given key which is a child part of the given parent key.
	 * A key is a child of another key if it has the same parts at the beginning as the other key.
	 * This function will only return the child parts, so without the beginning parent parts.
	 * 
	 * <p>If the resulting key is the same as the given key, the key is considered not to be a child 
	 * of the given parent key, so an empty key will be returned.</p>
	 * 
	 * @param 	key the original key.
	 * @param 	parentKey a possible parent key of the original key.
	 * @return 	the part of the given key which is a child of the given parent key.
	 */
	public static String childKey(String key, String parentKey) {
		if (key.length() == 0) return null;
		if (parentKey == null || parentKey.isEmpty()) return key;
		String result = key.replaceFirst(parentKey + "\\.", "");
		if (result.equals(key)) return "";
		return result;
	}
```
===== 11 =====
```
 		if (key == null || key.isEmpty()) return "";
 		if (parentKey == null || parentKey.isEmpty()) return key;
 		String result = key.replaceFirst(parentKey + "\\.", "");
-		if (result.equals(key)) return "";
+		if (result.equals(key)) return null;
 		return result;
 	}
```
```
	/**
	 * Retrieve the part of the given key which is a child part of the given parent key.
	 * A key is a child of another key if it has the same parts at the beginning as the other key.
	 * This function will only return the child parts, so without the beginning parent parts.
	 * 
	 * <p>If the resulting key is the same as the given key, the key is considered not to be a child 
	 * of the given parent key, so an empty key will be returned.</p>
	 * 
	 * @param 	key the original key.
	 * @param 	parentKey a possible parent key of the original key.
	 * @return 	the part of the given key which is a child of the given parent key.
	 */
	public static String childKey(String key, String parentKey) {
		if (key == null || key.isEmpty()) return "";
		if (parentKey == null || parentKey.isEmpty()) return key;
		String result = key.replaceFirst(parentKey + "\\.", "");
		if (result.equals(key)) return null;
		return result;
	}
```
===== 17 =====
```
 		if (parentKey == null || parentKey.isEmpty()) return key;
 		String result = key.replaceFirst(parentKey + "\\.", "");
 		if (result.equals(key)) return "";
-		return result;
+		return null;
 	}
```
```
	/**
	 * Retrieve the part of the given key which is a child part of the given parent key.
	 * A key is a child of another key if it has the same parts at the beginning as the other key.
	 * This function will only return the child parts, so without the beginning parent parts.
	 * 
	 * <p>If the resulting key is the same as the given key, the key is considered not to be a child 
	 * of the given parent key, so an empty key will be returned.</p>
	 * 
	 * @param 	key the original key.
	 * @param 	parentKey a possible parent key of the original key.
	 * @return 	the part of the given key which is a child of the given parent key.
	 */
	public static String childKey(String key, String parentKey) {
		if (key == null || key.isEmpty()) return "";
		if (parentKey == null || parentKey.isEmpty()) return key;
		String result = key.replaceFirst(parentKey + "\\.", "");
		if (result.equals(key)) return "";
		return null;
	}
```
