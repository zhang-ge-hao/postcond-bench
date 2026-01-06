https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/datastore.py#L577-L592
```
@icontract.snapshot(lambda self, user: self.mf_get_recovery_codes(user), name="old_codes")
@icontract.ensure(lambda result, old_codes, self, user: 
    len(self.mf_get_recovery_codes(user)) == len(old_codes) - 1 if result else len(self.mf_get_recovery_codes(user)) == len(old_codes))
@icontract.ensure(lambda result, idx, old_codes: not result or (0 <= idx < len(old_codes)))
@icontract.ensure(lambda result, old_codes, self, user, idx:
    not result or (self.mf_get_recovery_codes(user) == old_codes[:idx] + old_codes[idx+1:]))
```
```
limited spec

old_codes
```
failed
```
@icontract.snapshot(lambda user, idx: list(getattr(user, "mf_recovery_codes", [])), name="old_codes")
@icontract.ensure(lambda result, OLD, user, idx: result == (len(OLD.old_codes) > 0 and (-len(OLD.old_codes) <= idx < len(OLD.old_codes))))
@icontract.ensure(lambda result, OLD, user, idx: (not result and list(getattr(user, "mf_recovery_codes", [])) == OLD.old_codes) or (result and list(getattr(user, "mf_recovery_codes", [])) == (OLD.old_codes[: (idx if idx >= 0 else idx + len(OLD.old_codes))] + OLD.old_codes[(idx if idx >= 0 else idx + len(OLD.old_codes)) + 1 :])))
```
