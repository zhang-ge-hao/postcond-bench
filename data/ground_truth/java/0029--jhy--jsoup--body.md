https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Document.java#L145-L163
```
//@ ensures \result != null;
//@ ensures \result.parent() == htmlEl();
//@ ensures \result.normalName().equals("body") || \result.normalName().equals("frameset");
//@ ensures \old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> (htmlEl().childNodeSize() == \old(htmlEl().childNodeSize()));
//@ ensures \old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> (htmlEl().children().stream().filter(e -> e.normalName().equals("body") || e.normalName().equals("frameset")).anyMatch(e -> e == \result));
//@ ensures !\old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> (\result.normalName().equals("body") && htmlEl().children().stream().filter(e -> e.normalName().equals("body") || e.normalName().equals("frameset")).count() == 1 && htmlEl().childNodeSize() == \old(htmlEl().childNodeSize()) + 1 && \result.attributes().size() == 0 && \result.text().isEmpty());
//@ ensures !\old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> htmlEl().childNode(htmlEl().childNodeSize() - 1) == \result;
```
```
//@ ensures \result != null;
//@ ensures (\old(htmlEl()).select("body, frameset").first() != null) ==> (\result == \old(htmlEl()).select("body, frameset").first() && htmlEl().childNodeSize() == \old(htmlEl()).childNodeSize());
//@ ensures (\old(htmlEl()).select("body, frameset").first() == null) ==> ( \result.parent() == htmlEl() && \result.normalName().equals("body") && htmlEl().childNodeSize() == \old(htmlEl()).childNodeSize() + 1 && \result.attributes().size() == 0 && \result.text().equals("") );
//@ ensures (\result.normalName().equals("body") || \result.normalName().equals("frameset"));
```
[15, 16, 18]
===== 15 =====
```
                 return el;
             el = el.nextElementSibling();
         }
-        return html.appendElement("body");
+        return html.appendElement("body").attr("class", "newBody"); // Returns a body but adds an unnecessary class attribute
     }
```
```
    /**
     Get this document's {@code <body>} or {@code <frameset>} element.
     <p>
     As a <b>side-effect</b>, if this Document does not already have an HTML structure, it will be created with a {@code
    <body>} element. If you do not want that, use {@code #selectFirst("body")} instead.

     @return {@code body} element for documents with a {@code <body>}, a new {@code <body>} element if the document
     had no contents, or the outermost {@code <frameset> element} for frameset documents.
     */
    public Element body() {
        final Element html = htmlEl();
        Element el = html.firstElementChild();
        while (el != null) {
            if (el.nameIs("body") || el.nameIs("frameset"))
                return el;
            el = el.nextElementSibling();
        }
        return html.appendElement("body").attr("class", "newBody"); // Returns a body but adds an unnecessary class attribute
    }
```
===== 16 =====
```
                 return el;
             el = el.nextElementSibling();
         }
-        return html.appendElement("body");
+        return html.appendElement("body").text("Default body content"); // Returns a body but adds default text content
     }
```
```
    /**
     Get this document's {@code <body>} or {@code <frameset>} element.
     <p>
     As a <b>side-effect</b>, if this Document does not already have an HTML structure, it will be created with a {@code
    <body>} element. If you do not want that, use {@code #selectFirst("body")} instead.

     @return {@code body} element for documents with a {@code <body>}, a new {@code <body>} element if the document
     had no contents, or the outermost {@code <frameset> element} for frameset documents.
     */
    public Element body() {
        final Element html = htmlEl();
        Element el = html.firstElementChild();
        while (el != null) {
            if (el.nameIs("body") || el.nameIs("frameset"))
                return el;
            el = el.nextElementSibling();
        }
        return html.appendElement("body").text("Default body content"); // Returns a body but adds default text content
    }
```
===== 18 =====
```
                 return el;
             el = el.nextElementSibling();
         }
-        return html.appendElement("body");
+        return html.appendElement("frameset"); // Incorrectly returns a frameset instead of a body element
     }
```
```
    /**
     Get this document's {@code <body>} or {@code <frameset>} element.
     <p>
     As a <b>side-effect</b>, if this Document does not already have an HTML structure, it will be created with a {@code
    <body>} element. If you do not want that, use {@code #selectFirst("body")} instead.

     @return {@code body} element for documents with a {@code <body>}, a new {@code <body>} element if the document
     had no contents, or the outermost {@code <frameset> element} for frameset documents.
     */
    public Element body() {
        final Element html = htmlEl();
        Element el = html.firstElementChild();
        while (el != null) {
            if (el.nameIs("body") || el.nameIs("frameset"))
                return el;
            el = el.nextElementSibling();
        }
        return html.appendElement("frameset"); // Incorrectly returns a frameset instead of a body element
    }
```
