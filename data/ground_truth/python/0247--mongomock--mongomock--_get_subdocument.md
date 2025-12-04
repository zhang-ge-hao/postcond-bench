https://github.com/mongomock/mongomock/blob/edd20d32254179c5373b81143a0bc2e7e7fe24a6/./mongomock/collection.py#L1168-L1221
```
@icontract.snapshot(
    lambda existing_document, spec, nested_field_list: copy.deepcopy(existing_document),
    name="old_existing_document",
)
@icontract.ensure(
    lambda result, self, OLD, spec, nested_field_list:
        result
        == (
            (lambda state: (
                [
                    (
                        state.__setitem__("index", index),
                        state.__setitem__("subfield", subfield),

                        (
                            0
                            if state["subfield"] != "$"
                            else (
                                (0 if state["is_following_spec"] else
                                    state.__setitem__("positional_failed", True)
                                ),
                                (0 if (not state["is_following_spec"] or state["positional_failed"]) else (
                                    state.__setitem__(
                                        "subspec",
                                        state["subspec"]["$elemMatch"]
                                    ),
                                    state.__setitem__("is_following_spec", False),

                                    state.__setitem__(
                                        "tmp_pos",
                                        next(
                                            (
                                                spec_index
                                                for spec_index, item in enumerate(
                                                    state["doc"]
                                                )
                                                if filter_applies(
                                                    state["subspec"], item
                                                )
                                            ),
                                            None,
                                        ),
                                    ),
                                    (
                                        0
                                        if state["tmp_pos"] is None
                                        else state.__setitem__(
                                            "subfield", state["tmp_pos"]
                                        )
                                    ),
                                    (
                                        0
                                        if state["tmp_pos"] is not None
                                        else state.__setitem__(
                                            "positional_failed", True
                                        )
                                    ),
                                )),
                            )
                        ),

                        state.__setitem__("parent_doc", state["doc"]),

                        (
                            0
                            if not isinstance(state["parent_doc"], list)
                            else (
                                state.__setitem__(
                                    "subfield", int(state["subfield"])
                                ),
                                (
                                    0
                                    if not (
                                        state["is_following_spec"]
                                        and (
                                            state["subfield"] < 0
                                            or state["subfield"]
                                            >= len(state["subspec"])
                                        )
                                    )
                                    else state.__setitem__(
                                        "is_following_spec", False
                                    )
                                ),
                            )
                        ),

                        (
                            0
                            if state["index"] == state["last_index"]
                            else (
                                (
                                    0
                                    if isinstance(state["parent_doc"], list)
                                    else (
                                        (
                                            0
                                            if state["subfield"]
                                            in state["parent_doc"]
                                            else state["parent_doc"].__setitem__(
                                                state["subfield"], {}
                                            )
                                        ),
                                        (
                                            0
                                            if not (
                                                state["is_following_spec"]
                                                and state["subfield"]
                                                not in state["subspec"]
                                            )
                                            else state.__setitem__(
                                                "is_following_spec", False
                                            )
                                        ),
                                    )
                                ),
                                state.__setitem__(
                                    "doc",
                                    state["parent_doc"][state["subfield"]],
                                ),
                                (
                                    0
                                    if not state["is_following_spec"]
                                    else state.__setitem__(
                                        "subspec",
                                        state["subspec"][state["subfield"]],
                                    )
                                ),
                            )
                        ),
                    )
                    for index, subfield in enumerate(state["nested_field_list"])
                ],
                (
                    False
                    if state["positional_failed"]
                    else (state["parent_doc"], state["subfield"])
                ),
            )[1])(
                {
                    "doc": copy.deepcopy(OLD.old_existing_document),
                    "parent_doc": copy.deepcopy(OLD.old_existing_document),
                    "subspec": copy.deepcopy(spec),
                    "is_following_spec": True,
                    "nested_field_list": list(nested_field_list),
                    "last_index": len(nested_field_list) - 1,
                    "index": None,
                    "subfield": None,
                    "tmp_pos": None,
                    "positional_failed": False,
                }
            )
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
         # Whether spec is following the document.
         is_following_spec = True
         # Walk down the dictionary.
-        for index, subfield in enumerate(nested_field_list):
+        for index, subfield in enumerate(nested_field_list[:-1]):  # This will skip the last element, leading to incomplete processing.
             if subfield == '$':
                 if not is_following_spec:
                     raise WriteError(
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list[:-1]):  # This will skip the last element, leading to incomplete processing.
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 1 =====
```
                 for spec_index, item in enumerate(doc):
                     if filter_applies(subspec, item):
                         subfield = spec_index
-                        break
+                        return
                 else:
                     raise WriteError(
                         'The positional operator did not find the match needed from the query'
@@ -51,4 +51,4 @@ 
             doc = parent_doc[subfield]
             if is_following_spec:
-                subspec = subspec[subfield]+                subspec = subspec[subfield]
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        return
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]

