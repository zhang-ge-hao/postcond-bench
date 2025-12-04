https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asn1crypto/_iri.py#L224-L270
```
@icontract.snapshot(lambda byte_string: byte_string, name="bs")
@icontract.snapshot(lambda remap: remap, name="rm")
@icontract.snapshot(lambda preserve: preserve, name="pv")
@icontract.ensure(
    lambda result, byte_string:
        (byte_string is None and result is None) or
        (byte_string is not None and isinstance(result, str))
)
@icontract.ensure(
    lambda result, byte_string:
        (byte_string == b'') == (result == '')
)
@icontract.ensure(
    lambda result, byte_string:
        (byte_string is None) or (byte_string == b'') or (result != '')
)
@icontract.ensure(
    lambda result, OLD:
        (not OLD.pv or not OLD.rm) or
        all(
            (c in result)
            if (OLD.bs is not None and c.encode('ascii') in OLD.bs)
            else True
            for c in (OLD.rm or [])
        )
)
@icontract.ensure(
    lambda result, OLD:
        (OLD.pv or not OLD.rm) or
        all(
            (('%%%02x' % ord(c)) in result)
            if (OLD.bs is not None and c.encode('ascii') in OLD.bs)
            else True
            for c in (OLD.rm or [])
        )
)
@icontract.ensure(
    lambda result, OLD:
        (not OLD.pv) or
        all(
            p not in result
            for p in ['\x1A', '\x1C', '\x1D', '\x1E', '\x1F']
        )
)
@icontract.ensure(
    lambda result, OLD:
        (not OLD.pv) or
        (OLD.bs is None) or
        all(
            (
                OLD.bs[j] < 0x20 or OLD.bs[j] > 0x7E
                or (OLD.rm is not None and chr(OLD.bs[j]) in OLD.rm)
                or (
                    (
                        j - 2 >= 0
                        and OLD.bs[j - 2] == ord('%')
                        and chr(OLD.bs[j - 1]) in '0123456789ABCDEFabcdef'
                        and chr(OLD.bs[j    ]) in '0123456789ABCDEFabcdef'
                    )
                    or (
                        j - 1 >= 0 and j + 1 < len(OLD.bs)
                        and OLD.bs[j - 1] == ord('%')
                        and chr(OLD.bs[j    ]) in '0123456789ABCDEFabcdef'
                        and chr(OLD.bs[j + 1]) in '0123456789ABCDEFabcdef'
                    )
                    or (
                        j + 2 < len(OLD.bs)
                        and OLD.bs[j    ] == ord('%')
                        and chr(OLD.bs[j + 1]) in '0123456789ABCDEFabcdef'
                        and chr(OLD.bs[j + 2]) in '0123456789ABCDEFabcdef'
                    )
                )
                or chr(OLD.bs[j]) in result
            )
            for j in range(len(OLD.bs))
        )
)
@icontract.ensure(
    lambda result, OLD:
        (not OLD.pv) or
        (OLD.bs is None) or
        (not OLD.rm) or
        (len(OLD.rm) != 1) or
        (len(OLD.bs) == 0) or
        (ord(OLD.rm[0]) > 127) or
        any(b != ord(OLD.rm[0]) for b in OLD.bs) or
        result == OLD.rm[0] * len(OLD.bs)
)
```
```
@icontract.snapshot(lambda byte_string: byte_string, name="bs")
@icontract.snapshot(lambda remap: remap, name="rm")
@icontract.snapshot(lambda preserve: preserve, name="pv")
@icontract.ensure(lambda result, byte_string: (byte_string is None and result is None) or (byte_string is not None and isinstance(result, str)))
@icontract.ensure(lambda result, byte_string: (byte_string == b'') == (result == ''))
@icontract.ensure(lambda result, byte_string: (byte_string is None) or (byte_string == b'') or (result != ''))
@icontract.ensure(lambda result, OLD: (not OLD.pv or not (OLD.rm)) or all((c in result) if (OLD.bs is not None and c.encode('ascii') in OLD.bs) else True for c in (OLD.rm or [])))
@icontract.ensure(lambda result, OLD: (OLD.pv or not (OLD.rm)) or all((('%%%02x' % ord(c)) in result) if (OLD.bs is not None and c.encode('ascii') in OLD.bs) else True for c in (OLD.rm or [])))
@icontract.ensure(lambda result, OLD: (not OLD.pv) or all(p not in result for p in ['\x1A','\x1C','\x1D','\x1E','\x1F']))
```
[6, 10, 11]
===== 6 =====
```
         for char in remap:
             replacement = replacements.pop(0)
             preserve_unmap[replacement] = char
-            byte_string = byte_string.replace(char.encode('ascii'), replacement.encode('ascii'))
+            byte_string = byte_string.replace(char.encode('ascii'), replacement.encode('ascii') + b'extra')  # Adds extra bytes
 
     byte_string = unquote_to_bytes(byte_string)
```
```
def _urlunquote(byte_string, remap=None, preserve=None):
    """
    Unquotes a URI portion from a byte string into unicode using UTF-8

    :param byte_string:
        A byte string of the data to unquote

    :param remap:
        A list of characters (as unicode) that should be re-mapped to a
        %XX encoding. This is used when characters are not valid in part of a
        URL.

    :param preserve:
        A bool - indicates that the chars to be remapped if they occur in
        non-hex form, should be preserved. E.g. / for URL path.

    :return:
        A unicode string
    """

    if byte_string is None:
        return byte_string

    if byte_string == b'':
        return ''

    if preserve:
        replacements = ['\x1A', '\x1C', '\x1D', '\x1E', '\x1F']
        preserve_unmap = {}
        for char in remap:
            replacement = replacements.pop(0)
            preserve_unmap[replacement] = char
            byte_string = byte_string.replace(char.encode('ascii'), replacement.encode('ascii') + b'extra')  # Adds extra bytes

    byte_string = unquote_to_bytes(byte_string)

    if remap:
        for char in remap:
            byte_string = byte_string.replace(char.encode('ascii'), ('%%%02x' % ord(char)).encode('ascii'))

    output = byte_string.decode('utf-8', 'iriutf8')

    if preserve:
        for replacement, original in preserve_unmap.items():
            output = output.replace(replacement, original)

    return output
```
===== 10 =====
```
 
     if preserve:
         for replacement, original in preserve_unmap.items():
-            output = output.replace(replacement, original)
+            output = None
 
-    return output+    return output
```
```
def _urlunquote(byte_string, remap=None, preserve=None):
    """
    Unquotes a URI portion from a byte string into unicode using UTF-8

    :param byte_string:
        A byte string of the data to unquote

    :param remap:
        A list of characters (as unicode) that should be re-mapped to a
        %XX encoding. This is used when characters are not valid in part of a
        URL.

    :param preserve:
        A bool - indicates that the chars to be remapped if they occur in
        non-hex form, should be preserved. E.g. / for URL path.

    :return:
        A unicode string
    """

    if byte_string is None:
        return byte_string

    if byte_string == b'':
        return ''

    if preserve:
        replacements = ['\x1A', '\x1C', '\x1D', '\x1E', '\x1F']
        preserve_unmap = {}
        for char in remap:
            replacement = replacements.pop(0)
            preserve_unmap[replacement] = char
            byte_string = byte_string.replace(char.encode('ascii'), replacement.encode('ascii'))

    byte_string = unquote_to_bytes(byte_string)

    if remap:
        for char in remap:
            byte_string = byte_string.replace(char.encode('ascii'), ('%%%02x' % ord(char)).encode('ascii'))

    output = byte_string.decode('utf-8', 'iriutf8')

    if preserve:
        for replacement, original in preserve_unmap.items():
            output = None

    return output

```
===== 11 =====
```
 
     if preserve:
         for replacement, original in preserve_unmap.items():
-            output = output.replace(replacement, original)
+            output = original
 
     return output
```
```
def _urlunquote(byte_string, remap=None, preserve=None):
    """
    Unquotes a URI portion from a byte string into unicode using UTF-8

    :param byte_string:
        A byte string of the data to unquote

    :param remap:
        A list of characters (as unicode) that should be re-mapped to a
        %XX encoding. This is used when characters are not valid in part of a
        URL.

    :param preserve:
        A bool - indicates that the chars to be remapped if they occur in
        non-hex form, should be preserved. E.g. / for URL path.

    :return:
        A unicode string
    """

    if byte_string is None:
        return byte_string

    if byte_string == b'':
        return ''

    if preserve:
        replacements = ['\x1A', '\x1C', '\x1D', '\x1E', '\x1F']
        preserve_unmap = {}
        for char in remap:
            replacement = replacements.pop(0)
            preserve_unmap[replacement] = char
            byte_string = byte_string.replace(char.encode('ascii'), replacement.encode('ascii'))

    byte_string = unquote_to_bytes(byte_string)

    if remap:
        for char in remap:
            byte_string = byte_string.replace(char.encode('ascii'), ('%%%02x' % ord(char)).encode('ascii'))

    output = byte_string.decode('utf-8', 'iriutf8')

    if preserve:
        for replacement, original in preserve_unmap.items():
            output = original

    return output
```
