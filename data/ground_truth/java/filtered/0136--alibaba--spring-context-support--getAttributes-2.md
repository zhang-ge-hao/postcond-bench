https://github.com/alibaba/spring-context-support/blob/184df1c8cd0b4c11e0c582039eddb308e8ef1761/./src/main/java/com/alibaba/spring/util/AnnotationUtils.java#L232-L274
```
🈚️

originally wrong. `String... ignoreAttributeNames`

//@ ensures \result != null;
//@ ensures ignoreAttributeNames == null || java.util.Arrays.stream(ignoreAttributeNames).noneMatch(n -> \result.containsKey(n));
//@ ensures !ignoreDefaultValue || org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap).entrySet().stream().noneMatch(e -> org.springframework.util.ObjectUtils.nullSafeEquals(e.getValue(), getDefaultValue(annotation, (String)e.getKey()))) || \result.size() < org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap).size();
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
===== 0 =====
```
 
         String[] actualIgnoreAttributeNames = ignoreAttributeNames;
 
-        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {
+        if (!ignoreDefaultValue && isEmpty(annotationAttributes)) {
 
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (!ignoreDefaultValue && isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 1 =====
```
 
         String[] actualIgnoreAttributeNames = ignoreAttributeNames;
 
-        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {
+        if (!ignoreDefaultValue || !isEmpty(annotationAttributes)) {
 
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (!ignoreDefaultValue || !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 2 =====
```
 
         String[] actualIgnoreAttributeNames = ignoreAttributeNames;
 
-        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {
+        if (ignoreDefaultValue && isEmpty(annotationAttributes)) {
 
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 3 =====
```
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
-                String attributeName = annotationAttribute.getKey();
+                String attributeName = "default"; // Assigning a constant string instead of the key
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = "default"; // Assigning a constant string instead of the key
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 4 =====
```
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
-                String attributeName = annotationAttribute.getKey();
+                String attributeName = annotationAttribute.getKey() + "_suffix"; // Appending a suffix to the key
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey() + "_suffix"; // Appending a suffix to the key
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 5 =====
```
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
-                String attributeName = annotationAttribute.getKey();
+                String attributeName = annotationAttribute.getKey().toUpperCase(); // Modifying the key to uppercase
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey().toUpperCase(); // Modifying the key to uppercase
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 6 =====
```
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
-                String attributeName = annotationAttribute.getKey();
+                String attributeName = annotationAttribute.getValue().toString(); // Using value instead of key
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getValue().toString(); // Using value instead of key
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 7 =====
```
             List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
-                String attributeName = annotationAttribute.getKey();
+                String attributeName = null; // Assigning null instead of the key
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = null; // Assigning null instead of the key
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 8 =====
```
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
-                Object attributeValue = annotationAttribute.getValue();
+                Object attributeValue = annotationAttribute.getKey(); // This incorrectly assigns the key instead of the value.
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
                 }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getKey(); // This incorrectly assigns the key instead of the value.
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 9 =====
```
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
-                Object attributeValue = annotationAttribute.getValue();
+                Object attributeValue = annotationAttribute.getValue() instanceof String ? null : annotationAttribute.getValue(); // This will set attributeValue to null for String types, causing them to be ignored.
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
                 }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue() instanceof String ? null : annotationAttribute.getValue(); // This will set attributeValue to null for String types, causing them to be ignored.
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 10 =====
```
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
-                Object attributeValue = annotationAttribute.getValue();
+                Object attributeValue = annotationAttribute.getValue().toString(); // This converts the value to a String, potentially losing type information.
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
                 }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue().toString(); // This converts the value to a String, potentially losing type information.
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 11 =====
```
 
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
-                Object attributeValue = annotationAttribute.getValue();
+                Object attributeValue = null; // This will cause all attributes to be ignored.
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                     attributeNamesToIgnore.add(attributeName);
                 }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = null; // This will cause all attributes to be ignored.
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 12 =====
```
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
-                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
+                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, "nonExistentAttribute"))) {
                     attributeNamesToIgnore.add(attributeName);
                 }
             }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, "nonExistentAttribute"))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 13 =====
```
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
-                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
+                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName + "Suffix"))) {
                     attributeNamesToIgnore.add(attributeName);
                 }
             }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName + "Suffix"))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 14 =====
```
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
-                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
+                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName) + "ExtraValue")) {
                     attributeNamesToIgnore.add(attributeName);
                 }
             }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName) + "ExtraValue")) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 15 =====
