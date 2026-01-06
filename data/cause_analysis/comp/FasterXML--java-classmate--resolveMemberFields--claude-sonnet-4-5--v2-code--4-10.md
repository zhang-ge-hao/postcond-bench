https://github.com/FasterXML/java-classmate/blob/f9841eaf0a30f8b29c0b405c16219585480a58a6/./src/main/java/com/fasterxml/classmate/ResolvedTypeWithMembers.java#L264-L309
```
//@ ensures \result != null;
//@ ensures \result.length >= 0;
//@ ensures (\result.length == 0) ==> (\result == NO_RESOLVED_FIELDS);
//@ ensures (\result.length > 0) ==> (\result != NO_RESOLVED_FIELDS);
//@ ensures java.util.Arrays.stream(\result).allMatch(f -> f != null);
//@ ensures java.util.Arrays.stream(\result).allMatch(f -> f instanceof ResolvedField);
```
```
return value - inner repository type


return value content

repository defined type
```
passed
```
//@ ensures (java.util.Arrays.stream(\old(_types)).filter(t -> !t.isMixin()).flatMap(t -> t.getType().getMemberFields().stream()).filter(f -> (\old(_fieldFilter) == null) || \old(_fieldFilter).include(f)).findAny().isPresent()) <==> (\result != NO_RESOLVED_FIELDS);
//@ ensures \result.length == java.util.Arrays.stream(\old(_types)).filter(t -> !t.isMixin()).flatMap(t -> t.getType().getMemberFields().stream()).filter(f -> (\old(_fieldFilter) == null) || \old(_fieldFilter).include(f)).map(f -> f.getName()).collect(java.util.stream.Collectors.toSet()).size();
//@ ensures java.util.Arrays.stream(\result).allMatch(r -> r != null && r.getRawMember() != null);
//@ ensures java.util.Arrays.stream(\result).map(r -> r.getName()).collect(java.util.stream.Collectors.toSet()).equals(java.util.Arrays.stream(\old(_types)).filter(t -> !t.isMixin()).flatMap(t -> t.getType().getMemberFields().stream()).filter(f -> (\old(_fieldFilter) == null) || \old(_fieldFilter).include(f)).map(f -> f.getName()).collect(java.util.stream.Collectors.toSet()));
//@ ensures java.util.Arrays.stream(\result).map(r -> r.getName()).collect(java.util.stream.Collectors.toSet()).size() == \result.length;
//@ ensures java.util.Arrays.stream(\old(_types)).filter(t -> t.isMixin()).flatMap(t -> t.getType().getMemberFields().stream()).filter(raw -> (\old(_fieldFilter) == null) || \old(_fieldFilter).include(raw)).allMatch(raw -> java.util.Arrays.stream(raw.getAnnotations()).filter(ann -> \old(_annotationHandler).includeMethodAnnotation(ann)).allMatch(ann -> java.util.Arrays.stream(\result).anyMatch(r -> r.getName().equals(raw.getName()) && r.get(ann.annotationType()) != null)));
//@ ensures java.util.Arrays.stream(\old(_types)).filter(t -> t.isMixin()).flatMap(t -> t.getType().getMemberFields().stream()).filter(raw -> (\old(_fieldFilter) == null) || \old(_fieldFilter).include(raw)).allMatch(raw -> java.util.Arrays.stream(raw.getAnnotations()).filter(ann -> !\old(_annotationHandler).includeMethodAnnotation(ann)).allMatch(ann -> java.util.Arrays.stream(\result).noneMatch(r -> r.getName().equals(raw.getName()) && r.get(ann.annotationType()) != null)));
```
===== 10: failed =====
```
                     if ((_fieldFilter != null) && !_fieldFilter.include(raw)) {
                         continue;
                     }
-                    ResolvedField field = fields.get(raw.getName());
+                    ResolvedField field = null; // This will cause a NullPointerException later when trying to apply overrides.
                     if (field != null) {
                         for (Annotation ann : raw.getAnnotations()) {
                             if (_annotationHandler.includeMethodAnnotation(ann)) {
```
```
    /**
     * Method for fully resolving field definitions and associated annotations.
     * Neither field definitions nor associated annotations inherit, but we may
     * still need to add annotation overrides, as well as filter out filters
     * and annotations that caller is not interested in.
     */
    protected ResolvedField[] resolveMemberFields()
    {
        LinkedHashMap<String, ResolvedField> fields = new LinkedHashMap<String, ResolvedField>();

        /* Fields need different handling: must start from bottom; and annotations only get added
         * as overrides, never as defaults. And sub-classes fully mask fields. This makes
         * handling bit simpler than that of member methods.
         */
        for (int typeIndex = _types.length; --typeIndex >= 0; ) {
            HierarchicType thisType = _types[typeIndex];
            // If it's just a mix-in, add annotations as overrides
            if (thisType.isMixin()) {
                for (RawField raw : thisType.getType().getMemberFields()) {
                    if ((_fieldFilter != null) && !_fieldFilter.include(raw)) {
                        continue;
                    }
                    ResolvedField field = null; // This will cause a NullPointerException later when trying to apply overrides.
                    if (field != null) {
                        for (Annotation ann : raw.getAnnotations()) {
                            if (_annotationHandler.includeMethodAnnotation(ann)) {
                                field.applyOverride(ann);
                            }
                        }
                    }
                }
            } else { // If actual type, add fields, masking whatever might have existed before:
                for (RawField field : thisType.getType().getMemberFields()) {
                    if ((_fieldFilter != null) && !_fieldFilter.include(field)) {
                        continue;
                    }
                    fields.put(field.getName(), resolveField(field));
                }
            }
        }
        // and that's it?
        if (fields.size() == 0) {
            return NO_RESOLVED_FIELDS;
        }
        return fields.values().toArray(new ResolvedField[0]);
    }
```
