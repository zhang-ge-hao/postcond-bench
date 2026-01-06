https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/testing/resource.py#L40-L78
```
@icontract.ensure(lambda resource, req: resource.captured_req is req)
@icontract.ensure(lambda resource, resp: resource.captured_resp is resp)
@icontract.ensure(lambda resource, params: resource.captured_kwargs is params)
@icontract.ensure(lambda req, resource: (not bool(req.get_header('capture-req-body-bytes'))) or (resource.captured_req_body is not None and resource.captured_req_media is None))
@icontract.ensure(lambda req, resource: (bool(req.get_header('capture-req-body-bytes')) or not bool(req.get_header('capture-req-media'))) or (resource.captured_req_media is not None and resource.captured_req_body is None))
@icontract.ensure(lambda req, resource: (bool(req.get_header('capture-req-body-bytes')) or bool(req.get_header('capture-req-media'))) or (resource.captured_req_body is None and resource.captured_req_media is None))
@icontract.ensure(lambda resource: not (resource.captured_req_body is not None and resource.captured_req_media is not None))
@icontract.ensure(lambda req, resource: (resource.captured_req_body is None) or bool(req.get_header('capture-req-body-bytes')))
@icontract.ensure(lambda req, resource: (resource.captured_req_media is None) or (not bool(req.get_header('capture-req-body-bytes')) and bool(req.get_header('capture-req-media'))))
```
```
Hallucination.

@icontract.ensure(lambda req, resource: (bool(req.get_header('capture-req-body-bytes')) or not bool(req.get_header('capture-req-media'))) or (resource.captured_req_media is not None and resource.captured_req_body is None))

can infer to:

not req.get_header('capture-req-body-bytes') and req.get_header('capture-req-media') ==> resource.captured_req_media is not None

the branch position is:
simple_resource.captured_req_media = req.get_media()

can infer to:

req.get_media() is not None

Therefore, the LLM has hallucination on "media cannot be None". But in practice, when `test_null_json_media` is called, the media is None.
```
icontract_fail
```
@icontract.ensure(lambda req, resource: resource.captured_req is req)
@icontract.ensure(lambda resp, resource: resource.captured_resp is resp)
@icontract.ensure(lambda params, resource: resource.captured_kwargs is params)
@icontract.ensure(lambda req, resource: (bool(req.get_header('capture-req-body-bytes')) and resource.captured_req_body is not None) or (not bool(req.get_header('capture-req-body-bytes')) and resource.captured_req_body is None))
@icontract.ensure(lambda req, resource: (not bool(req.get_header('capture-req-body-bytes'))) or (isinstance(resource.captured_req_body, (bytes, bytearray)) and len(resource.captured_req_body) == int(req.get_header('capture-req-body-bytes'))))
@icontract.ensure(lambda req, resource: (bool(req.get_header('capture-req-body-bytes')) and resource.captured_req_media is None) or (not bool(req.get_header('capture-req-body-bytes')) and ((bool(req.get_header('capture-req-media')) and resource.captured_req_media == req.get_media()) or (not bool(req.get_header('capture-req-media')) and resource.captured_req_media is None))))
```
