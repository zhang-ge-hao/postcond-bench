https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/ReadYamlMapping.java#L230-L276
```
🈚️

No API.
Need validate private field. `previous` in `ReadFlowMapping`, etc.

//@ ensures this.all == \old(this.all);
//@ ensures this.significant == \old(this.significant);
//@ ensures this.previous == \old(this.previous);
//@ ensures this.commentStop == \old(this.commentStop);
//@ ensures \result == null || key == null || java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().contains(key));
//@ ensures key == null || !java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().startsWith(key + ":")) || \result != null;
//@ ensures key == null || !java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().startsWith("\"" + key + "\":")) || \result != null;
//@ ensures key == null || !java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().startsWith("'" + key + "':")) || \result != null;
//@ ensures key == null || !java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().startsWith("- " + key + ":")) || \result != null;
//@ ensures key == null || !java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().startsWith("- \"" + key + "\":")) || \result != null;
//@ ensures key == null || !java.util.stream.StreamSupport.stream(this.significant.spliterator(), false).anyMatch(line -> line.trimmed().startsWith("- '" + key + "':")) || \result != null;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
===== 0 =====
```
             "\"" + key + "\"",
             "'" + key + "'",
         };
-        for(final String tryKey : keys) {
+        for(final String tryKey : new String[] { "dummyKey" }) {
             for (final YamlLine line : this.significant) {
                 final String trimmed = line.trimmed();
                 final String relaxedKey = relaxed(tryKey);
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : new String[] { "dummyKey" }) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 1 =====
```
             "'" + key + "'",
         };
         for(final String tryKey : keys) {
-            for (final YamlLine line : this.significant) {
+            for (final YamlLine line : this.significant) { if (line.number() % 2 == 0) continue;
                 final String trimmed = line.trimmed();
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) { if (line.number() % 2 == 0) continue;
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 2 =====
```
             "'" + key + "'",
         };
         for(final String tryKey : keys) {
-            for (final YamlLine line : this.significant) {
+            for (final YamlLine line : this.significant) { if (line.number() == 0) break;
                 final String trimmed = line.trimmed();
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) { if (line.number() == 0) break;
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 3 =====
```
         };
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
-                final String trimmed = line.trimmed();
+                final String trimmed = line.toString(); // This will not give the trimmed version of the line.
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.toString(); // This will not give the trimmed version of the line.
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 4 =====
```
         };
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
-                final String trimmed = line.trimmed();
+                final String trimmed = line.trimmed() + " "; // This adds an extra space at the end, which can affect key matching logic.
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed() + " "; // This adds an extra space at the end, which can affect key matching logic.
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 5 =====
```
         };
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
-                final String trimmed = line.trimmed();
+                final String trimmed = line.trimmed().replace(" ", ""); // This removes all spaces, which can lead to incorrect key matching.
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed().replace(" ", ""); // This removes all spaces, which can lead to incorrect key matching.
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 6 =====
```
         };
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
-                final String trimmed = line.trimmed();
+                final String trimmed = line.trimmed().substring(1); // This removes the first character, which may lead to incorrect parsing of keys.
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed().substring(1); // This removes the first character, which may lead to incorrect parsing of keys.
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 7 =====
```
         };
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
-                final String trimmed = line.trimmed();
+                final String trimmed = line.trimmed().toUpperCase(); // This changes the case of the line, potentially affecting key matching.
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed().toUpperCase(); // This changes the case of the line, potentially affecting key matching.
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 8 =====
```
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
                 final String trimmed = line.trimmed();
-                final String relaxedKey = relaxed(tryKey);
+                final String relaxedKey = relaxed(tryKey + " "); // Adding a space to the key, which will cause regex mismatches
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey + " "); // Adding a space to the key, which will cause regex mismatches
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 9 =====
```
         for(final String tryKey : keys) {
             for (final YamlLine line : this.significant) {
                 final String trimmed = line.trimmed();
-                final String relaxedKey = relaxed(tryKey);
+                final String relaxedKey = relaxed(tryKey.toUpperCase()); // Modifying the key to uppercase, which may not match the original
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey.toUpperCase()); // Modifying the key to uppercase, which may not match the original
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 10 =====
```
                 final String trimmed = line.trimmed();
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
-                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
+                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\*$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
                     value = this.significant.nextYamlNode(line);
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\*$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 11 =====
```
                 final String trimmed = line.trimmed();
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
-                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
+                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\?$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
                     value = this.significant.nextYamlNode(line);
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\?$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 12 =====
```
                 final String relaxedKey = relaxed(tryKey);
                 if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
-                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
+                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[ ]*$")
                 ) {
                     value = this.significant.nextYamlNode(line);
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[ ]*$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 13 =====
```
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
-                    value = this.significant.nextYamlNode(line);
+                    value = new ReadFlowMapping(this.getPreviousLine(line), this.all); // Incorrectly creating a flow mapping instead of getting the node
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                     value = new ReadFlowMapping(
                         this.getPreviousLine(line),
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = new ReadFlowMapping(this.getPreviousLine(line), this.all); // Incorrectly creating a flow mapping instead of getting the node
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 14 =====
```
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
-                    value = this.significant.nextYamlNode(line);
+                    value = new ReadPlainScalar(this.all, line); // Incorrectly treating the line as a plain scalar instead of a node
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                     value = new ReadFlowMapping(
                         this.getPreviousLine(line),
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = new ReadPlainScalar(this.all, line); // Incorrectly treating the line as a plain scalar instead of a node
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 15 =====
```
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
-                    value = this.significant.nextYamlNode(line);
+                    value = null; // Assigning null instead of the actual node
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                     value = new ReadFlowMapping(
                         this.getPreviousLine(line),
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = null; // Assigning null instead of the actual node
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 16 =====
```
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
                     value = this.significant.nextYamlNode(line);
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\(.*$")) {
                     value = new ReadFlowMapping(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\(.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 17 =====
```
                     || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                 ) {
                     value = this.significant.nextYamlNode(line);
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                     value = new ReadFlowMapping(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 18 =====
```
                     value = this.significant.nextYamlNode(line);
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                     value = new ReadFlowMapping(
-                        this.getPreviousLine(line),
+                        this.all.line(line.number() - 2),
                         this.all
                     );
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.all.line(line.number() - 2),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 19 =====
```
                         this.getPreviousLine(line),
                         this.all
                     );
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\(.*$")) {
                     value = new ReadFlowSequence(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\(.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 20 =====
```
                         this.getPreviousLine(line),
                         this.all
                     );
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*\\]")) {
                     value = new ReadFlowSequence(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*\\]")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 21 =====
```
                         this.getPreviousLine(line),
                         this.all
                     );
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*\\]$")) {
                     value = new ReadFlowSequence(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*\\]$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 22 =====
```
                         this.getPreviousLine(line),
                         this.all
                     );
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                     value = new ReadFlowSequence(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 23 =====
```
                         this.getPreviousLine(line),
                         this.all
                     );
-                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
+                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*\\}$")) {
                     value = new ReadFlowSequence(
                         this.getPreviousLine(line),
                         this.all
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*\\}$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 24 =====
```
                     );
                 } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                     value = new ReadFlowSequence(
-                        this.getPreviousLine(line),
+                        this.all.line(line.number() - 2),
                         this.all
                     );
                 } else if((trimmed.startsWith(tryKey + ":")
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.all.line(line.number() - 2),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 25 =====
```
                     );
                 } else if((trimmed.startsWith(tryKey + ":")
                         || trimmed.startsWith("- " + tryKey + ":"))
-                        && trimmed.length() > 1
+                        && trimmed.length() < 1
                 ) {
                     value = new ReadPlainScalar(this.all, line);
                 }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() < 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 26 =====
```
                     );
                 } else if((trimmed.startsWith(tryKey + ":")
                         || trimmed.startsWith("- " + tryKey + ":"))
-                        && trimmed.length() > 1
+                        && trimmed.length() < 2
                 ) {
                     value = new ReadPlainScalar(this.all, line);
                 }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() < 2
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 27 =====
```
                     );
                 } else if((trimmed.startsWith(tryKey + ":")
                         || trimmed.startsWith("- " + tryKey + ":"))
-                        && trimmed.length() > 1
+                        && trimmed.length() <= 1
                 ) {
                     value = new ReadPlainScalar(this.all, line);
                 }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() <= 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 28 =====
```
                     );
                 } else if((trimmed.startsWith(tryKey + ":")
                         || trimmed.startsWith("- " + tryKey + ":"))
-                        && trimmed.length() > 1
+                        && trimmed.length() == 1
                 ) {
                     value = new ReadPlainScalar(this.all, line);
                 }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() == 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 29 =====
