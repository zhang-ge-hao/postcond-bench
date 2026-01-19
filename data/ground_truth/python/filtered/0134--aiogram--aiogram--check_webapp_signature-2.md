https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/web_app_signature.py#L16-L57
```
🈚️

It's hard

@icontract.ensure(
    lambda bot_id, init_data, public_key_bytes, result:
        # 如果函数返回 False，我们对它不做任何强约束（短路直接 True）
        (not result)
        or (
            # ===== 以下是“规范算法”：用 Telegram 文档里的流程重算一遍 =====
            # 1) 解析 init_data
            (parsed_data := dict(parse_qsl(init_data, strict_parsing=True))) is not None
            # 2) 取出并移除 signature 参数
            and (signature_b64 := parsed_data.pop("signature", None)) is not None
            # 3) hash 字段在构造 data_check_string 时必须被排除
            and (parsed_data.pop("hash", None) or True)
            # 4) 构造 data_check_string
            and (
                data_check_string := (
                    f"{bot_id}:WebAppData\n"
                    + "\n".join(
                        f"{k}={v}"
                        for k, v in sorted(parsed_data.items(), key=itemgetter(0))
                    )
                )
            ) is not None
            # 5) 还原 signature 的字节
            and (
                signature := base64.urlsafe_b64decode(
                    signature_b64 + "=" * (-len(signature_b64) % 4)
                )
            ) is not None
            # 6) 构造 Ed25519 公钥
            and (
                public_key := Ed25519PublicKey.from_public_bytes(public_key_bytes)
            ) is not None
            # 7) 使用 Ed25519 验证签名：如果成功则返回 None，不抛异常
            and public_key.verify(signature, data_check_string.encode()) is None
        ),
    "If check_webapp_signature returns True, the signature MUST be valid "
    "according to the Telegram WebApp specification.",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
===== 0 =====
```
     :return: True if signature is valid, False otherwise
     """
     try:
-        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
+        parsed_data = dict(parse_qsl(None, strict_parsing=True))
     except ValueError:
         return False
 
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(None, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 1 =====
```
     try:
         parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
     except ValueError:
-        return False
+        return True
 
     signature_b64 = parsed_data.pop("signature", None)
     if not signature_b64:
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return True

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 2 =====
```
     except ValueError:
         return False
 
-    signature_b64 = parsed_data.pop("signature", None)
+    signature_b64 = None
     if not signature_b64:
         return False
 
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = None
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 3 =====
```
     except ValueError:
         return False
 
-    signature_b64 = parsed_data.pop("signature", None)
+    signature_b64 = parsed_data.get("signature", None)
     if not signature_b64:
         return False
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.get("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 4 =====
```
     except ValueError:
         return False
 
-    signature_b64 = parsed_data.pop("signature", None)
+    signature_b64 = parsed_data.pop("SIGNATURE", None)
     if not signature_b64:
         return False
 
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("SIGNATURE", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 5 =====
```
     except ValueError:
         return False
 
-    signature_b64 = parsed_data.pop("signature", None)
+    signature_b64 = parsed_data.pop("XXsignatureXX", None)
     if not signature_b64:
         return False
 
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("XXsignatureXX", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 6 =====
```
     except ValueError:
         return False
 
-    signature_b64 = parsed_data.pop("signature", None)
+    signature_b64 = parsed_data.pop("sig", None)
     if not signature_b64:
         return False
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("sig", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 7 =====
```
     except ValueError:
         return False
 
-    signature_b64 = parsed_data.pop("signature", None)
+    signature_b64 = parsed_data.pop(None, None)
     if not signature_b64:
         return False
 
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop(None, None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 8 =====
```
 
     signature_b64 = parsed_data.pop("signature", None)
     if not signature_b64:
-        return False
+        return True
 
     parsed_data.pop("hash", None)
 
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return True

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 9 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("HASH", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("HASH", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 10 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("XXhashXX", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("XXhashXX", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 11 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("bot_id", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("bot_id", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 12 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("data", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("data", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 13 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("extra_info", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("extra_info", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 14 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("signature", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("signature", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 15 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop("timestamp", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("timestamp", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 16 =====
```
     if not signature_b64:
         return False
 
-    parsed_data.pop("hash", None)
+    parsed_data.pop(None, None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop(None, None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 17 =====
```
 
     parsed_data.pop("hash", None)
 
-    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
+    data_check_string = f"{bot_id}:WebAppData\n" + "XX\nXX".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
     )
     message = data_check_string.encode()
@@ -39,4 +39,4 @@     except InvalidSignature:
         return False
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "XX\nXX".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True

```
===== 18 =====
```
     parsed_data.pop("hash", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
-        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
+        f"{k}:{v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
     )
     message = data_check_string.encode()
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}:{v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 19 =====
```
     parsed_data.pop("hash", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
-        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
+        f"{k}={v}" for k, v in parsed_data.items()
     )
     message = data_check_string.encode()
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in parsed_data.items()
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 20 =====
```
     parsed_data.pop("hash", None)
 
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
-        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
+        f"{k}={v}" for k, v in sorted(parsed_data.items(), reverse=True)
     )
     message = data_check_string.encode()
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), reverse=True)
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 21 =====
```
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
     )
-    message = data_check_string.encode()
+    message = data_check_string.encode('utf-16')
 
     padding = "=" * (-len(signature_b64) % 4)
     signature = base64.urlsafe_b64decode(signature_b64 + padding)
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode('utf-16')

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 22 =====
```
     data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
         f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
     )
-    message = data_check_string.encode()
+    message = data_check_string.encode() + b'\x00'
 
     padding = "=" * (-len(signature_b64) % 4)
     signature = base64.urlsafe_b64decode(signature_b64 + padding)
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode() + b'\x00'

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 23 =====
```
     message = data_check_string.encode()
 
     padding = "=" * (-len(signature_b64) % 4)
-    signature = base64.urlsafe_b64decode(signature_b64 + padding)
+    signature = base64.b64decode(signature_b64 + padding)
 
     public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 24 =====
```
     padding = "=" * (-len(signature_b64) % 4)
     signature = base64.urlsafe_b64decode(signature_b64 + padding)
 
-    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
+    public_key = Ed25519PublicKey.from_public_bytes(b'\x00' * 32)  # Uses a zeroed-out public key
 
     try:
         public_key.verify(signature, message)
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(b'\x00' * 32)  # Uses a zeroed-out public key

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 25 =====
```
     padding = "=" * (-len(signature_b64) % 4)
     signature = base64.urlsafe_b64decode(signature_b64 + padding)
 
-    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
+    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes[::-1])  # Reverses the public key bytes
 
     try:
         public_key.verify(signature, message)
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes[::-1])  # Reverses the public key bytes

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return True
```
===== 26 =====
```
     public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
 
     try:
-        public_key.verify(signature, message)
+        public_key.verify(signature, b"")  # Verifies against an empty message
     except InvalidSignature:
         return False
     else:
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, b"")  # Verifies against an empty message
    except InvalidSignature:
        return False
    else:
        return True
```
===== 27 =====
```
     public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
 
     try:
-        public_key.verify(signature, message)
+        public_key.verify(signature, message + b"extra_data")  # Appends extra data to the message
     except InvalidSignature:
         return False
     else:
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message + b"extra_data")  # Appends extra data to the message
    except InvalidSignature:
        return False
    else:
        return True
```
===== 28 =====
```
     public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
 
     try:
-        public_key.verify(signature, message)
+        public_key.verify(signature, message + b"tampered")
     except InvalidSignature:
         return False
     else:
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message + b"tampered")
    except InvalidSignature:
        return False
    else:
        return True
```
===== 29 =====
```
     public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
 
     try:
-        public_key.verify(signature, message)
+        public_key.verify(signature, message[:10])  # Only verifies the first 10 bytes of the message
     except InvalidSignature:
         return False
     else:
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message[:10])  # Only verifies the first 10 bytes of the message
    except InvalidSignature:
        return False
    else:
        return True
```
===== 30 =====
```
     public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
 
     try:
-        public_key.verify(signature, message)
+        public_key.verify(signature, message[::-1])  # Verifies the message in reverse order
     except InvalidSignature:
         return False
     else:
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message[::-1])  # Verifies the message in reverse order
    except InvalidSignature:
        return False
    else:
        return True
```
===== 31 =====
```
     try:
         public_key.verify(signature, message)
     except InvalidSignature:
-        return False
+        return True
     else:
-        return True+        return True
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return True
    else:
        return True

```
===== 32 =====
```
     except InvalidSignature:
         return False
     else:
-        return True+        return False
```
```
def check_webapp_signature(
    bot_id: int,
    init_data: str,
    public_key_bytes: bytes = PRODUCTION_PUBLIC_KEY,
) -> bool:
    """
    Check incoming WebApp init data signature without bot token using only bot id.

    Source: https://core.telegram.org/bots/webapps#validating-data-for-third-party-use

    :param bot_id: Bot ID
    :param init_data: WebApp init data
    :param public_key: Public key
    :return: True if signature is valid, False otherwise
    """
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False

    signature_b64 = parsed_data.pop("signature", None)
    if not signature_b64:
        return False

    parsed_data.pop("hash", None)

    data_check_string = f"{bot_id}:WebAppData\n" + "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    message = data_check_string.encode()

    padding = "=" * (-len(signature_b64) % 4)
    signature = base64.urlsafe_b64decode(signature_b64 + padding)

    public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    else:
        return False

```
