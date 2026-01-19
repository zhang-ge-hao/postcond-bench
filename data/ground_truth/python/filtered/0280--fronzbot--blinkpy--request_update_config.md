https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/api.py#L499-L525
```
🈚️

async
```
```
    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)'''.strip())
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
     :param product_type: Camera product type "owl" or "catalina"
     :param data: string w/JSON dict of parameters/values to update
     """
-    if product_type == "owl":
+    if product_type != "owl":
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
@@ -24,4 +24,4 @@             product_type,
         )
         return None
-    return await http_post(blink, url, json=False, data=data)+    return await http_post(blink, url, json=False, data=data)
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type != "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)

```
===== 1 =====
```
     :param product_type: Camera product type "owl" or "catalina"
     :param data: string w/JSON dict of parameters/values to update
     """
-    if product_type == "owl":
+    if product_type != "owl":  # Negation of the correct condition
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type != "owl":  # Negation of the correct condition
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)
```
===== 2 =====
```
     :param product_type: Camera product type "owl" or "catalina"
     :param data: string w/JSON dict of parameters/values to update
     """
-    if product_type == "owl":
+    if product_type == "OWL":
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
@@ -24,4 +24,4 @@             product_type,
         )
         return None
-    return await http_post(blink, url, json=False, data=data)+    return await http_post(blink, url, json=False, data=data)
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "OWL":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)

```
===== 3 =====
```
     :param product_type: Camera product type "owl" or "catalina"
     :param data: string w/JSON dict of parameters/values to update
     """
-    if product_type == "owl":
+    if product_type == "XXowlXX":
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
@@ -24,4 +24,4 @@             product_type,
         )
         return None
-    return await http_post(blink, url, json=False, data=data)+    return await http_post(blink, url, json=False, data=data)
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "XXowlXX":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)

```
===== 4 =====
```
     :param product_type: Camera product type "owl" or "catalina"
     :param data: string w/JSON dict of parameters/values to update
     """
-    if product_type == "owl":
+    if product_type == "cat":  # Incorrect product type check
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "cat":  # Incorrect product type check
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)
```
===== 5 =====
```
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
         )
-    elif product_type == "catalina":
+    elif product_type != "catalina":
         url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
     else:
         _LOGGER.info(
@@ -24,4 +24,4 @@             product_type,
         )
         return None
-    return await http_post(blink, url, json=False, data=data)+    return await http_post(blink, url, json=False, data=data)
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type != "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)

```
===== 6 =====
```
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
         )
-    elif product_type == "catalina":
+    elif product_type == "CATALINA":
         url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
     else:
         _LOGGER.info(
@@ -24,4 +24,4 @@             product_type,
         )
         return None
-    return await http_post(blink, url, json=False, data=data)+    return await http_post(blink, url, json=False, data=data)
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "CATALINA":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)

```
===== 7 =====
```
             f"{blink.urls.base_url}/api/v1/accounts/"
             f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
         )
-    elif product_type == "catalina":
+    elif product_type == "XXcatalinaXX":
         url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
     else:
         _LOGGER.info(
@@ -24,4 +24,4 @@             product_type,
         )
         return None
-    return await http_post(blink, url, json=False, data=data)+    return await http_post(blink, url, json=False, data=data)
```
```
async def request_update_config(
    blink, network, camera_id, product_type="owl", data=None
):
    """
    Update camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    :param data: string w/JSON dict of parameters/values to update
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/"
            f"{blink.account_id}/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "XXcatalinaXX":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/update"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config update not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_post(blink, url, json=False, data=data)

```
