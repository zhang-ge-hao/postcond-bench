https://github.com/gaogaotiantian/objprint/blob/297932d68d336305111a084819ac5a48c2434da3/./src/objprint/objprint.py#L352-L394
```
🈚️

Iterable
```
```
@icontract.ensure(lambda result, self, obj, indent_level, cfg: result.startswith(self._get_header_footer(obj, cfg)[0]))
@icontract.ensure(lambda result, self, obj, indent_level, cfg: result.endswith(self._get_header_footer(obj, cfg)[1]))
@icontract.ensure(lambda result, self, obj, indent_level, cfg: not (len(self._get_header_footer(obj, cfg)[0]) > 1 and result.startswith(self._get_header_footer(obj, cfg)[0]) and result.endswith(self._get_header_footer(obj, cfg)[1]) and result[len(self._get_header_footer(obj, cfg)[0]):-len(self._get_header_footer(obj, cfg)[1])].strip() != "" and ("\n" not in result)))
@icontract.ensure(lambda result, self, obj, indent_level, cfg: True if ("\n" not in result) else (result.splitlines()[0] == self._get_header_footer(obj, cfg)[0] and result.splitlines()[-1] == self.add_indent('', indent_level, cfg) + self._get_header_footer(obj, cfg)[1]))
```
[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 26, 27, 29, 32, 33, 34, 35, 36, 37, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 66, 68, 69, 70]
===== 3 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements != -1:
             elems = list(elems)
         else:
             first_elems = []
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements != -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 4 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements != -1:
             elems = list(elems)
         else:
             first_elems = []
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements != -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 5 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements == +1:
             elems = list(elems)
         else:
             first_elems = []
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == +1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 6 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements == -2:
             elems = list(elems)
         else:
             first_elems = []
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -2:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 7 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements == 0:
             elems = list(elems)
         else:
             first_elems = []
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == 0:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 8 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements == 1:
             elems = list(elems)
         else:
             first_elems = []
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == 1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 9 =====
```
         """
         header, footer = self._get_header_footer(obj, cfg)
 
-        if cfg.elements == -1:
+        if cfg.elements > 0:
             elems = list(elems)
         else:
             first_elems = []
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements > 0:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 10 =====
```
         header, footer = self._get_header_footer(obj, cfg)
 
         if cfg.elements == -1:
-            elems = list(elems)
+            elems = list(elems)[:cfg.elements]  # Limits the number of elements to cfg.elements
         else:
             first_elems = []
             it = iter(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)[:cfg.elements]  # Limits the number of elements to cfg.elements
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 11 =====
```
         header, footer = self._get_header_footer(obj, cfg)
 
         if cfg.elements == -1:
-            elems = list(elems)
+            elems = sorted(elems)  # Sorts the elements, changing their original order
         else:
             first_elems = []
             it = iter(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = sorted(elems)  # Sorts the elements, changing their original order
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 12 =====
```
             elems = list(elems)
         else:
             first_elems = []
-            it = iter(elems)
+            it = iter([])  # Empty iterator
             try:
                 for _ in range(cfg.elements):
                     first_elems.append(next(it))
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter([])  # Empty iterator
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 13 =====
```
             first_elems = []
             it = iter(elems)
             try:
-                for _ in range(cfg.elements):
+                for _ in range(cfg.elements * 2):  # Iterates twice as many times as intended
                     first_elems.append(next(it))
             except StopIteration:
                 pass
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements * 2):  # Iterates twice as many times as intended
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 14 =====
```
             first_elems = []
             it = iter(elems)
             try:
-                for _ in range(cfg.elements):
+                for _ in range(cfg.elements + 1):  # Off-by-one error
                     first_elems.append(next(it))
             except StopIteration:
                 pass
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements + 1):  # Off-by-one error
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 15 =====
```
             first_elems = []
             it = iter(elems)
             try:
-                for _ in range(cfg.elements):
+                for _ in range(cfg.elements // 2):  # Only iterates half the intended times
                     first_elems.append(next(it))
             except StopIteration:
                 pass
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements // 2):  # Only iterates half the intended times
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 16 =====
```
             first_elems = []
             it = iter(elems)
             try:
-                for _ in range(cfg.elements):
+                for _ in range(min(cfg.elements, 0)):  # Always results in zero iterations
                     first_elems.append(next(it))
             except StopIteration:
                 pass
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(min(cfg.elements, 0)):  # Always results in zero iterations
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 17 =====
```
             it = iter(elems)
             try:
                 for _ in range(cfg.elements):
-                    first_elems.append(next(it))
+                    first_elems.append("...")  # Incorrectly appending a string instead of the next element
             except StopIteration:
                 pass
             if next(it, None) is not None:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append("...")  # Incorrectly appending a string instead of the next element
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 18 =====
```
             it = iter(elems)
             try:
                 for _ in range(cfg.elements):
-                    first_elems.append(next(it))
+                    first_elems.append(next(it) if next(it) else "default")  # Appending a default value if the next element is falsy
             except StopIteration:
                 pass
             if next(it, None) is not None:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it) if next(it) else "default")  # Appending a default value if the next element is falsy
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 19 =====
```
                     first_elems.append(next(it))
             except StopIteration:
                 pass
-            if next(it, None) is not None:
+            if next(it, ) is not None:
                 first_elems.append("...")
             elems = first_elems
 
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, ) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 20 =====
```
                 first_elems.append("...")
             elems = first_elems
 
