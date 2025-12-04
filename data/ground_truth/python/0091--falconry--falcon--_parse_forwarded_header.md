https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/forwarded.py#L93-L192
```
@icontract.ensure(
    lambda forwarded, result: 
    all(isinstance(elem, Forwarded) for elem in result) and (
        [
            (elem.src, elem.dest, elem.host, elem.scheme)
            for elem in result
        ]
        ==
        [
            spec_elem
            for spec_elem in [
                (lambda segment:
                    (lambda d: (
                        d.get('for'),
                        d.get('by'),
                        d.get('host'),
                        (
                            d.get('proto').lower()
                            if d.get('proto') is not None
                            else None
                        ),
                    ))(
                        {
                            name: value
                            for (name, value) in [
                                (lambda name, value: (
                                    name.lower(),
                                    (
                                        unquote_string(value)
                                        if (
                                            value is not None
                                            and len(value) > 0
                                            and value[0] == '"'
                                        )
                                        else value
                                    ),
                                ))(*m.groups())
                                for m in _FORWARDED_PAIR_RE.finditer(segment)
                            ]
                        }
                    )
                )(segment)
                for segment in forwarded.split(',')
            ]
            if any(v is not None for v in spec_elem)
        ]
    ),
)
```
```
@icontract.snapshot(lambda forwarded: forwarded.split(','), name="chunks")
@icontract.snapshot(lambda forwarded: [[(m.group(1).lower(), m.group(2)) for m in _FORWARDED_PAIR_RE.finditer(chunk)] for chunk in forwarded.split(',')], name="pairs_per_chunk")
@icontract.ensure(lambda OLD, result: len(result) == sum(1 for pairs in OLD.pairs_per_chunk if pairs))
@icontract.ensure(lambda result: all(isinstance(e, Forwarded) for e in result))
@icontract.ensure(lambda OLD, result: all(
    getattr(result[idx], attr) == exp.get(attr)
    for idx, exp in enumerate(
        [ { ({'by':'dest','for':'src','host':'host','proto':'scheme'}[n]) : ( (unquote_string(v) if (v and v[0] == '"') else v).lower() if n == 'proto' else (unquote_string(v) if (v and v[0] == '"') else v) )
            for n, v in pairs if n in ('by','for','host','proto') }
          for pairs in OLD.pairs_per_chunk if pairs ]
    )
    for attr in ('dest','src','host','scheme')
))
@icontract.ensure(lambda result: all((getattr(e, 'scheme') is None) or (isinstance(getattr(e, 'scheme'), str) and getattr(e, 'scheme') == getattr(e, 'scheme').lower()) for e in result))
@icontract.ensure(lambda result: all(getattr(e, 'dest') is None or isinstance(getattr(e, 'dest'), str) for e in result))
@icontract.ensure(lambda result: all(getattr(e, 'src') is None or isinstance(getattr(e, 'src'), str) for e in result))
@icontract.ensure(lambda result: all(getattr(e, 'host') is None or isinstance(getattr(e, 'host'), str) for e in result))
```
[1, 2, 4, 5, 6, 7, 10, 11, 64, 70, 71, 72, 73, 74, 83, 86, 88, 89, 90, 91, 92, 93, 94]
===== 1 =====
```
     elements = []
 
     pos = 0
-    end = len(forwarded)
+    end = 0  # This will cause the loop to never execute
     need_separator = False
     parsed_element = None
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = 0  # This will cause the loop to never execute
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 2 =====
```
     elements = []
 
     pos = 0
-    end = len(forwarded)
+    end = len(forwarded) // 2  # This will only process half of the forwarded header
     need_separator = False
     parsed_element = None
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded) // 2  # This will only process half of the forwarded header
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 4 =====
```
     need_separator = False
     parsed_element = None
 
-    while 0 <= pos < end:
+    while 0 < pos < end:
         match = _FORWARDED_PAIR_RE.match(forwarded, pos)
 
         if match is not None:  # got a valid forwarded-pair
@@ -97,4 +97,4 @@     if parsed_element:
         elements.append(parsed_element)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 < pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements

```
===== 5 =====
```
     need_separator = False
     parsed_element = None
 
-    while 0 <= pos < end:
+    while 1 <= pos < end:
         match = _FORWARDED_PAIR_RE.match(forwarded, pos)
 
         if match is not None:  # got a valid forwarded-pair
@@ -97,4 +97,4 @@     if parsed_element:
         elements.append(parsed_element)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 1 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements

```
===== 6 =====
```
     need_separator = False
     parsed_element = None
 
-    while 0 <= pos < end:
+    while pos < end and need_separator:  # Introduces a logical condition that may skip valid pairs
         match = _FORWARDED_PAIR_RE.match(forwarded, pos)
 
         if match is not None:  # got a valid forwarded-pair
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while pos < end and need_separator:  # Introduces a logical condition that may skip valid pairs
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 7 =====
```
     parsed_element = None
 
     while 0 <= pos < end:
