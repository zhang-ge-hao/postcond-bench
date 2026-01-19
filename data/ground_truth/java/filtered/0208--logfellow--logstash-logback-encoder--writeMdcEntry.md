https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/composite/loggingevent/MdcJsonProvider.java#L176-L196
```
🈚️

No api.
JsonGenerator only provides APIs for writing JSON and querying limited output context (such as getOutputContext()), but it does not expose its underlying output target (OutputStream / Writer, etc.) or the actual JSON content that has been written. As a result, JML postconditions cannot access “where the JSON was written to” or “what was actually written,” and can only express indirect, structural constraints based on the generator’s context—for example, checking that the current field name matches the expected one—rather than precisely verifying, from the final JSON output itself, that writeMdcEntry wrote the correct values or overall structure.

//@ ensures generator == \old(generator);
//@ ensures fieldName == \old(fieldName);
//@ ensures mdcKey == \old(mdcKey);
//@ ensures mdcValue == \old(mdcValue);
//@ ensures mdcEntryWriters != null;
//@ ensures includeMdcKeyNames != null;
//@ ensures excludeMdcKeyNames != null;
//@ ensures mdcKeyFieldNames != null;
//@ ensures mdcEntryWriters.size() == \old(mdcEntryWriters.size());
//@ ensures includeMdcKeyNames.size() == \old(includeMdcKeyNames.size());
//@ ensures excludeMdcKeyNames.size() == \old(excludeMdcKeyNames.size());
//@ ensures mdcKeyFieldNames.size() == \old(mdcKeyFieldNames.size());
//@ ensures mdcEntryWriters.isEmpty() && generator.getOutputContext() != null && generator.getOutputContext().hasCurrentName() ==> generator.getOutputContext().getCurrentName().equals(fieldName);
```
```
//@ ensures this.mdcEntryWriters.size() == \old(this.mdcEntryWriters.size());
//@ ensures this.includeMdcKeyNames.equals(\old(this.includeMdcKeyNames));
//@ ensures this.excludeMdcKeyNames.equals(\old(this.excludeMdcKeyNames));
//@ ensures this.mdcKeyFieldNames.equals(\old(this.mdcKeyFieldNames));
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
===== 0 =====
```
      * @param mdcValue  the value of the MDC map entry.
      */
     private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
-        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
+        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) { if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) break;
             if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                 return;
             }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) { if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) break;
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeObject(mdcValue);
    }
```
===== 1 =====
```
      * @param mdcValue  the value of the MDC map entry.
      */
     private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
-        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
+        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) { if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) { continue; }
             if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                 return;
             }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) { if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) { continue; }
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeObject(mdcValue);
    }
```
===== 2 =====
```
      */
     private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
         for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
-            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
+            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue) != true) {
                 return;
             }
         }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue) != true) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeObject(mdcValue);
    }
```
===== 3 =====
```
      */
     private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
         for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
-            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
+            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue) == false) {
                 return;
             }
         }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue) == false) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeObject(mdcValue);
    }
```
===== 4 =====
```
             }
         }
 
-        generator.writeFieldName(fieldName);
+        generator.writeFieldName(""); // Writing an empty field name
         generator.writeObject(mdcValue);
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(""); // Writing an empty field name
        generator.writeObject(mdcValue);
    }
```
===== 5 =====
```
             }
         }
 
-        generator.writeFieldName(fieldName);
+        generator.writeFieldName("defaultFieldName"); // Using a hardcoded field name
         generator.writeObject(mdcValue);
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName("defaultFieldName"); // Using a hardcoded field name
        generator.writeObject(mdcValue);
    }
```
===== 6 =====
```
             }
         }
 
-        generator.writeFieldName(fieldName);
+        generator.writeFieldName(fieldName.toUpperCase()); // Changing the case of the field name
         generator.writeObject(mdcValue);
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(fieldName.toUpperCase()); // Changing the case of the field name
        generator.writeObject(mdcValue);
    }
```
===== 7 =====
```
             }
         }
 
-        generator.writeFieldName(fieldName);
+        generator.writeFieldName(mdcKey);
         generator.writeObject(mdcValue);
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(mdcKey);
        generator.writeObject(mdcValue);
    }
```
===== 8 =====
```
         }
 
         generator.writeFieldName(fieldName);
-        generator.writeObject(mdcValue);
+        generator.writeNull();
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeNull();
    }
```
===== 9 =====
```
         }
 
         generator.writeFieldName(fieldName);
-        generator.writeObject(mdcValue);
+        generator.writeStartObject();
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeStartObject();
    }
```
===== 10 =====
```
         }
 
         generator.writeFieldName(fieldName);
-        generator.writeObject(mdcValue);
+        generator.writeString(mdcValue);
     }
```
```
    /**
     * Writes the MDC entry with the given generator by iterating over the chain of {@link #mdcEntryWriters}
     * in the given order till the first {@link MdcEntryWriter} returns true.
     * <p>
     * If none of the {@link #mdcEntryWriters} returned true, the MDC field is written as String value by default.
     *
     * @param generator the generator to write the entry to.
     * @param fieldName the field name to use when writing the entry.
     * @param mdcKey    the key of the MDC map entry.
     * @param mdcValue  the value of the MDC map entry.
     */
    private void writeMdcEntry(JsonGenerator generator, String fieldName, String mdcKey, String mdcValue) throws IOException {
        for (MdcEntryWriter mdcEntryWriter : this.mdcEntryWriters) {
            if (mdcEntryWriter.writeMdcEntry(generator, fieldName, mdcKey, mdcValue)) {
                return;
            }
        }

        generator.writeFieldName(fieldName);
        generator.writeString(mdcValue);
    }
```
