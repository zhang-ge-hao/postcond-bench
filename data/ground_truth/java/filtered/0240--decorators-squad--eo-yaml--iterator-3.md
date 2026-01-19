https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/StartMarkers.java#L57-L97
```
🈚️

Iterator
```
```
//@ ensures \result != null;
//@ ensures \old(this.yamlLines.iterator().hasNext()) ==> \result.hasNext();
//@ ensures !\old(this.yamlLines.iterator().hasNext()) ==> !\result.hasNext();
//@ ensures (\old(this.yamlLines.iterator().hasNext()) && \old(java.util.stream.StreamSupport.stream(java.util.Spliterators.spliteratorUnknownSize(this.yamlLines.iterator(),0), false).findFirst().isPresent() && "---".equals(java.util.stream.StreamSupport.stream(java.util.Spliterators.spliteratorUnknownSize(this.yamlLines.iterator(),0), false).findFirst().get().trimmed()))) ==> \result.hasNext();
```
[1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22]
===== 1 =====
```
     @Override
     public Iterator<YamlLine> iterator() {
         Iterator<YamlLine> iterator = this.yamlLines.iterator();
-        if (iterator.hasNext()) {
+        if (iterator.hasNext() && false) {
             final List<YamlLine> docsStart = new ArrayList<>();
             final YamlLine first = iterator.next();
             if("---".equals(first.trimmed())) {
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext() && false) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 2 =====
```
         if (iterator.hasNext()) {
             final List<YamlLine> docsStart = new ArrayList<>();
             final YamlLine first = iterator.next();
-            if("---".equals(first.trimmed())) {
+            if(!"---".equals(first.trimmed())) {
                 docsStart.add(first);
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if(!"---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 3 =====
```
         if (iterator.hasNext()) {
             final List<YamlLine> docsStart = new ArrayList<>();
             final YamlLine first = iterator.next();
-            if("---".equals(first.trimmed())) {
+            if("...".equals(first.trimmed())) {
                 docsStart.add(first);
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("...".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 4 =====
```
         if (iterator.hasNext()) {
             final List<YamlLine> docsStart = new ArrayList<>();
             final YamlLine first = iterator.next();
-            if("---".equals(first.trimmed())) {
+            if(first.trimmed().isEmpty()) {
                 docsStart.add(first);
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if(first.trimmed().isEmpty()) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 6 =====
```
             final List<YamlLine> docsStart = new ArrayList<>();
             final YamlLine first = iterator.next();
             if("---".equals(first.trimmed())) {
-                docsStart.add(first);
+                docsStart.add(new YamlLine.NullYamlLine());
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
             }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(new YamlLine.NullYamlLine());
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 7 =====
```
             final List<YamlLine> docsStart = new ArrayList<>();
             final YamlLine first = iterator.next();
             if("---".equals(first.trimmed())) {
-                docsStart.add(first);
+                docsStart.add(null);
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
             }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(null);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 8 =====
```
             if("---".equals(first.trimmed())) {
                 docsStart.add(first);
             } else {
-                docsStart.add(new YamlLine.NullYamlLine());
+                
             }
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 9 =====
```
             if("---".equals(first.trimmed())) {
                 docsStart.add(first);
             } else {
-                docsStart.add(new YamlLine.NullYamlLine());
+                docsStart.add(first); // Adding the first line again instead of a NullYamlLine
             }
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(first); // Adding the first line again instead of a NullYamlLine
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 10 =====
```
             if("---".equals(first.trimmed())) {
                 docsStart.add(first);
             } else {
-                docsStart.add(new YamlLine.NullYamlLine());
+                docsStart.add(null); // Adding a null reference instead of a NullYamlLine
             }
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(null); // Adding a null reference instead of a NullYamlLine
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 11 =====
```
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
             }
-            while (iterator.hasNext()) {
+            for (int i = 0; i < 1; i++) {
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
                 if ("---".equals(currentLine)) {
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            for (int i = 0; i < 1; i++) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 12 =====
```
             } else {
                 docsStart.add(new YamlLine.NullYamlLine());
             }
-            while (iterator.hasNext()) {
+            if (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
                 if ("---".equals(currentLine)) {
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            if (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 13 =====
```
             }
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
-                final String currentLine = current.trimmed();
+                final String currentLine = current.trimmed().replaceAll("-", ""); // Removes dashes, making "---" unrecognizable
                 if ("---".equals(currentLine)) {
                     docsStart.add(current);
                 }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed().replaceAll("-", ""); // Removes dashes, making "---" unrecognizable
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 14 =====
```
             }
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
-                final String currentLine = current.trimmed();
+                final String currentLine = current.trimmed().substring(0, 2); // Only takes the first two characters, which may not be "---"
                 if ("---".equals(currentLine)) {
                     docsStart.add(current);
                 }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed().substring(0, 2); // Only takes the first two characters, which may not be "---"
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 15 =====
```
             }
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
-                final String currentLine = current.trimmed();
+                final String currentLine = null; // Sets currentLine to null, which will cause a NullPointerException on comparison
                 if ("---".equals(currentLine)) {
                     docsStart.add(current);
                 }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = null; // Sets currentLine to null, which will cause a NullPointerException on comparison
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 16 =====
```
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
-                if ("---".equals(currentLine)) {
+                if (!"---".equals(currentLine)) {
                     docsStart.add(current);
                 }
             }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if (!"---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 17 =====
```
             while (iterator.hasNext()) {
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
-                if ("---".equals(currentLine)) {
+                if (currentLine.length() > 3 && currentLine.substring(0, 3).equals("---")) {
                     docsStart.add(current);
                 }
             }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if (currentLine.length() > 3 && currentLine.substring(0, 3).equals("---")) {
                    docsStart.add(current);
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 18 =====
```
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
                 if ("---".equals(currentLine)) {
-                    docsStart.add(current);
+                    
                 }
             }
             iterator = docsStart.iterator();
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 19 =====
```
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
                 if ("---".equals(currentLine)) {
-                    docsStart.add(current);
+                    docsStart.add(first); // Always adds the first line again instead of the current line
                 }
             }
             iterator = docsStart.iterator();
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(first); // Always adds the first line again instead of the current line
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 20 =====
```
                 final YamlLine current = iterator.next();
                 final String currentLine = current.trimmed();
                 if ("---".equals(currentLine)) {
-                    docsStart.add(current);
+                    docsStart.add(new YamlLine.NullYamlLine());
                 }
             }
             iterator = docsStart.iterator();
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(new YamlLine.NullYamlLine());
                }
            }
            iterator = docsStart.iterator();
        }
        return iterator;
    }
```
===== 22 =====
```
                     docsStart.add(current);
                 }
             }
-            iterator = docsStart.iterator();
+            iterator = this.yamlLines.iterator(); // Returning the original iterator instead of the filtered one
         }
         return iterator;
     }
```
```
    /**
     * Returns an iterator containing only the Start Marker lines (---),
     * with the possible exception of the FIRST line, which can also be
     * the NullYamlLine (in YAML Streams, the Start Marker
     * of the first document can be missing). e.g. Both are valid:
     * <pre>
     * ---
     * test: 1
     * ---
     * test 2
     * </pre>
     * and
     * <pre>
     * test: 1
     * ---
     * test: 2
     * </pre>
     * @return Iterator over these yaml lines.
     */
    @Override
    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = new ArrayList<>();
            final YamlLine first = iterator.next();
            if("---".equals(first.trimmed())) {
                docsStart.add(first);
            } else {
                docsStart.add(new YamlLine.NullYamlLine());
            }
            while (iterator.hasNext()) {
                final YamlLine current = iterator.next();
                final String currentLine = current.trimmed();
                if ("---".equals(currentLine)) {
                    docsStart.add(current);
                }
            }
            iterator = this.yamlLines.iterator(); // Returning the original iterator instead of the filtered one
        }
        return iterator;
    }
```