```
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
-                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
+                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName).toString())) {
                     attributeNamesToIgnore.add(attributeName);
                 }
             }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName).toString())) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 16 =====
```
             for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
-                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
+                if (nullSafeEquals(attributeValue, null)) {
                     attributeNamesToIgnore.add(attributeName);
                 }
             }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, null)) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 17 =====
```
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
-                    attributeNamesToIgnore.add(attributeName);
+                    
                 }
             }
             // extends the ignored list
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 18 =====
```
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
-                    attributeNamesToIgnore.add(attributeName);
+                    attributeNamesToIgnore.add(attributeName + "_ignored");
                 }
             }
             // extends the ignored list
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName + "_ignored");
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 19 =====
```
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
-                    attributeNamesToIgnore.add(attributeName);
+                    attributeNamesToIgnore.add(attributeName.toUpperCase());
                 }
             }
             // extends the ignored list
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName.toUpperCase());
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 20 =====
```
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
-                    attributeNamesToIgnore.add(attributeName);
+                    attributeNamesToIgnore.clear();
                 }
             }
             // extends the ignored list
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.clear();
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 21 =====
```
                 String attributeName = annotationAttribute.getKey();
                 Object attributeValue = annotationAttribute.getValue();
                 if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
-                    attributeNamesToIgnore.add(attributeName);
+                    attributeNamesToIgnore.remove(attributeName);
                 }
             }
             // extends the ignored list
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.remove(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
    }
```
===== 22 =====
```
             actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
         }
 
-        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
+        return getAttributes(annotationAttributes, null, actualIgnoreAttributeNames);
     }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, null, actualIgnoreAttributeNames);
    }
```
===== 23 =====
```
             actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
         }
 
-        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
+        return getAttributes(annotationAttributes, propertyResolver, ignoreAttributeNames);
     }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, ignoreAttributeNames);
    }
```
===== 24 =====
```
             actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
         }
 
-        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
+        return getAttributes(annotationAttributes, propertyResolver, new String[0]);
     }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, new String[0]);
    }
```
===== 25 =====
```
             actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
         }
 
-        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
+        return getAttributes(annotationAttributes, propertyResolver, null);
     }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return getAttributes(annotationAttributes, propertyResolver, null);
    }
```
===== 26 =====
```
             actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
         }
 
-        return getAttributes(annotationAttributes, propertyResolver, actualIgnoreAttributeNames);
+        return null;
     }
```
```
    /**
     * @param annotation             specified {@link Annotation}
     * @param propertyResolver       {@link PropertyResolver} instance, e.g {@link Environment}
     * @param classValuesAsString    whether to turn Class references into Strings (for
     *                               compatibility with {@link org.springframework.core.type.AnnotationMetadata} or to
     *                               preserve them as Class references
     * @param nestedAnnotationsAsMap whether to turn nested Annotation instances into
     *                               {@link AnnotationAttributes} maps (for compatibility with
     *                               {@link org.springframework.core.type.AnnotationMetadata} or to preserve them as
     *                               Annotation instances
     * @param ignoreDefaultValue     whether ignore default value or not
     * @param ignoreAttributeNames   the attribute names of annotation should be ignored
     * @return
     * @since 1.0.11
     */
    public static Map<String, Object> getAttributes(Annotation annotation,
                                                    PropertyResolver propertyResolver,
                                                    boolean classValuesAsString,
                                                    boolean nestedAnnotationsAsMap,
                                                    boolean ignoreDefaultValue,
                                                    String... ignoreAttributeNames) {

        Map<String, Object> annotationAttributes = org.springframework.core.annotation.AnnotationUtils.getAnnotationAttributes(annotation, classValuesAsString, nestedAnnotationsAsMap);

        String[] actualIgnoreAttributeNames = ignoreAttributeNames;

        if (ignoreDefaultValue && !isEmpty(annotationAttributes)) {

            List<String> attributeNamesToIgnore = new LinkedList<String>(asList(ignoreAttributeNames));

            for (Map.Entry<String, Object> annotationAttribute : annotationAttributes.entrySet()) {
                String attributeName = annotationAttribute.getKey();
                Object attributeValue = annotationAttribute.getValue();
                if (nullSafeEquals(attributeValue, getDefaultValue(annotation, attributeName))) {
                    attributeNamesToIgnore.add(attributeName);
                }
            }
            // extends the ignored list
            actualIgnoreAttributeNames = attributeNamesToIgnore.toArray(new String[attributeNamesToIgnore.size()]);
        }

        return null;
    }
```
