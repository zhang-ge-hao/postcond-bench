https://github.com/restfb/restfb/blob/9a98b76187b276a824fcd9109da988c2cc7c970a/./src/main/java/com/restfb/util/ReflectionUtils.java#L104-L146
```
🈚️

It's hard.

//@ ensures \result != null;
//@ ensures \old(FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType))) != null ==> \result == \old(FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType)));
//@ ensures \old(FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType))) == null ==> FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(\old(type), annotationType)) == \result;
//@ ensures java.util.stream.IntStream.range(0, \result.size()).allMatch(i -> \result.get(i) != null && \result.get(i).getField() != null && \result.get(i).getAnnotation() != null);
//@ ensures java.util.stream.IntStream.range(0, \result.size()).allMatch(i -> \result.get(i).getField().getAnnotation(annotationType) == \result.get(i).getAnnotation());
//@ ensures \result != null && \old(type) != null && annotationType != null && \old(type) != java.lang.Object.class ==> java.util.Arrays.stream(\old(type).getDeclaredFields()).filter(f -> f.getAnnotation(annotationType) != null).allMatch(f -> \result.stream().anyMatch(fwa -> fwa.getField() == f && fwa.getAnnotation() == f.getAnnotation(annotationType)));
//@ ensures \result != null && \old(type) != null && annotationType != null && \old(type).getSuperclass() != null && \old(type).getSuperclass() != java.lang.Object.class ==> java.util.Arrays.stream(\old(type).getSuperclass().getDeclaredFields()).filter(f -> f.getAnnotation(annotationType) != null).allMatch(f -> \result.stream().anyMatch(fwa -> fwa.getField() == f && fwa.getAnnotation() == f.getAnnotation(annotationType)));
//@ ensures \result != null && \old(type) != null && annotationType != null && \old(type).getSuperclass() != null && \old(type).getSuperclass().getSuperclass() != null && \old(type).getSuperclass().getSuperclass() != java.lang.Object.class ==> java.util.Arrays.stream(\old(type).getSuperclass().getSuperclass().getDeclaredFields()).filter(f -> f.getAnnotation(annotationType) != null).allMatch(f -> \result.stream().anyMatch(fwa -> fwa.getField() == f && fwa.getAnnotation() == f.getAnnotation(annotationType)));
//@ ensures \result != null && \old(type) != null && annotationType != null && \old(type).getSuperclass() != null && \old(type).getSuperclass().getSuperclass() != null && \old(type).getSuperclass().getSuperclass().getSuperclass() != null && \old(type).getSuperclass().getSuperclass().getSuperclass() != java.lang.Object.class ==> java.util.Arrays.stream(\old(type).getSuperclass().getSuperclass().getSuperclass().getDeclaredFields()).filter(f -> f.getAnnotation(annotationType) != null).allMatch(f -> \result.stream().anyMatch(fwa -> fwa.getField() == f && fwa.getAnnotation() == f.getAnnotation(annotationType)));
```
```
//@ ensures \result != null;
//@ ensures \old(FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType))) != null ==> \result == \old(FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType)));
//@ ensures \old(FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType))) == null ==> FIELDS_WITH_ANNOTATION_CACHE.get(new ClassAnnotationCacheKey(type, annotationType)) == \result;
//@ ensures java.util.stream.IntStream.range(0, \result.size()).allMatch(i -> \result.get(i) != null && \result.get(i).getField() != null && \result.get(i).getAnnotation() != null);
//@ ensures java.util.stream.IntStream.range(0, \result.size()).allMatch(i -> \result.get(i).getField().getAnnotation(annotationType) == \result.get(i).getAnnotation());
```
[3, 4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17]
===== 3 =====
```
     List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();
 
     // Walk all superclasses looking for annotated fields until we hit Object
-    while (!Object.class.equals(type) && type != null) {
+    while (!Object.class.equals(type) && type == null) {
       for (Field field : type.getDeclaredFields()) {
         T annotation = field.getAnnotation(annotationType);
         if (annotation != null) {
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type == null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 4 =====
```
     List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();
 
     // Walk all superclasses looking for annotated fields until we hit Object
