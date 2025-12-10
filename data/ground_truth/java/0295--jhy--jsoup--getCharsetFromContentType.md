https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/helper/DataUtil.java#L352-L367
```
//@ ensures (\result == null ? (contentType == null ? null : (contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") == -1 ? null : validateCharset(contentType.substring(java.util.stream.IntStream.range(contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") + "charset=".length(), contentType.length()).filter(i -> !java.lang.Character.isWhitespace(contentType.charAt(i))).findFirst().orElse(contentType.length()), java.util.stream.IntStream.range(java.util.stream.IntStream.range(contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") + "charset=".length(), contentType.length()).filter(i -> !java.lang.Character.isWhitespace(contentType.charAt(i))).findFirst().orElse(contentType.length()), contentType.length()).filter(i -> java.lang.Character.isWhitespace(contentType.charAt(i)) || contentType.charAt(i) == ';' || contentType.charAt(i) == ',').findFirst().orElse(contentType.length())).replace("charset=", "")))) == null : ((contentType == null ? null : (contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") == -1 ? null : validateCharset(contentType.substring(java.util.stream.IntStream.range(contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") + "charset=".length(), contentType.length()).filter(i -> !java.lang.Character.isWhitespace(contentType.charAt(i))).findFirst().orElse(contentType.length()), java.util.stream.IntStream.range(java.util.stream.IntStream.range(contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") + "charset=".length(), contentType.length()).filter(i -> !java.lang.Character.isWhitespace(contentType.charAt(i))).findFirst().orElse(contentType.length()), contentType.length()).filter(i -> java.lang.Character.isWhitespace(contentType.charAt(i)) || contentType.charAt(i) == ';' || contentType.charAt(i) == ',').findFirst().orElse(contentType.length())).replace("charset=", "")))) != null && \result.equals(contentType == null ? null : (contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") == -1 ? null : validateCharset(contentType.substring(java.util.stream.IntStream.range(contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") + "charset=".length(), contentType.length()).filter(i -> !java.lang.Character.isWhitespace(contentType.charAt(i))).findFirst().orElse(contentType.length()), java.util.stream.IntStream.range(java.util.stream.IntStream.range(contentType.toLowerCase(java.util.Locale.ENGLISH).indexOf("charset=") + "charset=".length(), contentType.length()).filter(i -> !java.lang.Character.isWhitespace(contentType.charAt(i))).findFirst().orElse(contentType.length()), contentType.length()).filter(i -> java.lang.Character.isWhitespace(contentType.charAt(i)) || contentType.charAt(i) == ';' || contentType.charAt(i) == ',').findFirst().orElse(contentType.length())).replace("charset=", ""))))));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
===== 0 =====
```
      * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
-        if (contentType == null) return null;
+        if (contentType != null) return null;
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType != null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 1 =====
```
      * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
-        if (contentType == null) return null;
+        if (contentType != null) return null; // Incorrectly returns null if contentType is not null
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType != null) return null; // Incorrectly returns null if contentType is not null
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 2 =====
```
      * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
-        if (contentType == null) return null;
+        if (contentType == null) return "";
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return "";
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 3 =====
```
      * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
-        if (contentType == null) return null;
+        if (contentType.contains("charset")) return null; // Returns null if "charset" is found, which is incorrect
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType.contains("charset")) return null; // Returns null if "charset" is found, which is incorrect
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 4 =====
```
      * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
-        if (contentType == null) return null;
+        if (contentType.startsWith("text/")) return null; // Returns null for any content type starting with "text/"
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType.startsWith("text/")) return null; // Returns null for any content type starting with "text/"
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 5 =====
```
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
         if (contentType == null) return null;
-        Matcher m = charsetPattern.matcher(contentType);
+        Matcher m = charsetPattern.matcher(contentType.replace("charset=", "")); // This removes the "charset=" part before matching, leading to incorrect behavior.
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType.replace("charset=", "")); // This removes the "charset=" part before matching, leading to incorrect behavior.
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 6 =====
```
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
         if (contentType == null) return null;
-        Matcher m = charsetPattern.matcher(contentType);
+        Matcher m = charsetPattern.matcher(contentType.substring(0, contentType.length() - 1)); // This will cause an IndexOutOfBoundsException if contentType is empty.
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType.substring(0, contentType.length() - 1)); // This will cause an IndexOutOfBoundsException if contentType is empty.
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 7 =====
```
      */
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
         if (contentType == null) return null;
-        Matcher m = charsetPattern.matcher(contentType);
+        Matcher m = charsetPattern.matcher(contentType.toLowerCase()); // This will cause case sensitivity issues.
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType.toLowerCase()); // This will cause case sensitivity issues.
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 8 =====
```
     static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
         if (contentType == null) return null;
         Matcher m = charsetPattern.matcher(contentType);
