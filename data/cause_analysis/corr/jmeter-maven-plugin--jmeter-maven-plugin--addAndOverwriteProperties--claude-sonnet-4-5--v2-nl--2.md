https://github.com/jmeter-maven-plugin/jmeter-maven-plugin/blob/13092f3e53c1f9e0f87a81c5b47bc5d814530d55/./src/main/java/com/lazerycode/jmeter/properties/PropertiesFile.java#L93-L107
```
//@ ensures additionalProperties == null || additionalProperties.keySet().stream().allMatch(key -> this.properties.containsKey(key));
//@ ensures additionalProperties == null || additionalProperties.entrySet().stream().allMatch(entry -> entry.getKey() == null || entry.getValue() == null || this.properties.get(entry.getKey()).equals(entry.getValue()));
//@ ensures \old(this.properties.keySet()).stream().filter(key -> additionalProperties == null || !additionalProperties.containsKey(key)).allMatch(key -> this.properties.containsKey(key) && this.properties.get(key).equals(\old(this.properties.get(key))));
```
```
limited spec

.allMatch(key -> this.properties.containsKey(key) && this.properties.get(key).equals(\old(this.properties.get(key))))
```
compile_failure
```
//@ ensures additionalProperties.values().stream().noneMatch(v -> v == null);
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) != null).allMatch(k -> additionalProperties.containsKey((String)k) && java.util.Objects.equals(additionalProperties.get((String)k), \old(new java.util.HashMap<String,String>(additionalProperties)).get(k)));
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) == null).allMatch(k -> !additionalProperties.containsKey((String)k));
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) != null && !((String)\old(new java.util.HashMap<String,String>(additionalProperties)).get(k)).trim().isEmpty()).allMatch(k -> java.util.Objects.equals(properties.getProperty((String)k), (String)\old(new java.util.HashMap<String,String>(additionalProperties)).get(k)));
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) == null || ((String)\old(new java.util.HashMap<String,String>(additionalProperties)).get(k)).trim().isEmpty()).allMatch(k -> java.util.Objects.equals(properties.getProperty((String)k), ((java.util.Properties)\old((java.util.Properties)properties.clone())).getProperty((String)k)));

```
