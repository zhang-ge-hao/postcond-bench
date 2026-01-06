https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/forwarded.py#L93-L192
```
@icontract.snapshot(lambda forwarded: forwarded[:], name="forwarded_pre")
@icontract.ensure(lambda OLD, forwarded: forwarded == OLD.forwarded_pre)
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(isinstance(el, Forwarded) for el in result))
@icontract.ensure(lambda result: all((el.src is None or isinstance(el.src, str)) and (el.dest is None or isinstance(el.dest, str)) and (el.host is None or isinstance(el.host, str)) and (el.scheme is None or isinstance(el.scheme, str)) for el in result))
@icontract.ensure(lambda result: all((el.scheme is None) or (el.scheme == el.scheme.lower()) for el in result))
@icontract.ensure(lambda forwarded, result: ('=' in forwarded) or (len(result) == 0))
@icontract.ensure(lambda forwarded, result: len(result) <= forwarded.count(',') + 1)
@icontract.ensure(lambda forwarded, result: ('by=' in forwarded.lower()) or all(el.dest is None for el in result))
@icontract.ensure(lambda forwarded, result: ('for=' in forwarded.lower()) or all(el.src is None for el in result))
@icontract.ensure(lambda forwarded, result: ('host=' in forwarded.lower()) or all(el.host is None for el in result))
@icontract.ensure(lambda forwarded, result: ('proto=' in forwarded.lower()) or all(el.scheme is None for el in result))
```
```
Type error.

The replaced obj is str, do not have "scheme" attribute.

-                elements.append(parsed_element)
+                elements.append(parsed_element.host)
```
passed
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
===== 73 =====
local_crash
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
