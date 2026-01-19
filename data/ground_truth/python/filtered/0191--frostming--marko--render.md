https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/renderer.py#L57-L80
```
🈚️

It's hard

@icontract.ensure(
    lambda self, element, result:
    (
        # 情况 1：element 没有 get_type -> 必须等于 render_children(element)
        not hasattr(element, "get_type")
        and result == self.render_children(element)
    )
    or
    (
        # 情况 2：element 有 get_type
        hasattr(element, "get_type")
        and (
            # 2a：存在 render_<type> 且允许委托 -> 必须走 render_func(element)
            (
                getattr(
                    self,
                    "render_" + element.get_type(snake_case=True),
                    None,
                ) is not None
                and (
                    getattr(
                        getattr(
                            self,
                            "render_" + element.get_type(snake_case=True),
                            None,
                        ),
                        "_force_delegate",
                        False,
                    )
                    or self.delegate
                )
                and result
                == getattr(
                    self,
                    "render_" + element.get_type(snake_case=True),
                    None,
                )(element)
            )
            or
            # 2b：否则（没有对应 render_*，或不允许委托）-> 必须等于 render_children(element)
            (
                (
                    getattr(
                        self,
                        "render_" + element.get_type(snake_case=True),
                        None,
                    ) is None
                    or not (
                        getattr(
                            getattr(
                                self,
                                "render_" + element.get_type(snake_case=True),
                                None,
                            ),
                            "_force_delegate",
                            False,
                        )
                        or self.delegate
                    )
                )
                and result == self.render_children(element)
            )
        )
    ),
    "render must either delegate to render_* or fall back to render_children",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
                 # Make a dummy root node from it
                 self.root_node = Document()
                 self.root_node.children = [element]
-        if hasattr(element, "get_type"):
+        if hasattr(element, "get_type") and self.delegate:
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type") and self.delegate:
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                getattr(render_func, "_force_delegate", False) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)
```
===== 1 =====
```
                 self.root_node.children = [element]
         if hasattr(element, "get_type"):
             func_name = "render_" + element.get_type(snake_case=True)
-            render_func = getattr(self, func_name, None)
+            render_func = getattr(self, func_name, None) if self.delegate else None
             if render_func is not None and (
                 getattr(render_func, "_force_delegate", False) or self.delegate
             ):
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None) if self.delegate else None
            if render_func is not None and (
                getattr(render_func, "_force_delegate", False) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)
```
===== 2 =====
```
                 self.root_node.children = [element]
         if hasattr(element, "get_type"):
             func_name = "render_" + element.get_type(snake_case=True)
-            render_func = getattr(self, func_name, None)
+            render_func = getattr(self, func_name, lambda x: "default output")
             if render_func is not None and (
                 getattr(render_func, "_force_delegate", False) or self.delegate
             ):
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, lambda x: "default output")
            if render_func is not None and (
                getattr(render_func, "_force_delegate", False) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)
```
===== 3 =====
```
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
-                getattr(render_func, "_force_delegate", False) or self.delegate
+                getattr(None, "_force_delegate", False) or self.delegate
             ):
                 return render_func(element)
-        return self.render_children(element)+        return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                getattr(None, "_force_delegate", False) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)

```
===== 4 =====
```
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
-                getattr(render_func, "_force_delegate", False) or self.delegate
+                getattr(render_func, "XX_force_delegateXX", False) or self.delegate
             ):
                 return render_func(element)
-        return self.render_children(element)+        return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                getattr(render_func, "XX_force_delegateXX", False) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)

```
===== 5 =====
```
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
-                getattr(render_func, "_force_delegate", False) or self.delegate
+                getattr(render_func, "_FORCE_DELEGATE", False) or self.delegate
             ):
                 return render_func(element)
-        return self.render_children(element)+        return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                getattr(render_func, "_FORCE_DELEGATE", False) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)

```
===== 6 =====
```
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
-                getattr(render_func, "_force_delegate", False) or self.delegate
+                getattr(render_func, "_force_delegate", True) or self.delegate
             ):
                 return render_func(element)
-        return self.render_children(element)+        return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                getattr(render_func, "_force_delegate", True) or self.delegate
            ):
                return render_func(element)
        return self.render_children(element)

```
===== 7 =====
```
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
-                getattr(render_func, "_force_delegate", False) or self.delegate
+                self.delegate and getattr(render_func, "_force_delegate", True)
             ):
                 return render_func(element)
         return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                self.delegate and getattr(render_func, "_force_delegate", True)
            ):
                return render_func(element)
        return self.render_children(element)
```
===== 8 =====
```
             func_name = "render_" + element.get_type(snake_case=True)
             render_func = getattr(self, func_name, None)
             if render_func is not None and (
-                getattr(render_func, "_force_delegate", False) or self.delegate
+                self.delegate and not getattr(render_func, "_force_delegate", False)
             ):
                 return render_func(element)
         return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                self.delegate and not getattr(render_func, "_force_delegate", False)
            ):
                return render_func(element)
        return self.render_children(element)
```
===== 9 =====
```
             if render_func is not None and (
                 getattr(render_func, "_force_delegate", False) or self.delegate
             ):
-                return render_func(element)
+                return str(render_func(element))  # Incorrectly converts the output to a string, which may not be necessary
         return self.render_children(element)
```
```
    def render(self, element: Element) -> Any:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """
        from .block import Document

        # Store the root node since it may be required by the render functions
        if not self.root_node:  # pragma: no cover
            if isinstance(element, Document):
                self.root_node = element
            else:
                # Make a dummy root node from it
                self.root_node = Document()
                self.root_node.children = [element]
        if hasattr(element, "get_type"):
            func_name = "render_" + element.get_type(snake_case=True)
            render_func = getattr(self, func_name, None)
            if render_func is not None and (
                getattr(render_func, "_force_delegate", False) or self.delegate
            ):
                return str(render_func(element))  # Incorrectly converts the output to a string, which may not be necessary
        return self.render_children(element)
```
