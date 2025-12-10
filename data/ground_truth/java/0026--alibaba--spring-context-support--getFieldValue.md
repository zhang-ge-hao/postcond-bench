https://github.com/alibaba/spring-context-support/blob/184df1c8cd0b4c11e0c582039eddb308e8ef1761/./src/main/java/com/alibaba/spring/util/FieldUtils.java#L47-L86
```
//@ ensures fieldType != null && java.util.Arrays.stream(object.getClass().getDeclaredFields()).anyMatch(f -> f.getName().equals(fieldName) && f.getType().equals(fieldType)) ==> (fieldType.isPrimitive() ? \result != null : fieldType.isInstance(\result));
//@ ensures fieldType != null && !java.util.Arrays.stream(object.getClass().getDeclaredFields()).anyMatch(f -> f.getName().equals(fieldName) && f.getType().equals(fieldType)) ==> \result == null
//@ ensures object != null && ReflectionUtils.findField(object.getClass(), fieldName, fieldType) == null ==> \result == null;
//@ ensures object != null && ReflectionUtils.findField(object.getClass(), fieldName, fieldType) != null ==> java.util.stream.Stream.of(ReflectionUtils.findField(object.getClass(), fieldName, fieldType)).peek(f -> ReflectionUtils.makeAccessible(f)).allMatch(f -> java.util.Objects.equals(\result, (T)ReflectionUtils.getField(f, object)));
```
```
//@ ensures fieldType != null && java.util.Arrays.stream(object.getClass().getDeclaredFields()).anyMatch(f -> f.getName().equals(fieldName) && f.getType().equals(fieldType)) ==> (fieldType.isPrimitive() ? \result != null : fieldType.isInstance(\result));
//@ ensures fieldType != null && !java.util.Arrays.stream(object.getClass().getDeclaredFields()).anyMatch(f -> f.getName().equals(fieldName) && f.getType().equals(fieldType)) ==> \result == null
```
[2]
===== 2 =====
```
 
         T fieldValue = null;
 
-        Field field = ReflectionUtils.findField(object.getClass(), fieldName, fieldType);
+        Field field = ReflectionUtils.findField(object.getClass(), fieldName, int.class);
 
         if (field != null) {
```
```
    /**
     * Get {@link Field} Value
     *
     * @param object    {@link Object}
     * @param fieldName field name
     * @param fieldType field type
     * @param <T>       field type
     * @return {@link Field} Value
     */
    public static <T> T getFieldValue(Object object, String fieldName, Class<T> fieldType) {

        T fieldValue = null;

        Field field = ReflectionUtils.findField(object.getClass(), fieldName, int.class);

        if (field != null) {

            boolean accessible = field.isAccessible();

            try {

                if (!accessible) {
                    ReflectionUtils.makeAccessible(field);
                }

                fieldValue = (T) ReflectionUtils.getField(field, object);

            } finally {

                if (!accessible) {
                    field.setAccessible(accessible);
                }

            }

        }

        return fieldValue;

    }
```
