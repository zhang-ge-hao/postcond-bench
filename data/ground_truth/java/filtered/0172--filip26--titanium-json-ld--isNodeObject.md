https://github.com/filip26/titanium-json-ld/blob/620c2252128046a5e565dab96c219c4b9bb8f68a/./src/main/java/com/apicatalog/jsonld/lang/NodeObject.java#L32-L48
```
🈚️

originally wrong. 6 mutants passed and take a large ratio of all mutants.

//@ ensures true;
```
```
//@ ensures \result <==> (JsonUtils.isObject(value) && ((!value.asJsonObject().containsKey(Keywords.VALUE) && !value.asJsonObject().containsKey(Keywords.LIST) && !value.asJsonObject().containsKey(Keywords.SET)) || value.asJsonObject().keySet().stream().allMatch(k -> k.equals(Keywords.CONTEXT) || k.equals(Keywords.GRAPH)) ));
```
[2, 3, 7, 8, 9, 10]
===== 2 =====
```
     public static final boolean isNodeObject(JsonValue value) {
         return JsonUtils.isObject(value)
                     && ((!value.asJsonObject().containsKey(Keywords.VALUE)
-                                && !value.asJsonObject().containsKey(Keywords.LIST)
+                                && !value.asJsonObject().containsKey(Keywords.GRAPH)
                                 && !value.asJsonObject().containsKey(Keywords.SET))
 
                         || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
```
```
    /**
     * Check if the given value is valid node object.
     *
     * @see <a href="https://www.w3.org/TR/json-ld11/#dfn-node-object">Node Object</a>
     *
     * @param value to check
     * @return <code>true</code> if the provided value is valid node object
     */
    public static final boolean isNodeObject(JsonValue value) {
        return JsonUtils.isObject(value)
                    && ((!value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.GRAPH)
                                && !value.asJsonObject().containsKey(Keywords.SET))

                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
                        );
    }
```
===== 3 =====
```
     public static final boolean isNodeObject(JsonValue value) {
         return JsonUtils.isObject(value)
                     && ((!value.asJsonObject().containsKey(Keywords.VALUE)
-                                && !value.asJsonObject().containsKey(Keywords.LIST)
+                                && !value.asJsonObject().containsKey(Keywords.VALUE)
                                 && !value.asJsonObject().containsKey(Keywords.SET))
 
                         || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
```
```
    /**
     * Check if the given value is valid node object.
     *
     * @see <a href="https://www.w3.org/TR/json-ld11/#dfn-node-object">Node Object</a>
     *
     * @param value to check
     * @return <code>true</code> if the provided value is valid node object
     */
    public static final boolean isNodeObject(JsonValue value) {
        return JsonUtils.isObject(value)
                    && ((!value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.SET))

                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
                        );
    }
```
===== 7 =====
```
                                 && !value.asJsonObject().containsKey(Keywords.LIST)
                                 && !value.asJsonObject().containsKey(Keywords.SET))
 
-                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
+                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).contains(value.asJsonObject().get(Keywords.ID))
                         );
     }
```
```
    /**
     * Check if the given value is valid node object.
     *
     * @see <a href="https://www.w3.org/TR/json-ld11/#dfn-node-object">Node Object</a>
     *
     * @param value to check
     * @return <code>true</code> if the provided value is valid node object
     */
    public static final boolean isNodeObject(JsonValue value) {
        return JsonUtils.isObject(value)
                    && ((!value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.LIST)
                                && !value.asJsonObject().containsKey(Keywords.SET))

                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).contains(value.asJsonObject().get(Keywords.ID))
                        );
    }
```
===== 8 =====
```
                                 && !value.asJsonObject().containsKey(Keywords.LIST)
                                 && !value.asJsonObject().containsKey(Keywords.SET))
 
-                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
+                        || value.asJsonObject().containsKey(Keywords.CONTEXT) && value.asJsonObject().containsKey(Keywords.GRAPH)
                         );
     }
```
```
    /**
     * Check if the given value is valid node object.
     *
     * @see <a href="https://www.w3.org/TR/json-ld11/#dfn-node-object">Node Object</a>
     *
     * @param value to check
     * @return <code>true</code> if the provided value is valid node object
     */
    public static final boolean isNodeObject(JsonValue value) {
        return JsonUtils.isObject(value)
                    && ((!value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.LIST)
                                && !value.asJsonObject().containsKey(Keywords.SET))

                        || value.asJsonObject().containsKey(Keywords.CONTEXT) && value.asJsonObject().containsKey(Keywords.GRAPH)
                        );
    }
```
===== 9 =====
```
                                 && !value.asJsonObject().containsKey(Keywords.LIST)
                                 && !value.asJsonObject().containsKey(Keywords.SET))
 
-                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
+                        || value.asJsonObject().keySet().contains(Keywords.CONTEXT) || value.asJsonObject().keySet().contains(Keywords.GRAPH)
                         );
     }
```
```
    /**
     * Check if the given value is valid node object.
     *
     * @see <a href="https://www.w3.org/TR/json-ld11/#dfn-node-object">Node Object</a>
     *
     * @param value to check
     * @return <code>true</code> if the provided value is valid node object
     */
    public static final boolean isNodeObject(JsonValue value) {
        return JsonUtils.isObject(value)
                    && ((!value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.LIST)
                                && !value.asJsonObject().containsKey(Keywords.SET))

                        || value.asJsonObject().keySet().contains(Keywords.CONTEXT) || value.asJsonObject().keySet().contains(Keywords.GRAPH)
                        );
    }
```
===== 10 =====
```
                                 && !value.asJsonObject().containsKey(Keywords.LIST)
                                 && !value.asJsonObject().containsKey(Keywords.SET))
 
-                        || Arrays.asList(Keywords.CONTEXT, Keywords.GRAPH).containsAll(value.asJsonObject().keySet())
+                        || value.asJsonObject().keySet().size() > 2
                         );
     }
```
```
    /**
     * Check if the given value is valid node object.
     *
     * @see <a href="https://www.w3.org/TR/json-ld11/#dfn-node-object">Node Object</a>
     *
     * @param value to check
     * @return <code>true</code> if the provided value is valid node object
     */
    public static final boolean isNodeObject(JsonValue value) {
        return JsonUtils.isObject(value)
                    && ((!value.asJsonObject().containsKey(Keywords.VALUE)
                                && !value.asJsonObject().containsKey(Keywords.LIST)
                                && !value.asJsonObject().containsKey(Keywords.SET))

                        || value.asJsonObject().keySet().size() > 2
                        );
    }
```
