https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/safety/Safelist.java#L432-L464
```
🈚️

Originally wrong. `String... protocols`

//@ ensures \result == this;
//@ ensures this.protocols != null ==> this.protocols.containsKey(TagName.valueOf(tag));
//@ ensures this.protocols != null ==> this.protocols.get(TagName.valueOf(tag)) != null && ((java.util.Map) this.protocols.get(TagName.valueOf(tag))).containsKey(AttributeKey.valueOf(attribute));
//@ ensures ((java.util.Map) this.protocols.get(TagName.valueOf(tag))).get(AttributeKey.valueOf(attribute)) != null;
//@ ensures this.protocols != null ==> java.util.Arrays.stream(protocols).allMatch(p -> ((java.util.Set) ((java.util.Map) this.protocols.get(TagName.valueOf(tag))).get(AttributeKey.valueOf(attribute))).contains(Protocol.valueOf(p)));
//@ ensures this.protocols != null ==> ((\old(this.protocols.containsKey(TagName.valueOf(tag))) && \old(((java.util.Map) this.protocols.get(TagName.valueOf(tag))).containsKey(AttributeKey.valueOf(attribute)))) ==> ((java.util.Set) \old(((java.util.Map) this.protocols.get(TagName.valueOf(tag))).get(AttributeKey.valueOf(attribute)))).stream().allMatch(pp -> ((java.util.Set) ((java.util.Map) this.protocols.get(TagName.valueOf(tag))).get(AttributeKey.valueOf(attribute))).contains(pp)));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
         Validate.notEmpty(attribute);
         Validate.notNull(protocols);
 
-        TagName tagName = TagName.valueOf(tag);
+        TagName tagName = TagName.valueOf(tag.substring(0, 1).toLowerCase()); // Only takes the first character of the tag, leading to incorrect tag names.
         AttributeKey attrKey = AttributeKey.valueOf(attribute);
         Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
         Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag.substring(0, 1).toLowerCase()); // Only takes the first character of the tag, leading to incorrect tag names.
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 1 =====
```
         Validate.notNull(protocols);
 
         TagName tagName = TagName.valueOf(tag);
-        AttributeKey attrKey = AttributeKey.valueOf(attribute);
+        AttributeKey attrKey = AttributeKey.valueOf(attribute.substring(0, 1)); // Only takes the first character of the attribute name, leading to incorrect key usage.
         Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
         Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute.substring(0, 1)); // Only takes the first character of the attribute name, leading to incorrect key usage.
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 2 =====
```
         TagName tagName = TagName.valueOf(tag);
         AttributeKey attrKey = AttributeKey.valueOf(attribute);
         Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
-        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
+        Set<Protocol> protSet = attrMap.containsKey(attrKey) ? attrMap.get(attrKey) : new HashSet<>();
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.containsKey(attrKey) ? attrMap.get(attrKey) : new HashSet<>();

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 3 =====
```
         TagName tagName = TagName.valueOf(tag);
         AttributeKey attrKey = AttributeKey.valueOf(attribute);
         Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
-        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
+        Set<Protocol> protSet = attrMap.get(attrKey) != null ? attrMap.get(attrKey) : new HashSet<>();
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.get(attrKey) != null ? attrMap.get(attrKey) : new HashSet<>();

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 4 =====
```
         TagName tagName = TagName.valueOf(tag);
         AttributeKey attrKey = AttributeKey.valueOf(attribute);
         Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
-        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
+        Set<Protocol> protSet = new HashSet<>(attrMap.getOrDefault(attrKey, new HashSet<>()));
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = new HashSet<>(attrMap.getOrDefault(attrKey, new HashSet<>()));

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 5 =====
```
         Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
         Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
 
