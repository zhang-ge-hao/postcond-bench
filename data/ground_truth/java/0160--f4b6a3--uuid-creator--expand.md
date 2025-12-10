https://github.com/f4b6a3/uuid-creator/blob/3f41c3e6ed9fa3c229303672960570281f35a125/./src/main/java/com/github/f4b6a3/uuid/codec/base/BaseN.java#L284-L313
```
//@ ensures \result != null;
//@ ensures string.length() == 0 ==> \result.length() == 0;
//@ ensures string.length() == 1 ==> \result.length() == 1;
//@ ensures string.length() > 0 ==> \result.length() > 0;
//@ ensures string.length() > 0 ==> \result.charAt(0) == string.charAt(0);
//@ ensures string.length() > 0 ==> \result.charAt(\result.length() - 1) == string.charAt(string.length() - 1);
//@ ensures !string.contains(" ") ==> !\result.contains(" ");
//@ ensures (string.indexOf('-') >= 1 && string.indexOf('-') <= string.length() - 2 && com.github.f4b6a3.uuid.codec.base.BaseN.expand(string.charAt(string.indexOf('-') - 1), string.charAt(string.indexOf('-') + 1)).length != 0) ==> \result.contains(new String(com.github.f4b6a3.uuid.codec.base.BaseN.expand(string.charAt(string.indexOf('-') - 1), string.charAt(string.indexOf('-') + 1))));
//@ ensures java.util.stream.IntStream.range(1, string.length() - 1).filter(i -> string.charAt(i) == '-' && com.github.f4b6a3.uuid.codec.base.BaseN.expand(string.charAt(i - 1), string.charAt(i + 1)).length == 0 && string.indexOf(string.charAt(i - 1)) == string.lastIndexOf(string.charAt(i - 1))).allMatch(i -> \result.indexOf(string.charAt(i - 1)) != -1);
//@ ensures java.util.stream.IntStream.range(1, string.length() - 1).filter(i -> string.charAt(i) == '-' && com.github.f4b6a3.uuid.codec.base.BaseN.expand(string.charAt(i - 1), string.charAt(i + 1)).length == 0 && string.indexOf(string.charAt(i - 1)) == string.lastIndexOf(string.charAt(i - 1))).allMatch(i -> !\result.contains("" + string.charAt(i - 1) + string.charAt(i - 1)));
```
```
//@ ensures \result != null;
//@ ensures \old(string).length() == 0 ==> \result.length() == 0;
//@ ensures \old(string).length() > 0 ==> \result.length() > 0;
//@ ensures \old(string).length() > 0 ==> \result.charAt(0) == \old(string).charAt(0);
//@ ensures \old(string).length() > 0 ==> \result.charAt(\result.length() - 1) == \old(string).charAt(\old(string).length() - 1);
//@ ensures (\old(string).indexOf('-') >= 1 && \old(string).indexOf('-') <= \old(string).length() - 2 && expand(\old(string).charAt(\old(string).indexOf('-') - 1), \old(string).charAt(\old(string).indexOf('-') + 1)).length != 0) ==> \result.contains(new String(expand(\old(string).charAt(\old(string).indexOf('-') - 1), \old(string).charAt(\old(string).indexOf('-') + 1))));
```
[25, 26, 27, 28, 29, 35]
===== 25 =====
```
 					i += 2; // skip
 					buffer.append(expanded);
 				} else {
-					buffer.append(a);
+					
 				}
 			} else {
 				buffer.append(a);
```
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					
				}
			} else {
				buffer.append(a);
			}
			i++;
		}

		return buffer.toString();
	}
```
===== 26 =====
```
 					i += 2; // skip
 					buffer.append(expanded);
 				} else {
-					buffer.append(a);
+					buffer.append(Character.toUpperCase(a));
 				}
 			} else {
 				buffer.append(a);
```
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					buffer.append(Character.toUpperCase(a));
				}
			} else {
				buffer.append(a);
			}
			i++;
		}

		return buffer.toString();
	}
```
===== 27 =====
```
 					i += 2; // skip
 					buffer.append(expanded);
 				} else {
-					buffer.append(a);
+					buffer.append(a).append(' ');
 				}
 			} else {
 				buffer.append(a);
```
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					buffer.append(a).append(' ');
				}
			} else {
				buffer.append(a);
			}
			i++;
		}

		return buffer.toString();
	}
```
===== 28 =====
```
 					i += 2; // skip
 					buffer.append(expanded);
 				} else {
-					buffer.append(a);
+					buffer.append(a).append(a);
 				}
 			} else {
 				buffer.append(a);
```
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					buffer.append(a).append(a);
				}
			} else {
				buffer.append(a);
			}
			i++;
		}

		return buffer.toString();
	}
```
===== 29 =====
```
 					i += 2; // skip
 					buffer.append(expanded);
 				} else {
-					buffer.append(a);
+					buffer.append(b);
 				}
 			} else {
 				buffer.append(a);
```
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					buffer.append(b);
				}
			} else {
				buffer.append(a);
			}
			i++;
		}

		return buffer.toString();
	}
```
===== 35 =====
```
 					buffer.append(a);
 				}
 			} else {
-				buffer.append(a);
+				buffer.append(a).append(a); // Appends the character twice, altering the expected output length
 			}
 			i++;
 		}
```
```
	/**
	 * Expands character sequences similar to 0-9, a-z and A-Z.
	 * 
	 * @param string a string to be expanded
	 * @return a string
	 */
	protected static String expand(String string) {

		StringBuilder buffer = new StringBuilder();

		int i = 1;
		while (i <= string.length()) {
			final char a = string.charAt(i - 1); // previous char
			if ((i < string.length() - 1) && (string.charAt(i) == '-')) {
				final char b = string.charAt(i + 1); // next char
				char[] expanded = expand(a, b);
				if (expanded.length != 0) {
					i += 2; // skip
					buffer.append(expanded);
				} else {
					buffer.append(a);
				}
			} else {
				buffer.append(a).append(a); // Appends the character twice, altering the expected output length
			}
			i++;
		}

		return buffer.toString();
	}
```
