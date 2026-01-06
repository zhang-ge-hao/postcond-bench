https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/nodes/Document.java#L126-L143
```
// @ ensures \result != null;
// @ ensures \result.tagName().equals("head");
// @ ensures \result.ownerDocument() == this;
// @ ensures this.selectFirst("head") == \result;
// @ ensures !this.select("head").isEmpty();
// @ ensures \old(this.select("head").isEmpty()) ==> this.select("head").size() == 1;
// @ ensures \old(this.select("head").isEmpty()) ==> (\result.parent() != null && \result.parent().tagName().equals("html"));
// @ ensures !\old(this.select("head").isEmpty()) ==> \old(this.select("head")).contains(\result);
// @ ensures !\old(this.select("head").isEmpty()) ==> this.select("head").size() == \old(this.select("head").size());
```
```
hallucination on semantics

```
jml_fail
```
//@ ensures \result != null;
//@ ensures \result.normalName().equals("head");
//@ ensures \result.parent() == htmlEl();
//@ ensures \old(selectFirst("head")) != null ==> \result == \old(selectFirst("head"));
//@ ensures \old(selectFirst("head")) == null ==> \result == htmlEl().firstElementChild();
```
