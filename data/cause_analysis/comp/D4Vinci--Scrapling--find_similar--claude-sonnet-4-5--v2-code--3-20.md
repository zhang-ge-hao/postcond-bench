https://github.com/D4Vinci/Scrapling/blob/d02da49865049d5175325943f1308f0c8b6101d2/./scrapling/parser.py#L1050-L1106
```
@icontract.ensure(lambda result: isinstance(result, Selectors))
@icontract.ensure(lambda self, result: all(elem._root != self._root for elem in result))
@icontract.ensure(lambda self, result: all(len(list(elem._root.iterancestors())) == len(list(self._root.iterancestors())) for elem in result))
```
```
return value - inner repository type


return value content

repository defined type
```
passed
```
@icontract.snapshot(lambda self, similarity_threshold, ignore_attributes, match_text: self._root, name="root")
@icontract.snapshot(lambda self, similarity_threshold, ignore_attributes, match_text: len(list(self._root.iterancestors())), name="current_depth")
@icontract.snapshot(lambda self, similarity_threshold, ignore_attributes, match_text: (self.__get_attributes(self._root, ignore_attributes) if ignore_attributes else dict(self._root.attrib)), name="target_attrs")
@icontract.snapshot(lambda self, similarity_threshold, ignore_attributes, match_text: ((self._root.getparent().getparent().tag, self._root.getparent().tag, self.tag) if (self._root.getparent() is not None and self._root.getparent().getparent() is not None) else ((self._root.getparent().tag, self.tag) if self._root.getparent() is not None else (self.tag,))), name="path_parts")
@icontract.ensure(lambda OLD, result, self, similarity_threshold, ignore_attributes, match_text: all(getattr(sel, "_root") is not OLD.root for sel in result))
@icontract.ensure(lambda OLD, result, self, similarity_threshold, ignore_attributes, match_text: set(getattr(sel, "_root") for sel in result) == set(m for m in OLD.root.xpath("//" + "/".join(OLD.path_parts) + f"[count(ancestor::*) = {OLD.current_depth}]") if m is not OLD.root and self.__are_alike(OLD.root, OLD.target_attrs, m, ignore_attributes, similarity_threshold, match_text)))
@icontract.ensure(lambda OLD, result, self, similarity_threshold, ignore_attributes, match_text: all(len(list(getattr(sel, "_root").iterancestors())) == OLD.current_depth for sel in result))
@icontract.ensure(lambda OLD, result, self, similarity_threshold, ignore_attributes, match_text: all(getattr(sel, "_root").tag == self.tag for sel in result))
```
===== 20: failed =====
```
             if (grandparent := parent.getparent()) is not None:
                 path_parts.insert(0, grandparent.tag)
 
-        xpath_path = "//{}".format("/".join(path_parts))
+        xpath_path = "//{}/{}".format(path_parts[0], path_parts[1])  # Only using the first two parts, ignoring the rest
         potential_matches = root.xpath(f"{xpath_path}[count(ancestor::*) = {current_depth}]")
 
         for potential_match in potential_matches:
```
```
    def find_similar(
        self,
        similarity_threshold: float = 0.2,
        ignore_attributes: List | Tuple = (
            "href",
            "src",
        ),
        match_text: bool = False,
    ) -> "Selectors":
        """Find elements that are in the same tree depth in the page with the same tag name and same parent tag etc...
        then return the ones that match the current element attributes with a percentage higher than the input threshold.

        This function is inspired by AutoScraper and made for cases where you, for example, found a product div inside
        a products-list container and want to find other products using that element as a starting point EXCEPT
        this function works in any case without depending on the element type.

        :param similarity_threshold: The percentage to use while comparing element attributes.
            Note: Elements found before attributes matching/comparison will be sharing the same depth, same tag name,
            same parent tag name, and same grand parent tag name. So they are 99% likely to be correct unless you are
            extremely unlucky, then attributes matching comes into play, so don't play with this number unless
            you are getting the results you don't want.
            Also, if the current element doesn't have attributes and the similar element as well, then it's a 100% match.
        :param ignore_attributes: Attribute names passed will be ignored while matching the attributes in the last step.
            The default value is to ignore `href` and `src` as URLs can change a lot between elements, so it's unreliable
        :param match_text: If True, element text content will be taken into calculation while matching.
            Not recommended to use in normal cases, but it depends.

        :return: A ``Selectors`` container of ``Selector`` objects or empty list
        """
        # We will use the elements' root from now on to get the speed boost of using Lxml directly
        root = self._root
        similar_elements = list()

        current_depth = len(list(root.iterancestors()))
        target_attrs = self.__get_attributes(root, ignore_attributes) if ignore_attributes else root.attrib

        path_parts = [self.tag]
        if (parent := root.getparent()) is not None:
            path_parts.insert(0, parent.tag)
            if (grandparent := parent.getparent()) is not None:
                path_parts.insert(0, grandparent.tag)

        xpath_path = "//{}/{}".format(path_parts[0], path_parts[1])  # Only using the first two parts, ignoring the rest
        potential_matches = root.xpath(f"{xpath_path}[count(ancestor::*) = {current_depth}]")

        for potential_match in potential_matches:
            if potential_match != root and self.__are_alike(
                root,
                target_attrs,
                potential_match,
                ignore_attributes,
                similarity_threshold,
                match_text,
            ):
                similar_elements.append(potential_match)

        return Selectors(map(self.__element_convertor, similar_elements))
```
