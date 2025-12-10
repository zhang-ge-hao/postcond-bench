https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/extensions/MergedYamlMapping.java#L163-L236
```
//@ ensures \result != null;
//@ ensures original != null && changed != null ==> original.keys().stream().allMatch((YamlNode k) -> \result.keys().contains(k));
//@ ensures original != null && changed != null ==> changed.keys().stream().allMatch((YamlNode k) -> \result.keys().contains(k));
//@ ensures !overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && !(original.value(k) instanceof YamlMapping) && !(changed.value(k) instanceof YamlMapping) && !(original.value(k) instanceof YamlSequence) && !(changed.value(k) instanceof YamlSequence)).allMatch((YamlNode k) -> (\result.value(k) == null && original.value(k) == null) || (\result.value(k) != null && original.value(k) != null && \result.value(k).toString().equals(original.value(k).toString())));
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && !(original.value(k) instanceof YamlMapping) && !(changed.value(k) instanceof YamlMapping) && !(original.value(k) instanceof YamlSequence) && !(changed.value(k) instanceof YamlSequence)).allMatch((YamlNode k) -> (\result.value(k) == null && changed.value(k) == null) || (\result.value(k) != null && changed.value(k) != null && \result.value(k).toString().equals(changed.value(k).toString())));
//@ ensures original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && original.value(k) instanceof YamlMapping && changed.value(k) instanceof YamlMapping).allMatch((YamlNode k) -> ((YamlMapping)original.value(k)).keys().stream().allMatch((YamlNode nk) -> ((YamlMapping)\result.value(k)).keys().stream().anyMatch((YamlNode rk) -> rk.toString().equals(nk.toString()))) && ((YamlMapping)changed.value(k)).keys().stream().allMatch((YamlNode nk) -> ((YamlMapping)\result.value(k)).keys().stream().anyMatch((YamlNode rk) -> rk.toString().equals(nk.toString()))));
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && original.value(k) instanceof YamlSequence && changed.value(k) instanceof YamlSequence).allMatch((YamlNode k) -> ((YamlSequence)\result.value(k)).values().stream().allMatch((YamlNode rn) -> java.util.stream.Stream.concat(((YamlSequence)original.value(k)).values().stream(), ((YamlSequence)changed.value(k)).values().stream()).anyMatch((YamlNode n) -> n.toString().equals(rn.toString()))));
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && original.value(k) instanceof YamlSequence && changed.value(k) instanceof YamlSequence).allMatch((YamlNode k) -> java.util.stream.Stream.concat(((YamlSequence)original.value(k)).values().stream(), ((YamlSequence)changed.value(k)).values().stream()).map((YamlNode n) -> n.toString()).distinct().allMatch((String s) -> ((YamlSequence)\result.value(k)).values().stream().filter((YamlNode rn) -> rn.toString().equals(s)).count() == java.lang.Math.max(((YamlSequence)original.value(k)).values().stream().filter((YamlNode on) -> on.toString().equals(s)).count(), ((YamlSequence)changed.value(k)).values().stream().filter((YamlNode cn) -> cn.toString().equals(s)).count())));
//@ ensures !overrideConflicts && original != null ==> \result.comment().value().equals(original.comment().value());
//@ ensures overrideConflicts && original != null && changed != null && !changed.comment().value().isEmpty() ==> \result.comment().value().equals(changed.comment().value());
//@ ensures overrideConflicts && original != null && changed != null && changed.comment().value().isEmpty() ==> \result.comment().value().equals(original.comment().value());
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && original.value(k) instanceof YamlSequence && changed.value(k) instanceof YamlSequence).allMatch((YamlNode k) -> !((YamlSequence)changed.value(k)).comment().value().isEmpty() ? ((YamlSequence)\result.value(k)).comment().value().equals(((YamlSequence)changed.value(k)).comment().value()) : ((YamlSequence)\result.value(k)).comment().value().equals(((YamlSequence)original.value(k)).comment().value()));
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k0) -> changed.keys().contains(k0) && original.value(k0) instanceof YamlMapping && changed.value(k0) instanceof YamlMapping).allMatch((YamlNode k0) -> ((YamlMapping)original.value(k0)).keys().stream().filter((YamlNode k1) -> ((YamlMapping)original.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)changed.value(k0)).value(k1) instanceof YamlMapping).allMatch((YamlNode k1) -> ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).keys().stream().filter((YamlNode k2) -> ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) != null && ((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) != null && !(((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) instanceof YamlSequence) && !(((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) instanceof YamlSequence)).allMatch((YamlNode k2) -> \result.value(k0) instanceof YamlMapping && ((YamlMapping)\result.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2) != null && ((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2).toString().equals(((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2).toString()))));
//@ ensures !overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k0) -> changed.keys().contains(k0) && original.value(k0) instanceof YamlMapping && changed.value(k0) instanceof YamlMapping).allMatch((YamlNode k0) -> ((YamlMapping)original.value(k0)).keys().stream().filter((YamlNode k1) -> ((YamlMapping)original.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)changed.value(k0)).value(k1) instanceof YamlMapping).allMatch((YamlNode k1) -> ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).keys().stream().filter((YamlNode k2) -> ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) != null && ((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) != null && !(((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) instanceof YamlSequence) && !(((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) instanceof YamlSequence)).allMatch((YamlNode k2) -> \result.value(k0) instanceof YamlMapping && ((YamlMapping)\result.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2) != null && ((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2).toString().equals(((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2).toString()))));
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k0) -> changed.keys().contains(k0) && original.value(k0) instanceof YamlMapping && changed.value(k0) instanceof YamlMapping).allMatch((YamlNode k0) -> ((YamlMapping)original.value(k0)).keys().stream().filter((YamlNode k1) -> ((YamlMapping)changed.value(k0)).keys().contains(k1) && ((YamlMapping)original.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)changed.value(k0)).value(k1) instanceof YamlMapping).allMatch((YamlNode k1) -> ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).keys().stream().filter((YamlNode k2) -> ((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).keys().contains(k2) && ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) instanceof YamlMapping && ((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) instanceof YamlMapping).allMatch((YamlNode k2) -> ((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).keys().stream().filter((YamlNode k3) -> ((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).keys().contains(k3) && ((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3) != null && ((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3) != null && !(((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlSequence) && !(((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlSequence)).allMatch((YamlNode k3) -> \result.value(k0) instanceof YamlMapping && ((YamlMapping)\result.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2) instanceof YamlMapping && ((YamlMapping)((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2)).value(k3) != null && ((YamlMapping)((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2)).value(k3).toString().equals(((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3).toString())))));
//@ ensures !overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k0) -> changed.keys().contains(k0) && original.value(k0) instanceof YamlMapping && changed.value(k0) instanceof YamlMapping).allMatch((YamlNode k0) -> ((YamlMapping)original.value(k0)).keys().stream().filter((YamlNode k1) -> ((YamlMapping)changed.value(k0)).keys().contains(k1) && ((YamlMapping)original.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)changed.value(k0)).value(k1) instanceof YamlMapping).allMatch((YamlNode k1) -> ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).keys().stream().filter((YamlNode k2) -> ((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).keys().contains(k2) && ((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2) instanceof YamlMapping && ((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2) instanceof YamlMapping).allMatch((YamlNode k2) -> ((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).keys().stream().filter((YamlNode k3) -> ((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).keys().contains(k3) && ((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3) != null && ((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3) != null && !(((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlSequence) && !(((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlMapping) && !(((YamlMapping)((YamlMapping)((YamlMapping)changed.value(k0)).value(k1)).value(k2)).value(k3) instanceof YamlSequence)).allMatch((YamlNode k3) -> \result.value(k0) instanceof YamlMapping && ((YamlMapping)\result.value(k0)).value(k1) instanceof YamlMapping && ((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2) instanceof YamlMapping && ((YamlMapping)((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2)).value(k3) != null && ((YamlMapping)((YamlMapping)((YamlMapping)\result.value(k0)).value(k1)).value(k2)).value(k3).toString().equals(((YamlMapping)((YamlMapping)((YamlMapping)original.value(k0)).value(k1)).value(k2)).value(k3).toString())))));
//@ ensures overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && original.value(k) instanceof YamlMapping && changed.value(k) instanceof YamlMapping).allMatch((YamlNode k) -> !((YamlMapping)changed.value(k)).comment().value().isEmpty() ? ((YamlMapping)\result.value(k)).comment().value().equals(((YamlMapping)changed.value(k)).comment().value()) : ((YamlMapping)\result.value(k)).comment().value().equals(((YamlMapping)original.value(k)).comment().value()));
//@ ensures !overrideConflicts && original != null && changed != null ==> original.keys().stream().filter((YamlNode k) -> changed.keys().contains(k) && original.value(k) instanceof YamlMapping && changed.value(k) instanceof YamlMapping).allMatch((YamlNode k) -> ((YamlMapping)\result.value(k)).comment().value().equals(((YamlMapping)original.value(k)).comment().value()));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76]
===== 0 =====
```
     ) {
         YamlMappingBuilder originalBuilder = this
             .yamlMappingBuilderFrom(original);
-        final Set<YamlNode> changedKeys = changed.keys();
+        final Set<YamlNode> changedKeys = original.keys(); // This incorrectly uses the original keys instead of the changed ones.
         for(final YamlNode key : changedKeys) {
             final YamlNode originalValue = original.value(key);
             final YamlNode changedValue = changed.value(key);
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = original.keys(); // This incorrectly uses the original keys instead of the changed ones.
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 1 =====
```
         YamlMappingBuilder originalBuilder = this
             .yamlMappingBuilderFrom(original);
         final Set<YamlNode> changedKeys = changed.keys();
-        for(final YamlNode key : changedKeys) {
+        for(final YamlNode key : original.keys()) {
             final YamlNode originalValue = original.value(key);
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : original.keys()) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 2 =====
```
             .yamlMappingBuilderFrom(original);
         final Set<YamlNode> changedKeys = changed.keys();
         for(final YamlNode key : changedKeys) {
-            final YamlNode originalValue = original.value(key);
+            final YamlNode originalValue = changed.value(key); // This incorrectly assigns the changed value instead of the original
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = changed.value(key); // This incorrectly assigns the changed value instead of the original
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 3 =====
```
             .yamlMappingBuilderFrom(original);
         final Set<YamlNode> changedKeys = changed.keys();
         for(final YamlNode key : changedKeys) {
-            final YamlNode originalValue = original.value(key);
+            final YamlNode originalValue = null; // This will cause a NullPointerException later when accessed
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = null; // This will cause a NullPointerException later when accessed
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 4 =====
```
             .yamlMappingBuilderFrom(original);
         final Set<YamlNode> changedKeys = changed.keys();
         for(final YamlNode key : changedKeys) {
-            final YamlNode originalValue = original.value(key);
+            final YamlNode originalValue = original.value(changed.keys().iterator().next()); // This uses a random key from changed instead of the current key
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(changed.keys().iterator().next()); // This uses a random key from changed instead of the current key
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 5 =====
```
             .yamlMappingBuilderFrom(original);
         final Set<YamlNode> changedKeys = changed.keys();
         for(final YamlNode key : changedKeys) {
-            final YamlNode originalValue = original.value(key);
+            final YamlNode originalValue = original.value(key.toString()); // This incorrectly converts the key to a string, which may not match any original keys
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key.toString()); // This incorrectly converts the key to a string, which may not match any original keys
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 6 =====
```
         final Set<YamlNode> changedKeys = changed.keys();
         for(final YamlNode key : changedKeys) {
             final YamlNode originalValue = original.value(key);
-            final YamlNode changedValue = changed.value(key);
+            final YamlNode changedValue = null; // This will cause a NullPointerException later when accessed.
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
                 originalBuilder = originalBuilder.add(
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = null; // This will cause a NullPointerException later when accessed.
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 7 =====
```
         final Set<YamlNode> changedKeys = changed.keys();
         for(final YamlNode key : changedKeys) {
             final YamlNode originalValue = original.value(key);
-            final YamlNode changedValue = changed.value(key);
+            final YamlNode changedValue = original.value(key); // This incorrectly assigns the original value instead of the changed value.
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
                 originalBuilder = originalBuilder.add(
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = original.value(key); // This incorrectly assigns the original value instead of the changed value.
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 8 =====
```
             final YamlNode originalValue = original.value(key);
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
-                && originalValue instanceof YamlMapping) {
+                && changedValue == null) {
                 originalBuilder = originalBuilder.add(
                     key,
                     this.recursiveMerge(
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && changedValue == null) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 9 =====
```
             final YamlNode originalValue = original.value(key);
             final YamlNode changedValue = changed.value(key);
             if (changedValue instanceof YamlMapping
-                && originalValue instanceof YamlMapping) {
+                && originalValue instanceof YamlSequence) {
                 originalBuilder = originalBuilder.add(
                     key,
                     this.recursiveMerge(
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlSequence) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 10 =====
```
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
                 originalBuilder = originalBuilder.add(
-                    key,
+                    changedValue,
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    changedValue,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 11 =====
```
             if (changedValue instanceof YamlMapping
                 && originalValue instanceof YamlMapping) {
                 originalBuilder = originalBuilder.add(
-                    key,
+                    originalValue,
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    originalValue,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 12 =====
```
                 originalBuilder = originalBuilder.add(
                     key,
                     this.recursiveMerge(
-                        (YamlMapping) originalValue,
+                        (YamlMapping) changedValue,
                         (YamlMapping) changedValue,
                         overrideConflicts
                     )
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) changedValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 13 =====
```
                 originalBuilder = originalBuilder.add(
                     key,
                     this.recursiveMerge(
-                        (YamlMapping) originalValue,
+                        (YamlMapping) originalBuilder.build(""), // Building with an empty comment
                         (YamlMapping) changedValue,
                         overrideConflicts
                     )
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalBuilder.build(""), // Building with an empty comment
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 14 =====
```
                     key,
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
-                        (YamlMapping) changedValue,
+                        (YamlMapping) originalValue,
                         overrideConflicts
                     )
                 );
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) originalValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 15 =====
```
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
-                        overrideConflicts
+                        !overrideConflicts
                     )
                 );
             } else if(overrideConflicts
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        !overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 16 =====
```
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
-                        overrideConflicts
+                        false
                     )
                 );
             } else if(overrideConflicts
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        false
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 17 =====
```
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
-                        overrideConflicts
+                        overrideConflicts && false
                     )
                 );
             } else if(overrideConflicts
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts && false
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 18 =====
```
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
-                        overrideConflicts
+                        overrideConflicts || true
                     )
                 );
             } else if(overrideConflicts
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts || true
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 19 =====
```
                     this.recursiveMerge(
                         (YamlMapping) originalValue,
                         (YamlMapping) changedValue,
-                        overrideConflicts
+                        true
                     )
                 );
             } else if(overrideConflicts
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        true
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 20 =====
```
                         overrideConflicts
                     )
                 );
