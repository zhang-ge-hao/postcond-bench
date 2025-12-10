https://github.com/Mastercard/client-encryption-java/blob/f91ae60c3de7660fc9d8ce7b38adba751b2ed304/./src/main/java/com/mastercard/developer/utils/FeignUtils.java#L36-L57
```
//@ ensures name == null ==> \result == \old(response);
//@ ensures name != null && value != null ==> \result != \old(response);
//@ ensures name != null && value != null ==> (\result.headers().get(name) != null && \result.headers().get(name).size() == 1 && \result.headers().get(name).iterator().next().equals(value));
//@ ensures name != null && value == null ==> \result.headers().get(name) == null;
//@ ensures name != null && value == null ==> \result.headers().keySet().stream().noneMatch(h -> h != null && h.equalsIgnoreCase(name));
```
```
//@ ensures name == null ==> \result == \old(response);
//@ ensures name != null && value != null ==> \result != \old(response);
//@ ensures name != null && value != null ==> (\result.headers().get(name) != null && \result.headers().get(name).toArray()[0].equals(value));
//@ ensures name != null && value == null ==> \result.headers().get(name) == null
```
[10]
===== 10 =====
```
             }
         }
         if (value != null) {
-            headers.put(name, Collections.singleton(value));
+            headers.put(name, Collections.emptyList()); // This sets the header to an empty list, effectively removing it without indication.
         }
         return response.toBuilder()
                 .headers(headers)
```
```
    /**
     * Update the value of an HTTP response header and return the updated response. Delete the header if the value is null.
     */
    public static Response updateHeader(Response response, String name, String value) {
        if (name == null) {
            // Do nothing
            return response;
        }
        Map<String, Collection<String>> headers = new HashMap<>(response.headers()); // Headers is an UnmodifiableMap
        Set<String> headerNames = new HashSet<>(headers.keySet());
        for (String headerName : headerNames) {
            if (headerName.equalsIgnoreCase(name)) {
                headers.remove(headerName);
            }
        }
        if (value != null) {
            headers.put(name, Collections.emptyList()); // This sets the header to an empty list, effectively removing it without indication.
        }
        return response.toBuilder()
                .headers(headers)
                .build();
    }
```
