https://github.com/jmeter-maven-plugin/jmeter-maven-plugin/blob/13092f3e53c1f9e0f87a81c5b47bc5d814530d55/./src/main/java/com/lazerycode/jmeter/properties/PropertiesFile.java#L93-L107
```
//@ ensures additionalProperties.values().stream().noneMatch(v -> v == null);
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) != null).allMatch(k -> additionalProperties.containsKey((String)k) && java.util.Objects.equals(additionalProperties.get((String)k), \old(new java.util.HashMap<String,String>(additionalProperties)).get(k)));
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) == null).allMatch(k -> !additionalProperties.containsKey((String)k));
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) != null && !((String)\old(new java.util.HashMap<String,String>(additionalProperties)).get(k)).trim().isEmpty()).allMatch(k -> java.util.Objects.equals(properties.getProperty((String)k), (String)\old(new java.util.HashMap<String,String>(additionalProperties)).get(k)));
//@ ensures \old(new java.util.HashMap<String,String>(additionalProperties)).keySet().stream().filter(k -> \old(new java.util.HashMap<String,String>(additionalProperties)).get(k) == null || ((String)\old(new java.util.HashMap<String,String>(additionalProperties)).get(k)).trim().isEmpty()).allMatch(k -> java.util.Objects.equals(properties.getProperty((String)k), ((java.util.Properties)\old((java.util.Properties)properties.clone())).getProperty((String)k)));
```
```
//@ ensures !additionalProperties.values().contains(null);
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter") && \old(additionalProperties.get("log_level.jmeter")) != null && !\old(additionalProperties.get("log_level.jmeter")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter"), \old(additionalProperties.get("log_level.jmeter")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter") && (\old(additionalProperties.get("log_level.jmeter")) == null || \old(additionalProperties.get("log_level.jmeter")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter"), \old(properties.getProperty("log_level.jmeter")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter.junit") && \old(additionalProperties.get("log_level.jmeter.junit")) != null && !\old(additionalProperties.get("log_level.jmeter.junit")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter.junit"), \old(additionalProperties.get("log_level.jmeter.junit")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter.junit") && (\old(additionalProperties.get("log_level.jmeter.junit")) == null || \old(additionalProperties.get("log_level.jmeter.junit")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter.junit"), \old(properties.getProperty("log_level.jmeter.junit")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter.control") && \old(additionalProperties.get("log_level.jmeter.control")) != null && !\old(additionalProperties.get("log_level.jmeter.control")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter.control"), \old(additionalProperties.get("log_level.jmeter.control")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter.control") && (\old(additionalProperties.get("log_level.jmeter.control")) == null || \old(additionalProperties.get("log_level.jmeter.control")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter.control"), \old(properties.getProperty("log_level.jmeter.control")));
//@ ensures (\old(additionalProperties).containsKey("log_level.JMETER") && \old(additionalProperties.get("log_level.JMETER")) != null && !\old(additionalProperties.get("log_level.JMETER")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("log_level.JMETER"), \old(additionalProperties.get("log_level.JMETER")));
//@ ensures (\old(additionalProperties).containsKey("log_level.JMETER") && (\old(additionalProperties.get("log_level.JMETER")) == null || \old(additionalProperties.get("log_level.JMETER")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("log_level.JMETER"), \old(properties.getProperty("log_level.JMETER")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter.testbeans") && \old(additionalProperties.get("log_level.jmeter.testbeans")) != null && !\old(additionalProperties.get("log_level.jmeter.testbeans")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter.testbeans"), \old(additionalProperties.get("log_level.jmeter.testbeans")));
//@ ensures (\old(additionalProperties).containsKey("log_level.jmeter.testbeans") && (\old(additionalProperties.get("log_level.jmeter.testbeans")) == null || \old(additionalProperties.get("log_level.jmeter.testbeans")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("log_level.jmeter.testbeans"), \old(properties.getProperty("log_level.jmeter.testbeans")));
//@ ensures (\old(additionalProperties).containsKey("java.class.path") && \old(additionalProperties.get("java.class.path")) != null && !\old(additionalProperties.get("java.class.path")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("java.class.path"), \old(additionalProperties.get("java.class.path")));
//@ ensures (\old(additionalProperties).containsKey("java.class.path") && (\old(additionalProperties.get("java.class.path")) == null || \old(additionalProperties.get("java.class.path")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("java.class.path"), \old(properties.getProperty("java.class.path")));
//@ ensures (\old(additionalProperties).containsKey("user.dir") && \old(additionalProperties.get("user.dir")) != null && !\old(additionalProperties.get("user.dir")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("user.dir"), \old(additionalProperties.get("user.dir")));
//@ ensures (\old(additionalProperties).containsKey("user.dir") && (\old(additionalProperties.get("user.dir")) == null || \old(additionalProperties.get("user.dir")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("user.dir"), \old(properties.getProperty("user.dir")));
//@ ensures (\old(additionalProperties).containsKey("jmeterengine.remote.system.exit") && \old(additionalProperties.get("jmeterengine.remote.system.exit")) != null && !\old(additionalProperties.get("jmeterengine.remote.system.exit")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("jmeterengine.remote.system.exit"), \old(additionalProperties.get("jmeterengine.remote.system.exit")));
//@ ensures (\old(additionalProperties).containsKey("jmeterengine.remote.system.exit") && (\old(additionalProperties.get("jmeterengine.remote.system.exit")) == null || \old(additionalProperties.get("jmeterengine.remote.system.exit")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("jmeterengine.remote.system.exit"), \old(properties.getProperty("jmeterengine.remote.system.exit")));
//@ ensures (\old(additionalProperties).containsKey("jmeterengine.stopfail.system.exit") && \old(additionalProperties.get("jmeterengine.stopfail.system.exit")) != null && !\old(additionalProperties.get("jmeterengine.stopfail.system.exit")).trim().isEmpty()) ==> java.util.Objects.equals(properties.getProperty("jmeterengine.stopfail.system.exit"), \old(additionalProperties.get("jmeterengine.stopfail.system.exit")));
//@ ensures (\old(additionalProperties).containsKey("jmeterengine.stopfail.system.exit") && (\old(additionalProperties.get("jmeterengine.stopfail.system.exit")) == null || \old(additionalProperties.get("jmeterengine.stopfail.system.exit")).trim().isEmpty())) ==> java.util.Objects.equals(properties.getProperty("jmeterengine.stopfail.system.exit"), \old(properties.getProperty("jmeterengine.stopfail.system.exit")));
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
      * @param additionalProperties Map to merge into our Properties object
      */
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
-        additionalProperties.values().removeAll(Collections.singleton(null));
+        additionalProperties.values().clear();
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
             if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().clear();
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 1 =====
```
      * @param additionalProperties Map to merge into our Properties object
      */
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
-        additionalProperties.values().removeAll(Collections.singleton(null));
+        additionalProperties.values().retainAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
             if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().retainAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 2 =====
