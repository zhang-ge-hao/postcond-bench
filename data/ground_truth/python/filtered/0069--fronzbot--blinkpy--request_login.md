https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/api.py#L29-L80
```
🈚️

async
```
```
@icontract.snapshot(lambda login_data: dict(login_data), name="OLD_login")
@icontract.ensure(lambda _result, auth: getattr(getattr(auth, "query", None), "call_args", None) is not None)
@icontract.ensure(lambda _result, auth, url: getattr(auth.query.call_args[1], "get")( "url") == url)
@icontract.ensure(lambda _result, auth, login_data: auth.query.call_args[1].get("headers") == {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": DEFAULT_USER_AGENT,
    "hardware_id": login_data.get("device_id", "Blinkpy"),
})
@icontract.ensure(lambda _result, auth, login_data: (("2fa_code" not in login_data) or auth.query.call_args[1].get("headers").get("2fa-code") == login_data["2fa_code"]))
@icontract.ensure(lambda _result, auth, login_data, is_refresh: auth.query.call_args[1].get("data") == urlencode(
    {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
        **(
            ({"grant_type": OAUTH_GRANT_TYPE_REFRESH_TOKEN, "refresh_token": getattr(auth, "refresh_token", None)})
            if is_refresh
            else {"grant_type": OAUTH_GRANT_TYPE_PASSWORD, "password": login_data["password"]}
        )
    }
))
@icontract.ensure(lambda _result, auth: auth.query.call_args[1].get("json_resp") is False)
@icontract.ensure(lambda _result, auth: auth.query.call_args[1].get("reqtype") == "post")
@icontract.ensure(lambda _result, auth, is_retry: auth.query.call_args[1].get("is_retry") == is_retry)
@icontract.ensure(lambda _result, auth: auth.query.call_args[1].get("skip_refresh_check") is True)
@icontract.ensure(lambda OLD, login_data: dict(login_data) == OLD.OLD_login)
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]
===== 0 =====
```
     :param two_fa_code: 2FA code if required
     """
 
-    headers = {
-        "Content-Type": "application/x-www-form-urlencoded",
-        "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
-    }
+    headers = None
 
     # Add 2FA code to headers if provided
     if "2fa_code" in login_data:
@@ -49,4 +45,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = None

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 1 =====
```
     """
 
     headers = {
-        "Content-Type": "application/x-www-form-urlencoded",
+        "CONTENT-TYPE": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "CONTENT-TYPE": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 2 =====
```
     """
 
     headers = {
-        "Content-Type": "application/x-www-form-urlencoded",
+        "Content-Type": "APPLICATION/X-WWW-FORM-URLENCODED",
         "User-Agent": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "APPLICATION/X-WWW-FORM-URLENCODED",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 3 =====
```
     """
 
     headers = {
-        "Content-Type": "application/x-www-form-urlencoded",
+        "Content-Type": "XXapplication/x-www-form-urlencodedXX",
         "User-Agent": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "XXapplication/x-www-form-urlencodedXX",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 4 =====
```
     """
 
     headers = {
-        "Content-Type": "application/x-www-form-urlencoded",
+        "XXContent-TypeXX": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "XXContent-TypeXX": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 5 =====
```
     """
 
     headers = {
-        "Content-Type": "application/x-www-form-urlencoded",
+        "content-type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 6 =====
```
 
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
-        "User-Agent": DEFAULT_USER_AGENT,
+        "USER-AGENT": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
 
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "USER-AGENT": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 7 =====
```
 
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
-        "User-Agent": DEFAULT_USER_AGENT,
+        "XXUser-AgentXX": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
 
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "XXUser-AgentXX": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 8 =====
```
 
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
-        "User-Agent": DEFAULT_USER_AGENT,
+        "user-agent": DEFAULT_USER_AGENT,
         "hardware_id": login_data.get("device_id", "Blinkpy"),
     }
 
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 9 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "HARDWARE_ID": login_data.get("device_id", "Blinkpy"),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "HARDWARE_ID": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 10 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "XXhardware_idXX": login_data.get("device_id", "Blinkpy"),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "XXhardware_idXX": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 11 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("Blinkpy"),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 12 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", "BLINKPY"),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "BLINKPY"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 13 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", "Blinkpy") if "device_id" in login_data else "DefaultDevice",
     }
 
     # Add 2FA code to headers if provided
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy") if "device_id" in login_data else "DefaultDevice",
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 14 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", "Blinkpy").upper(),
     }
 
     # Add 2FA code to headers if provided
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy").upper(),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 15 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", "UnknownDevice"),
     }
 
     # Add 2FA code to headers if provided
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "UnknownDevice"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 16 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", "XXBlinkpyXX"),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "XXBlinkpyXX"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 17 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", "blinkpy"),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 18 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", ),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", ),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 19 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", None),
     }
 
     # Add 2FA code to headers if provided
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", None),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 20 =====
```
     headers = {
         "Content-Type": "application/x-www-form-urlencoded",
         "User-Agent": DEFAULT_USER_AGENT,
-        "hardware_id": login_data.get("device_id", "Blinkpy"),
+        "hardware_id": login_data.get("device_id", None),
     }
 
     # Add 2FA code to headers if provided
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", None),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 21 =====
```
 
     # Prepare form data for OAuth
     form_data = {
-        "username": login_data["username"],
+        "USERNAME": login_data["username"],
         "client_id": OAUTH_CLIENT_ID,
         "scope": OAUTH_SCOPE,
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "USERNAME": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 22 =====
```
 
     # Prepare form data for OAuth
     form_data = {
-        "username": login_data["username"],
+        "XXusernameXX": login_data["username"],
         "client_id": OAUTH_CLIENT_ID,
         "scope": OAUTH_SCOPE,
     }
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "XXusernameXX": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 23 =====
```
     # Prepare form data for OAuth
     form_data = {
         "username": login_data["username"],
-        "client_id": OAUTH_CLIENT_ID,
+        "CLIENT_ID": OAUTH_CLIENT_ID,
         "scope": OAUTH_SCOPE,
     }
 
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "CLIENT_ID": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 24 =====
```
     # Prepare form data for OAuth
     form_data = {
         "username": login_data["username"],
-        "client_id": OAUTH_CLIENT_ID,
+        "XXclient_idXX": OAUTH_CLIENT_ID,
         "scope": OAUTH_SCOPE,
     }
 
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "XXclient_idXX": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 25 =====
```
     form_data = {
         "username": login_data["username"],
         "client_id": OAUTH_CLIENT_ID,
-        "scope": OAUTH_SCOPE,
+        "SCOPE": OAUTH_SCOPE,
     }
 
     if is_refresh:
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "SCOPE": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 26 =====
```
     form_data = {
         "username": login_data["username"],
         "client_id": OAUTH_CLIENT_ID,
-        "scope": OAUTH_SCOPE,
+        "XXscopeXX": OAUTH_SCOPE,
     }
 
     if is_refresh:
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "XXscopeXX": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 27 =====
```
         "scope": OAUTH_SCOPE,
     }
 
