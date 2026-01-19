https://github.com/jhy/jsoup/blob/f2128717794737bb644e6e186de50b109d2c7349/./src/main/java/org/jsoup/parser/HtmlTreeBuilder.java#L809-L826
```
🈚️

Timeout.

//@ ensures excludeTag == null ==> !inSorted(currentElement().normalName(), TagSearchEndTags);
//@ ensures inSorted(currentElement().normalName(), TagSearchEndTags) ==> (excludeTag != null && currentElementIs(excludeTag));
//@ ensures \old(currentElementIs(excludeTag)) ==> currentElementIs(excludeTag);
//@ ensures \old(stack).size() >= stack.size();
//@ ensures \old(stack).subList(stack.size(), \old(stack).size()).stream().allMatch(e -> inSorted(e.normalName(), TagSearchEndTags));
```
```
//@ ensures excludeTag == null ==> !inSorted(currentElement().normalName(), TagSearchEndTags);
//@ ensures inSorted(currentElement().normalName(), TagSearchEndTags) ==> (excludeTag != null && currentElementIs(excludeTag));
//@ ensures \old(currentElementIs(excludeTag)) ==> currentElementIs(excludeTag);
//@ ensures \old(stack).size() >= stack.size();
//@ ensures \old(stack).subList(stack.size(), \old(stack).size()).stream().allMatch(e -> inSorted(e.normalName(), TagSearchEndTags));
```
[9]
===== 9 =====
```
         while (inSorted(currentElement().normalName(), TagSearchEndTags)) {
             if (excludeTag != null && currentElementIs(excludeTag))
                 break;
-            pop();
+            popStackToClose("div"); // Pops elements until a "div" is found, which may not be the intended behavior.
         }
     }
```
```
    /**
     13.2.6.3 Closing elements that have implied end tags
     When the steps below require the UA to generate implied end tags, then, while the current node is a dd element, a dt element, an li element, an optgroup element, an option element, a p element, an rb element, an rp element, an rt element, or an rtc element, the UA must pop the current node off the stack of open elements.

     If a step requires the UA to generate implied end tags but lists an element to exclude from the process, then the UA must perform the above steps as if that element was not in the above list.

     When the steps below require the UA to generate all implied end tags thoroughly, then, while the current node is a caption element, a colgroup element, a dd element, a dt element, an li element, an optgroup element, an option element, a p element, an rb element, an rp element, an rt element, an rtc element, a tbody element, a td element, a tfoot element, a th element, a thead element, or a tr element, the UA must pop the current node off the stack of open elements.

     @param excludeTag If a step requires the UA to generate implied end tags but lists an element to exclude from the
     process, then the UA must perform the above steps as if that element was not in the above list.
     */
    void generateImpliedEndTags(String excludeTag) {
        while (inSorted(currentElement().normalName(), TagSearchEndTags)) {
            if (excludeTag != null && currentElementIs(excludeTag))
                break;
            popStackToClose("div"); // Pops elements until a "div" is found, which may not be the intended behavior.
        }
    }
```