```
                     value = new ReadPlainScalar(this.all, line);
                 }
 
-                if(value != null) {
+                if(value != null && false) {
                     return value;
                 }
             }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null && false) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 30 =====
```
                     value = new ReadPlainScalar(this.all, line);
                 }
 
-                if(value != null) {
+                if(value != null && value.equals("unexpectedValue")) {
                     return value;
                 }
             }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null && value.equals("unexpectedValue")) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 31 =====
```
                     value = new ReadPlainScalar(this.all, line);
                 }
 
-                if(value != null) {
+                if(value == null || true) {
                     return value;
                 }
             }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value == null || true) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 32 =====
```
                     value = new ReadPlainScalar(this.all, line);
                 }
 
-                if(value != null) {
+                if(value == null) {
                     return value;
                 }
             }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value == null) {
                    return value;
                }
            }
        }
        return null;
    }
```
===== 33 =====
```
                 }
 
                 if(value != null) {
-                    return value;
+                    return null;
                 }
             }
         }
```
```
    /**
     * The YamlNode value associated with a String (scalar) key.
     * @param key String key.
     * @return YamlNode.
     * @checkstyle ReturnCount (50 lines)
     * @checkstyle LineLength (30 lines)
     */
    private YamlNode valueOfStringKey(final String key) {
        YamlNode value = null;
        final String[] keys = new String[] {
            key,
            "\"" + key + "\"",
            "'" + key + "'",
        };
        for(final String tryKey : keys) {
            for (final YamlLine line : this.significant) {
                final String trimmed = line.trimmed();
                final String relaxedKey = relaxed(tryKey);
                if(trimmed.matches("^-?[ ]*" + Pattern.quote(relaxedKey) + ":")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*>$")
                    || trimmed.matches("^" + Pattern.quote(relaxedKey) + ":[ ]*\\|[+-]?$")
                ) {
                    value = this.significant.nextYamlNode(line);
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\{.*$")) {
                    value = new ReadFlowMapping(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if(trimmed.matches(Pattern.quote(relaxedKey) + ":\\s*\\[.*$")) {
                    value = new ReadFlowSequence(
                        this.getPreviousLine(line),
                        this.all
                    );
                } else if((trimmed.startsWith(tryKey + ":")
                        || trimmed.startsWith("- " + tryKey + ":"))
                        && trimmed.length() > 1
                ) {
                    value = new ReadPlainScalar(this.all, line);
                }

                if(value != null) {
                    return null;
                }
            }
        }
        return null;
    }
```
