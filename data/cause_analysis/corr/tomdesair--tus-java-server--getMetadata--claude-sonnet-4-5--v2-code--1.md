https://github.com/tomdesair/tus-java-server/blob/1c4adf10e2ef29d86f94e572c35e7e22137ff3a0/./src/main/java/me/desair/tus/server/upload/UploadInfo.java#L99-L131
```
//@ ensures \result != null;
//@ ensures (encodedMetadata == null || encodedMetadata.trim().isEmpty()) ==> \result.isEmpty();
//@ ensures \result instanceof java.util.TreeMap;
//@ ensures \result.comparator() != null;
//@ ensures \result.comparator().equals(String.CASE_INSENSITIVE_ORDER);
```
```
hallucination on attribute

no `comparator()` in `Map<String, String>` class
only `SortedMap` have it
```
compile_failure
```
//@ ensures \result != null;
//@ ensures (\old(encodedMetadata) == null || StringUtils.isBlank(\old(encodedMetadata))) ==> \result.isEmpty();
//@ ensures java.util.Arrays.stream(splitToArray(\old(encodedMetadata), ",")).filter(s -> !StringUtils.isBlank(s)).allMatch(valuePair -> { String[] keyValue = splitToArray(valuePair, "\\s"); if (keyValue.length == 0) return true; String key = StringUtils.trimToEmpty(keyValue[0]); int i = 1; while (keyValue.length > i && StringUtils.isBlank(keyValue[i])) { i++; } String expected = keyValue.length > i ? decode(keyValue[i]) : null; return \result.containsKey(key) && java.util.Objects.equals(\result.get(key), expected); });
//@ ensures \result.keySet().stream().allMatch(k -> java.util.Arrays.stream(splitToArray(\old(encodedMetadata), ",")).filter(s -> !StringUtils.isBlank(s)).anyMatch(vp -> { String[] kv = splitToArray(vp, "\\s"); return kv.length > 0 && StringUtils.trimToEmpty(kv[0]).equals(k); }));
```
