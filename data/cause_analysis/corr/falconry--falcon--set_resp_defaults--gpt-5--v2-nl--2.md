https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/testing/resource.py#L107-L129
```
@icontract.ensure(lambda req, resp, resource, params: (not hasattr(resource, "_default_status")) or resp.status == resource._default_status)
@icontract.ensure(lambda req, resp, resource, params: (not hasattr(resource, "_default_body")) or (resource._default_body is None) or (isinstance(resource._default_body, (bytes, bytearray)) and getattr(resp, "data", None) == resource._default_body) or (not isinstance(resource._default_body, (bytes, bytearray)) and getattr(resp, "text", None) == resource._default_body))
@icontract.ensure(lambda req, resp, resource, params: (not hasattr(resource, "_default_headers")) or (resource._default_headers in (None, {})) or all(resp.headers.get(k) == v for k, v in resource._default_headers.items()))
```
```
hallucination on semantics

the comment does not mention what if _default_status is None
the implementation skipped if so, but the postcondition still validated
```
icontract_fail
```
@icontract.snapshot(lambda resp: resp.status, name="old_status")
@icontract.snapshot(lambda resp: resp.text, name="old_text")
@icontract.snapshot(lambda resp: resp.headers, name="old_headers")
@icontract.ensure(lambda OLD, req, resp, resource, params: (resource._default_status is None and resp.status == OLD.old_status) or (resource._default_status is not None and resp.status == resource._default_status))
@icontract.ensure(lambda OLD, req, resp, resource, params: (resource._default_body is None and resp.text == OLD.old_text) or (resource._default_body is not None and resp.text == resource._default_body))
@icontract.ensure(lambda OLD, req, resp, resource, params: (resource._default_headers is None and resp.headers == OLD.old_headers) or (resource._default_headers is not None and all(resp.get_header(k) == v for k, v in dict(resource._default_headers).items())))
```
