https://github.com/thombashi/pytablewriter/blob/5da77a0b64e15451aceed41350712425d95ead62/./pytablewriter/writer/text/_markdown.py#L128-L171
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
```
@icontract.snapshot(lambda self, _KWARGS: _KWARGS.get("flavor"), name="flavor_in")
@icontract.snapshot(lambda self: self._MarkdownTableWriter__flavor, name="old_flavor")
@icontract.snapshot(lambda self: type(self._styler), name="old_styler_type")
@icontract.ensure(lambda OLD, self: (OLD.flavor_in is None) or self._MarkdownTableWriter__flavor == normalize_md_flavor(OLD.flavor_in))
@icontract.ensure(lambda OLD, self: isinstance(self._styler, GFMarkdownStyler) if self._MarkdownTableWriter__flavor == MarkdownFlavor.GFM else isinstance(self._styler, MarkdownStyler))
```
[11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23]
===== 11 =====
```
         if "flavor" in kwargs:
             new_flavor = normalize_md_flavor(kwargs["flavor"])
             if new_flavor != self.__flavor:
-                self._clear_preprocess()
+                self._clear_preprocess() if False else None
                 self.__flavor = new_flavor
 
         if self.__flavor:
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess() if False else None
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 12 =====
```
         if "flavor" in kwargs:
             new_flavor = normalize_md_flavor(kwargs["flavor"])
             if new_flavor != self.__flavor:
-                self._clear_preprocess()
+                self._clear_preprocess() if self.__flavor != MarkdownFlavor.GFM else None
                 self.__flavor = new_flavor
 
         if self.__flavor:
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess() if self.__flavor != MarkdownFlavor.GFM else None
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 13 =====
```
         if "flavor" in kwargs:
             new_flavor = normalize_md_flavor(kwargs["flavor"])
             if new_flavor != self.__flavor:
-                self._clear_preprocess()
+                self._clear_preprocess() if self.__flavor == MarkdownFlavor.COMMON_MARK else None
                 self.__flavor = new_flavor
 
         if self.__flavor:
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess() if self.__flavor == MarkdownFlavor.COMMON_MARK else None
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 15 =====
```
                 self._clear_preprocess()
                 self.__flavor = new_flavor
 
-        if self.__flavor:
+        if self.__flavor == MarkdownFlavor.GFM or self.__flavor == MarkdownFlavor.JEKYLL:
             self._styler = self._create_styler(self)
 
         with self._logger:
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor == MarkdownFlavor.GFM or self.__flavor == MarkdownFlavor.JEKYLL:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 16 =====
```
                 self._clear_preprocess()
                 self.__flavor = new_flavor
 
-        if self.__flavor:
+        if self.__flavor in [MarkdownFlavor.GITHUB, MarkdownFlavor.GFM]:
             self._styler = self._create_styler(self)
 
         with self._logger:
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor in [MarkdownFlavor.GITHUB, MarkdownFlavor.GFM]:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 17 =====
```
                 self._logger.logger.debug("no tabular data found")
                 return
 
-            self.__write_chapter()
+            self.__write_chapter() if self.__flavor == MarkdownFlavor.GITHUB else None
             self._write_table(**kwargs)
             if self.is_write_null_line_after_table:
                 self.write_null_line()
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter() if self.__flavor == MarkdownFlavor.GITHUB else None
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 18 =====
```
 
             self.__write_chapter()
             self._write_table(**kwargs)
-            if self.is_write_null_line_after_table:
+            if not self.is_write_null_line_after_table:
                 self.write_null_line()
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if not self.is_write_null_line_after_table:
                self.write_null_line()
```
===== 19 =====
```
 
             self.__write_chapter()
             self._write_table(**kwargs)
-            if self.is_write_null_line_after_table:
+            if self.is_write_null_line_after_table == False:
                 self.write_null_line()
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table == False:
                self.write_null_line()
```
===== 20 =====
```
 
             self.__write_chapter()
             self._write_table(**kwargs)
-            if self.is_write_null_line_after_table:
+            if self.is_write_null_line_after_table and self.__flavor == MarkdownFlavor.GITHUB:
                 self.write_null_line()
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table and self.__flavor == MarkdownFlavor.GITHUB:
                self.write_null_line()
```
===== 21 =====
```
 
             self.__write_chapter()
             self._write_table(**kwargs)
-            if self.is_write_null_line_after_table:
+            if self.is_write_null_line_after_table is None:
                 self.write_null_line()
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table is None:
                self.write_null_line()
```
===== 22 =====
```
 
             self.__write_chapter()
             self._write_table(**kwargs)
-            if self.is_write_null_line_after_table:
+            if self.is_write_null_line_after_table or self.__flavor != MarkdownFlavor.KRAMDOWN:
                 self.write_null_line()
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table or self.__flavor != MarkdownFlavor.KRAMDOWN:
                self.write_null_line()
```
===== 23 =====
```
             self.__write_chapter()
             self._write_table(**kwargs)
             if self.is_write_null_line_after_table:
-                self.write_null_line()+                self.write_null_line() if self.__flavor == MarkdownFlavor.GITHUB else None
```
```
    def write_table(self, **kwargs: Any) -> None:
        """
        |write_table| with Markdown table format.

        Args:
            flavor (Optional[str]):
                possible flavors are as follows (case insensitive):

                    - ``"CommonMark"``
                    - ``"gfm"``
                    - ``"github"`` (alias of ``"gfm"``)
                    - ``kramdown``
                    - ``Jekyll`` (alias of ``"kramdown"``)

                Defaults to ``"CommonMark"``.

        Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        if "flavor" in kwargs:
            new_flavor = normalize_md_flavor(kwargs["flavor"])
            if new_flavor != self.__flavor:
                self._clear_preprocess()
                self.__flavor = new_flavor

        if self.__flavor:
            self._styler = self._create_styler(self)

        with self._logger:
            try:
                self._verify_property()
            except EmptyTableDataError:
                self._logger.logger.debug("no tabular data found")
                return

            self.__write_chapter()
            self._write_table(**kwargs)
            if self.is_write_null_line_after_table:
                self.write_null_line() if self.__flavor == MarkdownFlavor.GITHUB else None
```
