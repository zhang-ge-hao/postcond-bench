https://github.com/thombashi/pytablewriter/blob/5da77a0b64e15451aceed41350712425d95ead62/./pytablewriter/writer/text/_markdown.py#L128-L171
```
@icontract.snapshot(lambda self: self._MarkdownTableWriter__flavor, name="old_flavor")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda self, kwargs: ("flavor" not in kwargs) or (self._MarkdownTableWriter__flavor == normalize_md_flavor(kwargs["flavor"])))
@icontract.ensure(lambda OLD, self, kwargs: ("flavor" in kwargs) or (self._MarkdownTableWriter__flavor == OLD.old_flavor))
@icontract.ensure(lambda self: (isinstance(self._styler, GFMarkdownStyler) if self._MarkdownTableWriter__flavor == MarkdownFlavor.GFM else isinstance(self._styler, MarkdownStyler)))
```
```
Limited specification language knowledge.

E   The argument(s) of the contract condition have not been set: ['kwargs']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.snapshot(
    lambda self, _KWARGS: _KWARGS.get("flavor"),
    name="flavor_in",
)
@icontract.snapshot(
    lambda self: self._MarkdownTableWriter__flavor,
    name="old_flavor",
)
@icontract.snapshot(
    lambda self: getattr(self, "_styler", None),
    name="old_styler",
)
@icontract.snapshot(
    lambda self: (
        setattr(self, "_icontract_clear_preprocess_called", 0),
        setattr(self, "_icontract_orig_clear_preprocess", self._clear_preprocess),
        setattr(
            self,
            "_clear_preprocess",
            (lambda self=self: (
                lambda *args, **kwargs: (
                    setattr(
                        self,
                        "_icontract_clear_preprocess_called",
                        self._icontract_clear_preprocess_called + 1,
                    ),
                    self._icontract_orig_clear_preprocess(*args, **kwargs),
                )[1]
            ))(),
        ),
    ),
    name="patch_clear_preprocess",
)
@icontract.snapshot(
    lambda self: (
        setattr(self, "_icontract_write_chapter_called", 0),
        setattr(
            self,
            "_icontract_orig_write_chapter",
            self._MarkdownTableWriter__write_chapter,
        ),
        setattr(
            self,
            "_MarkdownTableWriter__write_chapter",
            (lambda self=self: (
                lambda *args, **kwargs: (
                    setattr(
                        self,
                        "_icontract_write_chapter_called",
                        self._icontract_write_chapter_called + 1,
                    ),
                    self._icontract_orig_write_chapter(*args, **kwargs),
                )[1]
            ))(),
        ),
    ),
    name="patch_write_chapter",
)
@icontract.snapshot(
    lambda self: (
        setattr(self, "_icontract_write_null_line_called", 0),
        setattr(
            self,
            "_icontract_orig_write_null_line",
            self.write_null_line,
        ),
        setattr(
            self,
            "write_null_line",
            (lambda self=self: (
                lambda *args, **kwargs: (
                    setattr(
                        self,
                        "_icontract_write_null_line_called",
                        self._icontract_write_null_line_called + 1,
                    ),
                    self._icontract_orig_write_null_line(*args, **kwargs),
                )[1]
            ))(),
        ),
    ),
    name="patch_write_null_line",
)
@icontract.snapshot(
    lambda self: bool(self.is_write_null_line_after_table),
    name="old_is_write_null_line_after_table",
)
@icontract.ensure(
    lambda OLD, self: (
        (
            OLD.flavor_in is None
            and self._MarkdownTableWriter__flavor == OLD.old_flavor
        )
        or (
            OLD.flavor_in is not None
            and self._MarkdownTableWriter__flavor
            == normalize_md_flavor(OLD.flavor_in)
        )
    )
)
@icontract.ensure(
    lambda self: (
        isinstance(self._styler, GFMarkdownStyler)
        if self._MarkdownTableWriter__flavor == MarkdownFlavor.GFM
        else isinstance(self._styler, MarkdownStyler)
    )
)
@icontract.ensure(
    lambda OLD, self: self._styler is not OLD.old_styler
)
@icontract.ensure(
    lambda OLD, self: (
        OLD.flavor_in is None
        or normalize_md_flavor(OLD.flavor_in) == OLD.old_flavor
        or self._icontract_clear_preprocess_called >= 1
    )
)
@icontract.ensure(
    lambda self: (
        not getattr(self, "value_matrix", None)
        or self._icontract_write_chapter_called >= 1
    )
)
@icontract.ensure(
    lambda OLD, self: (
        not getattr(self, "value_matrix", None)
        or self._icontract_write_null_line_called
        == (1 if OLD.old_is_write_null_line_after_table else 0)
    )
)
@icontract.ensure(
    lambda self: (
        setattr(self, "_clear_preprocess", self._icontract_orig_clear_preprocess),
        True,
    )[1]
)
@icontract.ensure(
    lambda self: (
        setattr(
            self,
            "_MarkdownTableWriter__write_chapter",
            self._icontract_orig_write_chapter,
        ),
        True,
    )[1]
)
@icontract.ensure(
    lambda self: (
        setattr(
            self,
            "write_null_line",
            self._icontract_orig_write_null_line,
        ),
        True,
    )[1]
)

```
