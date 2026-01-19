https://github.com/D4Vinci/Scrapling/blob/d02da49865049d5175325943f1308f0c8b6101d2/./scrapling/core/_html_utils.py#L284-L342
```
🈚️

It's hard

@icontract.ensure(
    lambda result, text, keep, remove_illegal, encoding:
        # 1) 返回值必须是 str
        isinstance(result, str)
        # 2) 如果原始文本里根本没有任何实体匹配，则结果必须原样不变
        and (
            _ent_re.search(to_unicode(text, encoding)) is not None
            or result == to_unicode(text, encoding)
        )
        # 3) 对所有“应该被 keep 的实体”，在结果中的出现次数必须与原文本一致
        and all(
            result.count(m.group(0)) ==
            to_unicode(text, encoding).count(m.group(0))
            for m in _ent_re.finditer(to_unicode(text, encoding))
            if (
                m.group("named") is not None
                and m.group("named").lower() in keep
            )
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74]
===== 0 =====
```
     def convert_entity(m: Match[str]) -> str:
         groups = m.groupdict()
         number = None
-        if groups.get("dec"):
+        if groups.get("DEC"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("DEC"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 1 =====
```
     def convert_entity(m: Match[str]) -> str:
         groups = m.groupdict()
         number = None
-        if groups.get("dec"):
+        if groups.get("XXdecXX"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("XXdecXX"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 2 =====
```
     def convert_entity(m: Match[str]) -> str:
         groups = m.groupdict()
         number = None
-        if groups.get("dec"):
+        if groups.get("dec") == "":
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec") == "":
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 3 =====
```
     def convert_entity(m: Match[str]) -> str:
         groups = m.groupdict()
         number = None
-        if groups.get("dec"):
+        if groups.get("dec") == "0":
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec") == "0":
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 4 =====
```
     def convert_entity(m: Match[str]) -> str:
         groups = m.groupdict()
         number = None
-        if groups.get("dec"):
+        if groups.get(None):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get(None):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 5 =====
```
         groups = m.groupdict()
         number = None
         if groups.get("dec"):
-            number = int(groups["dec"], 10)
+            number = None
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = None
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 6 =====
```
         groups = m.groupdict()
         number = None
         if groups.get("dec"):
-            number = int(groups["dec"], 10)
+            number = int(10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 7 =====
```
         groups = m.groupdict()
         number = None
         if groups.get("dec"):
-            number = int(groups["dec"], 10)
+            number = int(groups["dec"], 11)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 11)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 8 =====
```
         groups = m.groupdict()
         number = None
         if groups.get("dec"):
-            number = int(groups["dec"], 10)
+            number = int(groups["dec"], 16)  # Incorrectly interpreting decimal as hexadecimal
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 16)  # Incorrectly interpreting decimal as hexadecimal
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 9 =====
```
         number = None
         if groups.get("dec"):
             number = int(groups["dec"], 10)
-        elif groups.get("hex"):
+        elif groups.get("HEX"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("HEX"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 10 =====
```
         number = None
         if groups.get("dec"):
             number = int(groups["dec"], 10)
-        elif groups.get("hex"):
+        elif groups.get("XXhexXX"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("XXhexXX"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 11 =====
```
         number = None
         if groups.get("dec"):
             number = int(groups["dec"], 10)
-        elif groups.get("hex"):
+        elif groups.get("hex") == "":
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex") == "":
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 12 =====
```
         number = None
         if groups.get("dec"):
             number = int(groups["dec"], 10)
-        elif groups.get("hex"):
+        elif groups.get("hex") and groups.get("dec"):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex") and groups.get("dec"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 13 =====
```
         number = None
         if groups.get("dec"):
             number = int(groups["dec"], 10)
-        elif groups.get("hex"):
+        elif groups.get("hex") is True:
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex") is True:
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 14 =====
```
         number = None
         if groups.get("dec"):
             number = int(groups["dec"], 10)
-        elif groups.get("hex"):
+        elif groups.get(None):
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get(None):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 15 =====
```
         if groups.get("dec"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
-            number = int(groups["hex"], 16)
+            number = None
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = None
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 16 =====
```
         if groups.get("dec"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
-            number = int(groups["hex"], 16)
+            number = int(16)
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 17 =====
```
         if groups.get("dec"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
-            number = int(groups["hex"], 16)
+            number = int(groups["hex"], 16) + 1  # Off-by-one error in conversion
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16) + 1  # Off-by-one error in conversion
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 18 =====
```
         if groups.get("dec"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
-            number = int(groups["hex"], 16)
+            number = int(groups["hex"], 16) - 1  # Off-by-one error in conversion
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16) - 1  # Off-by-one error in conversion
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 19 =====
```
         if groups.get("dec"):
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
-            number = int(groups["hex"], 16)
+            number = int(groups["hex"], 17)
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 17)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 20 =====
```
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
-        elif groups.get("named"):
+        elif groups.get("NAMED"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("NAMED"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 21 =====
```
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
-        elif groups.get("named"):
+        elif groups.get("XXnamedXX"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("XXnamedXX"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 22 =====
```
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
-        elif groups.get("named"):
+        elif groups.get(None):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get(None):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 23 =====
```
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
-        elif groups.get("named"):
+        if groups.get("named") == "":
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        if groups.get("named") == "":
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 24 =====
```
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
-        elif groups.get("named"):
+        if groups.get("named") in name2codepoint:
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        if groups.get("named") in name2codepoint:
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 25 =====
```
             number = int(groups["dec"], 10)
         elif groups.get("hex"):
             number = int(groups["hex"], 16)
-        elif groups.get("named"):
+        if groups.get("named") is True:
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        if groups.get("named") is True:
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 26 =====
```
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
-            if entity_name.lower() in keep:
+            if entity_name.lower() not in keep:
                 return m.group(0)
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() not in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 27 =====
```
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
-            if entity_name.lower() in keep:
+            if entity_name.lower() not in keep:
                 return m.group(0)
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() not in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 28 =====
```
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
-            if entity_name.lower() in keep:
+            if entity_name.upper() in keep:
                 return m.group(0)
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.upper() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 29 =====
```
             number = int(groups["hex"], 16)
         elif groups.get("named"):
             entity_name = groups["named"]
-            if entity_name.lower() in keep:
+            if entity_name.upper() in keep:
                 return m.group(0)
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.upper() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 30 =====
```
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
-                return m.group(0)
+                return ""  # This will remove the entity instead of keeping it.
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return ""  # This will remove the entity instead of keeping it.
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 31 =====
```
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
-                return m.group(0)
+                return "&#" + str(number) + ";"  # This will convert the entity to a numeric reference instead of keeping the original.
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return "&#" + str(number) + ";"  # This will convert the entity to a numeric reference instead of keeping the original.
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 32 =====
```
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
-                return m.group(0)
+                return "unknown_entity"  # This will replace the entity with a placeholder string.
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return "unknown_entity"  # This will replace the entity with a placeholder string.
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 33 =====
```
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
-                return m.group(0)
+                return chr(0)  # This will replace the entity with a null character, which may lead to unexpected behavior.
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return chr(0)  # This will replace the entity with a null character, which may lead to unexpected behavior.
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 34 =====
```
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
-                return m.group(0)
+                return m.group(0).upper()  # This will return the entity in uppercase, altering its representation.
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0).upper()  # This will return the entity in uppercase, altering its representation.
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 35 =====
```
         elif groups.get("named"):
             entity_name = groups["named"]
             if entity_name.lower() in keep:
-                return m.group(0)
+                return m.group(1)
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(1)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 36 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = None
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = None
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 37 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name) and name2codepoint.get(entity_name.lower())
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) and name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 38 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name) if entity_name in name2codepoint else None  # Returns None if not found
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) if entity_name in name2codepoint else None  # Returns None if not found
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 39 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name) or name2codepoint.get(None)
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(None)
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 40 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.upper())
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.upper())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 41 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name, -1)  # Defaults to -1 if not found, which is invalid
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name, -1)  # Defaults to -1 if not found, which is invalid
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 42 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name, 0)  # Defaults to 0 if not found
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name, 0)  # Defaults to 0 if not found
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 43 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name, 0xFFFD)  # Defaults to the replacement character if not found
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name, 0xFFFD)  # Defaults to the replacement character if not found
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 44 =====
```
             entity_name = groups["named"]
             if entity_name.lower() in keep:
                 return m.group(0)
-            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
+            number = name2codepoint.get(entity_name.upper())  # Only checks uppercase entity names
         if number is not None:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name.upper())  # Only checks uppercase entity names
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 45 =====
```
             if entity_name.lower() in keep:
                 return m.group(0)
             number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
-        if number is not None:
+        if number == 0:
             # Browsers typically
             # interpret numeric character references in the 80-9F range as representing the characters mapped
             # to bytes 80-9F in the Windows-1252 encoding. For more info
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number == 0:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 46 =====
```
             # to bytes 80-9F in the Windows-1252 encoding. For more info
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
-                if 0x80 <= number <= 0x9F:
+                if 0x80 < number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 < number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 47 =====
```
             # to bytes 80-9F in the Windows-1252 encoding. For more info
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
-                if 0x80 <= number <= 0x9F:
+                if 0x90 <= number <= 0xA0:  # This condition incorrectly checks a different range
                     return bytes((number,)).decode("cp1252")
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x90 <= number <= 0xA0:  # This condition incorrectly checks a different range
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 48 =====
```
             # to bytes 80-9F in the Windows-1252 encoding. For more info
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
-                if 0x80 <= number <= 0x9F:
+                if 129 <= number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
@@ -56,4 +56,4 @@ 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 129 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 49 =====
```
             # to bytes 80-9F in the Windows-1252 encoding. For more info
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
-                if 0x80 <= number <= 0x9F:
+                if number < 0x80:  # This condition will incorrectly handle values below 0x80
                     return bytes((number,)).decode("cp1252")
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if number < 0x80:  # This condition will incorrectly handle values below 0x80
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 50 =====
```
             # to bytes 80-9F in the Windows-1252 encoding. For more info
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
-                if 0x80 <= number <= 0x9F:
+                if number > 0x9F:  # This condition will skip valid values in the range 0x80 to 0x9F
                     return bytes((number,)).decode("cp1252")
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if number > 0x9F:  # This condition will skip valid values in the range 0x80 to 0x9F
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 51 =====
```
             # to bytes 80-9F in the Windows-1252 encoding. For more info
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
-                if 0x80 <= number <= 0x9F:
+                if number >= 0x80:  # This condition will include values above 0x9F, which is incorrect
                     return bytes((number,)).decode("cp1252")
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if number >= 0x80:  # This condition will include values above 0x9F, which is incorrect
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 52 =====
```
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
                 if 0x80 <= number <= 0x9F:
-                    return bytes((number,)).decode("cp1252")
+                    return bytes((number,)).decode("ascii")  # Decodes using ASCII, which may not represent all characters correctly
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("ascii")  # Decodes using ASCII, which may not represent all characters correctly
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 53 =====
```
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
                 if 0x80 <= number <= 0x9F:
-                    return bytes((number,)).decode("cp1252")
+                    return bytes((number,)).decode("latin-1")  # Uses a different encoding that may not match the intended character set
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("latin-1")  # Uses a different encoding that may not match the intended character set
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 54 =====
```
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
                 if 0x80 <= number <= 0x9F:
-                    return bytes((number,)).decode("cp1252")
+                    return bytes((number,)).decode("utf-8")  # Uses the wrong encoding, leading to incorrect character representation
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("utf-8")  # Uses the wrong encoding, leading to incorrect character representation
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 55 =====
```
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
                 if 0x80 <= number <= 0x9F:
-                    return bytes((number,)).decode("cp1252")
+                    return chr(number)  # Incorrectly returns the character directly instead of decoding
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return chr(number)  # Incorrectly returns the character directly instead of decoding
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 56 =====
```
             # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
             try:
                 if 0x80 <= number <= 0x9F:
-                    return bytes((number,)).decode("cp1252")
+                    return str(number)  # Converts the number to a string instead of decoding it to a character
                 return chr(number)
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return str(number)  # Converts the number to a string instead of decoding it to a character
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 57 =====
```
             try:
                 if 0x80 <= number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
-                return chr(number)
+                return None
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return None
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 58 =====
```
             try:
                 if 0x80 <= number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
-                return chr(number)
+                return bytes((number,)).decode("utf-8")
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return bytes((number,)).decode("utf-8")
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 59 =====
```
             try:
                 if 0x80 <= number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
-                return chr(number)
+                return chr(number + 1)  # returning the next character instead of the intended one
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number + 1)  # returning the next character instead of the intended one
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 60 =====
```
             try:
                 if 0x80 <= number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
-                return chr(number)
+                return m.group(0)  # returning the original entity instead of the character
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return m.group(0)  # returning the original entity instead of the character
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 61 =====
```
             try:
                 if 0x80 <= number <= 0x9F:
                     return bytes((number,)).decode("cp1252")
-                return chr(number)
+                return str(number)
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return str(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 62 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return "" if not remove_illegal and groups.get("semicolon") else m.group(0)
 
     return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if not remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 63 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return "" if remove_illegal and groups.get("SEMICOLON") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("SEMICOLON") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 64 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return "" if remove_illegal and groups.get("XXsemicolonXX") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("XXsemicolonXX") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 65 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return "" if remove_illegal and groups.get("semicolon") else m.group(1)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(1)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 66 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return "" if remove_illegal and groups.get(None) else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get(None) else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 67 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return "" if remove_illegal or groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal or groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))

```
===== 68 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return m.group(0) if groups.get("semicolon") else ""  # Always keeps the entity
 
     return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return m.group(0) if groups.get("semicolon") else ""  # Always keeps the entity

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 69 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return m.group(0) if remove_illegal and groups.get("semicolon") else ""
 
     return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return m.group(0) if remove_illegal and groups.get("semicolon") else ""

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 70 =====
```
             except (ValueError, OverflowError):  # pragma: no cover
                 pass
 
-        return "" if remove_illegal and groups.get("semicolon") else m.group(0)
+        return m.group(0) if remove_illegal else ""
 
     return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return m.group(0) if remove_illegal else ""

    return _ent_re.sub(convert_entity, to_unicode(text, encoding))
```
===== 71 =====
```
 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(encoding))
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(encoding))

```
===== 72 =====
```
 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding)).replace(" ", "_")
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding)).replace(" ", "_")
```
===== 73 =====
```
 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding)).strip()
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding)).strip()
```
===== 74 =====
```
 
         return "" if remove_illegal and groups.get("semicolon") else m.group(0)
 
-    return _ent_re.sub(convert_entity, to_unicode(text, encoding))+    return _ent_re.sub(convert_entity, to_unicode(text, encoding)).upper()
```
```
def _replace_entities(
    text: StrOrBytes,
    keep: Iterable[str] = (),
    remove_illegal: bool = True,
    encoding: str = "utf-8",
) -> str:
    """Remove entities from the given `text` by converting them to their
    corresponding Unicode character.

    `text` can be a Unicode string or a byte string encoded in the given
    `encoding` (which defaults to 'utf-8').

    If `keep` is passed (with a list of entity names), those entities will
    be kept (they won't be removed).

    It supports both numeric entities (``&#nnnn;`` and ``&#hhhh;``)
    and named entities (such as ``&nbsp;`` or ``&gt;``).

    If `remove_illegal` is ``True``, entities that can't be converted are removed.
    If `remove_illegal` is ``False``, entities that can't be converted are kept "as
    is". For more information, see the tests.

    Always returns a Unicode string (with the entities removed).

    >>> _replace_entities(b'Price: &pound;100')
    'Price: \\xa3100'
    >>> print(_replace_entities(b'Price: &pound;100'))
    Price: £100
    >>>

    """

    def convert_entity(m: Match[str]) -> str:
        groups = m.groupdict()
        number = None
        if groups.get("dec"):
            number = int(groups["dec"], 10)
        elif groups.get("hex"):
            number = int(groups["hex"], 16)
        elif groups.get("named"):
            entity_name = groups["named"]
            if entity_name.lower() in keep:
                return m.group(0)
            number = name2codepoint.get(entity_name) or name2codepoint.get(entity_name.lower())
        if number is not None:
            # Browsers typically
            # interpret numeric character references in the 80-9F range as representing the characters mapped
            # to bytes 80-9F in the Windows-1252 encoding. For more info
            # see: http://en.wikipedia.org/wiki/Character_encodings_in_HTML
            try:
                if 0x80 <= number <= 0x9F:
                    return bytes((number,)).decode("cp1252")
                return chr(number)
            except (ValueError, OverflowError):  # pragma: no cover
                pass

        return "" if remove_illegal and groups.get("semicolon") else m.group(0)

    return _ent_re.sub(convert_entity, to_unicode(text, encoding)).upper()
```
