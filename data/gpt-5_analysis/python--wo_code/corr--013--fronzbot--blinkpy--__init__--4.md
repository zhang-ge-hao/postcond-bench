https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/auth.py#L28-L68
```
@icontract.ensure(lambda self, login_data: getattr(self, "login_data", getattr(self, "_login_data", None)) == login_data)
@icontract.ensure(lambda self, no_prompt: getattr(self, "no_prompt", getattr(self, "_no_prompt", None)) == no_prompt)
@icontract.ensure(lambda self, session: (session is None and (getattr(self, "session", getattr(self, "_session", None)) is None or isinstance(getattr(self, "session", getattr(self, "_session", None)), ClientSession))) or (getattr(self, "session", getattr(self, "_session", None)) is session))
@icontract.ensure(lambda self, agent: getattr(self, "agent", getattr(self, "_agent", None)) == agent)
@icontract.ensure(lambda self, app_build: getattr(self, "app_build", getattr(self, "_app_build", None)) == app_build)
@icontract.ensure(lambda self, callback: getattr(self, "callback", getattr(self, "_callback", None)) == callback)
```
```
Hallucination.

The comment does not specify the usage of "login_data".
@icontract.ensure(lambda self, login_data: getattr(self, "login_data", getattr(self, "_login_data", None)) == login_data)
This postcondition is from hallucination.
```
icontract_fail
```
@icontract.snapshot(lambda _ARGS: _ARGS[1] if len(_ARGS) > 1 else None, name="LD")
@icontract.ensure(lambda OLD, self: (OLD.LD is None and self.data == {}) or (OLD.LD is not None and self.data is OLD.LD))
@icontract.ensure(lambda OLD, self: self.token == (OLD.LD.get("token", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.expires_in == (OLD.LD.get("expires_in", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.expiration_date == (OLD.LD.get("expiration_date", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.refresh_token == (OLD.LD.get("refresh_token", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.host == (OLD.LD.get("host", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.region_id == (OLD.LD.get("region_id", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.client_id == (OLD.LD.get("client_id", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.account_id == (OLD.LD.get("account_id", None) if OLD.LD is not None else None))
@icontract.ensure(lambda OLD, self: self.user_id == (OLD.LD.get("user_id", None) if OLD.LD is not None else None))
@icontract.ensure(lambda self: self.login_response is None)
@icontract.ensure(lambda self: self.tier_info is None)
@icontract.ensure(lambda self: self.is_errored is False)
@icontract.ensure(lambda self, no_prompt: self.no_prompt == no_prompt)
@icontract.ensure(lambda self, agent: self._agent == agent)
@icontract.ensure(lambda self, app_build: self._app_build == app_build)
@icontract.ensure(lambda self, session: (session is not None and self.session is session) or (session is None and self.session is not None))
@icontract.ensure(lambda self, callback: self.callback is callback)
```
