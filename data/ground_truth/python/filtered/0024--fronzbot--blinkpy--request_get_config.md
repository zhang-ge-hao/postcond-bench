https://github.com/fronzbot/blinkpy/blob/1e868e2a19fa8b364f4e9164d1e31e7e4969c7fb/./blinkpy/api.py#L473-L496
```
🈚️

async
```
```
@icontract.snapshot(lambda product_type: product_type.lower(), name="pt_lower")
@icontract.ensure(lambda OLD, result, blink, network, camera_id: (
    (OLD.pt_lower == "owl" and getattr(blink.auth.query, "call_count", 0) == 1 and (blink.auth.query.call_args and f"/api/v1/accounts/{blink.account_id}/networks/{network}/owls/{camera_id}/config" in blink.auth.query.call_args[1].get("url", "")) and result is not None)
    or
    (OLD.pt_lower == "catalina" and getattr(blink.auth.query, "call_count", 0) == 1 and (blink.auth.query.call_args and f"/network/{network}/camera/{camera_id}/config" in blink.auth.query.call_args[1].get("url", "")) and result is not None)
    or
    (OLD.pt_lower not in ("owl", "catalina") and getattr(blink.auth.query, "call_count", 0) == 0 and result is None)
))
```
[0, 1, 2, 3, 4, 5, 6, 7]
===== 0 =====
```
     :param camera_id: ID of camera
     :param product_type: Camera product type "owl" or "catalina"
     """
-    if product_type == "owl":
+    if product_type != "owl":
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
@@ -21,4 +21,4 @@             product_type,
         )
         return None
-    return await http_get(blink, url)+    return await http_get(blink, url)
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type != "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)

```
===== 1 =====
```
     :param camera_id: ID of camera
     :param product_type: Camera product type "owl" or "catalina"
     """
-    if product_type == "owl":
+    if product_type != "owl":  # Negation of the correct condition
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type != "owl":  # Negation of the correct condition
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)
```
===== 2 =====
```
     :param camera_id: ID of camera
     :param product_type: Camera product type "owl" or "catalina"
     """
-    if product_type == "owl":
+    if product_type == "OWL":
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
@@ -21,4 +21,4 @@             product_type,
         )
         return None
-    return await http_get(blink, url)+    return await http_get(blink, url)
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type == "OWL":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)

```
===== 3 =====
```
     :param camera_id: ID of camera
     :param product_type: Camera product type "owl" or "catalina"
     """
-    if product_type == "owl":
+    if product_type == "XXowlXX":
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
@@ -21,4 +21,4 @@             product_type,
         )
         return None
-    return await http_get(blink, url)+    return await http_get(blink, url)
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type == "XXowlXX":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)

```
===== 4 =====
```
     :param camera_id: ID of camera
     :param product_type: Camera product type "owl" or "catalina"
     """
-    if product_type == "owl":
+    if product_type == "cat":  # Incorrect product type check
         url = (
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type == "cat":  # Incorrect product type check
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)
```
===== 5 =====
```
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
         )
-    elif product_type == "catalina":
+    elif product_type != "catalina":
         url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
     else:
         _LOGGER.info(
@@ -21,4 +21,4 @@             product_type,
         )
         return None
-    return await http_get(blink, url)+    return await http_get(blink, url)
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type != "catalina":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)

```
===== 6 =====
```
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
         )
-    elif product_type == "catalina":
+    elif product_type == "CATALINA":
         url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
     else:
         _LOGGER.info(
@@ -21,4 +21,4 @@             product_type,
         )
         return None
-    return await http_get(blink, url)+    return await http_get(blink, url)
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "CATALINA":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)

```
===== 7 =====
```
             f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
             f"/networks/{network}/owls/{camera_id}/config"
         )
-    elif product_type == "catalina":
+    elif product_type == "XXcatalinaXX":
         url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
     else:
         _LOGGER.info(
@@ -21,4 +21,4 @@             product_type,
         )
         return None
-    return await http_get(blink, url)+    return await http_get(blink, url)
```
```
async def request_get_config(blink, network, camera_id, product_type="owl"):
    """
    Get camera configuration.

    :param blink: Blink instance.
    :param network: Sync module network id.
    :param camera_id: ID of camera
    :param product_type: Camera product type "owl" or "catalina"
    """
    if product_type == "owl":
        url = (
            f"{blink.urls.base_url}/api/v1/accounts/{blink.account_id}"
            f"/networks/{network}/owls/{camera_id}/config"
        )
    elif product_type == "XXcatalinaXX":
        url = f"{blink.urls.base_url}/network/{network}/camera/{camera_id}/config"
    else:
        _LOGGER.info(
            "Camera %s with product type %s config get not implemented.",
            camera_id,
            product_type,
        )
        return None
    return await http_get(blink, url)

```
