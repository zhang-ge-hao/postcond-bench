https://github.com/mirromutth/r2dbc-mysql/blob/ba5401f05740752290979aa76b23caea6a3afdde/./src/main/java/dev/miku/r2dbc/mysql/Query.java#L225-L314
```
// @ ensures (start < 0 || start >= sql.length()) ==> \result == -1;
// @ ensures \result == -1 || (\result >= start && \result < sql.length() && sql.charAt(\result) == '?');
// @ ensures sql.toString().indexOf('?', start) < 0 ==> \result == -1;
// @ ensures \result >= 0 ==> sql.toString().indexOf('?', start) >= 0;
// @ ensures sql.length() == \old(sql.length());
// @ ensures start == \old(start);
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
//@ ensures \result >= -1 && \result < sql.length();
//@ ensures \result >= 0 ==> sql.charAt(\result) == '?';
//@ ensures \result == java.util.stream.IntStream.range(start, sql.length()).filter(i -> sql.charAt(i) == '?').filter(i -> !(java.util.stream.IntStream.range(0, i).anyMatch(a -> a + 1 < sql.length() && sql.charAt(a) == '/' && sql.charAt(a + 1) == '*' && java.util.stream.IntStream.range(a + 2, i + 1).noneMatch(b -> b + 1 < sql.length() && sql.charAt(b) == '*' && sql.charAt(b + 1) == '/')) || java.util.stream.IntStream.range(0, i).anyMatch(a -> a + 1 < sql.length() && sql.charAt(a) == '-' && sql.charAt(a + 1) == '-' && java.util.stream.IntStream.range(a + 2, i + 1).noneMatch(b -> sql.charAt(b) == '\n' || sql.charAt(b) == '\r')) || (java.util.stream.IntStream.range(0, i).filter(a -> sql.charAt(a) == '\'').count() % 2L == 1L) || (java.util.stream.IntStream.range(0, i).filter(a -> sql.charAt(a) == '\"').count() % 2L == 1L) || (java.util.stream.IntStream.range(0, i).filter(a -> sql.charAt(a) == '`').count() % 2L == 1L))).findFirst().orElse(-1);

```
===== 43: failed =====
```
 
                     break;
                 default:
-                    if (ch == '?') {
+                    if (ch == '\'') {
                         return offset - 1;
                     }
```
```
    /**
     * Locates the first occurrence of {@literal ?} return true in {@code sql} starting at {@code offset}.
     * <p>
     * The SQL string may contain:
     *
     * <ul>
     * <li>Literals, enclosed in single quotes ({@literal '}) </li>
     * <li>Literals, enclosed in double quotes ({@literal "}) </li>
     * <li>Literals, enclosed in backtick quotes ({@literal `}) </li>
     * <li>Escaped escapes or literal delimiters (i.e. {@literal ''}, {@literal ""} or {@literal ``})</li>
     * <li>Single-line comments beginning with {@literal --}</li>
     * <li>Multi-line comments beginning enclosed</li>
     * </ul>
     *
     * @param sql   the SQL string to search in.
     * @param start the offset to start searching.
     * @return the offset or a negative integer if not found.
     */
    private static int findParamMark(CharSequence sql, int start) {
        int offset = start;
        int length = sql.length();
        char ch;

        while (offset < length && offset >= 0) {
            ch = sql.charAt(offset++);
            switch (ch) {
                case '/':
                    if (offset == length) {
                        break;
                    }

                    if (sql.charAt(offset) == '*') {
                        // Consume if '/* ... */' comment.
                        while (++offset < length) {
                            if (sql.charAt(offset) == '*' && offset + 1 < length &&
                                sql.charAt(offset + 1) == '/') {
                                // If end of comment.
                                offset += 2;
                                break;
                            }
                        }
                        break;
                    }

                    break;
                case '-':
                    if (offset == length) {
                        break;
                    }

                    if (sql.charAt(offset) == '-') {
                        // Consume if '-- ... \n' comment.
                        while (++offset < length) {
                            char now = sql.charAt(offset);
                            if (now == '\n' || now == '\r') {
                                // If end of comment
                                offset++;
                                break;
                            }
                        }
                        break;
                    }

                    break;
                case '`':
                case '\'':
                case '"':
                    // Quote cases, should find same quote
                    while (offset < length) {
                        if (sql.charAt(offset++) == ch) {
                            if (length == offset || sql.charAt(offset) != ch) {
                                break;
                            }

                            ++offset;
                        }
                    }

                    break;
                default:
                    if (ch == '\'') {
                        return offset - 1;
                    }

                    break;
            }
        }

        return -1;
    }
```
