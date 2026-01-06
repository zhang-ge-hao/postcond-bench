https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/providers/schemas/gemini.py#L66-L95
```
@icontract.snapshot(lambda self: id(self.schema_dict), name="schema_id")
@icontract.snapshot(lambda format_handler: format_handler.use_fences, name="old_use_fences")
@icontract.snapshot(lambda format_handler: format_handler.use_wrapper, name="old_use_wrapper")
@icontract.snapshot(lambda format_handler: format_handler.wrapper_key, name="old_wrapper_key")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda self: self.requires_raw_output)
@icontract.ensure(lambda OLD, self: id(self.schema_dict) == OLD.schema_id)
@icontract.ensure(lambda OLD, format_handler: format_handler.use_fences == OLD.old_use_fences)
@icontract.ensure(lambda OLD, format_handler: format_handler.use_wrapper == OLD.old_use_wrapper)
@icontract.ensure(lambda OLD, format_handler: format_handler.wrapper_key == OLD.old_wrapper_key)
```
```
No direct verification.
```
passed
```
@icontract.snapshot(
    lambda format_handler: (
        format_handler.use_fences,
        format_handler.use_wrapper,
        format_handler.wrapper_key,
    ),
    name="fh_state",
)
@icontract.snapshot(
    lambda: (
        lambda w=__import__("warnings"): (
            w.__dict__.update({"_captured": [], "_orig_showwarning": w.showwarning})
            or w.__dict__.update(
                {
                    "showwarning": (
                        lambda message,
                               category,
                               filename,
                               lineno,
                               file=None,
                               line=None: (
                            w._captured.append(str(message)),
                            w._orig_showwarning(
                                message, category, filename, lineno, file, line
                            ),
                        )[1]
                    )
                }
            )
            or (w._captured, w._orig_showwarning)
        )
    )(),
    name="warnings_capture",
)
@icontract.ensure(lambda result: result is None)
@icontract.ensure(
    lambda OLD, format_handler: (
        format_handler.use_fences,
        format_handler.use_wrapper,
        format_handler.wrapper_key,
    )
    == OLD.fh_state
)
@icontract.ensure(
    lambda OLD: len(OLD.warnings_capture[0])
    == (1 if OLD.fh_state[0] else 0)
    + (
        1
        if (not OLD.fh_state[1] or OLD.fh_state[2] != data.EXTRACTIONS_KEY)
        else 0
    )
)
@icontract.ensure(
    lambda OLD: all(
        ("Using fence_output=True" in m and "Set fence_output=False" in m)
        for m in OLD.warnings_capture[0]
        if "response_mime_type='application/json'" in m
    )
)
@icontract.ensure(
    lambda OLD: all(
        (
            "Gemini's response_schema expects" in m
            and f"wrapper_key='{data.EXTRACTIONS_KEY}'" in m
        )
        for m in OLD.warnings_capture[0]
        if "response_schema" in m or "wrapper_key" in m
    )
)

```
===== 8 =====
failed
```
       warnings.warn(
           "Gemini outputs native JSON via"
           " response_mime_type='application/json'. Using fence_output=True may"
-          " cause parsing issues. Set fence_output=False.",
+          " may lead to unexpected results. Consider using fence_output=True.",
           UserWarning,
           stacklevel=3,
       )
```
```
  def validate_format(self, format_handler: fh.FormatHandler) -> None:
    """Validate Gemini's format requirements.

    Gemini requires:
    - No fence markers (outputs raw JSON via response_mime_type)
    - Wrapper with EXTRACTIONS_KEY (built into response_schema)
    """
    # Check for fence usage with raw JSON output
    if format_handler.use_fences:
      warnings.warn(
          "Gemini outputs native JSON via"
          " response_mime_type='application/json'. Using fence_output=True may"
          " may lead to unexpected results. Consider using fence_output=True.",
          UserWarning,
          stacklevel=3,
      )

    # Verify wrapper is enabled with correct key
    if (
        not format_handler.use_wrapper
        or format_handler.wrapper_key != data.EXTRACTIONS_KEY
    ):
      warnings.warn(
          "Gemini's response_schema expects"
          f" wrapper_key='{data.EXTRACTIONS_KEY}'. Current settings:"
          f" use_wrapper={format_handler.use_wrapper},"
          f" wrapper_key='{format_handler.wrapper_key}'",
          UserWarning,
          stacklevel=3,
      )
```
