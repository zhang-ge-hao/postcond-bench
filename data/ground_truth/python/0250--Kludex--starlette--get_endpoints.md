https://github.com/Kludex/starlette/blob/7e4b7428f273dbdc875dcd036d20804bcfc7b2ee/./starlette/schemas.py#L39-L86
```
@icontract.snapshot(lambda routes: routes, name="routes_snapshot")
@icontract.ensure(
    lambda OLD, self, routes, result:
    isinstance(result, list)
    and all(isinstance(e, EndpointInfo) for e in result)
    and all(isinstance(e.path, str) for e in result)
    and all(isinstance(e.http_method, str) for e in result)
    and all(e.http_method == e.http_method.lower() for e in result)
    and all(
        e.http_method in {"get", "post", "put", "patch", "delete", "options"}
        for e in result
    )
    and all(callable(e.func) for e in result)
    and all(
        {
            e.http_method
            for e in result
            if e.func is route.endpoint
            and e.path == self._remove_converter(route.path)
        }
        ==
        {
            method.lower()
            for method in (route.methods or ["GET"])
            if method != "HEAD"
        }
        for route in OLD.routes_snapshot
        if isinstance(route, Route)
        and getattr(route, "include_in_schema", False)
        and (inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint))
    )
    and all(
        {
            e.http_method
            for e in result
            if e.path == self._remove_converter(route.path)
            and any(
                hasattr(route.endpoint, m) and getattr(route.endpoint, m) is e.func
                for m in ["get", "post", "put", "patch", "delete", "options"]
            )
        }
        ==
        {
            m
            for m in ["get", "post", "put", "patch", "delete", "options"]
            if hasattr(route.endpoint, m)
        }
        for route in OLD.routes_snapshot
        if isinstance(route, Route)
        and getattr(route, "include_in_schema", False)
        and not (inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint))
    )
    and all(
        any(
            (e.path == self._remove_converter(route.path))
            and (e.func is route.endpoint)
            and (e.http_method == method.lower())
            for e in result
        )
        for route in OLD.routes_snapshot
        if isinstance(route, Route)
        and getattr(route, "include_in_schema", False)
        and (inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint))
        for method in (route.methods or ["GET"])
        if method != "HEAD"
    )
    and all(
        any(
            (e.path == self._remove_converter(route.path))
            and (e.func is getattr(route.endpoint, m))
            and (e.http_method == m)
            for e in result
        )
        for route in OLD.routes_snapshot
        if isinstance(route, Route)
        and getattr(route, "include_in_schema", False)
        and not (inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint))
        for m in ["get", "post", "put", "patch", "delete", "options"]
        if hasattr(route.endpoint, m)
    )
    and all(
        any(
            (
                e.path ==
                (
                    (self._remove_converter(parent.path) if isinstance(parent, Mount) else "")
                    + self._remove_converter(child.path)
                )
            )
            and (e.func is child.endpoint)
            and (e.http_method == method.lower())
            for e in result
        )
        for parent in OLD.routes_snapshot
        if isinstance(parent, (Mount, Host))
        for child in (getattr(parent, "routes", None) or [])
        if isinstance(child, Route)
        and getattr(child, "include_in_schema", False)
        and (inspect.isfunction(child.endpoint) or inspect.ismethod(child.endpoint))
        for method in (child.methods or ["GET"])
        if method != "HEAD"
    )
    and all(
        any(
            (
                e.path ==
                (
                    (self._remove_converter(parent.path) if isinstance(parent, Mount) else "")
                    + self._remove_converter(child.path)
                )
            )
            and (e.func is getattr(child.endpoint, m))
            and (e.http_method == m)
            for e in result
        )
        for parent in OLD.routes_snapshot
        if isinstance(parent, (Mount, Host))
        for child in (getattr(parent, "routes", None) or [])
        if isinstance(child, Route)
        and getattr(child, "include_in_schema", False)
        and not (inspect.isfunction(child.endpoint) or inspect.ismethod(child.endpoint))
        for m in ["get", "post", "put", "patch", "delete", "options"]
        if hasattr(child.endpoint, m)
    )
    and all(
        any(
            (
                e.path ==
                (
                    (self._remove_converter(parent.path) if isinstance(parent, Mount) else "")
                    + (self._remove_converter(child.path) if isinstance(child, Mount) else "")
                    + self._remove_converter(grandchild.path)
                )
            )
            and (e.func is grandchild.endpoint)
            and (e.http_method == method.lower())
            for e in result
        )
        for parent in OLD.routes_snapshot
        if isinstance(parent, (Mount, Host))
        for child in (getattr(parent, "routes", None) or [])
        if isinstance(child, (Mount, Host))
        for grandchild in (getattr(child, "routes", None) or [])
        if isinstance(grandchild, Route)
        and getattr(grandchild, "include_in_schema", False)
        and (inspect.isfunction(grandchild.endpoint) or inspect.ismethod(grandchild.endpoint))
        for method in (grandchild.methods or ["GET"])
        if method != "HEAD"
    )
    and all(
        any(
            (
                e.path ==
                (
                    (self._remove_converter(parent.path) if isinstance(parent, Mount) else "")
                    + (self._remove_converter(child.path) if isinstance(child, Mount) else "")
                    + self._remove_converter(grandchild.path)
                )
            )
            and (e.func is getattr(grandchild.endpoint, m))
            and (e.http_method == m)
            for e in result
        )
        for parent in OLD.routes_snapshot
        if isinstance(parent, (Mount, Host))
        for child in (getattr(parent, "routes", None) or [])
        if isinstance(child, (Mount, Host))
        for grandchild in (getattr(child, "routes", None) or [])
        if isinstance(grandchild, Route)
        and getattr(grandchild, "include_in_schema", False)
        and not (inspect.isfunction(grandchild.endpoint) or inspect.ismethod(grandchild.endpoint))
        for m in ["get", "post", "put", "patch", "delete", "options"]
        if hasattr(grandchild.endpoint, m)
    )
)
```
```
@icontract.snapshot(lambda routes: routes, name="routes_snapshot")
@icontract.ensure(lambda OLD, self, routes, result: isinstance(result, list))
@icontract.ensure(lambda OLD, self, routes, result: all(isinstance(e, EndpointInfo) for e in result))
@icontract.ensure(lambda OLD, self, routes, result: all(isinstance(e.path, str) for e in result))
@icontract.ensure(lambda OLD, self, routes, result: all(isinstance(e.http_method, str) for e in result))
@icontract.ensure(lambda OLD, self, routes, result: all(e.http_method == e.http_method.lower() for e in result))
@icontract.ensure(lambda OLD, self, routes, result: all(e.http_method in {"get", "post", "put", "patch", "delete", "options"} for e in result))
@icontract.ensure(lambda OLD, self, routes, result: all(callable(e.func) for e in result))
@icontract.ensure(lambda OLD, self, routes, result: all(
    any(
        (e.path == self._remove_converter(route.path)) and (e.func is route.endpoint) and (e.http_method == method.lower())
        for e in result
    )
    for route in OLD.routes_snapshot
    if isinstance(route, Route) and getattr(route, "include_in_schema", False) and (inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint))
    for method in (route.methods or ["GET"]) if method != "HEAD"
))
@icontract.ensure(lambda OLD, self, routes, result: all(
    any(
        (e.path == self._remove_converter(route.path)) and (e.func is getattr(route.endpoint, m)) and (e.http_method == m)
        for e in result
    )
    for route in OLD.routes_snapshot
    if isinstance(route, Route) and getattr(route, "include_in_schema", False) and not (inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint))
    for m in ["get", "post", "put", "patch", "delete", "options"] if hasattr(route.endpoint, m)
))
@icontract.ensure(lambda OLD, self, routes, result: all(
    any(
        (e.path == ((self._remove_converter(parent.path) if isinstance(parent, Mount) else "") + self._remove_converter(child.path))) and
        (e.func is child.endpoint) and
        (e.http_method == method.lower())
        for e in result
    )
    for parent in OLD.routes_snapshot if isinstance(parent, (Mount, Host))
    for child in (getattr(parent, "routes", None) or [])
    if isinstance(child, Route) and getattr(child, "include_in_schema", False) and (inspect.isfunction(child.endpoint) or inspect.ismethod(child.endpoint))
    for method in (child.methods or ["GET"]) if method != "HEAD"
))
@icontract.ensure(lambda OLD, self, routes, result: all(
    any(
        (e.path == ((self._remove_converter(parent.path) if isinstance(parent, Mount) else "") + self._remove_converter(child.path))) and
        (e.func is getattr(child.endpoint, m)) and
        (e.http_method == m)
        for e in result
    )
    for parent in OLD.routes_snapshot if isinstance(parent, (Mount, Host))
    for child in (getattr(parent, "routes", None) or [])
    if isinstance(child, Route) and getattr(child, "include_in_schema", False) and not (inspect.isfunction(child.endpoint) or inspect.ismethod(child.endpoint))
    for m in ["get", "post", "put", "patch", "delete", "options"] if hasattr(child.endpoint, m)
))
```
[3, 9, 37, 77]
===== 3 =====
```
         endpoints_info: list[EndpointInfo] = []
 
         for route in routes:
-            if isinstance(route, (Mount, Host)):
+            if isinstance(route, Mount):  # Missing Host check
                 routes = route.routes or []
                 if isinstance(route, Mount):
                     path = self._remove_converter(route.path)
```
```
    def get_endpoints(self, routes: list[BaseRoute]) -> list[EndpointInfo]:
        """
        Given the routes, yields the following information:

        - path
            eg: /users/
        - http_method
            one of 'get', 'post', 'put', 'patch', 'delete', 'options'
        - func
            method ready to extract the docstring
        """
        endpoints_info: list[EndpointInfo] = []

        for route in routes:
            if isinstance(route, Mount):  # Missing Host check
                routes = route.routes or []
                if isinstance(route, Mount):
                    path = self._remove_converter(route.path)
                else:
                    path = ""
                sub_endpoints = [
                    EndpointInfo(
                        path="".join((path, sub_endpoint.path)),
                        http_method=sub_endpoint.http_method,
                        func=sub_endpoint.func,
                    )
                    for sub_endpoint in self.get_endpoints(routes)
                ]
                endpoints_info.extend(sub_endpoints)

            elif not isinstance(route, Route) or not route.include_in_schema:
                continue

            elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                path = self._remove_converter(route.path)
                for method in route.methods or ["GET"]:
                    if method == "HEAD":
                        continue
                    endpoints_info.append(EndpointInfo(path, method.lower(), route.endpoint))
            else:
                path = self._remove_converter(route.path)
                for method in ["get", "post", "put", "patch", "delete", "options"]:
                    if not hasattr(route.endpoint, method):
                        continue
                    func = getattr(route.endpoint, method)
                    endpoints_info.append(EndpointInfo(path, method.lower(), func))

        return endpoints_info
```
===== 9 =====
```
                 if isinstance(route, Mount):
                     path = self._remove_converter(route.path)
                 else:
-                    path = ""
+                    path = "XXXX"
                 sub_endpoints = [
                     EndpointInfo(
                         path="".join((path, sub_endpoint.path)),
@@ -45,4 +45,4 @@                     func = getattr(route.endpoint, method)
                     endpoints_info.append(EndpointInfo(path, method.lower(), func))
 
-        return endpoints_info+        return endpoints_info
```
```
    def get_endpoints(self, routes: list[BaseRoute]) -> list[EndpointInfo]:
        """
        Given the routes, yields the following information:

        - path
            eg: /users/
        - http_method
            one of 'get', 'post', 'put', 'patch', 'delete', 'options'
        - func
            method ready to extract the docstring
        """
        endpoints_info: list[EndpointInfo] = []

        for route in routes:
            if isinstance(route, (Mount, Host)):
                routes = route.routes or []
                if isinstance(route, Mount):
                    path = self._remove_converter(route.path)
                else:
                    path = "XXXX"
                sub_endpoints = [
                    EndpointInfo(
                        path="".join((path, sub_endpoint.path)),
                        http_method=sub_endpoint.http_method,
                        func=sub_endpoint.func,
                    )
                    for sub_endpoint in self.get_endpoints(routes)
                ]
                endpoints_info.extend(sub_endpoints)

            elif not isinstance(route, Route) or not route.include_in_schema:
                continue

            elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                path = self._remove_converter(route.path)
                for method in route.methods or ["GET"]:
                    if method == "HEAD":
                        continue
                    endpoints_info.append(EndpointInfo(path, method.lower(), route.endpoint))
            else:
                path = self._remove_converter(route.path)
                for method in ["get", "post", "put", "patch", "delete", "options"]:
                    if not hasattr(route.endpoint, method):
                        continue
                    func = getattr(route.endpoint, method)
                    endpoints_info.append(EndpointInfo(path, method.lower(), func))

        return endpoints_info

```
===== 37 =====
```
 
             elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                 path = self._remove_converter(route.path)
-                for method in route.methods or ["GET"]:
+                for method in ["GET", "POST"]:  # Only considers GET and POST methods
                     if method == "HEAD":
                         continue
                     endpoints_info.append(EndpointInfo(path, method.lower(), route.endpoint))
```
```
    def get_endpoints(self, routes: list[BaseRoute]) -> list[EndpointInfo]:
        """
        Given the routes, yields the following information:

        - path
            eg: /users/
        - http_method
            one of 'get', 'post', 'put', 'patch', 'delete', 'options'
        - func
            method ready to extract the docstring
        """
        endpoints_info: list[EndpointInfo] = []

        for route in routes:
            if isinstance(route, (Mount, Host)):
                routes = route.routes or []
                if isinstance(route, Mount):
                    path = self._remove_converter(route.path)
                else:
                    path = ""
                sub_endpoints = [
                    EndpointInfo(
                        path="".join((path, sub_endpoint.path)),
                        http_method=sub_endpoint.http_method,
                        func=sub_endpoint.func,
                    )
                    for sub_endpoint in self.get_endpoints(routes)
                ]
                endpoints_info.extend(sub_endpoints)

            elif not isinstance(route, Route) or not route.include_in_schema:
                continue

            elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                path = self._remove_converter(route.path)
                for method in ["GET", "POST"]:  # Only considers GET and POST methods
                    if method == "HEAD":
                        continue
                    endpoints_info.append(EndpointInfo(path, method.lower(), route.endpoint))
            else:
                path = self._remove_converter(route.path)
                for method in ["get", "post", "put", "patch", "delete", "options"]:
                    if not hasattr(route.endpoint, method):
                        continue
                    func = getattr(route.endpoint, method)
                    endpoints_info.append(EndpointInfo(path, method.lower(), func))

        return endpoints_info
```
===== 77 =====
```
                     if not hasattr(route.endpoint, method):
                         continue
                     func = getattr(route.endpoint, method)
-                    endpoints_info.append(EndpointInfo(path, method.lower(), func))
+                    endpoints_info.append(None)
 
-        return endpoints_info+        return endpoints_info
```
```
    def get_endpoints(self, routes: list[BaseRoute]) -> list[EndpointInfo]:
        """
        Given the routes, yields the following information:

        - path
            eg: /users/
        - http_method
            one of 'get', 'post', 'put', 'patch', 'delete', 'options'
        - func
            method ready to extract the docstring
        """
        endpoints_info: list[EndpointInfo] = []

        for route in routes:
            if isinstance(route, (Mount, Host)):
                routes = route.routes or []
                if isinstance(route, Mount):
                    path = self._remove_converter(route.path)
                else:
                    path = ""
                sub_endpoints = [
                    EndpointInfo(
                        path="".join((path, sub_endpoint.path)),
                        http_method=sub_endpoint.http_method,
                        func=sub_endpoint.func,
                    )
                    for sub_endpoint in self.get_endpoints(routes)
                ]
                endpoints_info.extend(sub_endpoints)

            elif not isinstance(route, Route) or not route.include_in_schema:
                continue

            elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                path = self._remove_converter(route.path)
                for method in route.methods or ["GET"]:
                    if method == "HEAD":
                        continue
                    endpoints_info.append(EndpointInfo(path, method.lower(), route.endpoint))
            else:
                path = self._remove_converter(route.path)
                for method in ["get", "post", "put", "patch", "delete", "options"]:
                    if not hasattr(route.endpoint, method):
                        continue
                    func = getattr(route.endpoint, method)
                    endpoints_info.append(None)

        return endpoints_info

```
