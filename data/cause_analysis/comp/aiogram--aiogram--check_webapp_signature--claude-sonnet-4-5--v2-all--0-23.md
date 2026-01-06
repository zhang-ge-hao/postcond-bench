https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/web_app.py#L111-L140
```
@icontract.ensure(lambda result: isinstance(result, bool))
@icontract.ensure(
    lambda init_data, result: not result or "hash" in dict(parse_qsl(init_data)),
    "If signature is valid, init_data must contain hash parameter"
)
@icontract.ensure(
    lambda init_data, result: not result or len(dict(parse_qsl(init_data))) > 0,
    "If signature is valid, init_data must be non-empty"
)
```
```
return value - primitive-like/scalar types

return value content

primitive-like/scalar types
```
passed
```
@icontract.ensure(lambda result, init_data: ("hash=" in init_data) or (result is False))
@icontract.ensure(lambda result, token, init_data: ("hash=" not in init_data) or (lambda pd: result == hmac.compare_digest(hmac.new(key=hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256).digest(), msg="\n".join("{}={}".format(k, v) for k, v in sorted(((k, v) for k, v in pd.items() if k != "hash"), key=lambda x: x[0])).encode(), digestmod=hashlib.sha256).hexdigest(), pd.get("hash")))(dict(parse_qsl(init_data, strict_parsing=True))))
```
===== 23: failed =====
```
     data_check_string = "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
     )
-    secret_key = hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256)
+    secret_key = hmac.new(key=b"XXWebAppDataXX", msg=token.encode(), digestmod=hashlib.sha256)
     calculated_hash = hmac.new(
         key=secret_key.digest(),
         msg=data_check_string.encode(),
         digestmod=hashlib.sha256,
     ).hexdigest()
-    return hmac.compare_digest(calculated_hash, hash_)+    return hmac.compare_digest(calculated_hash, hash_)
```
```
def check_webapp_signature(token: str, init_data: str) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token: bot Token
    :param init_data: data from frontend to be validated
    :return:
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:  # pragma: no cover
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False
    hash_ = parsed_data.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(key=b"XXWebAppDataXX", msg=token.encode(), digestmod=hashlib.sha256)
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(calculated_hash, hash_)

```