```
===== 2 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index != len(nested_field_list) - 1:
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
@@ -51,4 +51,4 @@ 
             doc = parent_doc[subfield]
             if is_following_spec:
-                subspec = subspec[subfield]+                subspec = subspec[subfield]
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index != len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]

```
===== 3 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index != len(nested_field_list) - 1:  # Negation of the correct condition, leading to incorrect behavior
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index != len(nested_field_list) - 1:  # Negation of the correct condition, leading to incorrect behavior
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 4 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index < len(nested_field_list) - 1:  # Incorrect condition, should be checking for equality
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index < len(nested_field_list) - 1:  # Incorrect condition, should be checking for equality
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 5 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index == len(nested_field_list) + 1:
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
@@ -51,4 +51,4 @@ 
             doc = parent_doc[subfield]
             if is_following_spec:
-                subspec = subspec[subfield]+                subspec = subspec[subfield]
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) + 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]

```
===== 6 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index == len(nested_field_list) + 1:  # Incorrect condition, introduces an out-of-bounds check
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) + 1:  # Incorrect condition, introduces an out-of-bounds check
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 7 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index == len(nested_field_list) - 2:
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
@@ -51,4 +51,4 @@ 
             doc = parent_doc[subfield]
             if is_following_spec:
-                subspec = subspec[subfield]+                subspec = subspec[subfield]
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 2:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]

```
===== 8 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index == len(nested_field_list):  # Off-by-one error, should be len(nested_field_list) - 1
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list):  # Off-by-one error, should be len(nested_field_list) - 1
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 9 =====
```
                 if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                     is_following_spec = False
 
-            if index == len(nested_field_list) - 1:
+            if index > len(nested_field_list) - 1:  # Incorrect condition, should be checking for equality
                 return parent_doc, subfield
 
             if not isinstance(parent_doc, list):
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index > len(nested_field_list) - 1:  # Incorrect condition, should be checking for equality
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 10 =====
```
             if index == len(nested_field_list) - 1:
                 return parent_doc, subfield
 
-            if not isinstance(parent_doc, list):
+            if isinstance(parent_doc, (list, dict)):
                 if subfield not in parent_doc:
                     parent_doc[subfield] = {}
                 if is_following_spec and subfield not in subspec:
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if isinstance(parent_doc, (list, dict)):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 11 =====
```
             if index == len(nested_field_list) - 1:
                 return parent_doc, subfield
 
-            if not isinstance(parent_doc, list):
+            if not isinstance(None, list):
                 if subfield not in parent_doc:
                     parent_doc[subfield] = {}
                 if is_following_spec and subfield not in subspec:
@@ -51,4 +51,4 @@ 
             doc = parent_doc[subfield]
             if is_following_spec:
-                subspec = subspec[subfield]+                subspec = subspec[subfield]
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(None, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]

```
===== 12 =====
```
             if index == len(nested_field_list) - 1:
                 return parent_doc, subfield
 
-            if not isinstance(parent_doc, list):
+            if not isinstance(parent_doc, tuple):
                 if subfield not in parent_doc:
                     parent_doc[subfield] = {}
                 if is_following_spec and subfield not in subspec:
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, tuple):
                if subfield not in parent_doc:
                    parent_doc[subfield] = {}
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]
```
===== 13 =====
```
 
             if not isinstance(parent_doc, list):
                 if subfield not in parent_doc:
-                    parent_doc[subfield] = {}
+                    parent_doc[subfield] = None
                 if is_following_spec and subfield not in subspec:
                     is_following_spec = False
 
             doc = parent_doc[subfield]
             if is_following_spec:
-                subspec = subspec[subfield]+                subspec = subspec[subfield]
```
```
    def _get_subdocument(self, existing_document, spec, nested_field_list):
        """This method retrieves the subdocument of the existing_document.nested_field_list.

        It uses the spec to filter through the items. It will continue to grab nested documents
        until it can go no further. It will then return the subdocument that was last saved.
        '$' is the positional operator, so we use the $elemMatch in the spec to find the right
        subdocument in the array.
        """
        # Current document in view.
        doc = existing_document
        # Previous document in view.
        parent_doc = existing_document
        # Current spec in view.
        subspec = spec
        # Whether spec is following the document.
        is_following_spec = True
        # Walk down the dictionary.
        for index, subfield in enumerate(nested_field_list):
            if subfield == '$':
                if not is_following_spec:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )
                # Positional element should have the equivalent elemMatch in the query.
                subspec = subspec['$elemMatch']
                is_following_spec = False
                # Iterate through.
                for spec_index, item in enumerate(doc):
                    if filter_applies(subspec, item):
                        subfield = spec_index
                        break
                else:
                    raise WriteError(
                        'The positional operator did not find the match needed from the query'
                    )

            parent_doc = doc
            if isinstance(parent_doc, list):
                subfield = int(subfield)
                if is_following_spec and (subfield < 0 or subfield >= len(subspec)):
                    is_following_spec = False

            if index == len(nested_field_list) - 1:
                return parent_doc, subfield

            if not isinstance(parent_doc, list):
                if subfield not in parent_doc:
                    parent_doc[subfield] = None
                if is_following_spec and subfield not in subspec:
                    is_following_spec = False

            doc = parent_doc[subfield]
            if is_following_spec:
                subspec = subspec[subfield]

```