-        if (m.find()) {
+        if (m.matches()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
             return validateCharset(charset);
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.matches()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 9 =====
```
         if (contentType == null) return null;
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
-            String charset = m.group(1).trim();
+            String charset = m.group(1).concat("UTF-8"); // Appends "UTF-8" to the charset name, which is incorrect.
             charset = charset.replace("charset=", "");
             return validateCharset(charset);
         }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).concat("UTF-8"); // Appends "UTF-8" to the charset name, which is incorrect.
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 10 =====
```
         if (contentType == null) return null;
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
-            String charset = m.group(1).trim();
+            String charset = m.group(1).toUpperCase(); // Converts charset to uppercase, which may not be valid.
             charset = charset.replace("charset=", "");
             return validateCharset(charset);
         }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).toUpperCase(); // Converts charset to uppercase, which may not be valid.
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 11 =====
```
         if (contentType == null) return null;
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
-            String charset = m.group(1).trim();
+            String charset = m.group(1).trim().toLowerCase(); // Converts charset to lowercase, which may not be valid.
             charset = charset.replace("charset=", "");
             return validateCharset(charset);
         }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim().toLowerCase(); // Converts charset to lowercase, which may not be valid.
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 12 =====
```
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
-            charset = charset.replace("charset=", "");
+            charset = charset.concat("UTF-8");
             return validateCharset(charset);
         }
         return null;
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.concat("UTF-8");
            return validateCharset(charset);
        }
        return null;
    }
```
===== 13 =====
```
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
-            charset = charset.replace("charset=", "");
+            charset = charset.toLowerCase();
             return validateCharset(charset);
         }
         return null;
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.toLowerCase();
            return validateCharset(charset);
        }
        return null;
    }
```
===== 14 =====
```
         Matcher m = charsetPattern.matcher(contentType);
         if (m.find()) {
             String charset = m.group(1).trim();
-            charset = charset.replace("charset=", "");
+            charset = charset.trim();
             return validateCharset(charset);
         }
         return null;
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.trim();
            return validateCharset(charset);
        }
        return null;
    }
```
===== 15 =====
```
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
-            return validateCharset(charset);
+            return "";
         }
         return null;
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return "";
        }
        return null;
    }
```
===== 16 =====
```
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
-            return validateCharset(charset);
+            return charset.toLowerCase(); // Converts the charset to lowercase, which may not be valid for some charsets.
         }
         return null;
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return charset.toLowerCase(); // Converts the charset to lowercase, which may not be valid for some charsets.
        }
        return null;
    }
```
===== 17 =====
```
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
-            return validateCharset(charset);
+            return charset; // Returns the raw charset string without validation, which may lead to unsupported charset usage.
         }
         return null;
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return charset; // Returns the raw charset string without validation, which may lead to unsupported charset usage.
        }
        return null;
    }
```
===== 18 =====
```
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
-            return validateCharset(charset);
+            return null;
         }
         return null;
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return null;
        }
        return null;
    }
```
===== 19 =====
```
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
-            return validateCharset(charset);
+            return null; // Always returns null, causing the default charset to be used regardless of the content type.
         }
         return null;
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return null; // Always returns null, causing the default charset to be used regardless of the content type.
        }
        return null;
    }
```
===== 20 =====
```
         if (m.find()) {
             String charset = m.group(1).trim();
             charset = charset.replace("charset=", "");
-            return validateCharset(charset);
+            return validateCharset(charset + "invalid"); // Appends "invalid" to the charset, likely resulting in an unsupported charset.
         }
         return null;
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset + "invalid"); // Appends "invalid" to the charset, likely resulting in an unsupported charset.
        }
        return null;
    }
```
===== 21 =====
```
             charset = charset.replace("charset=", "");
             return validateCharset(charset);
         }
-        return null;
+        return "";
     }
```
```
    /**
     * Parse out a charset from a content type header. If the charset is not supported, returns null (so the default
     * will kick in.)
     * @param contentType e.g. "text/html; charset=EUC-JP"
     * @return "EUC-JP", or null if not found. Charset is trimmed and uppercased.
     */
    static @Nullable String getCharsetFromContentType(@Nullable String contentType) {
        if (contentType == null) return null;
        Matcher m = charsetPattern.matcher(contentType);
        if (m.find()) {
            String charset = m.group(1).trim();
            charset = charset.replace("charset=", "");
            return validateCharset(charset);
        }
        return "";
    }
```
