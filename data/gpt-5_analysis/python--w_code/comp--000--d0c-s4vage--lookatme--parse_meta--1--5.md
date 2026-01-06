https://github.com/d0c-s4vage/lookatme/blob/c05abe1804d93254e9139039937eed43fb6b49ab/./lookatme/parser.py#L201-L264
```
@icontract.snapshot(lambda input_data: MetaSchema().load_partial_styles({}, partial=True), name="default_meta")
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda result: isinstance(result[0], str))
@icontract.ensure(lambda result: isinstance(result[1], dict))
@icontract.ensure(lambda result, input_data: input_data.endswith(result[0]))
@icontract.ensure(lambda result, input_data: len(result[0]) <= len(input_data))
@icontract.ensure(lambda result, input_data: (result[0] == input_data) or (len(result[0]) < len(input_data)))
@icontract.ensure(lambda result, OLD, input_data: (result[0] != input_data) or (result[1] == OLD.default_meta))
@icontract.ensure(lambda result, OLD, input_data: (result[1] == OLD.default_meta) or (result[0] != input_data))
```
```
Branch Missed.

Missed `data = MetaSchema().loads_partial_styles(yaml_data, partial=True)` branch.
```
passed
```
@icontract.snapshot(lambda input_data: input_data, name="orig")
@icontract.ensure(
    lambda OLD, self, input_data, result:
        (result is not None)
        and isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], str)
        and isinstance(result[1], dict)
        and (lambda s: (lambda lines, marker_idxs: (
            (len(marker_idxs) < 2
             and result[0] == s
             and result[1] == MetaSchema().load_partial_styles({}, partial=True))
            or
            (len(marker_idxs) >= 2
             and (lambda first, second: (
                    (result[0] == s[sum((len(L) + 1) for L in lines[: second + 1]):])
                    and (result[1] == (
                        MetaSchema().loads_partial_styles(
                            "\n".join(lines[first + 1: second]),
                            partial=True
                        )
                        if (second - first - 1) > 0
                        else MetaSchema().load_partial_styles({}, partial=True)
                    ))
             ))(marker_idxs[0], marker_idxs[1]))
        ))(
            s.split("\n"),
            [i for i, ln in enumerate(s.split("\n"))
             if re.match(r'----*', ln.strip()) is not None]
        ))(OLD.orig)
)

```
===== 5 =====
failed
```
         yaml_data = []
         skipped_chars = 0
         for line in input_data.split("\n"):
-            skipped_chars += len(line) + 1
+            skipped_chars += len(line)  # Missing the +1 for the newline character
             stripped_line = line.strip()
 
             is_marker = (re.match(r'----*', stripped_line) is not None)
```
```
    @tutor(
        "general",
        "metadata",
        r"""
        The YAML metadata that can be prefixed in slides includes these top level
        fields:

        ```yaml
        ---
        title: "title"
        date: "date"
        author: "author"
        extensions:
          - extension 1
          # .. list of extensions
        styles:
          # .. nested style fields ..
        ---
        ```

        > **NOTE** The `styles` field will be explained in detail with each markdown
        > element.
        """,
        order=3,
    )
    def parse_meta(self, input_data) -> Tuple[AnyStr, Dict]:
        """Parse the PresentationMeta out of the input data

        :param str input_data: The input data string
        :returns: tuple of (remaining_data, meta)
        """
        found_first = False
        yaml_data = []
        skipped_chars = 0
        for line in input_data.split("\n"):
            skipped_chars += len(line)  # Missing the +1 for the newline character
            stripped_line = line.strip()

            is_marker = (re.match(r'----*', stripped_line) is not None)
            if is_marker:
                if not found_first:
                    found_first = True
                # found the second one
                else:
                    break

            if found_first and not is_marker:
                yaml_data.append(line)
                continue

            # there was no ----* marker
            if not found_first and stripped_line != "":
                break

        if not found_first:
            return input_data, MetaSchema().load_partial_styles({}, partial=True)

        new_input = input_data[skipped_chars:]
        if len(yaml_data) == 0:
            return new_input, MetaSchema().load_partial_styles({}, partial=True)

        yaml_data = "\n".join(yaml_data)
        data = MetaSchema().loads_partial_styles(yaml_data, partial=True)
        return new_input, data
```