```
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
-            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
+            if (additionalPropertiesMap.getValue() == null || additionalPropertiesMap.getValue().isEmpty()) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (additionalPropertiesMap.getValue() == null || additionalPropertiesMap.getValue().isEmpty()) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 3 =====
```
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
-            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
+            if (additionalPropertiesMap.getValue().isEmpty() || additionalPropertiesMap.getValue().length() < 3) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (additionalPropertiesMap.getValue().isEmpty() || additionalPropertiesMap.getValue().length() < 3) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 4 =====
```
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
-            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
+            if (additionalPropertiesMap.getValue().trim().equals(" ")) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (additionalPropertiesMap.getValue().trim().equals(" ")) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 5 =====
```
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
-            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
+            if (additionalPropertiesMap.getValue().trim().equalsIgnoreCase("")) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (additionalPropertiesMap.getValue().trim().equalsIgnoreCase("")) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 6 =====
```
     public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
-            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
+            if (additionalPropertiesMap.getValue().trim().length() == 0) {
                 properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (additionalPropertiesMap.getValue().trim().length() == 0) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 7 =====
```
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
             if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
-                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
+                
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
         }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 8 =====
```
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
             if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
-                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
+                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue() + "_default");
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
         }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue() + "_default");
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
===== 9 =====
```
         additionalProperties.values().removeAll(Collections.singleton(null));
         for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
             if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
-                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue());
+                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue().toUpperCase());
                 warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
             }
         }
```
```
    /**
     * Merge a Map of properties into our Properties object
     * The additions will overwrite any existing properties
     *
     * @param additionalProperties Map to merge into our Properties object
     */
    public void addAndOverwriteProperties(Map<String, String> additionalProperties) {
        additionalProperties.values().removeAll(Collections.singleton(null));
        for (Map.Entry<String, String> additionalPropertiesMap : additionalProperties.entrySet()) {
            if (!additionalPropertiesMap.getValue().trim().isEmpty()) {
                properties.setProperty(additionalPropertiesMap.getKey(), additionalPropertiesMap.getValue().toUpperCase());
                warnUserOfPossibleErrors(additionalPropertiesMap.getKey(), properties);
            }
        }
    }
```
