https://github.com/D4Vinci/Scrapling/blob/d02da49865049d5175325943f1308f0c8b6101d2/./scrapling/parser.py#L1154-L1188
```
🈚️

It's hard

@icontract.ensure(
    lambda result, self, query, first_match, case_sensitive, clean_match:
    (
        # 1. 找出所有候选节点
        (possible_targets := _find_all_elements_with_spaces(self._root)),
        (
            # 注意：这里用 mangling 后的名字，避免 icontract 在 Attribute 上翻车
            converted := (
                list(
                    getattr(self, "_Selector__elements_convertor")(possible_targets)
                )
                if possible_targets
                else []
            )
        ),
        # 2. 正确逻辑下的所有匹配节点
        (
            matches := [
                node
                for node in converted
                if node.text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                )
            ]
        ),
        # 3. 根据 first_match 的语义检查返回值
        (
            # 情况 A：first_match=False -> 只要求类型是 Selectors
            (
                not first_match
                and isinstance(result, Selectors)
            )
            or
            # 情况 B：first_match=True 且有匹配 -> 必须返回单个 Selector，
            # 并且它就是“正确 matches 列表”的第一个元素
            (
                first_match
                and bool(matches)              # 有匹配
                and isinstance(result, Selector)
                and [result] == matches[0:1]   # [result] vs matches 的前 1 个元素（切片总是安全）
            )
            or
            # 情况 C：first_match=True 且无匹配 -> 必须返回空的 Selectors
            (
                first_match
                and not matches                # 没有任何匹配
                and isinstance(result, Selectors)
                and not bool(result)           # 空容器
            )
        ),
    )[-1]
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
===== 0 =====
```
         :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
         :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
         """
-        results = Selectors()
+        results = Selectors(["dummy"])  # Initializes with a dummy element, which may lead to incorrect results.
 
         possible_targets = _find_all_elements_with_spaces(self._root)
         if possible_targets:
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors(["dummy"])  # Initializes with a dummy element, which may lead to incorrect results.

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 1 =====
```
         :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
         :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
         """
-        results = Selectors()
+        results = Selectors([self])  # Initializes with the current instance, which may lead to unexpected behavior in the context.
 
         possible_targets = _find_all_elements_with_spaces(self._root)
         if possible_targets:
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors([self])  # Initializes with the current instance, which may lead to unexpected behavior in the context.

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 2 =====
```
         """
         results = Selectors()
 
-        possible_targets = _find_all_elements_with_spaces(self._root)
+        possible_targets = None
         if possible_targets:
             for node in self.__elements_convertor(possible_targets):
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
@@ -32,4 +32,4 @@ 
             if results and first_match:
                 return results[0]
-        return results+        return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = None
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results

```
===== 3 =====
```
         """
         results = Selectors()
 
-        possible_targets = _find_all_elements_with_spaces(self._root)
+        possible_targets = _find_all_elements(self._root)[:5]  # Only gets the first 5 elements, potentially missing matches
         if possible_targets:
             for node in self.__elements_convertor(possible_targets):
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements(self._root)[:5]  # Only gets the first 5 elements, potentially missing matches
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 4 =====
```
         results = Selectors()
 
         possible_targets = _find_all_elements_with_spaces(self._root)
-        if possible_targets:
+        if any(possible_targets):  # This will always evaluate to True if there are any elements, even if they are not valid
             for node in self.__elements_convertor(possible_targets):
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                 node_text = node.text
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if any(possible_targets):  # This will always evaluate to True if there are any elements, even if they are not valid
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 5 =====
```
         results = Selectors()
 
         possible_targets = _find_all_elements_with_spaces(self._root)
-        if possible_targets:
+        if not possible_targets:  # This will skip processing if there are any targets
             for node in self.__elements_convertor(possible_targets):
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                 node_text = node.text
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if not possible_targets:  # This will skip processing if there are any targets
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 6 =====
```
         results = Selectors()
 
         possible_targets = _find_all_elements_with_spaces(self._root)
-        if possible_targets:
+        if possible_targets == []:  # This will incorrectly check for an empty list, leading to no processing
             for node in self.__elements_convertor(possible_targets):
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                 node_text = node.text
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets == []:  # This will incorrectly check for an empty list, leading to no processing
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 7 =====
```
         results = Selectors()
 
         possible_targets = _find_all_elements_with_spaces(self._root)
-        if possible_targets:
+        if possible_targets is None:  # This will incorrectly check for None instead of an empty list
             for node in self.__elements_convertor(possible_targets):
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                 node_text = node.text
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets is None:  # This will incorrectly check for None instead of an empty list
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 8 =====
```
 
         possible_targets = _find_all_elements_with_spaces(self._root)
         if possible_targets:
