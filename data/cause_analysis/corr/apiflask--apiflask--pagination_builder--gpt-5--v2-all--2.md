https://github.com/apiflask/apiflask/blob/13d2a1b51a7ec68fdcfb9c6250f2db107fcf359a/./src/apiflask/helpers.py#L29-L109
```
@icontract.snapshot(lambda: request.endpoint, name="endpoint")
@icontract.snapshot(lambda pagination: pagination.total, name="total")
@icontract.snapshot(lambda pagination: pagination.pages, name="pages")
@icontract.snapshot(lambda pagination: pagination.page, name="page")
@icontract.snapshot(lambda pagination: pagination.per_page, name="per_page")
@icontract.snapshot(lambda pagination: pagination.has_next, name="has_next")
@icontract.snapshot(lambda pagination: pagination.next_num, name="next_num")
@icontract.snapshot(lambda pagination: pagination.has_prev, name="has_prev")
@icontract.snapshot(lambda pagination: pagination.prev_num, name="prev_num")
@icontract.ensure(lambda result: set(result.keys()) == {'total', 'pages', 'per_page', 'page', 'next', 'prev', 'first', 'last', 'current'})
@icontract.ensure(lambda total, result: result['total'] == total)
@icontract.ensure(lambda pages, result: result['pages'] == pages)
@icontract.ensure(lambda per_page, result: result['per_page'] == per_page)
@icontract.ensure(lambda page, result: result['page'] == page)
@icontract.ensure(lambda endpoint, result: True if endpoint is not None else (result['first'] == '' and result['last'] == '' and result['current'] == '' and result['next'] == '' and result['prev'] == ''))
@icontract.ensure(lambda endpoint, per_page, kwargs, result: True if endpoint is None else result['first'] == url_for(endpoint, page=1, per_page=per_page, _external=True, **kwargs))
@icontract.ensure(lambda endpoint, pages, per_page, kwargs, result: True if endpoint is None else result['last'] == url_for(endpoint, page=pages, per_page=per_page, _external=True, **kwargs))
@icontract.ensure(lambda endpoint, page, per_page, kwargs, result: True if endpoint is None else result['current'] == url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs))
@icontract.ensure(lambda endpoint, has_next, next_num, per_page, kwargs, result: True if endpoint is None else (result['next'] == (url_for(endpoint, page=next_num, per_page=per_page, _external=True, **kwargs) if has_next else '')))
@icontract.ensure(lambda endpoint, has_prev, prev_num, per_page, kwargs, result: True if endpoint is None else (result['prev'] == (url_for(endpoint, page=prev_num, per_page=per_page, _external=True, **kwargs) if has_prev else '')))
```
```
limited spec

per_page
```
failed
```
@icontract.ensure(
    lambda result, pagination, _KWARGS:
        result == {
            'total': pagination.total,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'page': pagination.page,
            'next': (
                '' if (not pagination.has_next or request.endpoint is None)
                else url_for(
                    request.endpoint,
                    page=pagination.next_num,
                    per_page=pagination.per_page,
                    _external=True,
                    **_KWARGS
                )
            ),
            'prev': (
                '' if (not pagination.has_prev or request.endpoint is None)
                else url_for(
                    request.endpoint,
                    page=pagination.prev_num,
                    per_page=pagination.per_page,
                    _external=True,
                    **_KWARGS
                )
            ),
            'first': (
                '' if request.endpoint is None
                else url_for(
                    request.endpoint,
                    page=1,
                    per_page=pagination.per_page,
                    _external=True,
                    **_KWARGS
                )
            ),
            'last': (
                '' if request.endpoint is None
                else url_for(
                    request.endpoint,
                    page=pagination.pages,
                    per_page=pagination.per_page,
                    _external=True,
                    **_KWARGS
                )
            ),
            'current': (
                '' if request.endpoint is None
                else url_for(
                    request.endpoint,
                    page=pagination.page,
                    per_page=pagination.per_page,
                    _external=True,
                    **_KWARGS
                )
            ),
        }
)

```
