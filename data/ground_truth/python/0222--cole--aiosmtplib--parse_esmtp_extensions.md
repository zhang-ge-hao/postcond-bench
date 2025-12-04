https://github.com/cole/aiosmtplib/blob/70a849a81c455ba93ba5d704585825879647d5c3/./src/aiosmtplib/esmtp.py#L15-L72
```
@icontract.snapshot(lambda message: message.split("\n"), name="lines")
@icontract.snapshot(lambda message: message.split("\n")[0], name="first")
@icontract.ensure(
    lambda result:
    isinstance(result, tuple)
    and isinstance(result[0], dict)
    and isinstance(result[1], list)
)
@icontract.ensure(
    lambda result:
    all(isinstance(k, str) and k == k.lower() for k in result[0].keys())
)
@icontract.ensure(
    lambda result:
    all(isinstance(v, str) for v in result[0].values())
)
@icontract.ensure(
    lambda result:
    all(isinstance(a, str) and a == a.strip() and a == a.lower() for a in result[1])
)
@icontract.ensure(
    lambda OLD, result:
    result[0]
    == {
        m.group("ext").lower(): line[m.end("ext") :].strip()
        for line in OLD.lines[1:]
        for m in [EXTENSIONS_REGEX.match(line)]
        if m is not None
    }
)
@icontract.ensure(
    lambda OLD, result:
    set(result[1])
    == {
        OLDSTYLE_AUTH_REGEX.match(line).group("auth").lower().strip()
        for line in OLD.lines[1:]
        if OLDSTYLE_AUTH_REGEX.match(line) is not None
    }.union(
        {
            param.strip().lower()
            for line in OLD.lines[1:]
            for m in [EXTENSIONS_REGEX.match(line)]
            if m is not None and m.group("ext").lower() == "auth"
            for param in line[m.end("ext") :].strip().split()
            if param.strip()
        }
    )
)
@icontract.ensure(
    lambda OLD, result:
    (OLD.first.strip() not in result[0].keys())
    and (OLD.first.strip() not in result[0].values())
    and (OLD.first.strip() not in result[1])
)
```
```
@icontract.snapshot(lambda message: message.split("\n"), name="lines")
@icontract.snapshot(lambda message: message.split("\n")[0], name="first")
@icontract.ensure(lambda result: isinstance(result, tuple) and isinstance(result[0], dict) and isinstance(result[1], list))
@icontract.ensure(lambda result: all(isinstance(k, str) and k == k.lower() for k in result[0].keys()))
@icontract.ensure(lambda result: all(isinstance(v, str) for v in result[0].values()))
@icontract.ensure(lambda result: all(isinstance(a, str) and a == a.strip() and a == a.lower() for a in result[1]))
@icontract.ensure(lambda OLD, result: all((OLDSTYLE_AUTH_REGEX.match(line) is None) or (OLDSTYLE_AUTH_REGEX.match(line).group("auth").lower().strip() in result[1]) for line in OLD.lines[1:]))
@icontract.ensure(lambda result: ('auth' not in result[0]) or all(p.strip().lower() in result[1] for p in result[0]['auth'].split()))
@icontract.ensure(lambda OLD, result: (OLD.first.strip() not in result[0].keys()) and (OLD.first.strip() not in result[0].values()) and (OLD.first.strip() not in result[1]))
```
[4, 5, 6, 7, 8, 10, 20, 21, 22, 30, 31, 32, 33, 39]
===== 4 =====
```
     esmtp_extensions: dict[str, str] = {}
     auth_types: list[str] = []
 
-    response_lines = message.split("\n")
+    response_lines = message.split(None)
 
     # ignore the first line
     for line in response_lines[1:]:
@@ -55,4 +55,4 @@             if extension == "auth":
                 auth_types.extend([param.strip().lower() for param in params.split()])
 
-    return esmtp_extensions, auth_types+    return esmtp_extensions, auth_types
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split(None)

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types

```
===== 5 =====
```
     response_lines = message.split("\n")
 
     # ignore the first line
-    for line in response_lines[1:]:
+    for line in response_lines:  # This will include the first line, which should be ignored.
         # To be able to communicate with as many SMTP servers as possible,
         # we have to take the old-style auth advertisement into account,
         # because:
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines:  # This will include the first line, which should be ignored.
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 6 =====
```
     response_lines = message.split("\n")
 
     # ignore the first line
-    for line in response_lines[1:]:
+    for line in response_lines[1:2]:  # This will only process the second line, ignoring all others.
         # To be able to communicate with as many SMTP servers as possible,
         # we have to take the old-style auth advertisement into account,
         # because:
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:2]:  # This will only process the second line, ignoring all others.
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 7 =====
```
     response_lines = message.split("\n")
 
     # ignore the first line
-    for line in response_lines[1:]:
+    for line in response_lines[1:3]:  # This will only process the second and third lines, ignoring the rest.
         # To be able to communicate with as many SMTP servers as possible,
         # we have to take the old-style auth advertisement into account,
         # because:
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:3]:  # This will only process the second and third lines, ignoring the rest.
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 8 =====
```
     response_lines = message.split("\n")
 
     # ignore the first line
-    for line in response_lines[1:]:
+    for line in response_lines[1:][::2]:  # This will process every other line starting from the second line.
         # To be able to communicate with as many SMTP servers as possible,
         # we have to take the old-style auth advertisement into account,
         # because:
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:][::2]:  # This will process every other line starting from the second line.
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 10 =====
```
     response_lines = message.split("\n")
 
     # ignore the first line
-    for line in response_lines[1:]:
+    for line in response_lines[:-1]:  # This will skip the last line instead of the first.
         # To be able to communicate with as many SMTP servers as possible,
         # we have to take the old-style auth advertisement into account,
         # because:
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[:-1]:  # This will skip the last line instead of the first.
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 20 =====
```
         # It's actually stricter, in that only spaces are allowed between
         # parameters, but were not going to check for that here.  Note
         # that the space isn't present if there are no parameters.
