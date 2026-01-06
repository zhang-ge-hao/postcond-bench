https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/middleware.py#L103-L163
```
@icontract.snapshot(lambda req: id(req), name="req_id")
@icontract.snapshot(lambda resp: id(resp), name="resp_id")
@icontract.snapshot(lambda resource: id(resource), name="resource_id")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda req, OLD: id(req) == OLD.req_id)
@icontract.ensure(lambda resp, OLD: id(resp) == OLD.resp_id)
@icontract.ensure(lambda resource, OLD: id(resource) == OLD.resource_id)
```
```
missing attribute validation

validation on input parameter
repository defined type
```
passed
```
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: req.get_header('Origin'), name='origin')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: resp.get_header('Access-Control-Allow-Origin'), name='orig_resp_allow_origin')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: resp.get_header('Access-Control-Allow-Credentials'), name='orig_resp_allow_credentials')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: resp.get_header('Access-Control-Expose-Headers'), name='orig_resp_expose')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: resp.get_header('Allow'), name='orig_resp_Allow')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: resp.get_header('Access-Control-Allow-Private-Network'), name='orig_resp_private')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: req.method, name='req_method')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: req.get_header('Access-Control-Request-Method'), name='ac_req_method')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: req.get_header('Access-Control-Request-Headers', default='*'), name='ac_req_headers')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: req.get_header('Access-Control-Request-Private-Network'), name='ac_req_private')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: self.allow_origins, name='allow_origins')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: self.allow_credentials, name='allow_credentials')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: self.expose_headers, name='expose_headers')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: self.allow_private_network, name='allow_private_network')
@icontract.snapshot(lambda self, req, resp, resource, req_succeeded: req_succeeded, name='req_succeeded')
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.origin is None) <= (resp.get_header('Access-Control-Allow-Origin') == OLD.orig_resp_allow_origin and resp.get_header('Access-Control-Allow-Credentials') == OLD.orig_resp_allow_credentials and resp.get_header('Access-Control-Expose-Headers') == OLD.orig_resp_expose and resp.get_header('Allow') == OLD.orig_resp_Allow and resp.get_header('Access-Control-Allow-Private-Network') == OLD.orig_resp_private))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: ((OLD.origin is not None) and (not (OLD.allow_origins != '*' and OLD.origin not in OLD.allow_origins))) <= (True))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.origin is None or (OLD.allow_origins != '*' and OLD.origin not in OLD.allow_origins)) <= (resp.get_header('Access-Control-Allow-Origin') == OLD.orig_resp_allow_origin and resp.get_header('Access-Control-Allow-Credentials') == OLD.orig_resp_allow_credentials))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.origin is not None and (OLD.allow_origins == '*' or OLD.origin in OLD.allow_origins) and OLD.orig_resp_allow_origin is not None) <= (resp.get_header('Access-Control-Allow-Origin') == OLD.orig_resp_allow_origin and resp.get_header('Access-Control-Allow-Credentials') == OLD.orig_resp_allow_credentials))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.origin is not None and (OLD.allow_origins == '*' or OLD.origin in OLD.allow_origins) and OLD.orig_resp_allow_origin is None) <= (resp.get_header('Access-Control-Allow-Origin') == ('*' if OLD.allow_origins == '*' else OLD.origin)))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.origin is not None and (OLD.allow_origins == '*' or OLD.origin in OLD.allow_origins) and OLD.orig_resp_allow_origin is None and (OLD.allow_credentials == '*' or (OLD.origin in OLD.allow_credentials))) <= (resp.get_header('Access-Control-Allow-Origin') == OLD.origin and resp.get_header('Access-Control-Allow-Credentials') == 'true'))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.origin is not None and (OLD.allow_origins == '*' or OLD.origin in OLD.allow_origins) and OLD.orig_resp_allow_origin is None and not (OLD.allow_credentials == '*' or (OLD.origin in OLD.allow_credentials))) <= (resp.get_header('Access-Control-Allow-Credentials') == OLD.orig_resp_allow_credentials or resp.get_header('Access-Control-Allow-Credentials') is None))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (not bool(OLD.expose_headers)) <= (resp.get_header('Access-Control-Expose-Headers') == OLD.orig_resp_expose))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: bool(OLD.expose_headers) <= (resp.get_header('Access-Control-Expose-Headers') == OLD.expose_headers))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (not (OLD.req_succeeded and OLD.req_method == 'OPTIONS' and OLD.ac_req_method)) <= (resp.get_header('Allow') is None))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.req_succeeded and OLD.req_method == 'OPTIONS' and OLD.ac_req_method and OLD.orig_resp_Allow is None) <= (resp.get_header('Access-Control-Allow-Methods') is None and resp.get_header('Access-Control-Allow-Headers') is None and resp.get_header('Access-Control-Max-Age') is None and resp.get_header('Access-Control-Expose-Headers') is None and resp.get_header('Access-Control-Allow-Origin') is None))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.req_succeeded and OLD.req_method == 'OPTIONS' and OLD.ac_req_method and OLD.orig_resp_Allow is not None) <= (resp.get_header('Access-Control-Allow-Methods') == OLD.orig_resp_Allow and resp.get_header('Access-Control-Allow-Headers') == OLD.ac_req_headers and resp.get_header('Access-Control-Max-Age') == '86400'))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (not (OLD.req_succeeded and OLD.req_method == 'OPTIONS' and OLD.ac_req_method and OLD.allow_private_network and OLD.ac_req_private == 'true')) <= (resp.get_header('Access-Control-Allow-Private-Network') == OLD.orig_resp_private))
@icontract.ensure(lambda OLD, self, req, resp, resource, req_succeeded: (OLD.req_succeeded and OLD.req_method == 'OPTIONS' and OLD.ac_req_method and OLD.allow_private_network and OLD.ac_req_private == 'true') <= (resp.get_header('Access-Control-Allow-Private-Network') == 'true'))
```
===== 63: failed =====
```
             resp.set_header('Access-Control-Allow-Origin', set_origin)
 
         if self.expose_headers:
-            resp.set_header('Access-Control-Expose-Headers', self.expose_headers)
+            resp.set_header('Access-Control-Expose-Headers', self.allow_origins)
 
         if (
             req_succeeded
```
```
    def process_response(
        self, req: Request, resp: Response, resource: object, req_succeeded: bool
    ) -> None:
        """Implement the CORS policy for all routes.

        This middleware provides a simple out-of-the box CORS policy,
        including handling of preflighted requests from the browser.

        See also: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

        See also: https://www.w3.org/TR/cors/#resource-processing-model
        """

        origin = req.get_header('Origin')
        if origin is None:
            return

        if self.allow_origins != '*' and origin not in self.allow_origins:
            return

        if resp.get_header('Access-Control-Allow-Origin') is None:
            set_origin = '*' if self.allow_origins == '*' else origin
            if self.allow_credentials == '*' or origin in self.allow_credentials:
                set_origin = origin
                resp.set_header('Access-Control-Allow-Credentials', 'true')
            resp.set_header('Access-Control-Allow-Origin', set_origin)

        if self.expose_headers:
            resp.set_header('Access-Control-Expose-Headers', self.allow_origins)

        if (
            req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers', default='*'
            )

            if allow is None:
                # there is no allow set, remove all access control headers
                resp.delete_header('Access-Control-Allow-Methods')
                resp.delete_header('Access-Control-Allow-Headers')
                resp.delete_header('Access-Control-Max-Age')
                resp.delete_header('Access-Control-Expose-Headers')
                resp.delete_header('Access-Control-Allow-Origin')
            else:
                resp.set_header('Access-Control-Allow-Methods', allow)
                resp.set_header('Access-Control-Allow-Headers', allow_headers)
                resp.set_header('Access-Control-Max-Age', '86400')  # 24 hours

            if self.allow_private_network and (
                req.get_header('Access-Control-Request-Private-Network') == 'true'
            ):
                resp.set_header('Access-Control-Allow-Private-Network', 'true')
```