-            } else if(overrideConflicts
+            } else if(!overrideConflicts
                 && changedValue instanceof YamlSequence
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(!overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 21 =====
```
                         overrideConflicts
                     )
                 );
-            } else if(overrideConflicts
+            } else if(changedValue == null
                 && changedValue instanceof YamlSequence
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(changedValue == null
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 22 =====
```
                         overrideConflicts
                     )
                 );
-            } else if(overrideConflicts
+            } else if(changedValue instanceof YamlMapping && originalValue instanceof YamlMapping
                 && changedValue instanceof YamlSequence
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(changedValue instanceof YamlMapping && originalValue instanceof YamlMapping
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 23 =====
```
                         overrideConflicts
                     )
                 );
-            } else if(overrideConflicts
+            } else if(originalValue == null
                 && changedValue instanceof YamlSequence
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(originalValue == null
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 24 =====
```
                         overrideConflicts
                     )
                 );
-            } else if(overrideConflicts
+            } else if(originalValue instanceof YamlMapping
                 && changedValue instanceof YamlSequence
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(originalValue instanceof YamlMapping
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 25 =====
```
                     )
                 );
             } else if(overrideConflicts
-                && changedValue instanceof YamlSequence
+                && !(changedValue instanceof YamlSequence)
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && !(changedValue instanceof YamlSequence)
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 26 =====
```
                     )
                 );
             } else if(overrideConflicts
-                && changedValue instanceof YamlSequence
+                && changedValue instanceof YamlMapping
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlMapping
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 27 =====
```
                     )
                 );
             } else if(overrideConflicts
-                && changedValue instanceof YamlSequence
+                && originalValue instanceof YamlMapping
                 && originalValue instanceof YamlSequence){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && originalValue instanceof YamlMapping
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 28 =====
```
                 );
             } else if(overrideConflicts
                 && changedValue instanceof YamlSequence
-                && originalValue instanceof YamlSequence){
+                && changedValue instanceof YamlMapping){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
                 YamlSequenceBuilder originalSeqBuilder = this
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && changedValue instanceof YamlMapping){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 29 =====
```
                 );
             } else if(overrideConflicts
                 && changedValue instanceof YamlSequence
-                && originalValue instanceof YamlSequence){
+                && originalValue == null){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
                 YamlSequenceBuilder originalSeqBuilder = this
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue == null){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 30 =====
```
                 );
             } else if(overrideConflicts
                 && changedValue instanceof YamlSequence
-                && originalValue instanceof YamlSequence){
+                && originalValue instanceof YamlMapping){
                 final YamlSequence originalSeq = (YamlSequence) originalValue;
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
                 YamlSequenceBuilder originalSeqBuilder = this
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlMapping){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 31 =====
```
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
-                for (final YamlNode node : changedSeq.values()) {
+                for (final YamlNode node : changed.keys()) {
                     if (!originalSeq.values().contains(node)) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changed.keys()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 32 =====
```
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
-                for (final YamlNode node : changedSeq.values()) {
+                for (final YamlNode node : original.keys()) {
                     if (!originalSeq.values().contains(node)) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : original.keys()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 33 =====
```
                 final YamlSequence changedSeq = (YamlSequence) changedValue;
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
-                for (final YamlNode node : changedSeq.values()) {
+                for (final YamlNode node : originalSeq.values()) {
                     if (!originalSeq.values().contains(node)) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : originalSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 34 =====
```
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
-                    if (!originalSeq.values().contains(node)) {
+                    if (changedSeq.values().contains(node)) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
                 }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (changedSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 35 =====
```
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
-                    if (!originalSeq.values().contains(node)) {
+                    if (node != null) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
                 }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (node != null) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 36 =====
```
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
-                    if (!originalSeq.values().contains(node)) {
+                    if (originalSeq.values().contains(node)) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
                 }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 37 =====
```
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
-                    if (!originalSeq.values().contains(node)) {
+                    if (originalSeq.values().isEmpty()) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
                 }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (originalSeq.values().isEmpty()) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 38 =====
```
                 YamlSequenceBuilder originalSeqBuilder = this
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
-                    if (!originalSeq.values().contains(node)) {
+                    if (originalSeq.values().size() < changedSeq.values().size()) {
                         originalSeqBuilder = originalSeqBuilder.add(node);
                     }
                 }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (originalSeq.values().size() < changedSeq.values().size()) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 39 =====
```
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
                     if (!originalSeq.values().contains(node)) {
-                        originalSeqBuilder = originalSeqBuilder.add(node);
+                        originalSeqBuilder = originalSeqBuilder.add(changedValue);
                     }
                 }
                 final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(changedValue);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 40 =====
```
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
                     if (!originalSeq.values().contains(node)) {
-                        originalSeqBuilder = originalSeqBuilder.add(node);
+                        originalSeqBuilder = originalSeqBuilder.add(node).add(node);
                     }
                 }
                 final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node).add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 41 =====
```
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
                     if (!originalSeq.values().contains(node)) {
-                        originalSeqBuilder = originalSeqBuilder.add(node);
+                        originalSeqBuilder = originalSeqBuilder.add(node).add(originalValue);
                     }
                 }
                 final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node).add(originalValue);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 42 =====
```
                     .yamlSequenceBuilderFrom(originalSeq);
                 for (final YamlNode node : changedSeq.values()) {
                     if (!originalSeq.values().contains(node)) {
-                        originalSeqBuilder = originalSeqBuilder.add(node);
+                        originalSeqBuilder = originalSeqBuilder.add(originalValue);
                     }
                 }
                 final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(originalValue);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 43 =====
```
                     }
                 }
                 final Comment newComment;
-                if(!changedSeq.comment().value().isEmpty()){
+                if(!original.comment().value().isEmpty()){
                     newComment = changedSeq.comment();
                 }else{
                     newComment = originalSeq.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!original.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 44 =====
```
                     }
                 }
                 final Comment newComment;