-    while (!Object.class.equals(type) && type != null) {
+    while (type != null && !Object.class.equals(type) && type.getDeclaredFields().length > 0) {
       for (Field field : type.getDeclaredFields()) {
         T annotation = field.getAnnotation(annotationType);
         if (annotation != null) {
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (type != null && !Object.class.equals(type) && type.getDeclaredFields().length > 0) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 5 =====
```
     List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();
 
     // Walk all superclasses looking for annotated fields until we hit Object
-    while (!Object.class.equals(type) && type != null) {
+    while (type != null && !Object.class.equals(type.getSuperclass())) {
       for (Field field : type.getDeclaredFields()) {
         T annotation = field.getAnnotation(annotationType);
         if (annotation != null) {
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (type != null && !Object.class.equals(type.getSuperclass())) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 6 =====
```
     // Walk all superclasses looking for annotated fields until we hit Object
     while (!Object.class.equals(type) && type != null) {
       for (Field field : type.getDeclaredFields()) {
-        T annotation = field.getAnnotation(annotationType);
+        T annotation = null; // Always assigns null, causing no annotations to be found.
         if (annotation != null) {
           fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
         }
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = null; // Always assigns null, causing no annotations to be found.
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 8 =====
```
     while (!Object.class.equals(type) && type != null) {
       for (Field field : type.getDeclaredFields()) {
         T annotation = field.getAnnotation(annotationType);
-        if (annotation != null) {
+        if (field.getType() == Object.class) {
           fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
         }
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (field.getType() == Object.class) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 9 =====
```
       for (Field field : type.getDeclaredFields()) {
         T annotation = field.getAnnotation(annotationType);
         if (annotation != null) {
-          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
+          
         }
 
       }
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 12 =====
```
 
       }
 
-      type = type.getSuperclass();
+      type = Object.class; // This will cause the loop to always check against Object, missing other superclasses.
     }
 
     fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = Object.class; // This will cause the loop to always check against Object, missing other superclasses.
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 13 =====
```
 
       }
 
-      type = type.getSuperclass();
+      type = null; // This will cause the loop to terminate prematurely.
     }
 
     fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = null; // This will cause the loop to terminate prematurely.
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 14 =====
```
 
       }
 
-      type = type.getSuperclass();
+      type = type.getSuperclass().getSuperclass(); // This will skip one level of the superclass hierarchy, potentially missing annotated fields.
     }
 
     fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass().getSuperclass(); // This will skip one level of the superclass hierarchy, potentially missing annotated fields.
    }

    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 15 =====
```
       type = type.getSuperclass();
     }
 
-    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
+    fieldsWithAnnotation = Collections.emptyList(); // Replaces the list with an empty immutable list, losing all found fields
     FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
     return fieldsWithAnnotation;
   }
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = Collections.emptyList(); // Replaces the list with an empty immutable list, losing all found fields
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 16 =====
```
       type = type.getSuperclass();
     }
 
-    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
+    fieldsWithAnnotation = new ArrayList<>(); // Resets the list to an empty list, losing all found fields
     FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
     return fieldsWithAnnotation;
   }
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = new ArrayList<>(); // Resets the list to an empty list, losing all found fields
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
===== 17 =====
```
       type = type.getSuperclass();
     }
 
-    fieldsWithAnnotation = unmodifiableList(fieldsWithAnnotation);
+    fieldsWithAnnotation = new ArrayList<>(fieldsWithAnnotation.size()); // Creates an empty list with the same size, but no elements
     FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
     return fieldsWithAnnotation;
   }
```
```
  /**
   * Finds fields on the given {@code type} and all of its superclasses annotated with annotations of type
   * {@code annotationType}.
   * 
   * @param <T>
   *          The annotation type.
   * @param type
   *          The target type token.
   * @param annotationType
   *          The annotation type token.
   * @return A list of field/annotation pairs.
   */
  public static <T extends Annotation> List<FieldWithAnnotation<T>> findFieldsWithAnnotation(Class<?> type,
      Class<T> annotationType) {
    ClassAnnotationCacheKey cacheKey = new ClassAnnotationCacheKey(type, annotationType);

    @SuppressWarnings("unchecked")
    List<FieldWithAnnotation<T>> cachedResults =
        (List<FieldWithAnnotation<T>>) FIELDS_WITH_ANNOTATION_CACHE.get(cacheKey);

    if (cachedResults != null) {
      return cachedResults;
    }

    List<FieldWithAnnotation<T>> fieldsWithAnnotation = new ArrayList<>();

    // Walk all superclasses looking for annotated fields until we hit Object
    while (!Object.class.equals(type) && type != null) {
      for (Field field : type.getDeclaredFields()) {
        T annotation = field.getAnnotation(annotationType);
        if (annotation != null) {
          fieldsWithAnnotation.add(new FieldWithAnnotation<>(field, annotation));
        }

      }

      type = type.getSuperclass();
    }

    fieldsWithAnnotation = new ArrayList<>(fieldsWithAnnotation.size()); // Creates an empty list with the same size, but no elements
    FIELDS_WITH_ANNOTATION_CACHE.put(cacheKey, fieldsWithAnnotation);
    return fieldsWithAnnotation;
  }
```