-    if is_refresh:
+    if is_retry:  # Incorrectly checks for retry instead of refresh
         form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
         form_data["refresh_token"] = auth.refresh_token
     else:
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_retry:  # Incorrectly checks for retry instead of refresh
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 28 =====
```
         "scope": OAUTH_SCOPE,
     }
 
-    if is_refresh:
+    if login_data.get("2fa_code"):  # Checks for 2FA code instead of refresh
         form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
         form_data["refresh_token"] = auth.refresh_token
     else:
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if login_data.get("2fa_code"):  # Checks for 2FA code instead of refresh
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 29 =====
```
         "scope": OAUTH_SCOPE,
     }
 
-    if is_refresh:
+    if not is_refresh:  # Negates the condition, leading to incorrect behavior
         form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
         form_data["refresh_token"] = auth.refresh_token
     else:
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if not is_refresh:  # Negates the condition, leading to incorrect behavior
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 30 =====
```
     }
 
     if is_refresh:
-        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
+        form_data["GRANT_TYPE"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
         form_data["refresh_token"] = auth.refresh_token
     else:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["GRANT_TYPE"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 31 =====
```
     }
 
     if is_refresh:
-        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
+        form_data["XXgrant_typeXX"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
         form_data["refresh_token"] = auth.refresh_token
     else:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["XXgrant_typeXX"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 32 =====
```
     }
 
     if is_refresh:
-        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
+        form_data["grant_type"] = None
         form_data["refresh_token"] = auth.refresh_token
     else:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = None
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 33 =====
```
 
     if is_refresh:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
-        form_data["refresh_token"] = auth.refresh_token
+        form_data["REFRESH_TOKEN"] = auth.refresh_token
     else:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["REFRESH_TOKEN"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 34 =====
```
 
     if is_refresh:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
-        form_data["refresh_token"] = auth.refresh_token
+        form_data["XXrefresh_tokenXX"] = auth.refresh_token
     else:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["XXrefresh_tokenXX"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 35 =====
```
 
     if is_refresh:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
-        form_data["refresh_token"] = auth.refresh_token
+        form_data["refresh_token"] = None
     else:
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = None
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 36 =====
```
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
 
-    data = urlencode(form_data)
+    data = None
 
     return await auth.query(
         url=url,
@@ -49,4 +49,4 @@         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = None

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 37 =====
```
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
 
-    data = urlencode(form_data)
+    data = dumps(form_data)
 
     return await auth.query(
         url=url,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = dumps(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 38 =====
```
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
 
-    data = urlencode(form_data)
+    data = form_data
 
     return await auth.query(
         url=url,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = form_data

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 39 =====
```
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
 
-    data = urlencode(form_data)
+    data = urlencode(form_data) + "&extra_param=1"  # Adds an unexpected parameter
 
     return await auth.query(
         url=url,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data) + "&extra_param=1"  # Adds an unexpected parameter

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 40 =====
```
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
 
-    data = urlencode(form_data)
+    data = urlencode(login_data)
 
     return await auth.query(
         url=url,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(login_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 41 =====
```
         form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
         form_data["password"] = login_data["password"]
 
-    data = urlencode(form_data)
+    data = urlencode({})  # Empty dictionary
 
     return await auth.query(
         url=url,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode({})  # Empty dictionary

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 42 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
         headers=headers,
         data=data,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 43 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
+        url="",
         headers=headers,
         data=data,
         json_resp=False,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url="",
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 44 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
+        url=None,
         headers=headers,
         data=data,
         json_resp=False,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=None,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 45 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
+        url=None,
         headers=headers,
         data=data,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=None,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 46 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
+        url=auth.token,
         headers=headers,
         data=data,
         json_resp=False,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=auth.token,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 47 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
+        url=login_data.get("url", ""),
         headers=headers,
         data=data,
         json_resp=False,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=login_data.get("url", ""),
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 48 =====
```
     data = urlencode(form_data)
 
     return await auth.query(
-        url=url,
+        url=login_data["username"],
         headers=headers,
         data=data,
         json_resp=False,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=login_data["username"],
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 49 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
         data=data,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 50 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
+        headers=None,
         data=data,
         json_resp=False,
         reqtype="post",
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=None,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 51 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
+        headers=None,
         data=data,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=None,
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 52 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
+        headers={"Authorization": "Bearer invalid_token"},
         data=data,
         json_resp=False,
         reqtype="post",
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers={"Authorization": "Bearer invalid_token"},
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 53 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
+        headers={"Content-Type": "application/json"},
         data=data,
         json_resp=False,
         reqtype="post",
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers={"Content-Type": "application/json"},
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 54 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
+        headers={"User-Agent": "CustomUserAgent"},
         data=data,
         json_resp=False,
         reqtype="post",
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers={"User-Agent": "CustomUserAgent"},
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 55 =====
```
 
     return await auth.query(
         url=url,
-        headers=headers,
+        headers={},
         data=data,
         json_resp=False,
         reqtype="post",
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers={},
        data=data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 56 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
+        data="",
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data="",
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 57 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
+        data=None,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=None,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 58 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
+        data=None,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=None,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 59 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
+        data=login_data,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=login_data,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 60 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
+        data=login_data.get("password"),
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=login_data.get("password"),
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 61 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
+        data={"unexpected_key": "value"},
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data={"unexpected_key": "value"},
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
===== 62 =====
```
     return await auth.query(
         url=url,
         headers=headers,
-        data=data,
         json_resp=False,
         reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        json_resp=False,
        reqtype="post",
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 63 =====
```
         headers=headers,
         data=data,
         json_resp=False,
-        reqtype="post",
         is_retry=is_retry,
         skip_refresh_check=True,
-    )+    )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        is_retry=is_retry,
        skip_refresh_check=True,
    )

```
===== 64 =====
```
         headers=headers,
         data=data,
         json_resp=False,
-        reqtype="post",
+        reqtype="get",
         is_retry=is_retry,
         skip_refresh_check=True,
     )
```
```
async def request_login(
    auth,
    url,
    login_data,
    is_refresh=False,
    is_retry=False,
):
    """
    OAuth login request.

    :param auth: Auth instance.
    :param url: Login url.
    :param login_data: Dictionary containing blink login data.
    :param is_retry:
    :param two_fa_code: 2FA code if required
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": DEFAULT_USER_AGENT,
        "hardware_id": login_data.get("device_id", "Blinkpy"),
    }

    # Add 2FA code to headers if provided
    if "2fa_code" in login_data:
        headers["2fa-code"] = login_data["2fa_code"]

    # Prepare form data for OAuth
    form_data = {
        "username": login_data["username"],
        "client_id": OAUTH_CLIENT_ID,
        "scope": OAUTH_SCOPE,
    }

    if is_refresh:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_REFRESH_TOKEN
        form_data["refresh_token"] = auth.refresh_token
    else:
        form_data["grant_type"] = OAUTH_GRANT_TYPE_PASSWORD
        form_data["password"] = login_data["password"]

    data = urlencode(form_data)

    return await auth.query(
        url=url,
        headers=headers,
        data=data,
        json_resp=False,
        reqtype="get",
        is_retry=is_retry,
        skip_refresh_check=True,
    )
```
