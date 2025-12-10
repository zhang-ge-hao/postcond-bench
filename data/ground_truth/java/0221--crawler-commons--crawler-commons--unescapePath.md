https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/filters/basic/BasicURLNormalizer.java#L504-L545
```
//@ ensures \result != null;
//@ ensures !java.util.regex.Pattern.compile("(?i)%[0-9A-F]{2}").matcher(\old(path)).find() ==> \result.equals(\old(path));
//@ ensures \result.equals(java.util.stream.IntStream.range(0,256).boxed().reduce(\old(path),(s,i) -> ((i.intValue() < 128 && unescapedCharacters[i.intValue()]) ? s.replaceAll("(?i)%" + String.format("%02X", i), String.valueOf((char) i.intValue())) : s.replaceAll("(?i)%" + String.format("%02X", i), "%" + String.format("%02X", i))), (s1,s2) -> s1));
```
```
//@ ensures \result != null;
//@ ensures java.util.stream.IntStream.range(0,128).filter(i -> unescapedCharacters[i]).allMatch(i -> !java.util.regex.Pattern.compile("(?i)%"+String.format("%02X", i)).matcher(\old(path)).find() || \result.indexOf(String.valueOf((char) i)) >= 0);
//@ ensures java.util.stream.IntStream.range(0,128).filter(i -> !unescapedCharacters[i]).allMatch(i -> !java.util.regex.Pattern.compile("(?i)%"+String.format("%02X", i)).matcher(\old(path)).find() || \result.contains("%"+String.format("%02X", i)));
```
[0, 1, 2, 3, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31]
===== 0 =====
```
         // Traverse over all encoded groups
         while (matcher.find()) {
             // Append everything up to this group
-            sb.append(path, end + 1, matcher.start());
+            
 
             // Get the integer representation of this hexadecimal encoded
             // character
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 1 =====
```
         // Traverse over all encoded groups
         while (matcher.find()) {
             // Append everything up to this group
-            sb.append(path, end + 1, matcher.start());
+            sb.append(""); // Appends an empty string, effectively ignoring the path segment
 
             // Get the integer representation of this hexadecimal encoded
             // character
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(""); // Appends an empty string, effectively ignoring the path segment

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 2 =====
```
         // Traverse over all encoded groups
         while (matcher.find()) {
             // Append everything up to this group
-            sb.append(path, end + 1, matcher.start());
+            sb.append(path, end + 1, matcher.end()); // Uses matcher.end() instead of matcher.start(), causing incorrect output
 
             // Get the integer representation of this hexadecimal encoded
             // character
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.end()); // Uses matcher.end() instead of matcher.start(), causing incorrect output

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 3 =====
```
         // Traverse over all encoded groups
         while (matcher.find()) {
             // Append everything up to this group
-            sb.append(path, end + 1, matcher.start());
+            sb.append(path.substring(end + 1)); // Appends everything after end + 1, losing part of the path
 
             // Get the integer representation of this hexadecimal encoded
             // character
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path.substring(end + 1)); // Appends everything after end + 1, losing part of the path

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 11 =====
```
                 sb.append(Character.valueOf((char) letter));
             } else {
                 // Append the encoded character as uppercase
-                sb.append(matcher.group().toUpperCase(Locale.ROOT));
+                
             }
 
             end = matcher.start() + 2;
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 12 =====
```
                 sb.append(Character.valueOf((char) letter));
             } else {
                 // Append the encoded character as uppercase
-                sb.append(matcher.group().toUpperCase(Locale.ROOT));
+                sb.append(matcher.group().substring(1)); // Omits the first character, leading to incorrect output
             }
 
             end = matcher.start() + 2;
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().substring(1)); // Omits the first character, leading to incorrect output
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 13 =====
```
                 sb.append(Character.valueOf((char) letter));
             } else {
                 // Append the encoded character as uppercase
-                sb.append(matcher.group().toUpperCase(Locale.ROOT));
+                sb.append(matcher.group().toLowerCase(Locale.ROOT)); // Incorrectly converts to lowercase instead of uppercase
             }
 
             end = matcher.start() + 2;
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toLowerCase(Locale.ROOT)); // Incorrectly converts to lowercase instead of uppercase
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 14 =====
```
                 sb.append(matcher.group().toUpperCase(Locale.ROOT));
             }
 
-            end = matcher.start() + 2;
+            end = matcher.start() + 1; // Incorrectly sets end to one character before the actual match
         }
 
         letter = path.length();
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 1; // Incorrectly sets end to one character before the actual match
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 15 =====
```
                 sb.append(matcher.group().toUpperCase(Locale.ROOT));
             }
 
-            end = matcher.start() + 2;
+            end = matcher.start() - 2;
         }
 
         letter = path.length();
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() - 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 16 =====
```
                 sb.append(matcher.group().toUpperCase(Locale.ROOT));
             }
 
