https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/org/objectweb/asm/SymbolTable.java#L843-L866
```
//@ ensures \result != null;
//@ ensures \result.tag == tag;
//@ ensures (value == null) ==> (\result.value == null);
//@ ensures (value != null) ==> (\result.value != null && \result.value.equals(value));
//@ ensures \result.owner == null && \result.name == null;
//@ ensures \result.index >= 1 && \result.index < constantPoolCount;
//@ ensures constantPoolCount >= \old(constantPoolCount) && constantPoolCount <= \old(constantPoolCount) + 2;
//@ ensures entryCount >= \old(entryCount) && entryCount <= \old(entryCount) + 2;
//@ ensures constantPoolCount - \old(constantPoolCount) == entryCount - \old(entryCount);
//@ ensures constantPool.length >= \old(constantPool.length);
//@ ensures constantPool.length - \old(constantPool.length) >= 3 * (constantPoolCount - \old(constantPoolCount));
//@ ensures value != null && entryCount - \old(entryCount) == 2 ==> java.util.Arrays.stream(entries).anyMatch(e -> e != null && e.tag == Symbol.CONSTANT_UTF8_TAG && e.value != null && e.value.equals(value));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
     Entry entry = get(hashCode);
     while (entry != null) {
       if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
-        return entry;
+        return null;
       }
       entry = entry.next;
     }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return null;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value));
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 1 =====
```
       }
       entry = entry.next;
     }
-    constantPool.put12(tag, addConstantUtf8(value));
+    
     return put(new Entry(constantPoolCount++, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 2 =====
```
       }
       entry = entry.next;
     }
-    constantPool.put12(tag, addConstantUtf8(value));
+    constantPool.put12(tag, addConstantUtf8(value + " " + value)); // Duplicates the value with a space, leading to incorrect entries.
     return put(new Entry(constantPoolCount++, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value + " " + value)); // Duplicates the value with a space, leading to incorrect entries.
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 3 =====
```
       }
       entry = entry.next;
     }
-    constantPool.put12(tag, addConstantUtf8(value));
+    constantPool.put12(tag, addConstantUtf8(value + "extra")); // Adds "extra" to the value, changing its meaning.
     return put(new Entry(constantPoolCount++, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value + "extra")); // Adds "extra" to the value, changing its meaning.
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 4 =====
```
       }
       entry = entry.next;
     }
-    constantPool.put12(tag, addConstantUtf8(value));
+    constantPool.put12(tag, addConstantUtf8(value.replace("a", "b"))); // Replaces 'a' with 'b' in the value, changing its content.
     return put(new Entry(constantPoolCount++, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value.replace("a", "b"))); // Replaces 'a' with 'b' in the value, changing its content.
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 5 =====
```
       }
       entry = entry.next;
     }
-    constantPool.put12(tag, addConstantUtf8(value));
+    constantPool.put12(tag, addConstantUtf8(value.substring(1))); // Removes the first character of the value, which may lead to incorrect references.
     return put(new Entry(constantPoolCount++, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value.substring(1))); // Removes the first character of the value, which may lead to incorrect references.
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 6 =====
```
       }
       entry = entry.next;
     }
-    constantPool.put12(tag, addConstantUtf8(value));
+    constantPool.put12(tag, addConstantUtf8(value.toUpperCase())); // Converts the value to uppercase, potentially altering its intended use.
     return put(new Entry(constantPoolCount++, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value.toUpperCase())); // Converts the value to uppercase, potentially altering its intended use.
    return put(new Entry(constantPoolCount++, tag, value, hashCode));
  }
```
===== 7 =====
```
       entry = entry.next;
     }
     constantPool.put12(tag, addConstantUtf8(value));
-    return put(new Entry(constantPoolCount++, tag, value, hashCode));
+    return null;
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value));
    return null;
  }
```
===== 8 =====
```
       entry = entry.next;
     }
     constantPool.put12(tag, addConstantUtf8(value));
-    return put(new Entry(constantPoolCount++, tag, value, hashCode));
+    return put(new Entry(constantPoolCount++, tag, value.toUpperCase(), hashCode)); // value is modified to uppercase
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value));
    return put(new Entry(constantPoolCount++, tag, value.toUpperCase(), hashCode)); // value is modified to uppercase
  }
```
===== 9 =====
```
       entry = entry.next;
     }
     constantPool.put12(tag, addConstantUtf8(value));
-    return put(new Entry(constantPoolCount++, tag, value, hashCode));
+    return put(new Entry(constantPoolCount--, tag, value, hashCode));
   }
```
```
  /**
   * Adds a CONSTANT_Class_info, CONSTANT_String_info, CONSTANT_MethodType_info,
   * CONSTANT_Module_info or CONSTANT_Package_info to the constant pool of this symbol table. Does
   * nothing if the constant pool already contains a similar item.
   *
   * @param tag one of {@link Symbol#CONSTANT_CLASS_TAG}, {@link Symbol#CONSTANT_STRING_TAG}, {@link
   *     Symbol#CONSTANT_METHOD_TYPE_TAG}, {@link Symbol#CONSTANT_MODULE_TAG} or {@link
   *     Symbol#CONSTANT_PACKAGE_TAG}.
   * @param value an internal class name, an arbitrary string, a method descriptor, a module or a
   *     package name, depending on tag.
   * @return a new or already existing Symbol with the given value.
   */
  private Symbol addConstantUtf8Reference(final int tag, final String value) {
    int hashCode = hash(tag, value);
    Entry entry = get(hashCode);
    while (entry != null) {
      if (entry.tag == tag && entry.hashCode == hashCode && entry.value.equals(value)) {
        return entry;
      }
      entry = entry.next;
    }
    constantPool.put12(tag, addConstantUtf8(value));
    return put(new Entry(constantPoolCount--, tag, value, hashCode));
  }
```