-        extensions = EXTENSIONS_REGEX.match(line)
+        extensions = EXTENSIONS_REGEX.fullmatch(line)
         if extensions is not None:
             extension = extensions.group("ext").lower()
             params = extensions.string[extensions.end("ext") :].strip()
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.fullmatch(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 21 =====
```
         # It's actually stricter, in that only spaces are allowed between
         # parameters, but were not going to check for that here.  Note
         # that the space isn't present if there are no parameters.
-        extensions = EXTENSIONS_REGEX.match(line)
+        extensions = None
         if extensions is not None:
             extension = extensions.group("ext").lower()
             params = extensions.string[extensions.end("ext") :].strip()
@@ -55,4 +55,4 @@             if extension == "auth":
                 auth_types.extend([param.strip().lower() for param in params.split()])
 
-    return esmtp_extensions, auth_types+    return esmtp_extensions, auth_types
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = None
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types

```
===== 22 =====
```
         # parameters, but were not going to check for that here.  Note
         # that the space isn't present if there are no parameters.
         extensions = EXTENSIONS_REGEX.match(line)
-        if extensions is not None:
+        if line.startswith("250-"):
             extension = extensions.group("ext").lower()
             params = extensions.string[extensions.end("ext") :].strip()
             esmtp_extensions[extension] = params
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if line.startswith("250-"):
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 30 =====
```
         extensions = EXTENSIONS_REGEX.match(line)
         if extensions is not None:
             extension = extensions.group("ext").lower()
-            params = extensions.string[extensions.end("ext") :].strip()
+            params = extensions.string[extensions.end("ext") :].replace(" ", "_").strip()
             esmtp_extensions[extension] = params
 
             if extension == "auth":
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].replace(" ", "_").strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 31 =====
```
         extensions = EXTENSIONS_REGEX.match(line)
         if extensions is not None:
             extension = extensions.group("ext").lower()
-            params = extensions.string[extensions.end("ext") :].strip()
+            params = extensions.string[extensions.end("ext") :].strip() + " extra_param"
             esmtp_extensions[extension] = params
 
             if extension == "auth":
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip() + " extra_param"
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 32 =====
```
         extensions = EXTENSIONS_REGEX.match(line)
         if extensions is not None:
             extension = extensions.group("ext").lower()
-            params = extensions.string[extensions.end("ext") :].strip()
+            params = extensions.string[extensions.start("ext") :].strip()
             esmtp_extensions[extension] = params
 
             if extension == "auth":
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.start("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 33 =====
```
         extensions = EXTENSIONS_REGEX.match(line)
         if extensions is not None:
             extension = extensions.group("ext").lower()
-            params = extensions.string[extensions.end("ext") :].strip()
+            params = extensions.string[extensions.start("ext") :].strip().split(",")[0]
             esmtp_extensions[extension] = params
 
             if extension == "auth":
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.start("ext") :].strip().split(",")[0]
            esmtp_extensions[extension] = params

            if extension == "auth":
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
===== 39 =====
```
             params = extensions.string[extensions.end("ext") :].strip()
             esmtp_extensions[extension] = params
 
-            if extension == "auth":
+            if extension == "auth" or params:
                 auth_types.extend([param.strip().lower() for param in params.split()])
 
     return esmtp_extensions, auth_types
```
```
def parse_esmtp_extensions(message: str) -> tuple[dict[str, str], list[str]]:
    """
    Parse an EHLO response from the server into a dict of {extension: params}
    and a list of auth method names.

    It might look something like:

         220 size.does.matter.af.MIL (More ESMTP than Crappysoft!)
         EHLO heaven.af.mil
         250-size.does.matter.af.MIL offers FIFTEEN extensions:
         250-8BITMIME
         250-PIPELINING
         250-DSN
         250-ENHANCEDSTATUSCODES
         250-EXPN
         250-HELP
         250-SAML
         250-SEND
         250-SOML
         250-TURN
         250-XADR
         250-XSTA
         250-ETRN
         250-XGEN
         250 SIZE 51200000
    """
    esmtp_extensions: dict[str, str] = {}
    auth_types: list[str] = []

    response_lines = message.split("\n")

    # ignore the first line
    for line in response_lines[1:]:
        # To be able to communicate with as many SMTP servers as possible,
        # we have to take the old-style auth advertisement into account,
        # because:
        # 1) Else our SMTP feature parser gets confused.
        # 2) There are some servers that only advertise the auth methods we
        #    support using the old style.
        auth_match = OLDSTYLE_AUTH_REGEX.match(line)
        if auth_match is not None:
            auth_type = auth_match.group("auth")
            auth_types.append(auth_type.lower().strip())

        # RFC 1869 requires a space between ehlo keyword and parameters.
        # It's actually stricter, in that only spaces are allowed between
        # parameters, but were not going to check for that here.  Note
        # that the space isn't present if there are no parameters.
        extensions = EXTENSIONS_REGEX.match(line)
        if extensions is not None:
            extension = extensions.group("ext").lower()
            params = extensions.string[extensions.end("ext") :].strip()
            esmtp_extensions[extension] = params

            if extension == "auth" or params:
                auth_types.extend([param.strip().lower() for param in params.split()])

    return esmtp_extensions, auth_types
```
