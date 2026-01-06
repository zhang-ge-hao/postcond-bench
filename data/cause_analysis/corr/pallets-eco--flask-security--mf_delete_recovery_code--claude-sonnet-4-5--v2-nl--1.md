https://github.com/pallets-eco/flask-security/blob/06f37fa06ebbb0b9e87cd6819eb44d3aea050f60/./flask_security/datastore.py#L577-L592
```
@icontract.snapshot(lambda user, self: self.mf_get_recovery_codes(user), name="old_codes")
@icontract.snapshot(lambda user, self: len(self.mf_get_recovery_codes(user)), name="old_count")
@icontract.ensure(
    lambda result, old_count, user, self: 
    not result or len(self.mf_get_recovery_codes(user)) == old_count - 1,
    "If deletion succeeded, recovery codes count must decrease by 1"
)
@icontract.ensure(
    lambda result, old_codes, user, self:
    result or self.mf_get_recovery_codes(user) == old_codes,
    "If deletion failed, recovery codes must remain unchanged"
)
@icontract.ensure(
    lambda result, idx, old_count: not result or (0 <= idx < old_count),
    "Deletion can only succeed if index was valid"
)
@icontract.ensure(
    lambda result, idx, old_count: result or not (0 <= idx < old_count),
    "Deletion must fail if index was out of bounds"
)
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['old_count']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.snapshot(lambda user, idx: list(getattr(user, "mf_recovery_codes", [])), name="old_codes")
@icontract.ensure(lambda result, OLD, user, idx: result == (len(OLD.old_codes) > 0 and (-len(OLD.old_codes) <= idx < len(OLD.old_codes))))
@icontract.ensure(lambda result, OLD, user, idx: (not result and list(getattr(user, "mf_recovery_codes", [])) == OLD.old_codes) or (result and list(getattr(user, "mf_recovery_codes", [])) == (OLD.old_codes[: (idx if idx >= 0 else idx + len(OLD.old_codes))] + OLD.old_codes[(idx if idx >= 0 else idx + len(OLD.old_codes)) + 1 :])))
```