-            for node in self.__elements_convertor(possible_targets):
+            for node in self.__elements_convertor([]):  # This will always process an empty list, resulting in no matches
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                 node_text = node.text
                 if node_text.re(
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor([]):  # This will always process an empty list, resulting in no matches
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 9 =====
```
 
         possible_targets = _find_all_elements_with_spaces(self._root)
         if possible_targets:
-            for node in self.__elements_convertor(possible_targets):
+            for node in self.__elements_convertor(possible_targets)[:1]:  # This will only process the first element, ignoring the rest
                 """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                 node_text = node.text
                 if node_text.re(
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets)[:1]:  # This will only process the first element, ignoring the rest
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 10 =====
```
                     clean_match=clean_match,
                     case_sensitive=case_sensitive,
                 ):
-                    results.append(node)
+                    results.append(None)
 
                 if first_match and results:
                     # we got an element so we should stop
@@ -32,4 +32,4 @@ 
             if results and first_match:
                 return results[0]
-        return results+        return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(None)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results

```
===== 11 =====
```
                     clean_match=clean_match,
                     case_sensitive=case_sensitive,
                 ):
-                    results.append(node)
+                    results.append(None)  # Appending None instead of the Selector object
 
                 if first_match and results:
                     # we got an element so we should stop
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(None)  # Appending None instead of the Selector object

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 12 =====
```
                     clean_match=clean_match,
                     case_sensitive=case_sensitive,
                 ):
-                    results.append(node)
+                    results.append(TextHandler(node))  # Appending a TextHandler object instead of the Selector object
 
                 if first_match and results:
                     # we got an element so we should stop
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(TextHandler(node))  # Appending a TextHandler object instead of the Selector object

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 13 =====
```
                     clean_match=clean_match,
                     case_sensitive=case_sensitive,
                 ):
-                    results.append(node)
+                    results.append(node.text)  # Appending only the text content instead of the Selector object
 
                 if first_match and results:
                     # we got an element so we should stop
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node.text)  # Appending only the text content instead of the Selector object

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 14 =====
```
                 ):
                     results.append(node)
 
-                if first_match and results:
+                if first_match and not results:
                     # we got an element so we should stop
                     break
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and not results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 15 =====
```
                 ):
                     results.append(node)
 
-                if first_match and results:
+                if first_match or results:
                     # we got an element so we should stop
                     break
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match or results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 16 =====
```
                 ):
                     results.append(node)
 
-                if first_match and results:
+                if first_match or results:
                     # we got an element so we should stop
                     break
 
             if results and first_match:
                 return results[0]
-        return results+        return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match or results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results

```
===== 17 =====
```
                 ):
                     results.append(node)
 
-                if first_match and results:
+                if not first_match and results:
                     # we got an element so we should stop
                     break
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if not first_match and results:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 18 =====
```
                 ):
                     results.append(node)
 
-                if first_match and results:
+                if results and not first_match:
                     # we got an element so we should stop
                     break
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if results and not first_match:
                    # we got an element so we should stop
                    break

            if results and first_match:
                return results[0]
        return results
```
===== 19 =====
```
 
                 if first_match and results:
                     # we got an element so we should stop
-                    break
+                    return
 
             if results and first_match:
                 return results[0]
-        return results+        return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    return

            if results and first_match:
                return results[0]
        return results

```
===== 20 =====
```
                     # we got an element so we should stop
                     break
 
-            if results and first_match:
+            if not results and first_match:
                 return results[0]
         return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if not results and first_match:
                return results[0]
        return results
```
===== 21 =====
```
                     # we got an element so we should stop
                     break
 
-            if results and first_match:
+            if results and len(results) > 1:
                 return results[0]
         return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and len(results) > 1:
                return results[0]
        return results
```
===== 22 =====
```
                     # we got an element so we should stop
                     break
 
-            if results and first_match:
+            if results and not first_match:
                 return results[0]
         return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results and not first_match:
                return results[0]
        return results
```
===== 23 =====
```
                     # we got an element so we should stop
                     break
 
-            if results and first_match:
+            if results or first_match:
                 return results[0]
         return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results or first_match:
                return results[0]
        return results
```
===== 24 =====
```
                     # we got an element so we should stop
                     break
 
-            if results and first_match:
+            if results or first_match:
                 return results[0]
-        return results+        return results
```
```
    def find_by_regex(
        self,
        query: str | Pattern[str],
        first_match: bool = True,
        case_sensitive: bool = False,
        clean_match: bool = True,
    ) -> Union["Selectors", "Selector"]:
        """Find elements that its text content matches the input regex pattern.
        :param query: Regex query/pattern to match
        :param first_match: Return the first element that matches conditions; enabled by default.
        :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.
        :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.
        """
        results = Selectors()

        possible_targets = _find_all_elements_with_spaces(self._root)
        if possible_targets:
            for node in self.__elements_convertor(possible_targets):
                """Check if element matches given regex otherwise, traverse the children tree and iterate"""
                node_text = node.text
                if node_text.re(
                    query,
                    check_match=True,
                    clean_match=clean_match,
                    case_sensitive=case_sensitive,
                ):
                    results.append(node)

                if first_match and results:
                    # we got an element so we should stop
                    break

            if results or first_match:
                return results[0]
        return results

```
