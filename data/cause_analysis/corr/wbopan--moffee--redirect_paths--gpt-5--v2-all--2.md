https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/utils/file_helper.py#L25-L84
```
@icontract.snapshot(lambda document: document, name="orig_document")
@icontract.ensure(lambda result: isinstance(result, str))
@icontract.ensure(lambda orig_document, result:
    len([el[attr] for tag, attr in [('img','src'),('link','href'),('script','src'),('a','href')]
         for el in BeautifulSoup(result, "html.parser").find_all(tag) if el.has_attr(attr)]) ==
    len([unquote(el[attr]) for tag, attr in [('img','src'),('link','href'),('script','src'),('a','href')]
         for el in BeautifulSoup(orig_document, "html.parser").find_all(tag) if el.has_attr(attr)])
)
@icontract.ensure(lambda orig_document, result:
    all(
        (not (bool(urlparse(u).netloc) or (os.path.isabs(u) and os.path.exists(u)))) or (rv == u)
        for u, rv in zip(
            [unquote(el[attr]) for tag, attr in [('img','src'),('link','href'),('script','src'),('a','href')]
             for el in BeautifulSoup(orig_document, "html.parser").find_all(tag) if el.has_attr(attr)],
            [el[attr] for tag, attr in [('img','src'),('link','href'),('script','src'),('a','href')]
             for el in BeautifulSoup(result, "html.parser").find_all(tag) if el.has_attr(attr)]
        )
    )
)
@icontract.ensure(lambda document_path, resource_dir, orig_document, result:
    all(
        (rv == u) or
        (os.path.exists(os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(document_path), u)))) and
         rv == os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(document_path), u)))) or
        (os.path.exists(os.path.abspath(os.path.normpath(os.path.join(os.path.abspath(resource_dir), u)))) and
         rv == os.path.abspath(os.path.normpath(os.path.join(os.path.abspath(resource_dir), u)))) or
        (os.path.exists(os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(document_path), resource_dir, u)))) and
         rv == os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(document_path), resource_dir, u))))
        for u, rv in zip(
            [unquote(el[attr]) for tag, attr in [('img','src'),('link','href'),('script','src'),('a','href')]
             for el in BeautifulSoup(orig_document, "html.parser").find_all(tag) if el.has_attr(attr)],
            [el[attr] for tag, attr in [('img','src'),('link','href'),('script','src'),('a','href')]
             for el in BeautifulSoup(result, "html.parser").find_all(tag) if el.has_attr(attr)]
        )
    )
)
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['orig_document']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.ensure(
    lambda result, document, document_path, resource_dir=".":
        result
        == (
            (
                (soup := BeautifulSoup(document, "html.parser")),
                (
                    tag_attr_pairs := [
                        ("img", "src"),
                        ("link", "href"),
                        ("script", "src"),
                        ("a", "href"),
                    ]
                ),
                [
                    element.__setitem__(
                        attr,
                        (
                            (decoded := unquote(element[attr])),
                            (
                                decoded
                                if (
                                    bool(urlparse(decoded).netloc)
                                    or (
                                        os.path.isabs(decoded)
                                        and os.path.exists(decoded)
                                    )
                                )
                                else next(
                                    (
                                        abs_url
                                        for base in [
                                            os.path.dirname(document_path),
                                            os.path.abspath(resource_dir),
                                            os.path.join(
                                                os.path.dirname(document_path),
                                                resource_dir,
                                            ),
                                        ]
                                        for abs_url in [
                                            os.path.abspath(
                                                os.path.normpath(
                                                    os.path.join(base, decoded)
                                                )
                                            )
                                        ]
                                        if os.path.exists(abs_url)
                                        or (
                                            bool(urlparse(abs_url).netloc)
                                            or (
                                                os.path.isabs(abs_url)
                                                and os.path.exists(abs_url)
                                            )
                                        )
                                    ),
                                    decoded,
                                )
                            ),
                        )[-1],
                    )
                    for tag, attr in tag_attr_pairs
                    for element in soup.find_all(tag)
                    if element.has_attr(attr)
                ],
                str(soup),
            )[-1]
        )
)

```
