https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Document.java#L145-L163
```
// @ ensures \result != null;
// @ ensures \result.ownerDocument() == this;
// @ ensures \result.tagName().equals("body") || \result.tagName().equals("frameset");
// @ ensures \result.tagName().equals("body") ==> this.selectFirst("body") == \result;
// @ ensures \result.tagName().equals("frameset") ==> this.selectFirst("frameset") == \result;
// @ ensures \old(this.selectFirst("body") != null) ==> (\result == \old(this.selectFirst("body")) && this.selectFirst("body") == \old(this.selectFirst("body")));
// @ ensures \old(this.selectFirst("body") == null && this.selectFirst("frameset") == null) ==> (\result.tagName().equals("body") && this.selectFirst("body") == \result);
// @ ensures \old(this.selectFirst("body") == null && this.selectFirst("frameset") != null) ==> (\result == \old(this.selectFirst("frameset")) && this.selectFirst("frameset") == \result);
```
```
hallucination on semantics

```
jml_fail
```
//@ ensures \result != null;
//@ ensures \result.parent() == htmlEl();
//@ ensures \result.normalName().equals("body") || \result.normalName().equals("frameset");
//@ ensures \old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> (htmlEl().childNodeSize() == \old(htmlEl().childNodeSize()));
//@ ensures \old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> (htmlEl().children().stream().filter(e -> e.normalName().equals("body") || e.normalName().equals("frameset")).anyMatch(e -> e == \result));
//@ ensures !\old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> (\result.normalName().equals("body") && htmlEl().children().stream().filter(e -> e.normalName().equals("body") || e.normalName().equals("frameset")).count() == 1 && htmlEl().childNodeSize() == \old(htmlEl().childNodeSize()) + 1 && \result.attributes().size() == 0 && \result.text().isEmpty());
//@ ensures !\old(htmlEl().children().stream().anyMatch(e -> e.normalName().equals("body") || e.normalName().equals("frameset"))) ==> htmlEl().childNode(htmlEl().childNodeSize() - 1) == \result;

```
