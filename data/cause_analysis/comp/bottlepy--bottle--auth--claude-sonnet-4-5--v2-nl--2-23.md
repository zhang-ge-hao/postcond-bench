https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1460-L1472
```
@icontract.ensure(lambda result: result is None or (isinstance(result, tuple) and len(result) == 2))
@icontract.ensure(lambda result: result is None or isinstance(result[0], str))
@icontract.ensure(lambda result: result is None or (result[1] is None or isinstance(result[1], str)))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars

condition of none

built-in container of scalars
```
passed
```
@icontract.snapshot(lambda self: self.environ.get('HTTP_AUTHORIZATION', ''), name='auth_header')
@icontract.snapshot(lambda self: parse_auth(self.environ.get('HTTP_AUTHORIZATION', '')), name='basic')
@icontract.snapshot(lambda self: self.environ.get('REMOTE_USER'), name='ruser')
@icontract.ensure(lambda OLD, result, self: (result is None) or (isinstance(result, tuple) and len(result) == 2))
@icontract.ensure(lambda OLD, result, self: (OLD.basic and result == OLD.basic) or (not OLD.basic and ((OLD.ruser and result == (OLD.ruser, None)) or (not OLD.ruser and result is None))))
```
===== 23: failed =====
```
         basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
         if basic: return basic
         ruser = self.environ.get('REMOTE_USER')
-        if ruser: return (ruser, None)
+        if ruser: return (ruser, 'default_password')  # Returns a hardcoded password instead of None
         return None
```
```
    @property
    def auth(self):
        """ HTTP authentication data as a (user, password) tuple. This
            implementation currently supports basic (not digest) authentication
            only. If the authentication happened at a higher level (e.g. in the
            front web-server or a middleware), the password field is None, but
            the user field is looked up from the ``REMOTE_USER`` environ
            variable. On any errors, None is returned. """
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic: return basic
        ruser = self.environ.get('REMOTE_USER')
        if ruser: return (ruser, 'default_password')  # Returns a hardcoded password instead of None
        return None
```