-        for (String protocol : protocols) {
+        for (String protocol : new String[0]) {
             Validate.notEmpty(protocol);
             Protocol prot = Protocol.valueOf(protocol);
             protSet.add(prot);
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : new String[0]) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 6 =====
```
         Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());
 
         for (String protocol : protocols) {
-            Validate.notEmpty(protocol);
+            if (protocol.length() < 3) { protocol = "default"; } // This introduces a default value for short protocols
             Protocol prot = Protocol.valueOf(protocol);
             protSet.add(prot);
         }
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            if (protocol.length() < 3) { protocol = "default"; } // This introduces a default value for short protocols
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return this;
    }
```
===== 7 =====
```
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
-            Protocol prot = Protocol.valueOf(protocol);
+            Protocol prot = Protocol.valueOf(protocol + ":"); // Appends a colon to the protocol, which may cause mismatches in protocol validation.
             protSet.add(prot);
         }
         return this;
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol + ":"); // Appends a colon to the protocol, which may cause mismatches in protocol validation.
            protSet.add(prot);
        }
        return this;
    }
```
===== 8 =====
```
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
-            Protocol prot = Protocol.valueOf(protocol);
+            Protocol prot = Protocol.valueOf(protocol.replace("http", "htp")); // Intentionally misspells "http", leading to invalid protocol values.
             protSet.add(prot);
         }
         return this;
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol.replace("http", "htp")); // Intentionally misspells "http", leading to invalid protocol values.
            protSet.add(prot);
        }
        return this;
    }
```
===== 9 =====
```
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
-            Protocol prot = Protocol.valueOf(protocol);
+            Protocol prot = Protocol.valueOf(protocol.substring(1)); // Removes the first character of the protocol, potentially leading to invalid protocol values.
             protSet.add(prot);
         }
         return this;
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol.substring(1)); // Removes the first character of the protocol, potentially leading to invalid protocol values.
            protSet.add(prot);
        }
        return this;
    }
```
===== 10 =====
```
 
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
-            Protocol prot = Protocol.valueOf(protocol);
+            Protocol prot = Protocol.valueOf(protocol.toUpperCase()); // Converts protocol to uppercase, which may not match expected values.
             protSet.add(prot);
         }
         return this;
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol.toUpperCase()); // Converts protocol to uppercase, which may not match expected values.
            protSet.add(prot);
        }
        return this;
    }
```
===== 11 =====
```
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
             Protocol prot = Protocol.valueOf(protocol);
-            protSet.add(prot);
+            
         }
         return this;
     }
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            
        }
        return this;
    }
```
===== 12 =====
```
         for (String protocol : protocols) {
             Validate.notEmpty(protocol);
             Protocol prot = Protocol.valueOf(protocol);
-            protSet.add(prot);
+            protSet.add(null);
         }
         return this;
     }
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(null);
        }
        return this;
    }
```
===== 13 =====
```
             Protocol prot = Protocol.valueOf(protocol);
             protSet.add(prot);
         }
-        return this;
+        return null;
     }
```
```
    /**
     Add allowed URL protocols for an element's URL attribute. This restricts the possible values of the attribute to
     URLs with the defined protocol.
     <p>
     E.g.: <code>addProtocols("a", "href", "ftp", "http", "https")</code>
     </p>
     <p>
     To allow a link to an in-page URL anchor (i.e. <code>&lt;a href="#anchor"&gt;</code>, add a <code>#</code>:<br>
     E.g.: <code>addProtocols("a", "href", "#")</code>
     </p>

     @param tag       Tag the URL protocol is for
     @param attribute       Attribute name
     @param protocols List of valid protocols
     @return this, for chaining
     */
    public Safelist addProtocols(String tag, String attribute, String... protocols) {
        Validate.notEmpty(tag);
        Validate.notEmpty(attribute);
        Validate.notNull(protocols);

        TagName tagName = TagName.valueOf(tag);
        AttributeKey attrKey = AttributeKey.valueOf(attribute);
        Map<AttributeKey, Set<Protocol>> attrMap = this.protocols.computeIfAbsent(tagName, k -> new HashMap<>());
        Set<Protocol> protSet = attrMap.computeIfAbsent(attrKey, k -> new HashSet<>());

        for (String protocol : protocols) {
            Validate.notEmpty(protocol);
            Protocol prot = Protocol.valueOf(protocol);
            protSet.add(prot);
        }
        return null;
    }
```