-        multiline = False
+        multiline = True
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = True
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 25 =====
```
             elems = first_elems
 
         multiline = False
-        if len(header) > 1 and len(elems) > 0:
+        if len(header) > 1 and len(elems) >= 0:
             # If it's not built in, always do multiline
             multiline = True
         elif any(("\n" in elem for elem in elems)):
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) >= 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 26 =====
```
             elems = first_elems
 
         multiline = False
-        if len(header) > 1 and len(elems) > 0:
+        if len(header) > 1 or len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
         elif any(("\n" in elem for elem in elems)):
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 or len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 27 =====
```
             elems = first_elems
 
         multiline = False
-        if len(header) > 1 and len(elems) > 0:
+        if len(header) > 1 or len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
         elif any(("\n" in elem for elem in elems)):
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 or len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 29 =====
```
             elems = first_elems
 
         multiline = False
-        if len(header) > 1 and len(elems) > 0:
+        if len(header) >= 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
         elif any(("\n" in elem for elem in elems)):
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) >= 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 32 =====
```
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
-        elif any(("\n" in elem for elem in elems)):
+        elif all(("\n" in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif all(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 33 =====
```
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
-        elif any(("\n" in elem for elem in elems)):
+        elif all(("\n" not in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif all(("\n" not in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 34 =====
```
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
-        elif any(("\n" in elem for elem in elems)):
+        elif any(("XX\nXX" in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("XX\nXX" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 35 =====
```
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
-        elif any(("\n" in elem for elem in elems)):
+        elif any(("\n" in elem for elem in elems) and (len(elem) < 10 for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems) and (len(elem) < 10 for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 36 =====
```
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
-        elif any(("\n" in elem for elem in elems)):
+        elif any(("\n" not in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" not in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 37 =====
```
         if len(header) > 1 and len(elems) > 0:
             # If it's not built in, always do multiline
             multiline = True
-        elif any(("\n" in elem for elem in elems)):
+        elif any(("\n" not in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" not in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 40 =====
```
         elif any(("\n" in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
-        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
+        elif cfg.width is None and sum((len(elem) for elem in elems)) > cfg.width:
             multiline = True
 
         if multiline:
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 41 =====
```
         elif any(("\n" in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
-        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
+        elif cfg.width is not None and len(elems) < cfg.width:
             multiline = True
 
         if multiline:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and len(elems) < cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 42 =====
```
         elif any(("\n" in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
-        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
+        elif cfg.width is not None and len(elems) > cfg.width:
             multiline = True
 
         if multiline:
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and len(elems) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 43 =====
```
         elif any(("\n" in elem for elem in elems)):
             # Has \n, need multiple mode
             multiline = True
-        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
+        elif cfg.width is not None or sum((len(elem) for elem in elems)) > cfg.width:
             multiline = True
 
         if multiline:
@@ -40,4 +40,4 @@             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None or sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 44 =====
```
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
-            multiline = True
+            multiline = False
 
         if multiline:
             s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = False

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 45 =====
```
             # Has \n, need multiple mode
             multiline = True
         elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
-            multiline = True
+            multiline = None
 
         if multiline:
             s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = None

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 50 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = ", ".join(elems) + "..."
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ", ".join(elems) + "..."
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 51 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = ", ".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ", ".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 52 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = ",\n".join(elems)
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(elems)
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 53 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = ",\n".join(self.add_indent(elems, indent_level + 2, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 2, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 54 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = ",\n".join(self.add_indent(elems, indent_level - 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level - 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 55 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = ",\n".join(self.add_indent(elems, indent_level, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 56 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = "XX,\nXX".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = "XX,\nXX".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 57 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = "\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = "\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
```
===== 58 =====
```
             multiline = True
 
         if multiline:
-            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
+            s = None
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
             s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = None
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"

```
===== 66 =====
```
             s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
-            s = ", ".join(elems)
+            s = " | ".join(elems)
             return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = " | ".join(elems)
            return f"{header}{s}{footer}"
```
===== 68 =====
```
             s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
-            s = ", ".join(elems)
+            s = ", ".join(elems).upper()
             return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems).upper()
            return f"{header}{s}{footer}"
```
===== 69 =====
```
             s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
-            s = ", ".join(elems)
+            s = "; ".join(elems)
             return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = "; ".join(elems)
            return f"{header}{s}{footer}"
```
===== 70 =====
```
             s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
             return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
         else:
-            s = ", ".join(elems)
-            return f"{header}{s}{footer}"+            s = "XX, XX".join(elems)
+            return f"{header}{s}{footer}"
```
```
    def _get_pack_str(
            self,
            elems: Iterable[str],
            obj: Any,
            indent_level: int,
            cfg: _PrintConfig) -> str:
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            it = iter(elems)
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(it))
            except StopIteration:
                pass
            if next(it, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = "XX, XX".join(elems)
            return f"{header}{s}{footer}"

```
