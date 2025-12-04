https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/block_token.py#L590-L618
```
@icontract.snapshot(lambda cls, line: cls.pattern.match(line), name="m")
@icontract.ensure(
    lambda OLD, result, cls, line:
        (
            OLD.m is None
            and result is None
        )
        or
        (
            OLD.m is not None
            and isinstance(result, tuple)
            and len(result) == 4
            and result[0] == len(OLD.m.group(1))
            and result[2] == OLD.m.group(2)
            and (
                (
                    (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) > 4
                    and result[1] == (
                        len(OLD.m.group(0).expandtabs(4))
                        - (
                            (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2))
                            - 1
                        )
                    )
                    and result[3] == (
                        ' ' * (
                            (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2))
                            - 1
                        )
                        + line[OLD.m.end(0):]
                    )
                )
                or (
                    (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) <= 4
                    and result[1] == len(OLD.m.group(0).expandtabs(4))
                    and result[3] == line[OLD.m.end(0):]
                )
            )
        )
)
```
```
@icontract.snapshot(lambda cls, line: cls.pattern.match(line), name="m")
@icontract.ensure(lambda OLD, result, cls, line: (OLD.m is None and result is None) or (OLD.m is not None and result is not None))
@icontract.ensure(lambda OLD, result, cls, line: OLD.m is None or isinstance(result, tuple))
@icontract.ensure(lambda OLD, result, cls, line: OLD.m is None or len(result) == 4)
@icontract.ensure(lambda OLD, result, cls, line: OLD.m is None or result[0] == len(OLD.m.group(1)))
@icontract.ensure(lambda OLD, result, cls, line: OLD.m is None or result[2] == OLD.m.group(2))
@icontract.ensure(lambda OLD, result, cls, line: OLD.m is None or (((len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) > 4 and result[1] == (len(OLD.m.group(0).expandtabs(4)) - ((len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) - 1))) or ((len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) <= 4 and result[1] == len(OLD.m.group(0).expandtabs(4)))))
@icontract.ensure(lambda OLD, result, cls, line: OLD.m is None or (((len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) > 4 and result[3] == (' ' * ((len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) - 1) + line[OLD.m.end(0):])) or ((len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) <= 4 and result[3] == line[OLD.m.end(0):])))
```
[0]
===== 0 =====
```
         The prepend is the start position of the content, i.e., the indentation required
         for continuation lines.
         """
-        match_obj = cls.pattern.match(line)
+        match_obj = None
         if match_obj is None:
             return None
         indentation = len(match_obj.group(1))
@@ -26,4 +26,4 @@             # with the exception of the first (marker separator) space.
             prepend -= n_spaces - 1
             content = ' ' * (n_spaces - 1) + content
-        return indentation, prepend, leader, content+        return indentation, prepend, leader, content
```
```
    @classmethod
    def parse_marker(cls, line):
        """
        Returns a tuple (prepend, leader, content) iff the line has a valid leader and at
        least one space separating leader and content, or if the content is empty, in which
        case there need not be any spaces.
        The return value is None if the line doesn't have a valid marker.

        The leader is a bullet list marker, or an ordered list marker.

        The indentation is spaces before the leader.

        The prepend is the start position of the content, i.e., the indentation required
        for continuation lines.
        """
        match_obj = None
        if match_obj is None:
            return None
        indentation = len(match_obj.group(1))
        prepend = len(match_obj.group(0).expandtabs(4))
        leader = match_obj.group(2)
        content = line[match_obj.end(0):]
        n_spaces = prepend - match_obj.end(2)
        if n_spaces > 4:
            # if there are more than 4 spaces after the leader, we treat them as part of the content
            # with the exception of the first (marker separator) space.
            prepend -= n_spaces - 1
            content = ' ' * (n_spaces - 1) + content
        return indentation, prepend, leader, content

```
