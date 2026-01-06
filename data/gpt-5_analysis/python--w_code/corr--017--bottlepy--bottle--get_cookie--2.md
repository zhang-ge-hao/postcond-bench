https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1175-L1191
```
@icontract.snapshot(lambda self, key: self.cookies.get(key), name="raw_cookie")
@icontract.snapshot(lambda self, key, secret, digestmod: (lambda cv: (False, None) if not (secret and isinstance(cv, str) and cv.startswith('!') and ('?' in cv)) else (lambda sigmsg: (lambda sig, msg: (lambda digest: (lambda ok: (ok, (pickle.loads(base64.b64decode(msg))[1] if ok else None)))(_lscmp(sig, base64.b64encode(digest)) and (lambda dst: (bool(dst) and dst[0] == key))(pickle.loads(base64.b64decode(msg)))))(hmac.new(tob(secret), msg, digestmod=digestmod).digest()))(cv[1:].split('?', 1)))(self.cookies.get(key)), name="signed")
@icontract.ensure(lambda OLD, result, secret, default: (not secret) or result == (OLD.signed[1] if OLD.signed[0] else default))
@icontract.ensure(lambda OLD, result, secret, default: secret or result == (OLD.raw_cookie or default))
```
```
Syntax error.

E   SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```
syntax_error
```
@icontract.snapshot(lambda self, key, default=None, secret=None, digestmod=hashlib.sha256: self.cookies.get(key), name="raw")
@icontract.ensure(lambda OLD, result, key, default=None, secret=None, digestmod=hashlib.sha256:
    (not secret and result == (OLD.raw or default))
    or (secret and (
        (OLD.raw is None and result == default)
        or (not (OLD.raw and OLD.raw.startswith('!') and '?' in OLD.raw) and result == default)
        or (
            OLD.raw and OLD.raw.startswith('!') and '?' in OLD.raw and (
                (
                    _lscmp(
                        tuple(map(tob, OLD.raw[1:].split('?', 1)))[0],
                        base64.b64encode(
                            hmac.new(
                                tob(secret),
                                tuple(map(tob, OLD.raw[1:].split('?', 1)))[1],
                                digestmod=digestmod
                            ).digest()
                        )
                    )
                    and (
                        pickle.loads(base64.b64decode(tuple(map(tob, OLD.raw[1:].split('?', 1)))[1]))
                        and pickle.loads(base64.b64decode(tuple(map(tob, OLD.raw[1:].split('?', 1)))[1]))[0] == key
                        and result == pickle.loads(base64.b64decode(tuple(map(tob, OLD.raw[1:].split('?', 1)))[1]))[1]
                    )
                )
                or (
                    not _lscmp(
                        tuple(map(tob, OLD.raw[1:].split('?', 1)))[0],
                        base64.b64encode(
                            hmac.new(
                                tob(secret),
                                tuple(map(tob, OLD.raw[1:].split('?', 1)))[1],
                                digestmod=digestmod
                            ).digest()
                        )
                    ) and result == default
                )
            )
        )
    ))
)
```