-        match = _FORWARDED_PAIR_RE.match(forwarded, pos)
+        match = None
 
         if match is not None:  # got a valid forwarded-pair
             if need_separator:
@@ -97,4 +97,4 @@     if parsed_element:
         elements.append(parsed_element)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = None

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements

```
===== 10 =====
```
         match = _FORWARDED_PAIR_RE.match(forwarded, pos)
 
         if match is not None:  # got a valid forwarded-pair
-            if need_separator:
+            if not need_separator:
                 # bad syntax here, skip to next comma
                 pos = forwarded.find(',', pos)
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if not need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 11 =====
```
         match = _FORWARDED_PAIR_RE.match(forwarded, pos)
 
         if match is not None:  # got a valid forwarded-pair
-            if need_separator:
+            if not parsed_element:
                 # bad syntax here, skip to next comma
                 pos = forwarded.find(',', pos)
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if not parsed_element:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 64 =====
```
                     parsed_element.scheme = value.lower()
 
         elif forwarded[pos] == ',':  # next forwarded-element
-            need_separator = False
+            need_separator = True
             pos += 1
 
             # NOTE(kgriffs): It's possible that we arrive here without a
@@ -97,4 +97,4 @@     if parsed_element:
         elements.append(parsed_element)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = True
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements

```
===== 70 =====
```
             # NOTE(kgriffs): It's possible that we arrive here without a
             # parsed element if the header is malformed.
             if parsed_element:
-                elements.append(parsed_element)
+                elements.append(None)
                 parsed_element = None
 
         elif forwarded[pos] == ';':  # next forwarded-pair
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(None)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 71 =====
```
             # NOTE(kgriffs): It's possible that we arrive here without a
             # parsed element if the header is malformed.
             if parsed_element:
-                elements.append(parsed_element)
+                elements.append(None)
                 parsed_element = None
 
         elif forwarded[pos] == ';':  # next forwarded-pair
@@ -97,4 +97,4 @@     if parsed_element:
         elements.append(parsed_element)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(None)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements

```
===== 72 =====
```
             # NOTE(kgriffs): It's possible that we arrive here without a
             # parsed element if the header is malformed.
             if parsed_element:
-                elements.append(parsed_element)
+                elements.append(parsed_element.dest)
                 parsed_element = None
 
         elif forwarded[pos] == ';':  # next forwarded-pair
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element.dest)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 73 =====
```
             # NOTE(kgriffs): It's possible that we arrive here without a
             # parsed element if the header is malformed.
             if parsed_element:
-                elements.append(parsed_element)
+                elements.append(parsed_element.host)
                 parsed_element = None
 
         elif forwarded[pos] == ';':  # next forwarded-pair
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element.host)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 74 =====
```
             # NOTE(kgriffs): It's possible that we arrive here without a
             # parsed element if the header is malformed.
             if parsed_element:
-                elements.append(parsed_element)
+                elements.append(parsed_element.src)
                 parsed_element = None
 
         elif forwarded[pos] == ';':  # next forwarded-pair
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element.src)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 83 =====
```
 
         else:
             # bad syntax here, skip to next comma
-            pos = forwarded.find(',', pos)
+            pos = end  # Move to the end of the string, effectively skipping the rest of the header
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
     if parsed_element:
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = end  # Move to the end of the string, effectively skipping the rest of the header

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements
```
===== 86 =====
```
 
         else:
             # bad syntax here, skip to next comma
-            pos = forwarded.find(',', pos)
+            pos = forwarded.find('XX,XX', pos)
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
     if parsed_element:
         elements.append(parsed_element)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find('XX,XX', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element)

    return elements

```
===== 88 =====
```
             pos = forwarded.find(',', pos)
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
-    if parsed_element:
+    if len(elements) > 0:  # This will incorrectly check the elements list instead of parsed_element
         elements.append(parsed_element)
 
     return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if len(elements) > 0:  # This will incorrectly check the elements list instead of parsed_element
        elements.append(parsed_element)

    return elements