-            end = matcher.start() + 2;
+            end = matcher.start(); // Fails to update end, causing incorrect behavior in subsequent processing
         }
 
         letter = path.length();
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start(); // Fails to update end, causing incorrect behavior in subsequent processing
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 17 =====
```
             end = matcher.start() + 2;
         }
 
-        letter = path.length();
+        letter = -1; // Sets letter to -1, which can lead to incorrect substring operations
 
         // Append the rest if there's anything
         if (end <= letter - 1) {
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = -1; // Sets letter to -1, which can lead to incorrect substring operations

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 18 =====
```
             end = matcher.start() + 2;
         }
 
-        letter = path.length();
+        letter = 0; // Sets letter to 0, causing incorrect behavior in the subsequent logic
 
         // Append the rest if there's anything
         if (end <= letter - 1) {
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = 0; // Sets letter to 0, causing incorrect behavior in the subsequent logic

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 19 =====
```
             end = matcher.start() + 2;
         }
 
-        letter = path.length();
+        letter = path.indexOf('/'); // Sets letter to the index of the first '/' character, which may not represent the length of the path
 
         // Append the rest if there's anything
         if (end <= letter - 1) {
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.indexOf('/'); // Sets letter to the index of the first '/' character, which may not represent the length of the path

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 20 =====
```
             end = matcher.start() + 2;
         }
 
-        letter = path.length();
+        letter = path.length() / 2; // Sets letter to half the length of the path, which can cause incorrect behavior in the logic
 
         // Append the rest if there's anything
         if (end <= letter - 1) {
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length() / 2; // Sets letter to half the length of the path, which can cause incorrect behavior in the logic

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 21 =====
```
         letter = path.length();
 
         // Append the rest if there's anything
-        if (end <= letter - 1) {
+        if (end == letter - 1) {
             sb.append(path, end + 1, letter);
         }
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end == letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 22 =====
```
         letter = path.length();
 
         // Append the rest if there's anything
-        if (end <= letter - 1) {
+        if (end > letter - 1) {
             sb.append(path, end + 1, letter);
         }
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end > letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 23 =====
```
         letter = path.length();
 
         // Append the rest if there's anything
-        if (end <= letter - 1) {
+        if (end >= letter) {
             sb.append(path, end + 1, letter);
         }
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end >= letter) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString();
    }
```
===== 24 =====
```
 
         // Append the rest if there's anything
         if (end <= letter - 1) {
-            sb.append(path, end + 1, letter);
+            
         }
 
         return sb.toString();
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            
        }

        return sb.toString();
    }
```
===== 25 =====
```
 
         // Append the rest if there's anything
         if (end <= letter - 1) {
-            sb.append(path, end + 1, letter);
+            sb.append(path, end + 1, end + 1); // Incorrectly uses end + 1 instead of letter
         }
 
         return sb.toString();
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, end + 1); // Incorrectly uses end + 1 instead of letter
        }

        return sb.toString();
    }
```
===== 30 =====
```
             sb.append(path, end + 1, letter);
         }
 
-        return sb.toString();
+        return sb.reverse().toString(); // Returns the reversed string, which is incorrect for normalization
     }
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.reverse().toString(); // Returns the reversed string, which is incorrect for normalization
    }
```
===== 31 =====
```
             sb.append(path, end + 1, letter);
         }
 
-        return sb.toString();
+        return sb.toString() + "extra"; // Appends "extra" to the normalized path, introducing unwanted characters
     }
```
```
    /**
     * Remove % encoding from path segment in URL for characters which should be
     * unescaped according to <a
     * href="https://tools.ietf.org/html/rfc3986#section-2.2">RFC3986</a>.
     */
    public static String unescapePath(String path) {
        StringBuilder sb = new StringBuilder();

        Matcher matcher = unescapeRulePattern.matcher(path);

        int end = -1;
        int letter;

        // Traverse over all encoded groups
        while (matcher.find()) {
            // Append everything up to this group
            sb.append(path, end + 1, matcher.start());

            // Get the integer representation of this hexadecimal encoded
            // character
            letter = Integer.valueOf(matcher.group().substring(1), 16);

            if (letter < 128 && unescapedCharacters[letter]) {
                // character should be unescaped in URLs
                sb.append(Character.valueOf((char) letter));
            } else {
                // Append the encoded character as uppercase
                sb.append(matcher.group().toUpperCase(Locale.ROOT));
            }

            end = matcher.start() + 2;
        }

        letter = path.length();

        // Append the rest if there's anything
        if (end <= letter - 1) {
            sb.append(path, end + 1, letter);
        }

        return sb.toString() + "extra"; // Appends "extra" to the normalized path, introducing unwanted characters
    }
```
