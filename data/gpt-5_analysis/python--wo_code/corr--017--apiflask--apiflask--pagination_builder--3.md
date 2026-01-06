https://github.com/apiflask/apiflask/blob/13d2a1b51a7ec68fdcfb9c6250f2db107fcf359a/./src/apiflask/helpers.py#L29-L109
```
@icontract.snapshot(lambda pagination: pagination.page, name="old_page")
@icontract.snapshot(lambda pagination: pagination.per_page, name="old_per_page")
@icontract.snapshot(lambda pagination: pagination.pages, name="old_pages")
@icontract.snapshot(lambda pagination: pagination.total, name="old_total")
@icontract.snapshot(lambda pagination: pagination.has_next, name="old_has_next")
@icontract.snapshot(lambda pagination: pagination.has_prev, name="old_has_prev")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result: all(k in result for k in ("page", "per_page", "pages", "total")))
@icontract.ensure(lambda result, pagination: result["page"] == pagination.page)
@icontract.ensure(lambda result, pagination: result["per_page"] == pagination.per_page)
@icontract.ensure(lambda result, pagination: result["pages"] == pagination.pages)
@icontract.ensure(lambda result, pagination: result["total"] == pagination.total)
@icontract.ensure(lambda result, pagination: ("next" not in result) or ((pagination.has_next and result["next"] is not None) or (not pagination.has_next and result["next"] is None)))
@icontract.ensure(lambda result, pagination: ("prev" not in result) or ((pagination.has_prev and result["prev"] is not None) or (not pagination.has_prev and result["prev"] is None)))
@icontract.ensure(lambda OLD, pagination: pagination.page == OLD.old_page)
@icontract.ensure(lambda OLD, pagination: pagination.per_page == OLD.old_per_page)
@icontract.ensure(lambda OLD, pagination: pagination.pages == OLD.old_pages)
@icontract.ensure(lambda OLD, pagination: pagination.total == OLD.old_total)
@icontract.ensure(lambda OLD, pagination: pagination.has_next == OLD.old_has_next)
@icontract.ensure(lambda OLD, pagination: pagination.has_prev == OLD.old_has_prev)
```
```
Hallucination.

When pagination.has_prev is False, result["prev"] should be "" but not None.
```
icontract_fail
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
