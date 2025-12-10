https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/helper/W3CDom.java#L100-L148
```
//@ ensures \result != null;
//@ ensures doc.getDocumentElement() == null || \result.contains("<" + doc.getDocumentElement().getNodeName());
//@ ensures doc.getDocumentElement() == null || \result.length() > 0;
//@ ensures \result.length() == 0 || \result.charAt(\result.length() - 1) != ' ';
//@ ensures doc.getDocumentElement() == null || doc.getDocumentElement().getAttributes() == null || doc.getDocumentElement().getAttributes().getLength() <= 0 || \result.indexOf(' ') >= 0;
//@ ensures doc.getDoctype() != null && !StringUtil.isBlank(doc.getDoctype().getPublicId()) ==> \result.contains("PUBLIC \"" + doc.getDoctype().getPublicId() + "\"");
//@ ensures doc.getDoctype() != null && !StringUtil.isBlank(doc.getDoctype().getSystemId()) ==> \result.contains("\"" + doc.getDoctype().getSystemId() + "\"");
//@ ensures doc.getDoctype() != null && StringUtil.isBlank(doc.getDoctype().getPublicId()) ==> !\result.contains("PUBLIC \"\"");
//@ ensures doc.getDoctype() != null && doc.getDoctype().getName().equalsIgnoreCase("html") && StringUtil.isBlank(doc.getDoctype().getPublicId()) && StringUtil.isBlank(doc.getDoctype().getSystemId()) ==> \result.contains("SYSTEM \"about:legacy-compat\"");
//@ ensures properties != null && properties.containsKey(OutputKeys.ENCODING) && properties.get(OutputKeys.ENCODING) != null && !"".equals(properties.get(OutputKeys.ENCODING)) ==> \result.contains("encoding=\"" + properties.get(OutputKeys.ENCODING) + "\"");
//@ ensures properties != null && "xml".equals(properties.get(OutputKeys.METHOD)) && !(properties.containsKey(OutputKeys.OMIT_XML_DECLARATION) && "yes".equals(properties.get(OutputKeys.OMIT_XML_DECLARATION))) ==> \result.startsWith("<?xml");
//@ ensures properties != null && "html".equals(properties.get(OutputKeys.METHOD)) ==> !\result.startsWith("<?xml");
//@ ensures properties != null && properties.containsKey(OutputKeys.OMIT_XML_DECLARATION) && "yes".equals(properties.get(OutputKeys.OMIT_XML_DECLARATION)) ==> !\result.contains("<?xml");
//@ ensures properties == null ==> !\result.contains("UTF-16");
```
```
//@ ensures \result != null;
//@ ensures doc.getDocumentElement() == null || \result.contains("<" + doc.getDocumentElement().getNodeName());
//@ ensures doc.getDocumentElement() == null || \result.length() > 0;
//@ ensures doc.getDoctype() != null && !StringUtil.isBlank(doc.getDoctype().getPublicId()) ==> \result.contains("\"" + doc.getDoctype().getPublicId() + "\"");
//@ ensures doc.getDoctype() != null && !StringUtil.isBlank(doc.getDoctype().getSystemId()) ==> \result.contains("\"" + doc.getDoctype().getSystemId() + "\"");
//@ ensures doc.getDoctype() != null && doc.getDoctype().getName().equalsIgnoreCase("html") && StringUtil.isBlank(doc.getDoctype().getPublicId()) && StringUtil.isBlank(doc.getDoctype().getSystemId()) ==> \result.contains("about:legacy-compat");
//@ ensures properties != null && properties.containsKey(OutputKeys.ENCODING) ==> \result.contains(properties.get(OutputKeys.ENCODING));
//@ ensures properties != null && "xml".equals(properties.get(OutputKeys.METHOD)) ==> \result.contains("<?xml");
//@ ensures properties != null && properties.containsKey(OutputKeys.OMIT_XML_DECLARATION) && "yes".equals(properties.get(OutputKeys.OMIT_XML_DECLARATION)) ==> !\result.contains("<?xml");
//@ ensures properties == null ==> !\result.contains("UTF-16");
```
[7, 8, 26, 35, 36]
===== 7 =====
```
             TransformerFactory tf = TransformerFactory.newInstance();
             Transformer transformer = tf.newTransformer();
             if (properties != null)
-                transformer.setOutputProperties(propertiesFromMap(properties));
+                transformer.setOutputProperty(OutputKeys.METHOD, "xml");
 
             if (doc.getDoctype() != null) {
                 DocumentType doctype = doc.getDoctype();
```
```
    /**
     * Serialize a W3C document to a String. Provide Properties to define output settings including if HTML or XML. If
     * you don't provide the properties ({@code null}), the output will be auto-detected based on the content of the
     * document.
     *
     * @param doc Document
     * @param properties (optional/nullable) the output properties to use. See {@link
     *     Transformer#setOutputProperties(Properties)} and {@link OutputKeys}
     * @return Document as string
     * @see #OutputHtml
     * @see #OutputXml
     * @see OutputKeys#ENCODING
     * @see OutputKeys#OMIT_XML_DECLARATION
     * @see OutputKeys#STANDALONE
     * @see OutputKeys#DOCTYPE_PUBLIC
     * @see OutputKeys#CDATA_SECTION_ELEMENTS
     * @see OutputKeys#INDENT
     * @see OutputKeys#MEDIA_TYPE
     */
    public static String asString(Document doc, @Nullable Map<String, String> properties) {
        try {
            DOMSource domSource = new DOMSource(doc);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            if (properties != null)
                transformer.setOutputProperty(OutputKeys.METHOD, "xml");

            if (doc.getDoctype() != null) {
                DocumentType doctype = doc.getDoctype();
                if (!StringUtil.isBlank(doctype.getPublicId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                if (!StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
                    // handle <!doctype html> for legacy dom.
                else if (doctype.getName().equalsIgnoreCase("html")
                    && StringUtil.isBlank(doctype.getPublicId())
                    && StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat");
            }

            transformer.transform(domSource, result);
            return writer.toString();

        } catch (TransformerException e) {
            throw new IllegalStateException(e);
        }
    }
```
===== 8 =====
```
 
             if (doc.getDoctype() != null) {
                 DocumentType doctype = doc.getDoctype();
-                if (!StringUtil.isBlank(doctype.getPublicId()))
+                if (StringUtil.isBlank(doctype.getPublicId())) // Negates the condition, leading to incorrect behavior
                     transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                 if (!StringUtil.isBlank(doctype.getSystemId()))
                     transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
```
```
    /**
     * Serialize a W3C document to a String. Provide Properties to define output settings including if HTML or XML. If
     * you don't provide the properties ({@code null}), the output will be auto-detected based on the content of the
     * document.
     *
     * @param doc Document
     * @param properties (optional/nullable) the output properties to use. See {@link
     *     Transformer#setOutputProperties(Properties)} and {@link OutputKeys}
     * @return Document as string
     * @see #OutputHtml
     * @see #OutputXml
     * @see OutputKeys#ENCODING
     * @see OutputKeys#OMIT_XML_DECLARATION
     * @see OutputKeys#STANDALONE
     * @see OutputKeys#DOCTYPE_PUBLIC
     * @see OutputKeys#CDATA_SECTION_ELEMENTS
     * @see OutputKeys#INDENT
     * @see OutputKeys#MEDIA_TYPE
     */
    public static String asString(Document doc, @Nullable Map<String, String> properties) {
        try {
            DOMSource domSource = new DOMSource(doc);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            if (properties != null)
                transformer.setOutputProperties(propertiesFromMap(properties));

            if (doc.getDoctype() != null) {
                DocumentType doctype = doc.getDoctype();
                if (StringUtil.isBlank(doctype.getPublicId())) // Negates the condition, leading to incorrect behavior
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                if (!StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
                    // handle <!doctype html> for legacy dom.
                else if (doctype.getName().equalsIgnoreCase("html")
                    && StringUtil.isBlank(doctype.getPublicId())
                    && StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat");
            }

            transformer.transform(domSource, result);
            return writer.toString();

        } catch (TransformerException e) {
            throw new IllegalStateException(e);
        }
    }
```
===== 26 =====
```
                 else if (doctype.getName().equalsIgnoreCase("html")
                     && StringUtil.isBlank(doctype.getPublicId())
                     && StringUtil.isBlank(doctype.getSystemId()))
-                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat");
+                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat-incorrect"); // Sets a similar but incorrect value
             }
 
             transformer.transform(domSource, result);
```
```
    /**
     * Serialize a W3C document to a String. Provide Properties to define output settings including if HTML or XML. If
     * you don't provide the properties ({@code null}), the output will be auto-detected based on the content of the
     * document.
     *
     * @param doc Document
     * @param properties (optional/nullable) the output properties to use. See {@link
     *     Transformer#setOutputProperties(Properties)} and {@link OutputKeys}
     * @return Document as string
     * @see #OutputHtml
     * @see #OutputXml
     * @see OutputKeys#ENCODING
     * @see OutputKeys#OMIT_XML_DECLARATION
     * @see OutputKeys#STANDALONE
     * @see OutputKeys#DOCTYPE_PUBLIC
     * @see OutputKeys#CDATA_SECTION_ELEMENTS
     * @see OutputKeys#INDENT
     * @see OutputKeys#MEDIA_TYPE
     */
    public static String asString(Document doc, @Nullable Map<String, String> properties) {
        try {
            DOMSource domSource = new DOMSource(doc);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            if (properties != null)
                transformer.setOutputProperties(propertiesFromMap(properties));

            if (doc.getDoctype() != null) {
                DocumentType doctype = doc.getDoctype();
                if (!StringUtil.isBlank(doctype.getPublicId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                if (!StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
                    // handle <!doctype html> for legacy dom.
                else if (doctype.getName().equalsIgnoreCase("html")
                    && StringUtil.isBlank(doctype.getPublicId())
                    && StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat-incorrect"); // Sets a similar but incorrect value
            }

            transformer.transform(domSource, result);
            return writer.toString();

        } catch (TransformerException e) {
            throw new IllegalStateException(e);
        }
    }
```
===== 35 =====
```
             }
 
             transformer.transform(domSource, result);
-            return writer.toString();
+            return writer.toString() + " "; // Appends a space at the end of the output, altering the expected format.
 
         } catch (TransformerException e) {
             throw new IllegalStateException(e);
```
```
    /**
     * Serialize a W3C document to a String. Provide Properties to define output settings including if HTML or XML. If
     * you don't provide the properties ({@code null}), the output will be auto-detected based on the content of the
     * document.
     *
     * @param doc Document
     * @param properties (optional/nullable) the output properties to use. See {@link
     *     Transformer#setOutputProperties(Properties)} and {@link OutputKeys}
     * @return Document as string
     * @see #OutputHtml
     * @see #OutputXml
     * @see OutputKeys#ENCODING
     * @see OutputKeys#OMIT_XML_DECLARATION
     * @see OutputKeys#STANDALONE
     * @see OutputKeys#DOCTYPE_PUBLIC
     * @see OutputKeys#CDATA_SECTION_ELEMENTS
     * @see OutputKeys#INDENT
     * @see OutputKeys#MEDIA_TYPE
     */
    public static String asString(Document doc, @Nullable Map<String, String> properties) {
        try {
            DOMSource domSource = new DOMSource(doc);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            if (properties != null)
                transformer.setOutputProperties(propertiesFromMap(properties));

            if (doc.getDoctype() != null) {
                DocumentType doctype = doc.getDoctype();
                if (!StringUtil.isBlank(doctype.getPublicId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                if (!StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
                    // handle <!doctype html> for legacy dom.
                else if (doctype.getName().equalsIgnoreCase("html")
                    && StringUtil.isBlank(doctype.getPublicId())
                    && StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat");
            }

            transformer.transform(domSource, result);
            return writer.toString() + " "; // Appends a space at the end of the output, altering the expected format.

        } catch (TransformerException e) {
            throw new IllegalStateException(e);
        }
    }
```
===== 36 =====
```
             }
 
             transformer.transform(domSource, result);
-            return writer.toString();
+            return writer.toString().replace(" ", "_"); // Replaces spaces with underscores, modifying the output format.
 
         } catch (TransformerException e) {
             throw new IllegalStateException(e);
```
```
    /**
     * Serialize a W3C document to a String. Provide Properties to define output settings including if HTML or XML. If
     * you don't provide the properties ({@code null}), the output will be auto-detected based on the content of the
     * document.
     *
     * @param doc Document
     * @param properties (optional/nullable) the output properties to use. See {@link
     *     Transformer#setOutputProperties(Properties)} and {@link OutputKeys}
     * @return Document as string
     * @see #OutputHtml
     * @see #OutputXml
     * @see OutputKeys#ENCODING
     * @see OutputKeys#OMIT_XML_DECLARATION
     * @see OutputKeys#STANDALONE
     * @see OutputKeys#DOCTYPE_PUBLIC
     * @see OutputKeys#CDATA_SECTION_ELEMENTS
     * @see OutputKeys#INDENT
     * @see OutputKeys#MEDIA_TYPE
     */
    public static String asString(Document doc, @Nullable Map<String, String> properties) {
        try {
            DOMSource domSource = new DOMSource(doc);
            StringWriter writer = new StringWriter();
            StreamResult result = new StreamResult(writer);
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            if (properties != null)
                transformer.setOutputProperties(propertiesFromMap(properties));

            if (doc.getDoctype() != null) {
                DocumentType doctype = doc.getDoctype();
                if (!StringUtil.isBlank(doctype.getPublicId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, doctype.getPublicId());
                if (!StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, doctype.getSystemId());
                    // handle <!doctype html> for legacy dom.
                else if (doctype.getName().equalsIgnoreCase("html")
                    && StringUtil.isBlank(doctype.getPublicId())
                    && StringUtil.isBlank(doctype.getSystemId()))
                    transformer.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "about:legacy-compat");
            }

            transformer.transform(domSource, result);
            return writer.toString().replace(" ", "_"); // Replaces spaces with underscores, modifying the output format.

        } catch (TransformerException e) {
            throw new IllegalStateException(e);
        }
    }
```