-                if(!changedSeq.comment().value().isEmpty()){
+                if(changedSeq.comment() == null){
                     newComment = changedSeq.comment();
                 }else{
                     newComment = originalSeq.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(changedSeq.comment() == null){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 45 =====
```
                     }
                 }
                 final Comment newComment;
-                if(!changedSeq.comment().value().isEmpty()){
+                if(changedSeq.comment().value().isEmpty()){
                     newComment = changedSeq.comment();
                 }else{
                     newComment = originalSeq.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 46 =====
```
                     }
                 }
                 final Comment newComment;
-                if(!changedSeq.comment().value().isEmpty()){
+                if(originalSeq.comment() == null){
                     newComment = changedSeq.comment();
                 }else{
                     newComment = originalSeq.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(originalSeq.comment() == null){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 47 =====
```
                     }
                 }
                 final Comment newComment;
-                if(!changedSeq.comment().value().isEmpty()){
+                if(originalSeq.comment().value().isEmpty()){
                     newComment = changedSeq.comment();
                 }else{
                     newComment = originalSeq.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(originalSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 48 =====
```
                 }
                 final Comment newComment;
                 if(!changedSeq.comment().value().isEmpty()){
-                    newComment = changedSeq.comment();
+                    newComment = originalSeq.comment(); // This will incorrectly retain the original comment instead of using the changed comment.
                 }else{
                     newComment = originalSeq.comment();
                 }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = originalSeq.comment(); // This will incorrectly retain the original comment instead of using the changed comment.
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 49 =====
```
                 if(!changedSeq.comment().value().isEmpty()){
                     newComment = changedSeq.comment();
                 }else{
-                    newComment = originalSeq.comment();
+                    newComment = changed.comment(); // This incorrectly uses the comment from the changed sequence instead of the original.
                 }
                 originalBuilder = originalBuilder.add(
                     key,
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = changed.comment(); // This incorrectly uses the comment from the changed sequence instead of the original.
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 50 =====
```
                 if(!changedSeq.comment().value().isEmpty()){
                     newComment = changedSeq.comment();
                 }else{
-                    newComment = originalSeq.comment();
+                    newComment = changedSeq.comment(); // This uses the comment from the changed sequence, which may not be appropriate.
                 }
                 originalBuilder = originalBuilder.add(
                     key,
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = changedSeq.comment(); // This uses the comment from the changed sequence, which may not be appropriate.
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 51 =====
```
                 if(!changedSeq.comment().value().isEmpty()){
                     newComment = changedSeq.comment();
                 }else{
-                    newComment = originalSeq.comment();
+                    newComment = original.comment(); // This incorrectly uses the original comment instead of the original sequence's comment.
                 }
                 originalBuilder = originalBuilder.add(
                     key,
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = original.comment(); // This incorrectly uses the original comment instead of the original sequence's comment.
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 52 =====
```
                     newComment = originalSeq.comment();
                 }
                 originalBuilder = originalBuilder.add(
-                    key,
+                    changedValue, // This will add the changed value instead of the sequence, which may not be the intended behavior.
                     originalSeqBuilder.build(newComment.value())
                 );
             } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    changedValue, // This will add the changed value instead of the sequence, which may not be the intended behavior.
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 53 =====
```
                     newComment = originalSeq.comment();
                 }
                 originalBuilder = originalBuilder.add(
-                    key,
+                    originalValue, // This will incorrectly add the original value instead of the new sequence, leading to data loss.
                     originalSeqBuilder.build(newComment.value())
                 );
             } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    originalValue, // This will incorrectly add the original value instead of the new sequence, leading to data loss.
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 54 =====
```
                 );
             } else {
                 final YamlNode newValue;
-                if (originalValue != null) {
+                if (changedValue == null) {
                     if (overrideConflicts) {
                         newValue = changedValue;
                     } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (changedValue == null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 55 =====
```
                 );
             } else {
                 final YamlNode newValue;
-                if (originalValue != null) {
+                if (changedValue instanceof YamlMapping) {
                     if (overrideConflicts) {
                         newValue = changedValue;
                     } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (changedValue instanceof YamlMapping) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 56 =====
```
                 );
             } else {
                 final YamlNode newValue;
-                if (originalValue != null) {
+                if (originalValue == null) {
                     if (overrideConflicts) {
                         newValue = changedValue;
                     } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue == null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 57 =====
```
                 );
             } else {
                 final YamlNode newValue;
-                if (originalValue != null) {
+                if (originalValue instanceof YamlMapping) {
                     if (overrideConflicts) {
                         newValue = changedValue;
                     } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue instanceof YamlMapping) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 58 =====
```
                 );
             } else {
                 final YamlNode newValue;
-                if (originalValue != null) {
+                if (overrideConflicts && originalValue == null) {
                     if (overrideConflicts) {
                         newValue = changedValue;
                     } else {
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (overrideConflicts && originalValue == null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 59 =====
```
             } else {
                 final YamlNode newValue;
                 if (originalValue != null) {
-                    if (overrideConflicts) {
+                    if (!overrideConflicts) {
                         newValue = changedValue;
                     } else {
                         newValue = originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (!overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 60 =====
```
             } else {
                 final YamlNode newValue;
                 if (originalValue != null) {
-                    if (overrideConflicts) {
+                    if (changedValue == null) {
                         newValue = changedValue;
                     } else {
                         newValue = originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (changedValue == null) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 61 =====
```
             } else {
                 final YamlNode newValue;
                 if (originalValue != null) {
-                    if (overrideConflicts) {
+                    if (originalValue == null) {
                         newValue = changedValue;
                     } else {
                         newValue = originalValue;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (originalValue == null) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 62 =====
```
                 } else {
                     newValue = changedValue;
                 }
-                originalBuilder = originalBuilder.add(key, newValue);
+                originalBuilder = originalBuilder.add(key, changedValue); // Adds the changed value directly, ignoring the overrideConflicts flag
             }
         }
         final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, changedValue); // Adds the changed value directly, ignoring the overrideConflicts flag
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 63 =====
```
                 } else {
                     newValue = changedValue;
                 }
-                originalBuilder = originalBuilder.add(key, newValue);
+                originalBuilder = originalBuilder.add(key, originalValue); // Adds the original value instead of the new value
             }
         }
         final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, originalValue); // Adds the original value instead of the new value
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 64 =====
```
                 } else {
                     newValue = changedValue;
                 }
-                originalBuilder = originalBuilder.add(key, newValue);
+                originalBuilder = originalBuilder.add(key, originalValue); // Adds the original value, effectively ignoring the changes
             }
         }
         final Comment newComment;
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, originalValue); // Adds the original value, effectively ignoring the changes
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 65 =====
```
             }
         }
         final Comment newComment;
-        if(overrideConflicts && !changed.comment().value().isEmpty()){
+        if(!overrideConflicts && !changed.comment().value().isEmpty()){
             newComment = changed.comment();
         }else{
             newComment = original.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(!overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 66 =====
```
             }
         }
         final Comment newComment;
-        if(overrideConflicts && !changed.comment().value().isEmpty()){
+        if(!overrideConflicts || changed.comment().value().isEmpty()){
             newComment = changed.comment();
         }else{
             newComment = original.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(!overrideConflicts || changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 67 =====
```
             }
         }
         final Comment newComment;
-        if(overrideConflicts && !changed.comment().value().isEmpty()){
+        if(overrideConflicts && changed.comment().value().isEmpty() && original.comment().value().isEmpty()){
             newComment = changed.comment();
         }else{
             newComment = original.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && changed.comment().value().isEmpty() && original.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 68 =====
```
             }
         }
         final Comment newComment;
-        if(overrideConflicts && !changed.comment().value().isEmpty()){
+        if(overrideConflicts && changed.comment().value().isEmpty()){
             newComment = changed.comment();
         }else{
             newComment = original.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 69 =====
```
             }
         }
         final Comment newComment;
-        if(overrideConflicts && !changed.comment().value().isEmpty()){
+        if(overrideConflicts || changed.comment().value().isEmpty()){
             newComment = changed.comment();
         }else{
             newComment = original.comment();
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts || changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 70 =====
```
         }
         final Comment newComment;
         if(overrideConflicts && !changed.comment().value().isEmpty()){
-            newComment = changed.comment();
+            newComment = original.comment(); // This will incorrectly use the original comment instead of the changed one.
         }else{
             newComment = original.comment();
         }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = original.comment(); // This will incorrectly use the original comment instead of the changed one.
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 71 =====
```
         if(overrideConflicts && !changed.comment().value().isEmpty()){
             newComment = changed.comment();
         }else{
-            newComment = original.comment();
+            newComment = changed.comment(); // This will incorrectly use the comment from the changed mapping instead of the original.
         }
         return originalBuilder.build(newComment.value());
     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = changed.comment(); // This will incorrectly use the comment from the changed mapping instead of the original.
        }
        return originalBuilder.build(newComment.value());
    }
```
===== 72 =====
```
         }else{
             newComment = original.comment();
         }
-        return originalBuilder.build(newComment.value());
+        return null;
     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return null;
    }
```
===== 73 =====
```
         }else{
             newComment = original.comment();
         }
-        return originalBuilder.build(newComment.value());
+        return originalBuilder.build(""); // Returns an empty comment instead of the correct one.
     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(""); // Returns an empty comment instead of the correct one.
    }
```
===== 74 =====
```
         }else{
             newComment = original.comment();
         }
-        return originalBuilder.build(newComment.value());
+        return originalBuilder.build("Merged Comment"); // Returns a hardcoded comment that does not reflect the actual merge.
     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build("Merged Comment"); // Returns a hardcoded comment that does not reflect the actual merge.
    }
```
===== 75 =====
```
         }else{
             newComment = original.comment();
         }
-        return originalBuilder.build(newComment.value());
+        return originalBuilder.build(newComment.value() + " - Updated"); // Appends extra text to the comment, altering its intended meaning.
     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(newComment.value() + " - Updated"); // Appends extra text to the comment, altering its intended meaning.
    }
```
===== 76 =====
```
         }else{
             newComment = original.comment();
         }
-        return originalBuilder.build(newComment.value());
+        return originalBuilder.build(original.comment().value()); // Returns the original comment instead of the new one.
     }
```
```
    /**
     * Recursively merge to mappings.
     * @param original Original mapping.
     * @param changed Changed mapping.
     * @param overrideConflicts Should conflicting keys be overridden or not?
     * @return Merged mapping.
     * @checkstyle CyclomaticComplexity (200 lines)
     * @checkstyle ExecutableStatementCount (200 lines)
     */
    private YamlMapping recursiveMerge(
        final YamlMapping original,
        final YamlMapping changed,
        final boolean overrideConflicts
    ) {
        YamlMappingBuilder originalBuilder = this
            .yamlMappingBuilderFrom(original);
        final Set<YamlNode> changedKeys = changed.keys();
        for(final YamlNode key : changedKeys) {
            final YamlNode originalValue = original.value(key);
            final YamlNode changedValue = changed.value(key);
            if (changedValue instanceof YamlMapping
                && originalValue instanceof YamlMapping) {
                originalBuilder = originalBuilder.add(
                    key,
                    this.recursiveMerge(
                        (YamlMapping) originalValue,
                        (YamlMapping) changedValue,
                        overrideConflicts
                    )
                );
            } else if(overrideConflicts
                && changedValue instanceof YamlSequence
                && originalValue instanceof YamlSequence){
                final YamlSequence originalSeq = (YamlSequence) originalValue;
                final YamlSequence changedSeq = (YamlSequence) changedValue;
                YamlSequenceBuilder originalSeqBuilder = this
                    .yamlSequenceBuilderFrom(originalSeq);
                for (final YamlNode node : changedSeq.values()) {
                    if (!originalSeq.values().contains(node)) {
                        originalSeqBuilder = originalSeqBuilder.add(node);
                    }
                }
                final Comment newComment;
                if(!changedSeq.comment().value().isEmpty()){
                    newComment = changedSeq.comment();
                }else{
                    newComment = originalSeq.comment();
                }
                originalBuilder = originalBuilder.add(
                    key,
                    originalSeqBuilder.build(newComment.value())
                );
            } else {
                final YamlNode newValue;
                if (originalValue != null) {
                    if (overrideConflicts) {
                        newValue = changedValue;
                    } else {
                        newValue = originalValue;
                    }
                } else {
                    newValue = changedValue;
                }
                originalBuilder = originalBuilder.add(key, newValue);
            }
        }
        final Comment newComment;
        if(overrideConflicts && !changed.comment().value().isEmpty()){
            newComment = changed.comment();
        }else{
            newComment = original.comment();
        }
        return originalBuilder.build(original.comment().value()); // Returns the original comment instead of the new one.
    }
```