```
===== 89 =====
```
             pos = forwarded.find(',', pos)
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
-    if parsed_element:
+    if not parsed_element:  # This will skip adding valid parsed elements
         elements.append(parsed_element)
 
     return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if not parsed_element:  # This will skip adding valid parsed elements
        elements.append(parsed_element)

    return elements
```
===== 90 =====
```
             pos = forwarded.find(',', pos)
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
-    if parsed_element:
+    if parsed_element is None:  # This will also skip adding valid parsed elements
         elements.append(parsed_element)
 
     return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element is None:  # This will also skip adding valid parsed elements
        elements.append(parsed_element)

    return elements
```
===== 91 =====
```
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
     if parsed_element:
-        elements.append(parsed_element)
+        elements.append(None)
 
     return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(None)

    return elements
```
===== 92 =====
```
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
     if parsed_element:
-        elements.append(parsed_element)
+        elements.append(None)
 
-    return elements+    return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(None)

    return elements

```
===== 93 =====
```
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
     if parsed_element:
-        elements.append(parsed_element)
+        elements.append(parsed_element) if parsed_element.dest else None
 
     return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element) if parsed_element.dest else None

    return elements
```
===== 94 =====
```
 
     # NOTE(kgriffs): Add the last forwarded-element, if any
     if parsed_element:
-        elements.append(parsed_element)
+        elements.append(parsed_element) if parsed_element.scheme == 'http' else None
 
     return elements
```
```
def _parse_forwarded_header(forwarded: str) -> List[Forwarded]:
    """Parse the value of a Forwarded header.

    Makes an effort to parse Forwarded headers as specified by RFC 7239:

    - It checks that every value has valid syntax in general as specified
      in section 4: either a 'token' or a 'quoted-string'.
    - It un-escapes found escape sequences.
    - It does NOT validate 'by' and 'for' contents as specified in section
      6.
    - It does NOT validate 'host' contents (Host ABNF).
    - It does NOT validate 'proto' contents for valid URI scheme names.

    Arguments:
        forwarded (str): Value of a Forwarded header

    Returns:
        list: Sequence of Forwarded instances, representing each forwarded-element
        in the header, in the same order as they appeared in the header.
    """

    elements = []

    pos = 0
    end = len(forwarded)
    need_separator = False
    parsed_element = None

    while 0 <= pos < end:
        match = _FORWARDED_PAIR_RE.match(forwarded, pos)

        if match is not None:  # got a valid forwarded-pair
            if need_separator:
                # bad syntax here, skip to next comma
                pos = forwarded.find(',', pos)

            else:
                pos += len(match.group(0))
                need_separator = True

                name, value = match.groups()

                # NOTE(kgriffs): According to RFC 7239, parameter
                # names are case-insensitive.
                name = name.lower()

                if value[0] == '"':
                    value = unquote_string(value)

                # NOTE(kgriffs): If this is the first pair we've encountered
                # for this forwarded-element, initialize a new object.
                if not parsed_element:
                    parsed_element = Forwarded()

                if name == 'by':
                    parsed_element.dest = value
                elif name == 'for':
                    parsed_element.src = value
                elif name == 'host':
                    parsed_element.host = value
                elif name == 'proto':
                    # NOTE(kgriffs): RFC 7239 only requires that
                    # the "proto" value conform to the Host ABNF
                    # described in RFC 7230. The Host ABNF, in turn,
                    # does not require that the scheme be in any
                    # particular case, so we normalize it here to be
                    # consistent with the WSGI spec that *does*
                    # require the value of 'wsgi.url_scheme' to be
                    # either 'http' or 'https' (case-sensitive).
                    parsed_element.scheme = value.lower()

        elif forwarded[pos] == ',':  # next forwarded-element
            need_separator = False
            pos += 1

            # NOTE(kgriffs): It's possible that we arrive here without a
            # parsed element if the header is malformed.
            if parsed_element:
                elements.append(parsed_element)
                parsed_element = None

        elif forwarded[pos] == ';':  # next forwarded-pair
            need_separator = False
            pos += 1

        elif forwarded[pos] in ' \t':
            # Allow whitespace even between forwarded-pairs, though
            # RFC 7239 doesn't. This simplifies code and is in line
            # with Postel's law.
            pos += 1

        else:
            # bad syntax here, skip to next comma
            pos = forwarded.find(',', pos)

    # NOTE(kgriffs): Add the last forwarded-element, if any
    if parsed_element:
        elements.append(parsed_element) if parsed_element.scheme == 'http' else None

    return elements
```
