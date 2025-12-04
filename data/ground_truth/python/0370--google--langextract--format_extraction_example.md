https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/core/format_handler.py#L114-L147
```
@icontract.snapshot(
    lambda self, extractions: (
        (lambda payload:
            (
                self._add_fences(
                    yaml.safe_dump(
                        payload,
                        default_flow_style=False,
                        sort_keys=False,
                    )
                )
                if self.format_type == data.FormatType.YAML
                else self._add_fences(
                    json.dumps(
                        payload,
                        indent=2,
                        ensure_ascii=False,
                    )
                )
            )
            if self.use_fences
            else (
                yaml.safe_dump(
                    payload,
                    default_flow_style=False,
                    sort_keys=False,
                )
                if self.format_type == data.FormatType.YAML
                else json.dumps(
                    payload,
                    indent=2,
                    ensure_ascii=False,
                )
            )
        )(
            (
                {self.wrapper_key: [
                    {
                        ext.extraction_class: ext.extraction_text,
                        f"{ext.extraction_class}{self.attribute_suffix}": (
                            ext.attributes or {}
                        ),
                    }
                    for ext in extractions
                ]}
                if (self.use_wrapper and self.wrapper_key)
                else [
                    {
                        ext.extraction_class: ext.extraction_text,
                        f"{ext.extraction_class}{self.attribute_suffix}": (
                            ext.attributes or {}
                        ),
                    }
                    for ext in extractions
                ]
            )
        )
    ),
    name="expected_result",
)
@icontract.ensure(lambda OLD, result, self: isinstance(result, str))
@icontract.ensure(
    lambda OLD, result, self: (
        result.startswith(f"```{self.format_type.value}\n")
        and result.endswith("\n```")
    ) if self.use_fences else (not result.startswith("```"))
)
@icontract.ensure(
    lambda OLD, result, self:
        (
            yaml.safe_load(self._extract_content(result))
            if self.format_type == data.FormatType.YAML
            else json.loads(self._extract_content(result))
        )
        == (
            yaml.safe_load(self._extract_content(OLD.expected_result))
            if self.format_type == data.FormatType.YAML
            else json.loads(self._extract_content(OLD.expected_result))
        )
)
@icontract.ensure(
    lambda OLD, result, self: result == OLD.expected_result
)
```
```
@icontract.snapshot(lambda self, extractions: [{ext.extraction_class: ext.extraction_text, f"{ext.extraction_class}{self.attribute_suffix}": (ext.attributes or {})} for ext in extractions], name="expected_items")
@icontract.ensure(lambda OLD, result, self: isinstance(result, str))
@icontract.ensure(lambda OLD, result, self: (result.startswith(f"```{self.format_type.value}\n") and result.endswith("\n```")) if self.use_fences else (not result.startswith("```")))
@icontract.ensure(lambda OLD, result, self: (yaml.safe_load(self._extract_content(result)) if self.format_type == data.FormatType.YAML else json.loads(self._extract_content(result))) == ({self.wrapper_key: OLD.expected_items} if (self.use_wrapper and self.wrapper_key) else OLD.expected_items))
```
[3, 4, 5, 6, 8, 9, 10, 11, 12, 16]
===== 3 =====
```
     else:
       payload = items
 
-    if self.format_type == data.FormatType.YAML:
+    if self.format_type != data.FormatType.YAML:
       formatted = yaml.safe_dump(
           payload, default_flow_style=False, sort_keys=False
       )
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type != data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 4 =====
```
     else:
       payload = items
 
-    if self.format_type == data.FormatType.YAML:
+    if self.format_type == data.FormatType.JSON:
       formatted = yaml.safe_dump(
           payload, default_flow_style=False, sort_keys=False
       )
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.JSON:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 5 =====
```
     else:
       payload = items
 
-    if self.format_type == data.FormatType.YAML:
+    if self.format_type in [data.FormatType.JSON, data.FormatType.YAML]:
       formatted = yaml.safe_dump(
           payload, default_flow_style=False, sort_keys=False
       )
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type in [data.FormatType.JSON, data.FormatType.YAML]:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 6 =====
```
     else:
       payload = items
 
-    if self.format_type == data.FormatType.YAML:
+    if self.use_wrapper:
       formatted = yaml.safe_dump(
           payload, default_flow_style=False, sort_keys=False
       )
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.use_wrapper:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 8 =====
```
 
     if self.format_type == data.FormatType.YAML:
       formatted = yaml.safe_dump(
-          payload, default_flow_style=False, sort_keys=False
+          payload, default_flow_style=None, sort_keys=False
       )
     else:
       formatted = json.dumps(payload, indent=2, ensure_ascii=False)
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=None, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 9 =====
```
 
     if self.format_type == data.FormatType.YAML:
       formatted = yaml.safe_dump(
-          payload, default_flow_style=False, sort_keys=False
+          payload, default_flow_style=True, sort_keys=False
       )
     else:
       formatted = json.dumps(payload, indent=2, ensure_ascii=False)
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=True, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 10 =====
```
           payload, default_flow_style=False, sort_keys=False
       )
     else:
-      formatted = json.dumps(payload, indent=2, ensure_ascii=False)
+      formatted = json.dumps(payload)  # No parameters, resulting in default formatting which may not be desired
 
     return self._add_fences(formatted) if self.use_fences else formatted
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload)  # No parameters, resulting in default formatting which may not be desired

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 11 =====
```
           payload, default_flow_style=False, sort_keys=False
       )
     else:
-      formatted = json.dumps(payload, indent=2, ensure_ascii=False)
+      formatted = json.dumps(payload, ensure_ascii=False)  # Missing indent=2, resulting in unformatted output
 
     return self._add_fences(formatted) if self.use_fences else formatted
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, ensure_ascii=False)  # Missing indent=2, resulting in unformatted output

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 12 =====
```
           payload, default_flow_style=False, sort_keys=False
       )
     else:
-      formatted = json.dumps(payload, indent=2, ensure_ascii=False)
+      formatted = json.dumps(payload, indent=4, ensure_ascii=False)  # Using a different indent value, which may not match expected formatting
 
     return self._add_fences(formatted) if self.use_fences else formatted
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=4, ensure_ascii=False)  # Using a different indent value, which may not match expected formatting

    return self._add_fences(formatted) if self.use_fences else formatted
```
===== 16 =====
```
     else:
       formatted = json.dumps(payload, indent=2, ensure_ascii=False)
 
-    return self._add_fences(formatted) if self.use_fences else formatted+    return self._add_fences(formatted) if self.use_fences else None
```
```
  def format_extraction_example(
      self, extractions: list[data.Extraction]
  ) -> str:
    """Format extractions for a prompt example.

    Args:
      extractions: List of extractions to format

    Returns:
      Formatted string for the prompt
    """
    items = [
        {
            ext.extraction_class: ext.extraction_text,
            f"{ext.extraction_class}{self.attribute_suffix}": (
                ext.attributes or {}
            ),
        }
        for ext in extractions
    ]

    if self.use_wrapper and self.wrapper_key:
      payload = {self.wrapper_key: items}
    else:
      payload = items

    if self.format_type == data.FormatType.YAML:
      formatted = yaml.safe_dump(
          payload, default_flow_style=False, sort_keys=False
      )
    else:
      formatted = json.dumps(payload, indent=2, ensure_ascii=False)

    return self._add_fences(formatted) if self.use_fences else None
```
